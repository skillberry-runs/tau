# Optimize the capability — ship the edit with the largest expected objective score gain

## THE READER (who consumes what you edit)
At runtime these capabilities are read by `aws/gpt-oss-120b` — capability tier: **mid**. The reader is a mid-capability model (e.g. ~100B open weights). Be EXPLICIT: imperative step-by-step rules, at least one worked few-shot example per non-trivial behavior, short decision chains, and literal argument/slot-filling docs on every tool parameter. Lean HARD on deterministic tool-code enforcement — a behavioral rule it 'knows' but skips must be enforced in code, not restated in prose.
Optimize your edits for THIS reader's capability level, not for your own. When the reader is weaker than you, prefer explicit rules, worked examples, and code enforcement over terse prose you would personally infer.


Focus: every failing task on the val split. Current val reward 0.533: 3 solid / 4 flaky / 3 failing of 10 tasks.



GOAL: raise the objective score as much as you can THIS iteration, then STOP (the harness
re-scores your work; don't run the evaluation yourself). Every capability you were given is fair game. Take your time, study these instructions in detail and be meticulous. Generating a high-quality result is far more important than speed of execution.

## PREPARATION: 
Complete these steps before beginning to work on the edits. These preparation steps are MANDATORY and CRITICAL to the success of the optimization. Make sure you complete them properly before doing anything else.
### 1. Understand the objective score
The intake for this optimization defines an *objective score* function that should guide you in selecting edits to ship. It should be available either as a default score when nothing is defined in the intake, or as a specific score that is explicitly defined in the intake. Locate this objective score, study it very carefully, and understand its composition. In particular, identify each of the score's components, study them, and learn how to maximize the overall objective score as it is evaluated on each trace. 
### 2. Editing how-to. Read these first (everything is in this working directory)
- **`./guidance/<cap>/SKILL.md` for EACH selected capability — READ IT IN FULL before you
  edit; it is the MENU of improvement TYPES available to you.** Each capability skill lists
  the concrete kinds of change you can make (for a tools capability: in-body validation
  guards, normalization, computation, composite/atomic-write tools, loop/workflow tools,
  enriched return values + actionable errors, add/remove tools, sharpened descriptions;
  for a prompt capability: role/contract, decision-rule narrowing, missing-rule, worked
  example, consolidation). Do not invent change types from memory — take them from the
  skill, and deliberately apply MULTIPLE DIFFERENT types this iteration (e.g. several
  in-body guards + a compute tool + enriched errors + a couple of prompt rules), matching
  each cluster to the strongest type the skill describes for it. (Tool code? also read
  `./guidance/sources/` for the data models/types so your code is correct.)
- `./guidance/diagnose/SKILL.md` — the failure-clustering method. Use it.
- `./trajectories/` — the FULL traces of the current best candidate (the step you build
  on). The failure index ("ALWAYS-failing" / "FLAKY" sections) below summarizes them with argument-level feedback — read
  the actual traces for the clusters you'll fix, don't rely on the summary alone.
- `./LEDGER.md` — FACTS (read-only): every prior iteration's outcome + the exact tasks it
  broke/fixed. Start here: don't re-introduce a change that broke a task.
- `./JOURNAL.md` — the accumulating handover. Each entry is the optimizer's INTENT, and
  directly below it the framework stamps a **RESULT** line (objective: ACCEPTED/REJECTED ·
  Δ · the exact tasks fixed/broke). The RESULT lines — not the intent — are the truth of
  what worked: read them all before proposing. If the most recent RESULT is **REJECTED**,
  its batch was reverted; read that entry's `./prior_iterations/<id>/diff.patch`, keep the
  edits that did NOT appear in its `broke={...}`, and DROP or REDESIGN the ones that did —
  do NOT resubmit the whole rejected batch, and do NOT abandon the cluster. APPEND your new
  entry (intent only) below the marker; never edit earlier entries or re-try a refuted idea.
- `./RUNMAP.md` + `./prior_iterations/<id>/` — EVERY prior iteration's (accepted AND
  rejected) PROCESS.md + diff.patch. Read the one(s) that touched a cluster you're about to
  work on, so you build on what worked and avoid repeating what regressed.
