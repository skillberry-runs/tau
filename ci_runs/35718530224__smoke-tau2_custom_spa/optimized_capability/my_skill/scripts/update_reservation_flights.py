def update_reservation_flights(reservation_id: str, cabin: str, flights: list, payment_id: str):
    """
    Update the flight information of a reservation.

    Args:
        reservation_id: The reservation ID, such as 'ZFA04Y'.
        cabin: The cabin class of the ENTIRE reservation ('basic_economy', 'economy', or 'business'). If the flights are unchanged, pass the reservation's current cabin.
        flights: A list describing the ENTIRE new itinerary, EARLIEST FIRST — every segment that should be on the reservation after the update, INCLUDING any segment that is not changing. Each item MUST be exactly {"flight_number": "HAT056", "date": "2024-05-25"} (date is YYYY-MM-DD). Do NOT include origin, destination, or price — they are ignored. Dropping an unchanged segment will delete it from the reservation.
        payment_id: A SINGLE payment id from the user's profile used to pay any price difference (or receive a refund). Use a 'credit_card_...' or a 'gift_card_...' id. A 'certificate_...' is NOT allowed for updates. Pass the id string, e.g. 'credit_card_7815826'.

    Returns:
        The updated reservation, or an actionable error string if the request is invalid.
    """
    def _norm_flights(fl):
        out = []
        for f in fl:
            if isinstance(f, dict):
                nf = {k: f[k] for k in ("flight_number", "date") if k in f}
                out.append(nf if nf else f)
            else:
                out.append(f)
        return out

    def _norm_pid(pid):
        if isinstance(pid, dict):
            return pid.get("payment_id", pid.get("id", pid))
        return pid

    flights = _norm_flights(flights)
    payment_id = _norm_pid(payment_id)

    result = env_update_reservation_flights(reservation_id=reservation_id, cabin=cabin, flights=flights, payment_id=payment_id)

    if isinstance(result, str):
        low = result.lower()
        if "certificate" in low:
            return (result + " | A certificate cannot pay for an update. Retry with a "
                    "'credit_card_...' payment_id (or a 'gift_card_...' with enough balance) "
                    "from the user's profile.")
        if "gift card balance" in low or "gift_card balance" in low:
            return (result + " | This gift card lacks the funds for the price difference. "
                    "Retry with a 'credit_card_...' payment_id from the user's profile.")
    return result
