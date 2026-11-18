# PROCESS — what I did this iteration (explainability; REQUIRED)

## Ranked issue list (clusters by # failing tasks × trials, biggest first)
| rank | cluster | tasks | shared root cause | tag | planned change class |
| --- | --- | --- | --- | --- | --- |
| 1 | Wrong write args on book_reservation | 23, (8/25 if they reach book) | (a) payment dicts use profile keys `id`/`source`/`type` instead of `payment_id` → hard pydantic crash; (b) `amount` miscomputed → "Payment amount does not add up"; (c) flights carry extra keys | BEHAVIORAL/RULE | in-body normalization + auto-fill payment amount |
| 2 | Recoverable payment errors strand agent on updates | 17, 22 | agent pays an update with a certificate (forbidden) or an underfunded gift card; opaque error → thrash/give up | BEHAVIORAL | enriched actionable error return |
| 3 | update_reservation_passengers count/format | 17, 22 | passenger objects miss dob or wrong count; opaque "Number of passengers does not match" | KNOWLEDGE | normalize + enriched error stating exact required count |
| 4 | update_reservation_flights partial itinerary / wrong payment | 11, 17, 22, 37 | agent omits unchanged segments or uses wrong payment id | KNOWLEDGE/BEHAVIORAL | normalize flights + sharpened docstring (ENTIRE itinerary) + enriched errors |
| — | ACTION STALL / narrated-not-executed | 8, 11, 25 | agent gathers info, narrates, never calls the write (turn budget burned on redundant reads/over-confirmation) | BEHAVIORAL | NOT directly fixable from tool surface (cannot force a call); lowered the barrier to booking via payment auto-fill + clearer docstrings |
| — | premature transfer_to_human_agents | 12, 37 | agent gives up and escalates | DECISION | SKIPPED — blocking transfer is an unbounded permission change; too risky |

## Changes made this iteration (real CODE across 4 tools; passing task 19 uses only cancel → zero blast radius on all four)
| cluster | edit class | file / tool | what & why it generalizes | protects passing? |
| --- | --- | --- | --- | --- |
| 1 | in-body normalization + computation (levers 1,8) | book_reservation.py | strip flights to {flight_number,date}; map payment `id`→`payment_id` & drop extras; strip passengers to {first,last,dob}; on "total price is X" auto-fill amount (single method → total; multi with one credit_card → remainder). General: fires on the failure class, not a literal. | Yes — not called by task 19 |
| 2,4 | normalization + enriched error (levers 1,8) | update_reservation_flights.py | strip flights to {flight_number,date}; accept dict payment_id; append actionable next-step to certificate / gift-card-balance errors | Yes |
| 2 | enriched error + normalize pid (lever 8) | update_reservation_baggages.py | append actionable next-step to certificate / gift-card errors; accept dict payment_id | Yes |
| 3 | normalize + enriched error (levers 1,8) | update_reservation_passengers.py | strip passengers to {first,last,dob}; on count mismatch fetch reservation and state the EXACT required count | Yes |

All docstrings also hardened for the mid-tier reader (gpt-oss-120b): literal per-parameter formats + one worked example each (payment object shape, flight object shape, ENTIRE-itinerary rule).

## Verify-the-fix (ran the REAL bodies with mocked primitives on trace-style args)
- book_reservation, task-23 args `payment=[{"id":"certificate_3765853","source":"certificate","amount":500}]`, flights w/ extra keys, wrong amount → normalized to `[{"payment_id":"certificate_3765853","amount":871}]`, flights → `[{"flight_number":"HAT023","date":"2024-05-26"}]`, auto-filled, booking SUCCEEDS. Well-formed single-payment correct-amount call → unchanged, ONE backend call (no spurious retry). Split w/o credit card & wrong sum → not auto-filled, returns the original actionable error.
- update_reservation_flights, cert payment → error + "Retry with a credit_card_..."; gift-card-insufficient (task-17 QKRY03 args) → error + credit-card hint; flights normalized to {flight_number,date}.
- update_reservation_passengers, task-17/22 count-mismatch → error + "This reservation has 2 passenger(s); pass exactly 2 (you passed 1)".
- update_reservation_baggages, success path → passthrough unchanged.
- Blast radius: the ONLY passing task (19) calls get_user_details/get_reservation_details/cancel_reservation — none of which I touched. All four edited tools are absent from every passing trajectory ⇒ BOUNDED/zero-blast by construction.
- Syntax + one-top-level-def check passed for all 14 scripts.

## Process & features used
- Serial (single agent). Diagnosed all 10 trajectories directly (agent tool-calls vs gold action_checks) and read the real tau2 backend (`bench_repo`→ found at skillberry-benchmarks) to get exact write semantics (Payment requires `payment_id`; FlightInfo is {flight_number,date}; certificate forbidden on updates; exact payment-total rule).
- Prior iterations: none — this is iteration 1 (seed only; LEDGER/JOURNAL empty).

## Good things to PRESERVE
- Payment-key normalization (`id`→`payment_id`) and single-/credit-card payment auto-fill on book_reservation — removes the dominant hard-crash + arithmetic blocker.
- The zero-blast-radius fact: passing task 19 is cancel-only, so book/update tool edits cannot regress it.

## Deliberately skipped
- Blocking/altering transfer_to_human_agents (tasks 12, 37): would be an UNBOUNDED decision/permission change; cannot verify it won't flip a held-out task where escalation is the gold answer.
- Forcing a write on pure ACTION-STALL tasks (8, 11, 25): impossible from the tool surface — a tool can't call itself. Addressed indirectly by lowering the barrier to booking.