- `./PROCESS.md` — your REQUIRED explainability file for THIS iteration (template inside).
- `./guidance/optimizer/<name>.md` — your agent's subagent/parallelism features (optional).


#### Process (do this, then STOP)
**Parallelism:** Your agent supports parallel subagents/worktrees (see ./guidance/optimizer/claude-code.md). FAN OUT to cover MANY clusters at once: one read-only subagent per trajectory-group to diagnose, then one edit-subagent per issue (each in its own worktree), then MERGE every edit into this ONE candidate with no conflicts. This is how a single iteration fixes many issues across many trajectories, not just the biggest one.
1. Read your capability SKILL(s) + the diagnose method + the cross-iteration files
   (LEDGER facts, JOURNAL handover, RUNMAP for clusters you'll touch).
2. Diagnose THIS iteration's `./trajectories/` (not stale signatures). Cluster ALL failures by
   shared root cause: total, partial-credit, AND communication/omission. Rank clusters by
   LEVERAGE = (# failing tasks x trials x score recoverable), biggest first.
3. For each cluster pick the strongest improvement TYPE from the capability SKILL(s) and draft the
   edit; use several different types across the iteration.
4. Ship every edit that is REAL and GENERAL together in this ONE candidate.
5. Fill `PROCESS.md` and APPEND your entry to `JOURNAL.md`. STOP.

#### Choose the lever by FAILURE TYPE
- **RULE VIOLATION** (the agent breaks a rule it could follow): on a code surface, move the rule
  into the body of the tool that governs it (a guard that raises an actionable error, or returns the
  corrected value). On a prompt surface, make the rule unmissable: a checklisted step, a worked
  counterexample, the reason behind it.
- **CAPABILITY GAP / ACTION STALL** (no reliable way to do the thing, or the agent narrates an
  action and never executes it): prose alone leaves a hard zero at zero. Add a tool, helper script
  or ordered procedure that makes the action happen and changes the graded outcome.
- **KNOWLEDGE GAP** (a format, criterion or fact the agent cannot derive): state it precisely, once,
  in the prompt or a docstring. Don't restate a rule the agent already has.
- **DECISION / PERMISSION** (it acted where it should have refused, or the reverse): encode the exact
  discriminating condition rather than flipping a global default. A rule that says when to act and
  when not to, with the reason, usually beats a blanket loosening or tightening.

Also improve tool RETURN values and error messages (what is wrong, the valid options, the next
step) when a recoverable error stranded the agent. Never delete a needed rule; change or
consolidate it instead.

#### CHECK each edit before you keep it
- State the failing trace(s) it targets and the turn where behavior changes.
- Code edit: if you can run the function on the trace's arguments, do; otherwise read it through
  against the trace. A guard that cannot fire on the failing input is dead code.
- Prompt edit: confirm the missing fact or procedure is now stated, general and unambiguous.
- Record one line per edit in PROCESS.md: `trace <task> -> <what changes>; class: <...>; touches N failing tasks`.


#### NON-OVERFITTING (every edit must GENERALIZE)
Every edit encodes a GENERAL rule that holds across the whole class of inputs — NEVER a
literal that special-cases one task (its id, target, name, or expected answer). A guard
fires on the general condition ("the id is not in the user's records", "the record is in
a state that forbids this action"), NOT `if record_id == "<TASK_SPECIFIC_ID>"`. ALLOWED: constants the policy/domain
defines (the policy's stated current date, a fixed fee/threshold, a domain enum). Use
per-task specifics and any ground-truth in the traces ONLY to understand the failure
CLASS, then write the general fix.

#### Handover (REQUIRED before you STOP)
- **PROCESS.md** (this iteration): the ranked cluster list (with leverage + RULE/GAP/
  KNOWLEDGE tag), every kept edit + its lever, the CHECK line, the class of tasks it covers and how many
  failing traces it touches per edit, what you deliberately skipped and why, and (if you used subagents) that you did.
- **DIAGNOSIS.json** (OPTIONAL but recommended): a machine-readable diagnosis file that makes
  your diagnosis available to the dashboard. If absent, the dashboard will parse PROCESS.md
  tables when present, or show only outcome data. The schema:
  ```json
  {
    "candidate": "cand_NNNN",
    "headline": "Brief summary of this iteration's strategy",
    "clusters": [
      {"id": "A", "name": "Short cluster name",
       "detail": "Root cause explanation", "tasks": ["task-id", ...],
       "scope": "BOUNDED|WIDESPREAD|SYSTEMIC", "latent": false,
       "tag": "KNOWLEDGE|BEHAVIORAL|CAPABILITY-GAP"}
    ],
    "edits": [
      {"id": "E1", "title": "What this edit does",
       "files": ["policy.md", "tools.py"], "lever": "CONTRACT|KNOWLEDGE|BEHAVIORAL|...",
       "clusters": ["A"], "blast_radius": "BOUNDED|MODERATE|WIDE",
       "verified": "How you tested it"}
    ],
    "skipped": [{"title": "What was skipped", "reason": "Why"}],
    "techniques": ["technique 1", "technique 2"]
  }
  ```
  Validation is advisory only and never blocks an iteration. Warnings are recorded when a
  task ID is not in the val split, an edit references a missing cluster, or an edit
  references a file that does not exist in the candidate.
- **JOURNAL.md** (append ONE entry below the marker; never edit earlier entries). Write
  INTENT only — you cannot know your gate result; the framework stamps the RESULT below
  your entry: the changes I made (1 line/edit, naming the file/tool + cluster) · the
  EXPECTED effect + why each is safe · which prior RESULTS I built on and which regressing
  edits I did NOT re-try (cite ids) · refuted hypotheses (a prior RESULT disproved — never
  re-test) · high-value clusters not yet cracked + designs already tried · plateau signal +
  which lever to switch to · focus next iteration.

## (a) 3 ALWAYS-failing task(s) — fix the shared root cause (full traces in ./trajectories/):
- 12 (reward 0.00): [trial 0 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): get_reservation_details: was never called (or not called correctly); search_direct_flight: gold performs this 2x, you called it 0x - you stopped before making all the required calls; calculate: was never called (or not called correctly); update_reservation_baggages: was never called (or not called correctly).
  
  [trial 1 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): search_direct_flight: gold performs this 2x, you called it 0x - you stopped before making all the required calls; calculate: was never called (or not called correctly); update_reservation_baggages: was never called (or not called correctly).
  
  [trial 2 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): calculate: was never called (or not called correctly); update_reservation_baggages: was never called (or not called correctly).
- 23 (reward 0.00): [trial 0 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): cancel_reservation: was never called (or not called correctly); book_reservation: gold performs this 3x, you called it 3x. 1 required piece(s) of information were not clearly communicated to the user. State the confirmations/details (e.g. the computed total, the new flight times) the policy requires you to convey.
  
  [trial 1 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): cancel_reservation: was never called (or not called correctly); book_reservation: gold performs this 3x, you called it 0x - you stopped before making all the required calls. 1 required piece(s) of information were not clearly communicated to the user. State the confirmations/details (e.g. the computed total, the new flight times) the policy requires you to convey.
  
  [trial 2 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): book_reservation: gold performs this 3x, you called it 3x.
- 40 (reward 0.00): Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): update_reservation_passengers: was never called (or not called correctly).

## (b) 4 FLAKY task(s) — pass sometimes; make the good behavior consistent (full traces in ./trajectories/):
(reward is the mean over trials — the honest signal; listed lowest reward first.)
- 17 (reward 0.33): [trial 0 reward 0.000, trial 1 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): update_reservation_flights: agent used cabin='economy', flights=[{'flight_number': 'HAT056', 'origin': 'EWR', 'destination': 'IAH', 'date': '2024-05-25', 'price': 71}, {'flight_number': 'HAT138', 'origin': 'IAH', 'destination': 'ORD', 'date': '2024-05-25', 'price': 60}], payment_id='gift_card_8190333', reservation_id='FQ8APE'; update_reservation_passengers: agent used passengers=[{'first_name': 'Omar', 'last_name': 'Rossi', 'dob': '1960-12-01'}], reservation_id='FQ8APE'.
  
  [trial 2 reward 1.000]
  Task reward: 1.000. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): update_reservation_flights: agent used cabin='economy', flights=[{'flight_number': 'HAT056', 'origin': 'EWR', 'destination': 'IAH', 'date': '2024-05-25', 'price': 71}, {'flight_number': 'HAT138', 'origin': 'IAH', 'destination': 'ORD', 'date': '2024-05-25', 'price': 60}], payment_id='gift_card_8190333', reservation_id='FQ8APE'.
- 8 (reward 0.67): [trial 0 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): get_reservation_details: was never called (or not called correctly); book_reservation: agent used cabin='economy', destination='PHL', flight_type='one_way', flights=[{'destination': 'PHL', 'date': '2024-05-26', 'flight_number': 'HAT139', 'origin': 'ORD'}], insurance='no', nonfree_baggages=0, origin='ORD', passengers=[{'first_name': 'Sophia', 'last_name': 'Silva', 'dob': '1957-10-05'}], payment_methods=[{'type': 'certificate', 'id': 'certificate_8045380'}] (not on the user's profile; available=['certificate_8045380', 'certificate_3887113', 'credit_card_4196779', 'gift_card_5094406']), total_baggages=0, user_id='sophia_silva_7557'.
  
  [trial 1 reward 1.000]
  Task reward: 1.000. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): get_reservation_details: agent used reservation_id='S61CZX'; book_reservation: agent used cabin='economy', destination='PHL', flight_type='one_way', flights=[{'flight_number': 'HAT271', 'origin': 'ORD', 'destination': 'PHL', 'date': '2024-05-26'}], insurance='no', nonfree_baggages=0, origin='ORD', passengers=[{'first_name': 'Sophia', 'last_name': 'Silva', 'dob': '1957-10-05'}, {'first_name': 'Kevin', 'last_name': 'Smith', 'dob': '2001-04-12'}], payment_methods=[{'source': 'certificate', 'id': 'certificate_8045380', 'amount': 500.0}] (not on the user's profile; available=['certificate_8045380', 'certificate_3887113', 'credit_card_4196779', 'gift_card_5094406']), total_baggages=0, user_id='sophia_silva_7557'.
  
  [trial 2 reward 1.000]
  Task reward: 1.000. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): book_reservation: agent used cabin='economy', destination='PHL', flight_type='one_way', flights=[{'flight_number': 'HAT271', 'origin': 'ORD', 'destination': 'PHL', 'date': '2024-05-26'}], insurance='no', nonfree_baggages=0, origin='ORD', passengers=[{'first_name': 'Sophia', 'last_name': 'Silva', 'dob': '1957-10-05'}, {'first_name': 'Kevin', 'last_name': 'Smith', 'dob': '2001-04-12'}], payment_methods=[{'payment_id': 'certificate_8045380'}] (not on the user's profile; available=['certificate_8045380', 'certificate_3887113', 'credit_card_4196779', 'gift_card_5094406']), total_baggages=0, user_id='sophia_silva_7557'.
- 11 (reward 0.67): [trial 0 reward 1.000]
  Task reward: 1.000. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): update_reservation_flights: agent used cabin='basic_economy', flights=[{'flight_number': 'HAT003', 'origin': 'LAS', 'destination': 'DEN', 'date': '2024-05-19', 'price': 561}, {'flight_number': 'HAT290', 'origin': 'DEN', 'destination': 'LAS', 'date': '2024-05-20', 'price': 1339}], payment_id='gift_card_1642017', reservation_id='GV1N64'.
  
  [trial 1 reward 1.000]
  Task reward: 1.000. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): update_reservation_flights: agent used cabin='basic_economy', flights=[{'flight_number': 'HAT003', 'origin': 'LAS', 'destination': 'DEN', 'date': '2024-05-19'}, {'flight_number': 'HAT290', 'origin': 'DEN', 'destination': 'LAS', 'date': '2024-05-20'}], payment_id='gift_card_1642017', reservation_id='GV1N64'.
  
  [trial 2 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): update_reservation_flights: agent used cabin='basic_economy', flights=[{'flight_number': 'HAT003', 'origin': 'LAS', 'destination': 'DEN', 'date': '2024-05-19'}, {'flight_number': 'HAT290', 'origin': 'DEN', 'destination': 'LAS', 'date': '2024-05-20'}], payment_id='gift_card_1642017', reservation_id='GV1N64'.
- 37 (reward 0.67): [trial 0 reward 0.000]
  Task reward: 0.000. Database state does NOT match the expected final state — a required write (book/update/cancel) was missing, wrong, or extra. See the per-action detail below for the specific wrong argument. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): search_direct_flight: gold performs this 2x, you called it 0x - you stopped before making all the required calls; update_reservation_flights: was never called (or not called correctly).
  
  [trial 1 reward 1.000]
  Task reward: 1.000. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): search_direct_flight: gold performs this 2x, you called it 0x - you stopped before making all the required calls; update_reservation_flights: agent used cabin='business', flights=[{'flight_number': 'HAT268', 'origin': 'JFK', 'destination': 'ATL', 'date': '2024-05-22', 'price': 136}, {'flight_number': 'HAT010', 'origin': 'ATL', 'destination': 'MCO', 'date': '2024-05-22', 'price': 109}], payment_id='credit_card_9074831', reservation_id='M20IZO'.
  
  [trial 2 reward 1.000]
  Task reward: 1.000. Action-trace detail (DIAGNOSTIC ONLY - this task is scored on DB/COMMUNICATE, so action checks do NOT affect your reward; use these only as a clue to the wrong write): search_direct_flight: gold performs this 2x, you called it 0x - you stopped before making all the required calls; update_reservation_flights: agent used cabin='business', flights=[{'flight_number': 'HAT268', 'origin': 'JFK', 'destination': 'ATL', 'date': '2024-05-22'}, {'flight_number': 'HAT010', 'origin': 'ATL', 'destination': 'MCO', 'date': '2024-05-22'}], payment_id='credit_card_9074831', reservation_id='M20IZO'.

