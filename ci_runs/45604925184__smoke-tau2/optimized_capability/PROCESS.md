# PROCESS — cand_0003 (parent cand_0002, val 0.617)

Headline: convert the one clean, verified lever left on this plateau — COMMUNICATE
omission of the exact $ — into a deterministic, DB-safe tool-return enrichment, and
add tight decision rules for the behavioral errors the traces show (trust system
prices / don't undo a correct reservation; act in-policy instead of transferring; no
unsolicited compensation). STALL that is uncontrollable is left alone.

Subagents used: yes — two read-only Explore subagents diagnosed the COMMUNICATE
traces (11, 23) and the STALL/DB-error traces (19, 37, 40, 25) in parallel before any
edit. Every code lever was then replayed on the live airline DB (gold-exact + no-op
on passing tasks) before shipping.

## Ranked clusters (leverage = #tasks × trials × recoverable, biggest first)
1. **COMMUNICATE — exact $ never spoken** [KNOWLEDGE] — task 11 (2/3 trials =0).
   Verified live: the refund **5244** IS already in `update_reservation_flights`'s
   return (`payment_history … -5244`), but the weak model echoes its own
   pre-confirmation estimate ($1515 = wrong prices, $1748 = forgot ×3 passengers)
   instead of reading it. On this val split only tasks 11 & 23 have non-empty
   `communicate_info`; 23's numbers are aggregations across 3 bookings and its 0-trials
   fail on DB sequence, so only 11 is a pure-COMMUNICATE recoverable here — but the
   class (state the charged/refunded figure) is SYSTEMIC on held-out tasks.
2. **Destructive / over-cautious decisions on user pushback** [BEHAVIORAL] — 25 t2
   (caved to a FALSE price complaint, cancelled a correct booking), 37 t0 (transferred
   instead of doing the permitted M20IZO upgrade), 37 t1 (offered an unsolicited
   certificate + changed flights without `search_direct_flight`). Real, generalizing
   (false pushback / over-caution is pervasive in tau2 airline).
3. **Uncontrollable USER_STOP** — 19 t1, 40 t1: the simulator bundles the confirmation
   with `###STOP###` in one user message, ending the episode before the agent gets an
   action turn. NOT narrate-without-call. No agent-side lever (confirmed by trace).
   SKIPPED.
4. **Flight/passenger selection (8) & multi-reservation split (23)** — model
   reasoning/selection; no general code or prose guard that would not overfit. SKIPPED.

## Edits kept (each REAL + GENERAL + CHECKED)
- **E1 tools.py `_with_payment_summary` + enriched returns on `book_reservation`,
  `update_reservation_flights`, `update_reservation_baggages`, `cancel_reservation`**
  (lever 8, enriched return). Returns `{**reservation.model_dump(), "payment_summary":
  "<exact $ + copy-ready sentence + 'use THIS figure, not your estimate'>"}`.
  class: every task that must state a charged/refunded amount. touches failing task 11
  directly (+ the whole held-out amount-communication class).
  CHECK (live DB): task 11 → "Refunded $5244" (`'5244' in summary` True); task 25 book
  → "$375" (stored cc 247 = gold); task 12 within-allowance → "$0" (nonfree 0, no new
  charge = gold); task 19 cancel → "$169"; task 17/22 → "$209"/"$0" with final DB
  cabin=economy,1 pax,3 bags = gold; task 37 → "$1194", cabin=business = gold. DB
  state IDENTICAL to cand_0002 in every case (returns are not hashed → strictly safe
  for passing tasks 12/17/22). All 14 tools still register.
- **E2 policy §4 rewrite** (contract/KNOWLEDGE). "Read `payment_summary` and state that
  exact figure; do NOT use your pre-call estimate — the common error is quoting a
  per-passenger amount and forgetting ×N passengers," + worked example ($5244 not
  $1748). class: amount-communication. touches task 11.
- **E3 policy §7 + §8** (DECISION). §7: the tools' prices are authoritative — never
  cancel/rebook/re-price a reservation that is already correct just because the user
  disputes a number. §8: do the in-policy action instead of transferring; `search`
  before changing flights; never offer compensation/certificates unsolicited. class:
  false-pushback / over-caution. touches 25 t2, 37 t0, 37 t1. Inherits the Operating-
  notes softness clause (judgement overrides when a rule would block the correct
  outcome).

## Preserved (must not regress)
All cand_0002 code guards are intact and re-verified: payment auto-correct + dict
normalization + `payment_history` re-sync (book), baggage free-allowance recompute +
`total_price>0` payment skip (book/baggages), and the cancel-flown guard (NQNU5R still
refused). Passing tasks 12, 17, 22 reproduce gold DB under the edited tools.

## Deliberately skipped
- Uncontrollable USER_STOP (19 t1, 40 t1) — no agent-side lever; documented, not chased.
- A prose "execute-in-the-same-turn-after-yes" anti-STALL rule — REFUTED (cand_0001;
  tools SKILL marks it rejected for narrated_without_action) AND the traces show these
  are not narrate-without-call at all (user ends first). Not re-tried.
- A composite confirm+write tool with primitive removal — unsafe here: cancel/update
  must stay refusable (cancel-flown guard, basic-economy flight-change), and tau2's
  confirmation is conversational, so no code path to merge. Not applicable.
- Task 8 flight/passenger selection, task 23 multi-reservation split — model reasoning;
  any guard would overfit a single task.
