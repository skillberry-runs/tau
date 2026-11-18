"""Airline tool set for the tau2-bench airline domain.

The ``AirlineTools`` class subclasses tau2's ``AirlineTools`` (to inherit the
private helpers — ``_get_user``, ``_get_reservation``, ``_search_direct_flight``,
... — and the ``ToolKitBase`` machinery) and re-declares every agent-callable tool
with its real tau2 body (copied verbatim from ``tau2.domains.airline.tools``).

The module-level ``REMOVE_TOOLS`` set names any tools to drop from the exposed
agent toolset (empty by default; the seed exposes tau2's default airline tools).

Note: this file does NOT use ``from __future__ import annotations``. Tool
signature annotations must be real, importable objects (not strings), because
tau2 builds each tool's parameter JSON-schema from the live signature via
``create_model(...).model_json_schema()`` and stringified forward refs would not
resolve. Every type used in a signature below is imported here.
"""

from copy import deepcopy
from datetime import datetime
from typing import List, Literal, Optional  # noqa: F401  (available for tool signatures)

from loguru import logger

from tau2.domains.airline.data_model import (
    AirportCode,
    AirportInfo,
    CabinClass,
    Certificate,
    DirectFlight,
    Flight,
    FlightDateStatus,
    FlightDateStatusAvailable,
    FlightDB,
    FlightInfo,
    FlightType,
    Insurance,
    Passenger,
    Payment,
    Reservation,
    ReservationFlight,
    User,
)
from tau2.domains.airline.tools import AirlineTools as _BaseAirlineTools
from tau2.environment.toolkit import ToolType, is_tool

# Names of tools to REMOVE from the exposed agent toolset. Empty by default
# (the seed exposes exactly tau2's default airline tools, unchanged).
REMOVE_TOOLS: set[str] = set()

# IATA -> human city name, used to make reservation routes legible so the agent
# can match a reservation to the trip the user described in words (e.g. the user
# says "New York to Chicago" and the reservation is EWR/Newark -> ORD/Chicago).
_AIRPORT_CITY: dict[str, str] = {
    "SFO": "San Francisco", "JFK": "New York", "LAX": "Los Angeles",
    "ORD": "Chicago", "DFW": "Dallas", "DEN": "Denver", "SEA": "Seattle",
    "ATL": "Atlanta", "MIA": "Miami", "BOS": "Boston", "PHX": "Phoenix",
    "IAH": "Houston", "LAS": "Las Vegas", "MCO": "Orlando", "EWR": "Newark",
    "CLT": "Charlotte", "MSP": "Minneapolis", "DTW": "Detroit",
    "PHL": "Philadelphia", "LGA": "LaGuardia",
}

# Metro-area groups: several airports serve the same city the user names. A user
# saying "New York" may mean JFK, LGA, or EWR (Newark). Each group is a set of
# IATA codes plus every colloquial name that should resolve to that whole set.
_METRO_GROUPS: list[tuple[set[str], set[str]]] = [
    ({"JFK", "LGA", "EWR"}, {"new york", "new york city", "nyc", "newark", "laguardia"}),
]


def _location_to_iata(loc: str) -> set[str]:
    """Resolve a user-supplied location (a 3-letter IATA code OR a city name)
    into the SET of IATA codes it could mean. Metro-area aware, so "New York"
    expands to {JFK, LGA, EWR}. Returns an empty set if nothing matches (caller
    then treats the filter as 'unknown' and does not exclude on it).
    """
    if not loc:
        return set()
    raw = loc.strip()
    up = raw.upper()
    low = raw.lower()
    codes: set[str] = set()
    # Direct IATA code (also pull in metro siblings, e.g. EWR -> {JFK,LGA,EWR}).
    if len(up) == 3 and up in _AIRPORT_CITY:
        codes.add(up)
    # City-name match against the canonical map.
    for iata, city in _AIRPORT_CITY.items():
        if city.lower() == low:
            codes.add(iata)
    # Metro-area expansion (by code already collected OR by colloquial name).
    for group, names in _METRO_GROUPS:
        if low in names or (codes & group):
            codes |= group
    return codes