## Currently PASSING (3 task(s)) — your edit MUST NOT regress these
These tasks already score ~1.0. Preserve their behavior: any edit that changes their trajectory is a regression and will be rejected. Protect: 19, 22, 25

## What you are editing (the allowed edit space)
The capability under optimization is composed of these editable artifact(s). Use the FULL edit space below — do not limit yourself to trivial wording tweaks.
- **system-prompt** — Optimize an agent's system prompt / policy text (instructions, output contract, decision policy).
  - Allowed edits: Edit the prompt/policy text: instructions, decision policy, and the output contract. Prefer sharpening rules the traces show the agent breaking; do not just append more preamble.
  - Full guidance (read it): ./guidance/system-prompt/SKILL.md
- **tools** — Optimize an agent's own tool surface — docs, parameter schema/API, tool code, composing tools that call existing tools, adding/removing tools.
  - Allowed edits: Edit tool names/descriptions, per-parameter docs, in-description examples, the JSON schema, and the handler code. HIGHEST-LEVERAGE EDIT: WRITE A NEW CODE-BEARING TOOL (a real body — loops, validation, calls to existing tools), because a deterministic tool can't be 'forgotten' the way a prompt rule can. Two patterns to prefer: (1) a VALIDATION/RULE-ENFORCEMENT tool that wraps a primitive — validate/normalize inputs, enforce a GENERAL rule, then delegate to the primitive (e.g. cancel_record_safely(id) checks cancellable then calls cancel_record), and REMOVE the raw primitive so the only path is the safe one; (2) a WORKFLOW/LOOP tool that collapses a recurring multi-step sequence or N repeated calls into ONE call with real loops (e.g. loop get_record over a list of ids). Keep the toolset LEAN — REPLACE/consolidate, don't accumulate. The body must be real code, never '...' or docstring-only. Selection is driven by the name+description; argument-filling by the parameter schema/enums.
  - Full guidance (read it): ./guidance/tools/SKILL.md
