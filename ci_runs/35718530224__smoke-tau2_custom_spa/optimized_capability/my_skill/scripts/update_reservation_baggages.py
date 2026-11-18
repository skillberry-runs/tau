def update_reservation_baggages(reservation_id: str, total_baggages: int, nonfree_baggages: int, payment_id: str):
    """
    Update the baggage information of a reservation. Only ADDING non-free bags costs money
    ($50 each); if nonfree_baggages is not increased, no payment is taken.

    Args:
        reservation_id: The reservation ID, such as 'ZFA04Y'.
        total_baggages: The updated TOTAL number of checked bags on the reservation (free + non-free), across all passengers.
        nonfree_baggages: The updated number of NON-FREE checked bags (each costs $50).
        payment_id: A SINGLE payment id from the user's profile to pay for any added non-free bags. Use a 'credit_card_...' or a 'gift_card_...' id. A 'certificate_...' is NOT allowed for updates. Pass the id string, e.g. 'credit_card_7815826'.

    Returns:
        The updated reservation, or an actionable error string if the request is invalid.
    """
    def _norm_pid(pid):
        if isinstance(pid, dict):
            return pid.get("payment_id", pid.get("id", pid))
        return pid

    payment_id = _norm_pid(payment_id)

    result = env_update_reservation_baggages(reservation_id=reservation_id, total_baggages=total_baggages, nonfree_baggages=nonfree_baggages, payment_id=payment_id)

    if isinstance(result, str):
        low = result.lower()
        if "certificate" in low:
            return (result + " | A certificate cannot pay for an update. Retry with a "
                    "'credit_card_...' payment_id (or a 'gift_card_...' with enough balance) "
                    "from the user's profile.")
        if "gift card balance" in low or "gift_card balance" in low:
            return (result + " | This gift card lacks the funds. Retry with a "
                    "'credit_card_...' payment_id from the user's profile.")
    return result
