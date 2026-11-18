# PROCESS — what I did this iteration (explainability; REQUIRED)

Capability type: **system-prompt** (`policy/policy.md`) + **tools** (`tools/tools.py`). Reader: `aws/gpt-oss-120b`, mid tier → explicit imperative rules, a worked example per behavior, deterministic enforcement in tool code.

## Ranked issue list (clusters by # failing tasks × trials × score recoverable, biggest first)
| rank | cluster | tasks | shared root cause | tag | planned change class |
| --- | --- | --- | --- | --- | --- |
| 1 | A: Action stall — write never executed | 8 (1/1 trials) | Agent summarized the booking, got user "yes", then the episode ended (USER_STOP) with `book_reservation` **never called**. DB stayed empty → DB reward 0. Generalizes to every book/modify/cancel task. | BEHAVIORAL / CAPABILITY-GAP | prompt execution contract + worked example |
| 2 | B: Incomplete reservation enumeration | 8 | User has 5 reservations `[NM1VX1,KC18K6,S61CZX,H8Q05L,WUNA5K]`; agent read only the first 4 and stopped, missing `WUNA5K` (the referenced May-10 ORD→PHL flight = gold action `8_1`). So it never found the flight number and booked the wrong/no flight. | CAPABILITY-GAP | new loop tool returning ALL reservations at once |
| 3 | C: Over-asking + stalling on an unverifiable premise | 8 | Agent asked for Sophia's DOB though it is in her profile; then looped on "which flight matches May 10" and nearly refused instead of presenting options and proceeding. | KNOWLEDGE / BEHAVIORAL | prompt rules (use on-file data; present options & proceed) |
| 4 | D: Wrong write arguments (esp. payment ≠ exact total) | 8 (class-wide) | `book_reservation` rejects a call whose payment amount ≠ exact total; complex 11-arg signature is hard for a mid model to slot-fill. Not reached in this trace (no booking happened) but a dominant DB-mismatch class across the airline distribution. | KNOWLEDGE | enriched tool docstring: price formula + full worked example + per-param slot docs |

## Changes made this iteration
| cluster | edit class | file / tool | what & why it generalizes | protects passing? |
| --- | --- | --- | --- | --- |
| A | add rule + worked example (output contract) | policy.md "How to complete a task" | A task is done only after the write tool RETURNS; the moment the user confirms, the very next turn MUST be the write call — no re-summary, no second confirmation. General to all book/modify/cancel. | Keeps existing "confirm before write" rule; only sharpens the step after "yes". |
| B | add loop tool (code body) | tools.py `get_all_reservation_details(user_id)` | Loops over `user.reservations`, returns every full Reservation in one call → agent cannot miss a reservation by stopping early. Deterministic. | Additive READ tool; `get_reservation_details` kept for known ids. |
| C | add rules | policy.md (steps 1 + "Finding a flight…") | Look up on-file data before asking; when a referenced record can't be found after checking ALL reservations + flight DB, present options and proceed. | No permission broadened; cuts over-asking only. |
| D | enrich docstring (per-param + example) | tools.py `book_reservation` | States the exact price formula, that payment must equal the total, certificate consumed in full, and a complete worked argument example. Helps mid model slot-fill correctly. | Behavior unchanged; only docs. Error bodies untouched. |

## Verify-the-fix (trace → what changes)
- trace 8 (cluster A): after user "yes", policy now forces the next turn to be the `book_reservation` call itself → the DB write actually happens instead of USER_STOP with an empty DB. class: action-stall (all write tasks); touches 1/1 failing traces, broad class.
- trace 8 (cluster B): `get_all_reservation_details("sophia_silva_7557")` returns all 5 reservations incl. `WUNA5K` (the gold-read record) in one call → agent finds the May-10 flight number and books the matching May-26 flight. Verified by reading the loop against `user.reservations` from the trace. class: history lookup / reservation-by-criteria.
- trace 8 (cluster C): profile already contains Sophia's dob → step 1 tells agent not to re-ask; "present options & proceed" removes the refusal loop. class: over-ask + unverifiable premise.
- trace 8 (cluster D): docstring now gives the price formula + full example → mid model builds a payment amount equal to the exact total, avoiding the "payment does not add up" rejection. class: all booking/modify writes. Not firing in this trace (no booking occurred) but general.

## Process & features used
- Serial (single-session) — one failing task, tightly coupled root causes; fan-out not warranted. Read the full trace via a JSON extraction script.
- Prior iterations read: none exist (seed baseline only; LEDGER/RUNMAP empty). This is iteration 1.

## Good things to PRESERVE
- The execution contract (act on confirmation; a write isn't done until the tool returns) — it is the dominant DB-reward lever.
- `get_all_reservation_details` loop tool — keep; do not collapse history searches back to per-id lookups.
- Enriched `book_reservation` price formula + worked example.

## Deliberately skipped
- A composite "book-and-confirm" atomic write tool: the primitive is fine; the failure was not calling it, which the prompt contract fixes. Adding a wrapper + removing the primitive risked breaking many passing call-sites without evidence.
- Seat-preference handling (aisle/middle): tau2 airline has no seat-assignment field in the data model, so it is unscoreable — not a DB lever.

---

# DIAGNOSIS.json — see sibling file DIAGNOSIS.json