## How your edit is judged
Algorithm: hill-climb:all. Your edited candidate is re-scored on the SAME held-out val tasks and compared to the current best (val reward 0.533). It is ACCEPTED only if the per-task improvement clears a significance bar (a noise margin), so a tiny or lucky change is rejected. Aim for a real, generalizing gain across a CLASS of failures — not a one-off patch to a single task (that overfits and gets rejected or hurts the held-out test).

#### Self-check before STOP
- Every kept edit is REAL (a failing trace shows it) and GENERAL (a class-level rule, no task id or answer),
  with its check line, class and coverage in PROCESS.md.
- You aimed at the largest expected objective score gain over the whole distribution: you covered the root
  causes that cost the most objective score degradation across failure types, not only the first cluster or the task you
  read last.
- You read each selected capability's `./guidance/<cap>/SKILL.md` and used the improvement types it
  offers, not one lever repeated.
- On a code surface, behavioral misses are enforced in code and any new tool closes a real gap
  the agent will call; on a prompt-only surface you used the structural-prose levers.
- You did not re-add anything LEDGER/JOURNAL show was rejected, and did not pad with cosmetic edits.
- PROCESS.md + JOURNAL.md are filled. Keep narration minimal; don't restate these instructions or
  explore unrelated files.


## Strategies for constructing edits:
In the list below you will find several highly-valuable strategies for selecting and constructing edits. Each edit you make should comply with all of them if possible, or at least with the vast majority of them, and be justified by the traces you analyze. 
### 1. Aim for the edit with the largest expected objective score gain on the WHOLE task distribution
Never rely only on a single task trace or just the tasks in front of you for when constructing an edit. The traces are a small sample of the failures the agent will meet.
Find the root causes that according to your estimate, should cause the most objective score decline in total across failure types. Based on those root causes, a good edit is a general
rule, check, procedure or tool that mitigates all or most of them. A timid one- or two-edit iteration is an under-used iteration; so is a patch that only fixes the task you read. Prefer one change that increases the objective score for many tasks over three changes that increase score for only one task. Fix as many distinct root causes as the traces support in this ONE candidate. Whole-file rewrites and restructurings are fine when the file's structure is the root cause.

