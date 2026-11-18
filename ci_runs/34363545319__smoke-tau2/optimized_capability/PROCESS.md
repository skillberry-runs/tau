# PROCESS — what I did this iteration (explainability; REQUIRED)

Iteration cand_0003 (LAST of run; prior state: cand_0001 ACCEPTED val 0.483, cand_0002 REJECTED val 0.567 Δ+0.083 on the significance bar though it broke NOTHING). Framework verdict on cand_0002: keep those edits and make the effect BIGGER (POWER/SIZE, not redesign). This candidate = cand_0002's verified-safe edit set, kept and made structurally STRONGER on the two clusters that repeatedly cost tasks: (A) wrong-reservation selection, (B) cancel-eligibility decision — plus the passenger-dob and communicate-amount wins carried forward.

## Ranked issue list (clusters by # failing tasks × trials, biggest first)
| rank | cluster | tasks | shared root cause | tag | change class this iter |
| --- | --- | --- | --- | --- | --- |
| 1 | **Wrong reservation selected** — user names a route ("my New York→Chicago trip"), agent grabs the FIRST reservation from get_user_details (unordered) and modifies the wrong one | 17, 22 | no route→reservation resolver; weak reader can't map "New York"→EWR/JFK/LGA nor scan the list | KNOWLEDGE/CAPABILITY gap | **CODE**: new deterministic `find_reservation(user_id, origin, destination)` read tool w/ metro-area alias map + policy procedure "call this FIRST, never take the first reservation" |
| 2 | **Cancel eligibility not enforced** — agent cancels a reservation that fails all 4 cancel rules, or cancels one with a flown segment; or transfers before doing a permitted write | 37 + cancel tasks | API doesn't check rules; weak reader skips the eligibility check | RULE-VIOLATION (decision) | **CODE**: in-body eligibility gate in `cancel_reservation` (flown-segment guard + 4-condition guard, conservative fallback) + policy prose |
| 3 | **Change-passenger dob** — surname fix, agent asks user to re-state an unchanged dob or transfers | 17-style | reader thinks every passenger field is required | arg-fill | **CODE**: dob auto-fill from existing reservation (positional) + policy dob-reuse rule |
| 4 | **Wrong communicated amount / no write on yes** (cand_0001 wins) | 8,11,12,19,40 | per-passenger math; confirm/execute split | KNOWLEDGE/BEHAVIORAL | PRESERVED cand_0001 code (enriched returns, payment auto-fill) + prose (execute-on-yes, multi-write, present-summary-early) |
| — | book "same flight" from remembered time; "cheapest" enumeration; past-date search | book tasks | reader guesses flight from recalled time / picks first | KNOWLEDGE | CODE: `search_direct_flight` past-date guard + policy "read prior reservation / enumerate cheapest" |

## Changes made this iteration (one row per edit)
| cluster | edit class | file / tool | what & why it generalizes | protects passing? |
| --- | --- | --- | --- | --- |
| 1 | NEW read tool + resolver (lever: loop/discriminating-predicate) | tools.py `find_reservation` + `_location_to_iata` + `_AIRPORT_CITY`/`_METRO_GROUPS` + `_reservation_summary` | resolves plain city OR IATA to a metro-aware IATA set, returns only reservations whose route matches; no filter → all. Directive docstring "Call FIRST for unknown reservation id" | YES — pure READ, no DB write; unused by passing tasks |
| 2 | in-body eligibility gate (lever: discriminating-predicate guard) | tools.py `cancel_reservation` | (a) raise if any segment already flown (`date[:10] < current_date`); (b) raise if NOT (booked_within_24h OR business OR insurance OR airline_cancelled). datetime parsed via `fromisoformat(str(...))`; except→`booked_within_24h=True` (conservative, never over-refuse) | YES — fires ONLY on ineligible/flown cancels; gold cancels (insurance, within-24h) pass through |
| 3 | positional dob auto-fill (lever: arg-fill) | tools.py `update_reservation_passengers` | fetch reservation, actionable count-mismatch error, fill missing `dob` positionally from existing pax when a dict omits it | YES — fires only when a dict OMITS dob; Passenger objects / full dicts untouched |
| — | past-date guard (lever: in-body validation) | tools.py `search_direct_flight` | raise actionable ValueError when `date[:10] < current_date`, redirect to find_reservation/get_reservation_details | YES — no-op for present/future searches (all passing searches) |
| 1 | policy procedure + worked example | policy.md "Modify flight → Finding the right reservation" | 4-step find_reservation procedure; "NEVER take the first reservation"; sanity-check the picked route | YES — additive guidance |
| 2 | policy prose | policy.md "Cancel flight" | check eligibility before calling; never cancel flown; complete permitted writes BEFORE transferring on mixed requests | YES — additive |
| 3 | policy prose | policy.md "Change passengers" | omit unchanged dob; never ask/transfer for a fetchable dob | YES — additive |
| — | policy prose | policy.md "Book flight → Identifying the flight" | same-flight → read prior reservation not recalled time; past-date search errors; cheapest → enumerate all, min total | YES — additive |
| 4 | PRESERVED | policy.md "Executing a confirmed action" | conditional-go-ahead, present-summary-early, multi-write rules (cand_0002 verified) | YES — additive |

