def update_reservation_passengers(reservation_id: str, passengers: list):
    """
    Update the passenger information of a reservation. The number of passengers CANNOT
    change — you must pass exactly the same COUNT of passengers the reservation already
    has (look it up with get_reservation_details first). To carry a passenger over
    unchanged, still include their full object.

    Args:
        reservation_id: The reservation ID, such as 'ZFA04Y'.
        passengers: A list, one object PER passenger, each exactly {"first_name": "Omar", "last_name": "Rossi", "dob": "1970-06-06"} (dob is YYYY-MM-DD). Every passenger needs a dob. The list LENGTH must equal the reservation's current passenger count.

    Returns:
        The updated reservation, or an actionable error string if the request is invalid.
    """
    def _norm_passengers(ps):
        out = []
        for p in ps:
            if isinstance(p, dict):
                np = {k: p[k] for k in ("first_name", "last_name", "dob") if k in p}
                out.append(np if np else p)
            else:
                out.append(p)
        return out

    passengers = _norm_passengers(passengers)
    result = env_update_reservation_passengers(reservation_id=reservation_id, passengers=passengers)

    if isinstance(result, str) and "number of passengers" in result.lower():
        try:
            details = env_get_reservation_details(reservation_id=reservation_id)
            need = len(details["passengers"])
            return (result + f" | This reservation has {need} passenger(s); pass exactly "
                    f"{need} passenger object(s) (you passed {len(passengers)}). Include every "
                    "existing passenger, changing only the fields that should change.")
        except Exception:
            return result
    return result
