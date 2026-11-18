def book_reservation(user_id: str, origin: str, destination: str, flight_type: str, cabin: str, flights: list, passengers: list, payment_methods: list, total_baggages: int, nonfree_baggages: int, insurance: str):
    """
    Book a reservation. The tool NORMALIZES your arguments and, when you pass a
    single payment method (or several with exactly one credit card), it AUTO-FILLS the
    payment amount to the exact total the system computes — so you do NOT have to get the
    arithmetic right yourself. Just pass the correct flights, passengers, and payment ids.

    Args:
        user_id: The user ID such as 'sara_doe_496'.
        origin: The IATA code for the ORIGIN of the whole trip such as 'SFO'.
        destination: The IATA code for the DESTINATION of the whole trip such as 'JFK'. For a round trip this is the farthest city, NOT the return-to origin.
        flight_type: 'one_way' or 'round_trip'.
        cabin: One of 'basic_economy', 'economy', or 'business'. Use the SAME cabin for every segment.
        flights: A list of flight segments, EARLIEST FIRST. Each item MUST be exactly {"flight_number": "HAT271", "date": "2024-05-26"} (date is YYYY-MM-DD). Do NOT include origin, destination, or price — they are ignored. Include EVERY segment (both legs of a round trip).
        passengers: A list, one object PER PASSENGER, each exactly {"first_name": "Sophia", "last_name": "Silva", "dob": "1957-10-05"} (dob is YYYY-MM-DD). Every passenger needs a dob; look it up in the user profile if it is not stated.
        payment_methods: A list of payment objects. Each item is {"payment_id": "credit_card_4196779", "amount": 228}. The 'payment_id' MUST be a key that exists in the user's profile payment_methods (e.g. 'credit_card_...', 'gift_card_...', 'certificate_...'); NOT 'id', 'source', or 'type'. If you pass a single payment method, the 'amount' is auto-corrected to the exact total, so any placeholder amount is fine. Example single: [{"payment_id": "certificate_8045380", "amount": 0}]. Example split: [{"payment_id": "gift_card_8516878", "amount": 128}, {"payment_id": "credit_card_9", "amount": 0}] — the credit card is auto-filled to cover the remainder.
        total_baggages: Total number of checked bags across all passengers.
        nonfree_baggages: Number of checked bags that are NOT free (each adds a $50 fee).
        insurance: 'yes' or 'no' (each insured passenger adds a $30 fee).

    Returns:
        The booked reservation, or an actionable error string if the request is invalid.
    """
    import re

    def _norm_flights(fl):
        out = []
        for f in fl:
            if isinstance(f, dict):
                nf = {k: f[k] for k in ("flight_number", "date") if k in f}
                out.append(nf if nf else f)
            else:
                out.append(f)
        return out

    def _norm_payments(pms):
        out = []
        for p in pms:
            if isinstance(p, dict):
                pid = p.get("payment_id", p.get("id"))
                np = {}
                if pid is not None:
                    np["payment_id"] = pid
                if p.get("amount") is not None:
                    np["amount"] = p["amount"]
                out.append(np if np else p)
            else:
                out.append(p)
        return out

    def _norm_passengers(ps):
        out = []
        for p in ps:
            if isinstance(p, dict):
                np = {k: p[k] for k in ("first_name", "last_name", "dob") if k in p}
                out.append(np if np else p)
            else:
                out.append(p)
        return out

    def _fix_amounts(pms, total):
        # Only touch dict payments; leave objects/unknowns alone.
        if len(pms) == 1 and isinstance(pms[0], dict):
            pms[0]["amount"] = total
            return True
        ids = [p.get("payment_id", "") if isinstance(p, dict) else "" for p in pms]
        cc = [i for i, pid in enumerate(ids) if isinstance(pid, str) and pid.startswith("credit_card")]
        if len(cc) == 1 and isinstance(pms[cc[0]], dict):
            others = sum((p.get("amount", 0) or 0) for i, p in enumerate(pms) if i != cc[0] and isinstance(p, dict))
            rem = total - others
            if rem > 0:
                pms[cc[0]]["amount"] = rem
                return True
        return False

    flights = _norm_flights(flights)
    passengers = _norm_passengers(passengers)
    payment_methods = _norm_payments(payment_methods)

    def _call():
        return env_book_reservation(
            user_id=user_id, origin=origin, destination=destination,
            flight_type=flight_type, cabin=cabin, flights=flights,
            passengers=passengers, payment_methods=payment_methods,
            total_baggages=total_baggages, nonfree_baggages=nonfree_baggages,
            insurance=insurance,
        )

    result = _call()
    # Auto-correct the payment amount when the ONLY problem is the arithmetic.
    if isinstance(result, str) and "total price is" in result:
        m = re.search(r"total price is (\d+)", result)
        if m and _fix_amounts(payment_methods, int(m.group(1))):
            result = _call()
    return result
