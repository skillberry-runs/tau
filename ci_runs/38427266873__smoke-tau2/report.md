## Smoke suite — tau2  (train-fit, no holdout)

Agent `ibm-ete-int/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete-int/claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `11` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `12` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `17` | 0.667 → 0.667 | +0.000 |  |
| tau2 | `19` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `25` | 0.667 → 0.667 | +0.000 |  |
| tau2 | `37` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `40` | 0.333 → 0.333 | +0.000 |  |

**Suite (train-fit):** mean reward 0.400 → 0.400 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $19.80 over 3 iter(s)

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.467 against the baseline's 0.400 — a spread of 0.067. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | traded | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|---|
| baseline | — | `seed` | — | 0.400 | — | $0.0000 | 0s | $0.0000 | 21m51s |
| iterate | 1 | `cand_0001` | ❌ | 0.267 | — | $7.4985 | 42m53s | $0.0000 | 29m03s |
| iterate | 2 | `cand_0002` | ❌ | 0.167 | — | $6.2195 | 36m14s | $0.0000 | 49m12s |
| iterate | 3 | `cand_0003` | ❌ | 0.500 | — | $6.0828 | 51m12s | $0.0000 | 57m56s |
| finalize | — | `seed` | — | 0.467 | — | $0.0000 | 0s | $0.0000 | 38m04s |

**Totals:** optimizer $19.8008 over 130m19s · eval $0.0000 over 196m06s
