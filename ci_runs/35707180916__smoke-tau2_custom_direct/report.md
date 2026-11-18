## Smoke suite — tau2_custom_direct  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 1 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2_custom_direct | `8` | 1.000 → 1.000 | +0.000 |  |
| tau2_custom_direct | `11` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_direct | `12` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_direct | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_direct | `19` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| tau2_custom_direct | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_direct | `23` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_direct | `25` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_direct | `37` | 1.000 → 1.000 | +0.000 |  |
| tau2_custom_direct | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.222 → 0.222 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $8.50 over 1 iter(s) · 1 task(s) infra-errored

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.400 against the baseline's 0.222 — a spread of 0.178. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.222 | $0.0000 | 0s | $0.0000 | 1m23s |
| iterate | 1 | `cand_0001` | ❌ | 0.375 | $8.4993 | 19m31s | $0.0000 | 1m47s |
| finalize | — | `seed` | — | 0.400 | $0.0000 | 0s | $0.0000 | 1m05s |

**Totals:** optimizer $8.4993 over 19m31s · eval $0.0000 over 4m15s
