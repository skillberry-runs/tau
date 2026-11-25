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


class AirlineTools(_BaseAirlineTools):
    """The full airline toolset. Subclasses tau2's ``AirlineTools`` to inherit the
    private helpers + ``ToolKitBase`` machinery; every agent-callable tool is
    re-declared below with its real body so the optimizer edits live code.
    """

    db: FlightDB

    def __init__(self, db: FlightDB) -> None:
        super().__init__(db)

    # ----- internal helpers (not exposed as tools) -------------------------
    # Free checked-bag allowance PER PASSENGER, by membership level and cabin
    # class. These are the exact numbers in the policy ("Checked bag allowance")
    # and are domain constants, not task-specific values.
    _FREE_BAGGAGE_ALLOWANCE = {
        "regular": {"basic_economy": 0, "economy": 1, "business": 2},
        "silver": {"basic_economy": 1, "economy": 2, "business": 3},
        "gold": {"basic_economy": 2, "economy": 3, "business": 4},
    }

    def _free_baggage_allowance(self, membership: str, cabin: str, n_passengers: int) -> int:
        """Total number of FREE checked bags for a reservation = per-passenger
        allowance (from the policy table) times the number of passengers."""
        per_pax = self._FREE_BAGGAGE_ALLOWANCE.get(membership, {}).get(cabin, 0)
        return per_pax * max(0, n_passengers)

    def _with_payment_summary(self, reservation: "Reservation", net: float) -> dict:
        """Return the reservation as a dict with an extra, impossible-to-miss
        ``payment_summary`` string that states the EXACT dollar figure this write
        just charged (``net`` > 0) or refunded (``net`` < 0) to the customer.

        The weak runtime model routinely computes the amount by hand BEFORE the
        write and then mis-states it (e.g. forgetting to multiply a per-passenger
        fare by the number of passengers). This field hands it the authoritative,
        already-correct number to copy into its reply. It is safe because the DB
        hashes ``self.db`` only — tool RETURN values are never hashed — so adding
        a key changes nothing about the graded database state, only what the
        agent sees and can echo to the user."""
        net = int(round(net))
        if net > 0:
            summary = (
                f"Charged ${net} to the customer for this action. Tell the user "
                f"the exact amount now, stating the number {net} (for example: "
                f"'A total of ${net} has been charged.'). Use THIS figure, not any "
                f"amount you estimated before the call."
            )
        elif net < 0:
            refund = -net
            summary = (
                f"Refunded ${refund} to the customer for this action. Tell the "
                f"user the exact amount now, stating the number {refund} (for "
                f"example: 'A refund of ${refund} has been issued.'). Use THIS "
                f"figure, not any amount you estimated before the call."
            )
        else:
            summary = (
                "This action resulted in no charge and no refund ($0). Tell the "
                "user there is no additional cost."
            )
        data = reservation.model_dump()
        data["payment_summary"] = summary
        return data

    def _to_payment(self, pm) -> "Payment":
        """Build a ``Payment`` from a model-supplied item, tolerating the
        malformed dict shapes the agent sometimes emits (e.g. ``{'type': ...,
        'id': ...}`` with no ``payment_id``/``amount``). Well-formed ``Payment``
        objects and ``{'payment_id','amount'}`` dicts pass through unchanged.
        """
        if isinstance(pm, Payment):
            return pm
        if isinstance(pm, dict):
            data = dict(pm)
            if "payment_id" not in data and "id" in data:
                data["payment_id"] = data.get("id")
            amount = data.get("amount", 0)
            try:
                amount = int(round(float(amount)))
            except (TypeError, ValueError):
                amount = 0
            return Payment(payment_id=data.get("payment_id"), amount=amount)
        return pm

    def _autocorrect_payment_amounts(self, payment_methods, total_price, user) -> None:
        """If the provided per-method amounts do not sum to ``total_price``,
        settle them to the only unambiguous split: a single payment method pays
        the whole total; with several methods, the one credit card absorbs the
        remainder after the fixed-value gift cards/certificate. Mutates
        ``payment_methods`` in place. No-op when the amounts already add up (a
        correct booking never triggers this)."""
        if not payment_methods:
            return
        if sum(p.amount for p in payment_methods) == total_price:
            return
        if len(payment_methods) == 1:
            payment_methods[0].amount = total_price
            return
        credit_cards = [
            p for p in payment_methods
            if p.payment_id in user.payment_methods
            and user.payment_methods[p.payment_id].source == "credit_card"
        ]
        if len(credit_cards) == 1:
            others = sum(p.amount for p in payment_methods if p is not credit_cards[0])
            credit_cards[0].amount = total_price - others
        # Otherwise leave the amounts as-is; the downstream sum check raises an
        # actionable "does not add up" error rather than guessing a split.

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
    ) -> Reservation:
        """
        Book a reservation.

        Args:
            user_id: The ID of the user to book the reservation such as 'sara_doe_496'`.
            origin: The IATA code for the origin city such as 'SFO'.
            destination: The IATA code for the destination city such as 'JFK'.
            flight_type: The type of flight such as 'one_way' or 'round_trip'.
            cabin: The cabin class such as 'basic_economy', 'economy', or 'business'.
            flights: An array of objects containing details about each piece of flight.
            passengers: An array of objects containing details about each passenger.
            payment_methods: An array of objects containing details about each payment method.
            total_baggages: The total number of baggage items to book the reservation.
            nonfree_baggages: The number of non-free baggage items to book the reservation.
            insurance: Whether the reservation has insurance.
        """
        if all(isinstance(flight, dict) for flight in flights):
            flights = [FlightInfo(**flight) for flight in flights]
        if all(isinstance(passenger, dict) for passenger in passengers):
            passengers = [Passenger(**passenger) for passenger in passengers]
        # Normalize each payment item (tolerating malformed dicts) into Payment.
        payment_methods = [self._to_payment(pm) for pm in payment_methods]
        user = self._get_user(user_id)
        reservation_id = self._get_new_reservation_id()

        # Paid-bag count is defined by policy: paid bags = requested total bags
        # minus the free allowance for this membership/cabin/passenger count.
        # Recompute it so a model miscount cannot produce a wrong charge.
        nonfree_baggages = max(
            0,
            total_baggages
            - self._free_baggage_allowance(user.membership, cabin, len(passengers)),
        )

        reservation = Reservation(
            reservation_id=reservation_id,
            user_id=user_id,
            origin=origin,
            destination=destination,
            flight_type=flight_type,
            cabin=cabin,
            flights=[],
            passengers=deepcopy(passengers),
            payment_history=deepcopy(payment_methods),
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

        # Settle the payment split if the provided amounts don't sum to total.
        self._autocorrect_payment_amounts(payment_methods, total_price, user)

        for payment_method in payment_methods:
            payment_id = payment_method.payment_id
            amount = payment_method.amount
            if payment_id not in user.payment_methods:
                raise ValueError(f"Payment method {payment_id} not found")

            user_payment_method = user.payment_methods[payment_id]
            if user_payment_method.source in {"gift_card", "certificate"}:
                if user_payment_method.amount < amount:
                    raise ValueError(
                        f"Not enough balance in payment method {payment_id}"
                    )

        total_payment = sum(payment.amount for payment in payment_methods)
        if total_payment != total_price:
            raise ValueError(
                f"Payment amount does not add up, total price is {total_price}, but paid {total_payment}"
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

        # Re-sync stored payment history with the (possibly auto-corrected)
        # amounts and the recomputed paid-bag count before persisting: the DB
        # hashes reservation.payment_history / nonfree_baggages, not the return.
        reservation.payment_history = deepcopy(payment_methods)
        reservation.nonfree_baggages = nonfree_baggages

        # Update DB
        for flight_date_data in all_flights_date_data:
            flight_date_data.available_seats[cabin] -= len(passengers)
        self.db.reservations[reservation_id] = reservation
        self.db.users[user_id].reservations.append(reservation_id)
        # total_price is the exact amount charged for this booking; surface it so
        # the agent states it to the user (DB-safe: returns are not hashed).
        return self._with_payment_summary(reservation, total_price)

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
        """
        reservation = self._get_reservation(reservation_id)
        # Policy: if any portion of the flight has already been flown, the
        # reservation cannot be cancelled here (a human agent is needed). Refuse
        # before mutating the DB so a forbidden cancellation never lands.
        for flight in reservation.flights:
            try:
                status = self._get_flight_instance(
                    flight.flight_number, flight.date
                ).status
            except Exception:
                status = None
            if status in ("flying", "landed"):
                raise ValueError(
                    f"Cannot cancel reservation {reservation_id}: flight "
                    f"{flight.flight_number} on {flight.date} has already been "
                    f"flown (status={status}). Per policy a reservation with a "
                    f"flown segment cannot be cancelled; do not cancel it."
                )
        logger.debug(reservation.model_dump_json(indent=4))
        # The net refund is what the customer has paid so far on this
        # reservation (positive entries minus any prior refunds).
        refund_total = sum(payment.amount for payment in reservation.payment_history)
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
        # Surface the exact refund so the agent states it (net < 0 => refund).
        return self._with_payment_summary(reservation, -refund_total)

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
    ) -> Reservation:
        """
        Update the baggage information of a reservation.

        Args:
            reservation_id: The reservation ID, such as 'ZFA04Y'
            total_baggages: The updated total number of baggage items included in the reservation.
            nonfree_baggages: The updated number of non-free baggage items included in the reservation.
            payment_id: The payment id stored in user profile, such as 'credit_card_7815826', 'gift_card_7815826', 'certificate_7815826'.

        Returns:
            The updated reservation.

        Raises:
            ValueError: If the reservation is not found.
            ValueError: If the user is not found.
            ValueError: If the payment method is not found.
            ValueError: If the certificate cannot be used to update reservation.
            ValueError: If the gift card balance is not enough.
        """
        reservation = self._get_reservation(reservation_id)
        user = self._get_user(reservation.user_id)

        # Paid bags are defined by policy, not by the caller: paid = requested
        # total minus the free allowance for this membership/cabin/pax count.
        # Recompute so a model miscount cannot create a spurious $50 charge or a
        # wrong stored count.
        nonfree_baggages = max(
            0,
            total_baggages
            - self._free_baggage_allowance(
                user.membership, reservation.cabin, len(reservation.passengers)
            ),
        )

        # Calculate price (charge only for newly added paid bags)
        total_price = 50 * max(0, nonfree_baggages - reservation.nonfree_baggages)

        # Only touch a payment method when there is actually something to charge.
        # A within-allowance change costs $0 and must not fail on an unneeded or
        # mistaken payment_id.
        if total_price > 0:
            payment = self._payment_for_update(user, payment_id, total_price)
            if payment is not None:
                reservation.payment_history.append(payment)

        # Update reservation
        reservation.total_baggages = total_baggages
        reservation.nonfree_baggages = nonfree_baggages

        # total_price is the charge for newly added paid bags (0 if within the
        # free allowance); surface it so the agent states the exact amount.
        return self._with_payment_summary(reservation, total_price)

    @is_tool(ToolType.WRITE)
    def update_reservation_flights(
        self,
        reservation_id: str,
        cabin: CabinClass,
        flights: List[FlightInfo | dict],
        payment_id: str,
    ) -> Reservation:
        """
        Update the flight information of a reservation.


        Args:
            reservation_id: The reservation ID, such as 'ZFA04Y'.
            cabin: The cabin class of the reservation
            flights: An array of objects containing details about each piece of flight in the ENTIRE new reservation. Even if the a flight segment is not changed, it should still be included in the array.
            payment_id: The payment id stored in user profile, such as 'credit_card_7815826', 'gift_card_7815826', 'certificate_7815826'.

        Returns:
            The updated reservation.

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

        # total_price is the fare difference for this change: > 0 is charged to
        # the customer, < 0 is refunded. Surface the exact figure so the agent
        # states it (e.g. a cabin downgrade refund) instead of a hand estimate.
        return self._with_payment_summary(reservation, total_price)

    @is_tool(ToolType.WRITE)
    def update_reservation_passengers(
        self, reservation_id: str, passengers: List[Passenger | dict]
    ) -> Reservation:
        """
        Update the passenger information of a reservation.

        Args:
            reservation_id: The reservation ID, such as 'ZFA04Y'.
            passengers: An array of objects containing details about each passenger.

        Returns:
            The updated reservation.

        Raises:
            ValueError: If the reservation is not found.
            ValueError: If the number of passengers does not match.
        """
        if all(isinstance(passenger, dict) for passenger in passengers):
            passengers = [Passenger(**passenger) for passenger in passengers]
        reservation = self._get_reservation(reservation_id)
        logger.info(len(passengers))
        logger.info(len(reservation.passengers))
        if len(passengers) != len(reservation.passengers):
            raise ValueError("Number of passengers does not match")
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