## Verify-the-fix (ran each tool body on exact failing-trace args; venv = tau2-bench/.venv, live airline db.json)
- `find_reservation("omar_rossi_1241","New York","Chicago")` → **['FQ8APE'] ONLY** (not the first/UM3OG5). Metro map: "New York"→{JFK,LGA,EWR} matches EWR origin. Fixes 17/22 wrong-reservation.
- `cancel_reservation` gate → **['IFOYYZ:REFUSED', 'NQNU5R:REFUSED', 'Z7GOZK:CANCELLED', 'K1NW8N:CANCELLED']**. Ineligible (basic-economy, >24h, no insurance) refused; gold cancels (Z7GOZK insurance=yes; K1NW8N booked 2024-05-14 within 24h) cancelled correctly — DB shows negative refund payment appended + status=cancelled. Confirms the gate does NOT regress gold cancels.
- `update_reservation_passengers("FQ8APE", [{first,last}])` (dob omitted) → reuses stored dob **'1960-12-01'**; no error, no transfer. Full-dict / Passenger inputs unaffected.
- `search_direct_flight(...,date="2024-05-01")` (past) → **REFUSED**; present/future dates unaffected.
- Registration: **15 tools** register via `get_tools()` (14 base + find_reservation); `ast.parse` OK; module imports clean.
- SAFE (passing tasks): write tools book_reservation / update_reservation_flights / update_reservation_baggages / calculate UNMODIFIED this iteration → T11 refund path and T25 charge path byte-for-byte unchanged.

## Process & features used
- Read LEDGER/JOURNAL/RUNMAP/prior_iterations, rejected.jsonl before proposing. Built ON cand_0002 (kept its edits) rather than redesigning, per its REJECT verdict.
- Fanned out 4 read-only diagnostic subagents (compact extractor `/tmp/extract.py` to avoid 182KB trajectory overflow) for argument-level root causes; verified every code edit by direct tool-body execution against the live DB, both fire-case and no-op case.

## Good things to PRESERVE (do not let a future iteration undo these)
- `find_reservation` metro-aware resolver — the only deterministic fix for the always-failing 17/22 route-selection cluster.
- `cancel_reservation` eligibility gate with conservative except-fallback (=True) — verified NOT to over-refuse gold cancels.
- Passenger dob positional auto-fill; enriched write-tool returns; single-payment amount auto-fill (cand_0001/0002 code).

## Deliberately skipped (cluster + why)
- Task 12 `calculate` requirement: verified it is NOT reward-relevant (diagnostic-only action trace) — adding a calculate rule would be prose bloat with no score effect.
- Re-adding execute-on-yes prose beyond what exists: meta-insight from cand_0001/0002 says the bare "Yes.###STOP###" no-write cases are a simulator artifact, not prose-fixable. Addressed only via the multi-write / present-summary-early rules already present.
- Task 37 max_steps/infra noise: not an editable capability.