Regressions are measured by the harness, not by you. Do not drop an edit that is well-supported by many traces, only because it might conceivably affect one passing task. Drop it when many traces show it would cause extensive damage measured by the objective score, or when it
is a guess no trace supports.

### 2. Keep an edit only if it is REAL and GENERAL
1. **REAL** — a failing trace in `./trajectories/` shows the problem (reward 0, partial credit, or a
   missing/incorrect report of what was done). Never edit for a hypothetical problem.
2. **GENERAL** — it states a rule, check or procedure for the whole CLASS of situations, never a
   literal that special-cases one task (its id, target, name or expected answer). In PROCESS.md
   write, per edit, the class it covers and how many of the failing traces it touches. Prefer edits
   that touch several tasks; keep a one-task edit only when its payoff is large and the class is
   clearly broader than that task. Constants the domain defines (a stated date, a fixed fee, an
   enum) are fine.
3. **CHECKED** — replay the failing trace against your edit by reading (where does the agent's
   behavior change?), and glance at one or two passing traces that use the same rule. If the
   benchmark runtime happens to be importable in this working directory you may run a small check;
   if it is not, do not spend turns trying to install it.

### 3. Make it work well for the tasks you're not seeing
Be aware that the eventual evaluation of the benchmark is using tasks and traces you may have not seen and may never see during this optimization. Therefore, changes you make should be generic and based on your broad and deep understanding of the entire domain of these tasks, as oppposed to being tied to specific tasks or even to just tasks you may have seen

