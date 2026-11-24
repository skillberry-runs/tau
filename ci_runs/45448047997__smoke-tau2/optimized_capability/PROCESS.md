# PROCESS — cand_0003 (parent cand_0002, val 0.567)

Reward model: **DB × COMMUNICATE** (product; either 0 ⇒ task 0). Tool RETURN values are
NOT hashed — only `self.db`. Diagnosed THIS iteration's `./trajectories/` (30 val trials
of cand_0002) by reading the actual traces, not the stale summary. The confirm-then-STOP
stall that dominated cand_0002's diagnosis is now largely gone (passing trials execute
the write directly). The residual loss is three DECISION/BEHAVIORAL patterns the mid
reader still gets wrong on some trials. I verified each code edit on the LIVE airline DB
with the edited `AirlineTools` (run venv).

## Ranked cluster list (leverage = # failing trials × score recoverable)

| rank | cluster | tasks (trials) | root cause | tag | lever |
|---|---|---|---|---|---|
| A | **Duplicated / compounding WRITE** | 23 t0/t1/t2 (ALWAYS-fail), 12 t0/t2, 8 t0/t1 | Agent writes, then re-writes to "correct" it. The first write is not undone: `book_reservation` makes a NEW reservation and each write appends a charge, so a corrective repeat STACKS → doubled DB → 0. 23 cancels then books 3×; 12 modifies business then economy; 8 books twice (different flight). | BEHAVIORAL | code: duplicate-booking guard in `book_reservation`; prose RULE 6 "one decision, one write" |
| B | **Cancel/split vs modify; over-transfer** | 23 t0/t1/t2, 11 t1, 19 t0/t1 | Wrong write-action choice. 23: user pressures agent to cancel + split one party into 3 reservations to use 3 certificates (policy forbids >1 cert/reservation). 11: "downgrade + refund difference" done as a full CANCEL instead of a cabin modification. 19: agent TRANSFERS instead of cancelling, having checked only the insurance condition and not the other three cancel-eligibility conditions. | DECISION | prose RULE 7 (cabin change = modify, never cancel-and-rebook / split to game payments) + RULE 5 cancel-eligibility check |
| C | **Wrong reservation targeted (grab-first-id)** | 17 t1, 22 t0/t1 | User names the trip by route ("New York to Chicago"), gives no id. Agent fetches the FIRST reservation id and acts on it (SEA→DFW `UM3OG5`) without confirming the route, instead of the matching `FQ8APE` (EWR→ORD, basic economy). Passing trials fetch several candidates and match. | CAPABILITY-GAP | code: new `find_reservation(user_id)` resolver returning a compact summary of ALL reservations in one call; RULE 5 points at it |

A+B overlap on the always-failing task 23 (3 trials, full recoverable) — the biggest
single leverage — and together cover every failing trial except the flight-selection
noise in 8 (wrong cheapest flight, a reasoning error no capability edit fixes cleanly).

## Edits made this iteration

| id | edit | file / surface | class (SKILL lever) | targets | protects passing? |
|---|---|---|---|---|---|
| E1 | New READ tool `find_reservation(user_id, origin?, destination?)` — loops the user's reservations, returns compact {id, origin, destination, flight_type, cabin, dates, num_passengers, status, matches_filter} so all candidates are visible in ONE call | tools.py | code: loop/resolver tool (lever 5) + literal per-param docs for the mid reader | C (17, 22) | yes — additive READ; passing tasks already resolve correctly |
| E2 | Duplicate-booking guard in `book_reservation`: before creating, scan the user's ACTIVE reservations; if one matches same origin/destination/flight_type/passenger-set/travel-dates, raise an actionable error naming the existing id and telling the agent to MODIFY it | tools.py | code: in-body guard (lever 1) | A (8; defends 23-style re-book) | yes — verified task 25 (same route/dates, DIFFERENT passenger count) does NOT fire |
| E3 | RULE 6 (new): "one decision, ONE write per reservation; never issue a corrected second write" with WRONG/CORRECT worked examples | policy.md | prose (add rule + reason + example) | A (12, 8, 23) | yes — passing trials already write once |
| E4 | RULE 7 (new): a cabin/flight/baggage change is a MODIFICATION — never cancel-and-rebook; never split one trip into several reservations to apply more certificates / lower a card charge; downgrade+refund = cabin modification, not cancel | policy.md | prose (add sourced decision rule + example) | B (23, 11) | yes — tightens, never loosens a passing decision |
| E5 | RULE 5: cancel-eligibility check — verify ALL four conditions (24h / airline-cancelled / business / insurance+covered) before transferring or refusing a cancellation; transfer only when no write tool can satisfy the request | policy.md | prose (tighten decision rule, traced to Cancel-flight policy) | B (19) | yes — states policy exactly, adds no new permission |
| E6 | RULE 5 disambiguation bullet rewritten to call `find_reservation` first and match by route/dates; "do not act on the first id you see" | policy.md | prose (rewrite + point at new tool) | C (17, 22) | yes |

## Verify-the-fix (ran against the LIVE airline DB with the edited AirlineTools, run venv)

- **Registration**: edited toolset imports and tau2 `get_tools()` returns **16** tools
  incl. `find_reservation` (< ~20 limit). No registration break.
- **E1 fires on C**: `find_reservation('omar_rossi_1241', origin='EWR', destination='ORD')`
  returns all 4 reservations and flags **FQ8APE** (EWR→ORD, basic_economy, 1 pax)
  `matches_filter=True`, the exact reservation the failing trials missed; `UM3OG5`
  (SEA→DFW, the one they wrongly grabbed) is `False`.
- **E2 fires on A, not on passing**: 1st book of a trip succeeds; an identical-trip 2nd
  book (same pax/route/dates, even a different flight number — the task-8 pattern) is
  BLOCKED with the actionable error. Task 25 (ivan_muller_7015 books DTW→SEA 1 pax while
  existing G72NSF is DTW→SEA **2 pax**) passes the guard — the passenger-set differs, so
  no false positive. A fresh unrelated booking succeeds.
- **E3–E6 (prose)**: each is general (no task id/answer), traces to the policy, and
  tightens (never loosens) a decision; renumbering RULE 6→RULE 8 kept every constraint.

## What I deliberately SKIPPED and why
- **Making `modify_reservation` idempotent (snapshot-restore) for task 12**: the only
  clean code fix would restore the pre-session reservation + user balances + seat
  availability before re-applying — too much state to restore correctly, high corruption
  risk. Handled task 12 with RULE 6 prose instead (no passing trial calls modify twice,
  so prose + the atomic tool suffice).
- **Removing the `update_*` primitives so `modify_reservation` is the only path** (the
  structural lever flagged in JOURNAL): passing 40 t2 and 12 t1 call `update_*` directly,
  and `modify_reservation` requires a `payment_id` even for free passenger-only changes —
  removal would strand those. Regression risk > upside; left additive.
- **Task 8 flight selection** (agent picks a non-cheapest flight): a reasoning error, not
  a capability gap; no general code/prose edit fixes it without hardcoding.

## Subagents / parallelism
Diagnosed directly (traces are compact JSON; a single pass over all 30 trials + targeted
live-DB checks was faster and more reliable than fan-out round-trips). No subagents used.