class AirlineTools(_BaseAirlineTools):
    """The full airline toolset. Subclasses tau2's ``AirlineTools`` to inherit the
    private helpers + ``ToolKitBase`` machinery; every agent-callable tool is
    re-declared below with its real body so the optimizer edits live code.
    """

    db: FlightDB

    def __init__(self, db: FlightDB) -> None:
        super().__init__(db)

    def _normalize_payment_methods(
        self, payment_methods: "List[Payment | dict]"
    ) -> list[dict]:
        """Coerce agent-supplied payment methods into a clean list of
        ``{"payment_id": str, "amount": int | None}`` dicts.

        This is tolerant of the two mistakes weaker models make most often:
          * using the key ``id`` (or ``source``/``type``) instead of ``payment_id``;
          * omitting ``amount`` entirely.
        ``amount`` is left as ``None`` when missing so the caller can auto-fill it
        (see ``book_reservation``); it is NOT invented here.
        """
        norm: list[dict] = []
        for pm in payment_methods:
            if isinstance(pm, Payment):
                norm.append({"payment_id": pm.payment_id, "amount": pm.amount})
                continue
            if isinstance(pm, dict):
                d = dict(pm)
                pid = d.get("payment_id") or d.get("id")
                if not pid:
                    raise ValueError(
                        "Each payment method needs a 'payment_id' such as "
                        "'credit_card_7815826', 'gift_card_7815826' or "
                        f"'certificate_7815826'. Got keys {sorted(d.keys())}."
                    )
                amt = d.get("amount")
                if amt is not None:
                    amt = int(round(float(amt)))
                norm.append({"payment_id": pid, "amount": amt})
                continue
            raise ValueError(f"Unrecognized payment method entry: {pm!r}")
        if not norm:
            raise ValueError("At least one payment method is required.")
        return norm

    @is_tool(ToolType.WRITE)
    def book_reservation(
        self,
        user_id: str,
        origin: str,
        destination: str,
        flight_type: FlightType,
        cabin: CabinClass,
        flights: List[FlightInfo | dict],
        passengers: List[Passenger | dict],
        payment_methods: List[Payment | dict],
        total_baggages: int,
        nonfree_baggages: int,
        insurance: Insurance,
    ) -> dict:
        """
        Book a reservation. Only call this AFTER you have listed the booking
        details to the user and the user has said yes / go ahead / proceed.

        The tool itself computes the total price (fares x passengers, plus
        $50 x nonfree_baggages, plus $30 x passengers if insurance == 'yes').
        You do NOT need to pre-compute the amount when paying with a SINGLE
        payment method: leave 'amount' off and the tool fills in the exact total
        for you. The returned 'payment_summary' / 'amount_charged' state the
        exact amount charged — repeat that figure back to the user.

        Args:
            user_id: The ID of the user to book the reservation such as 'sara_doe_496'.
            origin: The IATA code for the origin city such as 'SFO'.
            destination: The IATA code for the destination city such as 'JFK'.
            flight_type: The type of flight such as 'one_way' or 'round_trip'.
            cabin: The cabin class such as 'basic_economy', 'economy', or 'business'.
            flights: An array of flight-segment objects, each EXACTLY
                {"flight_number": "HAT001", "date": "2024-05-01"}. Do not add other keys.
            passengers: An array of passenger objects, each EXACTLY
                {"first_name": "Sara", "last_name": "Doe", "dob": "1990-04-05"}.
            payment_methods: An array of payment objects. Each MUST use the key
                'payment_id' (NOT 'id', 'type' or 'source'), e.g.
                [{"payment_id": "credit_card_7815826", "amount": 322}]. For a single
                payment method you may omit 'amount' and it is auto-filled to the
                full total. Valid payment_id prefixes: 'credit_card_', 'gift_card_',
                'certificate_'.
            total_baggages: The total number of baggage items to book the reservation.
            nonfree_baggages: The number of non-free (paid, $50 each) baggage items.
            insurance: Whether the reservation has insurance ('yes' or 'no').
        """
        if all(isinstance(flight, dict) for flight in flights):
            flights = [FlightInfo(**flight) for flight in flights]
        if all(isinstance(passenger, dict) for passenger in passengers):
            passengers = [Passenger(**passenger) for passenger in passengers]
        # Normalize the payment methods up front (tolerant of id/amount mistakes).
        norm_pms = self._normalize_payment_methods(payment_methods)

        user = self._get_user(user_id)
        reservation_id = self._get_new_reservation_id()

        reservation = Reservation(
            reservation_id=reservation_id,
            user_id=user_id,
            origin=origin,
            destination=destination,
            flight_type=flight_type,
            cabin=cabin,
            flights=[],
            passengers=deepcopy(passengers),
            payment_history=[],
            created_at=self._get_datetime(),
            total_baggages=total_baggages,
            nonfree_baggages=nonfree_baggages,
            insurance=insurance,
        )

        # Update flights and calculate price
        total_price = 0
        all_flights_date_data: list[FlightDateStatusAvailable] = []

        for flight_info in flights:
            flight_number = flight_info.flight_number
            flight = self._get_flight(flight_number)
            flight_date_data = self._get_flight_instance(
                flight_number=flight_number, date=flight_info.date
            )
            # Checking flight availability
            if not isinstance(flight_date_data, FlightDateStatusAvailable):
                raise ValueError(
                    f"Flight {flight_number} not available on date {flight_info.date}"
                )
            # Checking seat availability
            if flight_date_data.available_seats[cabin] < len(passengers):
                raise ValueError(f"Not enough seats on flight {flight_number}")
            # Calculate price
            price = flight_date_data.prices[cabin]
            # Update reservation
            reservation.flights.append(
                ReservationFlight(
                    origin=flight.origin,
                    destination=flight.destination,
                    flight_number=flight_number,
                    date=flight_info.date,
                    price=price,
                )
            )
            all_flights_date_data.append(flight_date_data)
            total_price += price * len(passengers)

        # Add insurance fee
        if insurance == "yes":
            total_price += 30 * len(passengers)

        # Add baggage fee
        total_price += 50 * nonfree_baggages

        # Auto-fill / auto-correct the payment amount. A single payment method
        # must always cover the full total exactly, so we set it deterministically
        # (fixes the frequent 'amount does not add up' / missing-amount errors).
        if len(norm_pms) == 1:
            norm_pms[0]["amount"] = total_price
        else:
            for pm in norm_pms:
                if pm["amount"] is None:
                    raise ValueError(
                        f"Missing 'amount' for payment method {pm['payment_id']!r}. "
                        f"Total price is {total_price}. With multiple payment methods, "
                        f"give each an integer 'amount' so they sum to exactly {total_price}."
                    )
        payment_methods = [
            Payment(payment_id=pm["payment_id"], amount=pm["amount"]) for pm in norm_pms
        ]
        reservation.payment_history = deepcopy(payment_methods)

        for payment_method in payment_methods:
            payment_id = payment_method.payment_id
            amount = payment_method.amount
            if payment_id not in user.payment_methods:
                raise ValueError(
                    f"Payment method {payment_id!r} not found in user profile. "
                    f"Available payment methods: {sorted(user.payment_methods.keys())}. "
                    f"Pass one of these as 'payment_id'."
                )

            user_payment_method = user.payment_methods[payment_id]
            if user_payment_method.source in {"gift_card", "certificate"}:
                if user_payment_method.amount < amount:
                    raise ValueError(
                        f"Not enough balance in payment method {payment_id} "
                        f"(balance ${user_payment_method.amount}, needs ${amount})"
                    )

        total_payment = sum(payment.amount for payment in payment_methods)
        if total_payment != total_price:
            raise ValueError(
                f"Payment amount does not add up, total price is {total_price}, but paid "
                f"{total_payment}. Adjust the amounts so they sum to exactly {total_price}."
            )

        # if checks pass, deduct payment
        for payment_method in payment_methods:
            payment_id = payment_method.payment_id
            amount = payment_method.amount
            user_payment_method = user.payment_methods[payment_id]
            if user_payment_method.source == "gift_card":
                user_payment_method.amount -= amount
            elif user_payment_method.source == "certificate":
                user.payment_methods.pop(payment_id)

        # Update DB
        for flight_date_data in all_flights_date_data:
            flight_date_data.available_seats[cabin] -= len(passengers)
        self.db.reservations[reservation_id] = reservation
        self.db.users[user_id].reservations.append(reservation_id)

        # Enriched return: give the agent the exact amount to report back so it
        # never has to recompute the total in its head.
        result = reservation.model_dump()
        result["amount_charged"] = total_price
        result["payment_summary"] = (
            f"Booked reservation {reservation_id}. Total charged: ${total_price} "
            f"for {len(passengers)} passenger(s), paid with "
            + ", ".join(f"${pm.amount} from {pm.payment_id}" for pm in payment_methods)
            + "."
        )
        return result

    @is_tool(ToolType.GENERIC)
    def calculate(self, expression: str) -> str:
        """
        Calculate the result of a mathematical expression.

        Args:
            expression: The mathematical expression to calculate, such as '2 + 2'. The expression can contain numbers, operators (+, -, *, /), parentheses, and spaces.

        Returns:
            The result of the mathematical expression.

        Raises:
            ValueError: If the expression is invalid.
        """
        if not all(char in "0123456789+-*/(). " for char in expression):
            raise ValueError("Invalid characters in expression")
        return str(round(float(eval(expression, {"__builtins__": None}, {})), 2))

    @is_tool(ToolType.WRITE)
    def cancel_reservation(self, reservation_id: str) -> Reservation:
        """
        Cancel the whole reservation.

        Args:
            reservation_id: The reservation ID, such as 'ZFA04Y'.

        Returns:
            The updated reservation.

        Raises:
            ValueError: If the reservation is not found.
            ValueError: If any flight segment has already been flown (transfer needed).
            ValueError: If the reservation does not meet ANY cancellation condition.
        """
        reservation = self._get_reservation(reservation_id)

        # ---- Policy eligibility gate (the API does NOT enforce these; the agent
        # must, so we enforce them here in code so an ineligible cancel can never
        # corrupt the database). All checks fire ONLY on the exact violating
        # condition, so an eligible cancel is never blocked. ----
        current_dt = self._get_datetime()
        current_date = str(current_dt)[:10]

        # (1) Already-flown segment -> cannot cancel, must transfer. A segment is
        # "flown" only if its date is strictly before the current date (same-day
        # flights are left to the agent so a legitimate same-day cancel is never
        # blocked).
        flown = [
            f.flight_number
            for f in reservation.flights
            if str(f.date)[:10] < current_date
        ]
        if flown:
            raise ValueError(
                f"Cannot cancel reservation {reservation_id}: flight segment(s) "
                f"{flown} already departed before {current_date} (already flown). "
                "Per policy a partially/fully flown reservation cannot be cancelled "
                "by the agent — transfer the user to a human agent instead."
            )

        # (2) Cancellation is allowed only if AT LEAST ONE of these holds:
        #   - booked within the last 24 hours
        #   - a flight in the reservation was cancelled by the airline
        #   - it is a business-cabin reservation
        #   - the reservation has travel insurance (a covered reason still needed,
        #     which only the agent can judge — so insurance alone lifts the block).
        # We compute the ones we can see. If NONE can hold, the reservation is
        # definitely not cancellable and we refuse (this is the SAFE, conservative
        # direction: we only block when every avenue is provably closed).
        booked_within_24h = False
        try:
            # _get_datetime() and created_at are ISO-8601 strings; parse both.
            now_dt = datetime.fromisoformat(str(current_dt))
            created_dt = datetime.fromisoformat(str(reservation.created_at))
            booked_within_24h = (now_dt - created_dt).total_seconds() <= 24 * 3600
        except Exception:
            # If we cannot parse the timestamps, do NOT block (conservative:
            # never over-refuse a possibly-eligible cancellation).
            booked_within_24h = True
        is_business = str(reservation.cabin) == "business"
        has_insurance = str(reservation.insurance) == "yes"
        airline_cancelled = False
        for f in reservation.flights:
            try:
                if str(self._get_flight_instance(f.flight_number, f.date).status) == "cancelled":
                    airline_cancelled = True
                    break
            except Exception:
                pass
        if not (booked_within_24h or is_business or has_insurance or airline_cancelled):
            raise ValueError(
                f"Cannot cancel reservation {reservation_id}: it meets none of the "
                "cancellation conditions (not booked within the last 24 hours, not "
                "airline-cancelled, not a business-cabin reservation, and no travel "
                f"insurance on file — cabin={reservation.cabin}, insurance="
                f"{reservation.insurance}, booked {str(reservation.created_at)[:10]}). "
                "Per policy this reservation cannot be cancelled — do NOT cancel it; "
                "explain this to the user."
            )

        logger.debug(reservation.model_dump_json(indent=4))
        # reverse the payment
        refunds = []
        for payment in reservation.payment_history:
            refunds.append(
                Payment(
                    payment_id=payment.payment_id,
                    amount=-payment.amount,
                )
            )
        reservation.payment_history.extend(refunds)
        reservation.status = "cancelled"
        logger.debug(self._get_reservation(reservation_id).model_dump_json(indent=4))
        # Release seats
        logger.warning("Seats release not implemented for cancellation!!!")
        return reservation

    @is_tool(ToolType.READ)
    def get_reservation_details(self, reservation_id: str) -> Reservation:
        """
        Get the details of a reservation.

        Args:
            reservation_id: The reservation ID, such as '8JX2WO'.

        Returns:
            The reservation details.

        Raises:
            ValueError: If the reservation is not found.
        """
        return self._get_reservation(reservation_id)

    def _reservation_summary(self, reservation) -> dict:
        """Build a compact, human-legible summary of ONE reservation so the agent
        can match it to the trip the user described in words."""
        o_city = _AIRPORT_CITY.get(reservation.origin, reservation.origin)
        d_city = _AIRPORT_CITY.get(reservation.destination, reservation.destination)
        return {
            "reservation_id": reservation.reservation_id,
            "route": f"{o_city} ({reservation.origin}) -> {d_city} ({reservation.destination})",
            "origin": reservation.origin,
            "destination": reservation.destination,
            "trip_type": str(reservation.flight_type),
            "cabin": str(reservation.cabin),
            "dates": sorted({str(f.date)[:10] for f in reservation.flights}),
            "passengers": [
                f"{p.first_name} {p.last_name}" for p in reservation.passengers
            ],
            "insurance": str(reservation.insurance),
        }

    @is_tool(ToolType.READ)
    def find_reservation(
        self,
        user_id: str,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
    ) -> list[dict]:
        """
        Find a user's reservation(s) BY ROUTE when the user describes a trip in
        words ("my New York to Chicago trip") but does NOT give a reservation id.

        Call this FIRST for any modify/cancel request where the reservation id is
        unknown — it removes the guesswork of picking the right reservation.

        How it matches: 'origin'/'destination' accept either a 3-letter IATA code
        ('EWR') OR a plain city name ('New York'); matching is metro-area aware, so
        'New York' matches Newark (EWR), JFK, and LaGuardia (LGA). If you pass only
        one of origin/destination, it filters on that one. If you pass neither, it
        returns ALL of the user's reservations so you can pick.

        Each returned row has 'reservation_id', a human 'route'
        ("Newark (EWR) -> Chicago (ORD)"), 'cabin', 'trip_type', 'dates',
        'passengers' and 'insurance'. Decision rule:
          - Exactly ONE row -> that is the reservation; use its reservation_id.
          - MORE than one, or ZERO -> ask the user which reservation before acting.
          - If a change the user requested is ALREADY true in a row (e.g. they ask
            to upgrade to economy but that row is already economy), it is probably
            the WRONG row — re-check the route.

        Args:
            user_id: The user whose reservations to search, e.g. 'omar_rossi_1241'.
            origin: OPTIONAL origin the user named — IATA ('EWR') or city ('New York').
            destination: OPTIONAL destination — IATA ('ORD') or city ('Chicago').

        Returns:
            A list of matching reservation summary dicts (see above).
        """
        user = self._get_user(user_id)
        want_o = _location_to_iata(origin) if origin else None
        want_d = _location_to_iata(destination) if destination else None
        rows: list[dict] = []
        for rid in user.reservations:
            try:
                reservation = self._get_reservation(rid)
            except Exception:
                continue
            # A filter only excludes when it resolved to a known set of codes AND
            # the reservation's endpoint is not in it (unknown/blank filter = no
            # exclusion, so a mis-typed city never hides everything).
            if want_o and reservation.origin not in want_o:
                continue
            if want_d and reservation.destination not in want_d:
                continue
            rows.append(self._reservation_summary(reservation))
        return rows

    @is_tool(ToolType.READ)
    def get_user_details(self, user_id: str) -> User:
        """
        Get the details of a user, including their reservations.

        Args:
            user_id: The user ID, such as 'sara_doe_496'.

        Returns:
            The user details.

        Raises:
            ValueError: If the user is not found.
        """
        return self._get_user(user_id)

    @is_tool(ToolType.READ)
    def list_all_airports(self) -> AirportInfo:
        """Returns a list of all available airports.

        Returns:
            A dictionary mapping IATA codes to AirportInfo objects.
        """
        return [
            AirportCode(iata="SFO", city="San Francisco"),
            AirportCode(iata="JFK", city="New York"),
            AirportCode(iata="LAX", city="Los Angeles"),
            AirportCode(iata="ORD", city="Chicago"),
            AirportCode(iata="DFW", city="Dallas"),
            AirportCode(iata="DEN", city="Denver"),
            AirportCode(iata="SEA", city="Seattle"),
            AirportCode(iata="ATL", city="Atlanta"),
            AirportCode(iata="MIA", city="Miami"),
            AirportCode(iata="BOS", city="Boston"),
            AirportCode(iata="PHX", city="Phoenix"),
            AirportCode(iata="IAH", city="Houston"),
            AirportCode(iata="LAS", city="Las Vegas"),
            AirportCode(iata="MCO", city="Orlando"),
            AirportCode(iata="EWR", city="Newark"),
            AirportCode(iata="CLT", city="Charlotte"),
            AirportCode(iata="MSP", city="Minneapolis"),
            AirportCode(iata="DTW", city="Detroit"),
            AirportCode(iata="PHL", city="Philadelphia"),
            AirportCode(iata="LGA", city="LaGuardia"),
        ]

    @is_tool(ToolType.READ)
    def search_direct_flight(
        self, origin: str, destination: str, date: str
    ) -> list[DirectFlight]:
        """
        Search for direct flights between two cities on a specific date.

        Args:
            origin: The origin city airport in three letters, such as 'JFK'.
            destination: The destination city airport in three letters, such as 'LAX'.
            date: The date of the flight in the format 'YYYY-MM-DD', such as '2024-01-01'.

        Returns:
            The direct flights between the two cities on the specific date.
        """
        # A search for a PAST date always returns nothing (those flights have
        # departed and cannot be booked). Agents sometimes loop on this when a
        # user refers to "the flight I took on <past date>". Redirect them to the
        # source of truth instead of returning an empty list they re-query.
        current_date = str(self._get_datetime())[:10]
        if str(date)[:10] < current_date:
            raise ValueError(
                f"Date {date} is in the past (current date is {current_date}); past "
                "flights cannot be searched or booked. If the user wants to re-book a "
                "flight they took/booked earlier, do NOT search this date — call "
                "find_reservation / get_reservation_details to read the exact "
                "flight_number(s) from that prior reservation, then search or book "
                "those flights on the NEW travel date."
            )
        return self._search_direct_flight(
            date=date, origin=origin, destination=destination
        )

    @is_tool(ToolType.READ)
    def search_onestop_flight(
        self, origin: str, destination: str, date: str
    ) -> list[tuple[DirectFlight, DirectFlight]]:
        """
        Search for one-stop flights between two cities on a specific date.

        Args:
            origin: The origin city airport in three letters, such as 'JFK'.
            destination: The destination city airport in three letters, such as 'LAX'.
            date: The date of the flight in the format 'YYYY-MM-DD', such as '2024-05-01'.

        Returns:
            A list of pairs of DirectFlight objects.
        """
        results = []
        for result1 in self._search_direct_flight(
            date=date, origin=origin, destination=None
        ):
            result1.date = date
            date2 = (
                f"2024-05-{int(date[-2:]) + 1}"
                if "+1" in result1.scheduled_arrival_time_est
                else date
            )
            for result2 in self._search_direct_flight(
                date=date2,
                origin=result1.destination,
                destination=destination,
                leave_after=result1.scheduled_arrival_time_est,
            ):
                result2.date = date2
                results.append([result1, result2])
        return results

    @is_tool(ToolType.WRITE)
    def send_certificate(self, user_id: str, amount: int) -> str:
        """
        Send a certificate to a user. Be careful!

        Args:
            user_id: The ID of the user to book the reservation, such as 'sara_doe_496'.
            amount: The amount of the certificate to send.

        Returns:
            A message indicating the certificate was sent.

        Raises:
            ValueError: If the user is not found.
        """
        user = self._get_user(user_id)

        # add a certificate, assume at most 3 cases per task
        for payment_id in [f"certificate_{id}" for id in self._get_new_payment_id()]:
            if payment_id not in user.payment_methods:
                new_payment = Certificate(
                    id=payment_id,
                    amount=amount,
                    source="certificate",
                )
                user.payment_methods[payment_id] = new_payment
                return f"Certificate {payment_id} added to user {user_id} with amount {amount}."
        raise ValueError("Too many certificates")

    @is_tool(ToolType.GENERIC)
    def transfer_to_human_agents(self, summary: str) -> str:
        """
        Transfer the user to a human agent, with a summary of the user's issue.
        Only transfer if
         -  the user explicitly asks for a human agent
         -  given the policy and the available tools, you cannot solve the user's issue.

        Args:
            summary: A summary of the user's issue.

        Returns:
            A message indicating the user has been transferred to a human agent.
        """
        return "Transfer successful"

    @is_tool(ToolType.WRITE)
    def update_reservation_baggages(
        self,
        reservation_id: str,
        total_baggages: int,
        nonfree_baggages: int,
        payment_id: str,
    ) -> dict:
        """
        Update the baggage information of a reservation. Only call this after the
        user has confirmed. Each paid (non-free) bag costs $50; the tool computes
        the charge and reports it in 'payment_summary' / 'amount_charged'.

        Args:
            reservation_id: The reservation ID, such as 'ZFA04Y'
            total_baggages: The updated TOTAL number of baggage items (free + paid).
            nonfree_baggages: The updated number of non-free (paid, $50 each) bags. If the
                free allowance covers all requested bags, set this to 0 (no charge).
            payment_id: A single payment id already in the user profile, such as
                'credit_card_7815826', 'gift_card_7815826'. A certificate cannot be used.

        Returns:
            A dict of the updated reservation plus 'amount_charged' and 'payment_summary'.

        Raises:
            ValueError: If the reservation is not found.
            ValueError: If the user is not found.
            ValueError: If the payment method is not found.
            ValueError: If the certificate cannot be used to update reservation.
            ValueError: If the gift card balance is not enough.
        """
        reservation = self._get_reservation(reservation_id)
        user = self._get_user(reservation.user_id)

        # Calculate price
        total_price = 50 * max(0, nonfree_baggages - reservation.nonfree_baggages)

        # Create payment
        payment = self._payment_for_update(user, payment_id, total_price)
        if payment is not None:
            reservation.payment_history.append(payment)

        # Update reservation
        reservation.total_baggages = total_baggages
        reservation.nonfree_baggages = nonfree_baggages

        # Enriched return: exact baggage charge for the agent to report.
        result = reservation.model_dump()
        result["amount_charged"] = total_price
        if total_price > 0:
            result["payment_summary"] = (
                f"Updated to {total_baggages} total bag(s) ({nonfree_baggages} paid). "
                f"Charged ${total_price} to {payment_id}."
            )
        else:
            result["payment_summary"] = (
                f"Updated to {total_baggages} total bag(s). No baggage charge "
                f"(all within the free allowance)."
            )
        return result

    @is_tool(ToolType.WRITE)
    def update_reservation_flights(
        self,
        reservation_id: str,
        cabin: CabinClass,
        flights: List[FlightInfo | dict],
        payment_id: str,
    ) -> dict:
        """
        Update the flight information (and/or cabin) of a reservation. Only call
        this after the user has confirmed. The tool computes the price difference
        (already multiplied by the number of passengers) and reports the exact
        charge or refund in 'payment_summary' / 'amount_charged' / 'amount_refunded'.

        Args:
            reservation_id: The reservation ID, such as 'ZFA04Y'.
            cabin: The cabin class for the WHOLE reservation ('basic_economy',
                'economy' or 'business'). All segments share one cabin. To change
                only the cabin (e.g. a downgrade), pass the SAME flight segments
                with the new cabin.
            flights: An array of EVERY flight segment in the new reservation, each
                EXACTLY {"flight_number": "HAT001", "date": "2024-05-01"}. Include
                unchanged segments too — anything omitted is dropped.
            payment_id: A single payment id already in the user profile, such as
                'credit_card_7815826' or 'gift_card_7815826', used to charge a
                difference or receive a refund. A certificate cannot be used here.

        Returns:
            A dict of the updated reservation plus 'amount_charged'/'amount_refunded'
            and a 'payment_summary'.

        Raises:
            ValueError: If the reservation is not found.
            ValueError: If the user is not found.
            ValueError: If the payment method is not found.
            ValueError: If the certificate cannot be used to update reservation.
            ValueError: If the gift card balance is not enough.
        """
        if all(isinstance(flight, dict) for flight in flights):
            flights = [FlightInfo(**flight) for flight in flights]
        reservation = self._get_reservation(reservation_id)
        user = self._get_user(reservation.user_id)

        # update flights and calculate price
        total_price = 0
        reservation_flights = []
        for flight_info in flights:
            # if existing flight, keep it
            matching_reservation_flight = next(
                (
                    reservation_flight
                    for reservation_flight in reservation.flights
                    if reservation_flight.flight_number == flight_info.flight_number
                    and reservation_flight.date == flight_info.date
                    and cabin == reservation.cabin
                ),
                None,
            )
            if matching_reservation_flight:
                total_price += matching_reservation_flight.price * len(
                    reservation.passengers
                )
                reservation_flights.append(matching_reservation_flight)
                continue

            # If new flight:
            flight = self._get_flight(flight_info.flight_number)
            # Check flight availability
            flight_date_data = self._get_flight_instance(
                flight_number=flight_info.flight_number,
                date=flight_info.date,
            )
            if not isinstance(flight_date_data, FlightDateStatusAvailable):
                raise ValueError(
                    f"Flight {flight_info.flight_number} not available on date {flight_info.date}"
                )

            # Check seat availability
            if flight_date_data.available_seats[cabin] < len(reservation.passengers):
                raise ValueError(
                    f"Not enough seats on flight {flight_info.flight_number}"
                )

            # Calculate price and add to reservation
            reservation_flight = ReservationFlight(
                flight_number=flight_info.flight_number,
                date=flight_info.date,
                price=flight_date_data.prices[cabin],
                origin=flight.origin,
                destination=flight.destination,
            )
            total_price += reservation_flight.price * len(reservation.passengers)
            reservation_flights.append(reservation_flight)

        # Deduct amount already paid for reservation
        total_price -= sum(flight.price for flight in reservation.flights) * len(
            reservation.passengers
        )

        # Create payment
        payment = self._payment_for_update(user, payment_id, total_price)
        if payment is not None:
            reservation.payment_history.append(payment)

        # Update reservation
        reservation.flights = reservation_flights
        reservation.cabin = cabin  # This was missing from original TauBench

        # Enriched return: state the exact charge/refund (already multiplied by the
        # number of passengers) so the agent reports the correct figure to the user.
        npax = len(reservation.passengers)
        new_flights_total = sum(f.price for f in reservation.flights) * npax
        result = reservation.model_dump()
        result["amount_charged"] = total_price if total_price > 0 else 0
        result["amount_refunded"] = -total_price if total_price < 0 else 0
        result["new_flights_total_price"] = new_flights_total
        if total_price > 0:
            result["payment_summary"] = (
                f"Charged ${total_price} to {payment_id}. New flights total: "
                f"${new_flights_total} for {npax} passenger(s)."
            )
        elif total_price < 0:
            result["payment_summary"] = (
                f"Refunded ${-total_price} to {payment_id}. New flights total: "
                f"${new_flights_total} for {npax} passenger(s)."
            )
        else:
            result["payment_summary"] = (
                f"No price difference; nothing charged or refunded. New flights total: "
                f"${new_flights_total} for {npax} passenger(s)."
            )
        return result

    @is_tool(ToolType.WRITE)
    def update_reservation_passengers(
        self, reservation_id: str, passengers: List[Passenger | dict]
    ) -> Reservation:
        """
        Update the passenger information of a reservation.

        Args:
            reservation_id: The reservation ID, such as 'ZFA04Y'.
            passengers: An array with ONE object per existing passenger, in the
                same order as the reservation, each EXACTLY
                {"first_name": "Mei", "last_name": "Garcia", "dob": "1989-12-13"}.
                You MUST pass every passenger (the count cannot change). For a
                passenger whose date of birth is NOT changing you may OMIT 'dob' —
                the tool reads the stored value from the reservation for you, so
                you never need to ask the user for a date of birth already on file.

        Returns:
            The updated reservation.

        Raises:
            ValueError: If the reservation is not found.
            ValueError: If the number of passengers does not match.
        """
        reservation = self._get_reservation(reservation_id)

        # The passenger COUNT cannot change (policy). Give an actionable error
        # naming the required count and the names currently on the reservation.
        if len(passengers) != len(reservation.passengers):
            existing = [f"{p.first_name} {p.last_name}" for p in reservation.passengers]
            raise ValueError(
                f"Number of passengers does not match: reservation {reservation_id} has "
                f"{len(reservation.passengers)} passenger(s) ({existing}) but you passed "
                f"{len(passengers)}. Pass exactly one object per existing passenger, in "
                "order. The number of passengers cannot be changed."
            )

        # Auto-fill any missing 'dob' POSITIONALLY from the existing reservation,
        # so a name/field correction never stalls waiting for a date of birth the
        # reservation already holds. Fires ONLY when a dict omits 'dob'; a fully
        # specified passenger (Passenger object or dict with dob) is untouched.
        norm_passengers: list[Passenger] = []
        for idx, passenger in enumerate(passengers):
            if isinstance(passenger, Passenger):
                norm_passengers.append(passenger)
                continue
            d = dict(passenger)
            if not d.get("dob"):
                d["dob"] = reservation.passengers[idx].dob
            norm_passengers.append(Passenger(**d))
        passengers = norm_passengers

        logger.info(len(passengers))
        logger.info(len(reservation.passengers))
        reservation.passengers = deepcopy(passengers)
        return reservation

    @is_tool(ToolType.READ)
    def get_flight_status(self, flight_number: str, date: str) -> str:
        """
        Get the status of a flight.

        Args:
            flight_number: The flight number.
            date: The date of the flight.

        Returns:
            The status of the flight.

        Raises:
            ValueError: If the flight is not found.
        """
        return self._get_flight_instance(flight_number, date).status