### 4. Make capabilities that are SOFT and allow JUDGEMENT CALLS
The agent executing the benchmark with these capbilities is maximizing the benchmark's reward. Getting the highest reward is that agent's utmost goal, and that trumps complying and using any of the capabilities you ship. Therefore, each capability you add or edit must have a "softness" clause that does two things. First, it reminds the agent executing the benchmark of its ulimate goal of executing each task successfully according to the benchmark's guidelines so that the benchmark gives the highest reward for the agent's exectuion. Second, if the agent estimates that complying with that specific capability may interfere with a successful highest-reward execution, the agent is allowed NOT to comply with the capability and excercise a JUDGEMENT CALL to operate differently instead. 
For example, consider the following scenario. The selected core capability is a text instruction "Never open the door". The task has a user asking the agent to open the door and talk to a person. The benchmark requires accurate execution of the user's request for maximum reward. Clearly, in this scenario, complying with the capability should interfere with getting maximum task reward. Therefore, a reasonable "softness clause" for the capability can be "Never open the door unless you estimate that interferes with accomplishing the task at maximum reward, in which case you are allowed not to comply with this rule.". 

### 5. Edits with code changes, text changes or both
1. A capability you select for editing or generating (if adding new) may contain code, text prompts or both. **Considering code changes should be done with great care.** Code is deterministic, with fixed behavior. Therefore, code changes must be GENERIC and CLEAR, to avoid helping some tasks while degrading other tasks. When the change you intend to impose is not suitable to be expressed in code due to these limitations, you may consider implementing the change in text, which is often more flexible. For genericity in text as well, you may include alternatives in the text for addressing task variations.
2. **For editing tools, use the whole tools skill.** Study `./guidance/tools/SKILL.md` (the
   `skills/capabilities/tools` skill) carefully and use the full range of what it offers:
   update tool descriptions, update tool code, add new tools and remove tools that hurt.

### 6. On code surfaces (tools, MCP): prefer code over prose
Applies only if a selected capability edits code. A BEHAVIORAL miss (the agent knows the rule but skips it: doesn't look a record up first, acts on a guess, miscomputes a total) is not fixed by one more prose rule; enforce it in the tool body (a guard that raises an actionable error, a computation, a composite tool). Add a new tool when it closes a real gap the agent will call;
don't defer a capability-gap cluster to a later iteration. Prompt-only and skill-only surfaces
have no code lever: use the structural-prose equivalents in the capability skill (an ordered
procedure, a checklist step, a worked example, a tightened output contract).



## Run budget — THIS MAY BE YOUR LAST ITERATION (iteration 3/3 (0 after this one); 0/3 consecutive rejects)
Update `META_INSIGHTS.md` and `FRAMEWORK_IMPROVEMENTS.md` THIS iteration — there may be no next one to do it in.

## Cross-iteration files in THIS working dir (clean ownership — read all)
- `LEDGER.md` — FACTS (framework, read-only): every iteration's outcome + the tasks it MEASURABLY broke/fixed, plus the ones whose move was under 2·SE and so resolves nothing. Never re-introduce a change that broke a task; never redesign an edit because a task landed in `unresolved`.
- `JOURNAL.md` — HANDOVER (yours, append-only across the whole run): read the whole thing, then APPEND your entry for this iteration below the marker line. Do NOT edit earlier entries. This is how you avoid repeating refuted ideas and hitting the same plateau.
- `PROCESS.md` — EXPLAINABILITY (yours, REQUIRED this iteration): fill it in as you work (ranked issues, every edit + class, verify-the-fix, subagents/features used, what to preserve, what you skipped). It is snapshotted with your candidate.
- `RUNMAP.md` + `./prior_iterations/<id>/` — every prior iteration's PROCESS.md + capability diff, copied in for you. Read the ones targeting your cluster BEFORE proposing, so you build on prior work instead of repeating it.
- `INSIGHTS.md` — SUMMARIZED, VERIFIED findings (yours, append-only, optional most iterations): a distilled 'what worked / what didn't / what's promising' a future iteration reads INSTEAD of the whole journal. Add an entry whenever you have a new CONFIRMED finding (cite the RESULT that confirmed it).
- `META_INSIGHTS.md` — about the SEARCH PROCESS itself (yours, append-only): which strategies helped or stalled, what to try next. Update AT LEAST once, at the end of the run.
- `FRAMEWORK_IMPROVEMENTS.md` — cross-run suggestions for cap-evolve ITSELF, not this task (yours, append-only, optional): what confused you or was missing about the framework. Update AT LEAST once, at the end of the run.
- `.capevolve/run_suite/rejected.jsonl` — ALREADY-REFUTED approaches (framework, read-only; JSON lines, one per rejected candidate with the gate's reason). Read it and make each proposal STRUCTURALLY different from what is in it. Its sibling `history.jsonl` is the same record for accepts.

