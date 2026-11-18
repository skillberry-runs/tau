## Smoke suite — tau2_sierra_blackbox  (train-fit, no holdout)

Agent `ibm-ete-int/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete-int/claude-opus-4-8` · 1 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2_sierra_blackbox | `8` | 1.000 → 1.000 | +0.000 |  |
| tau2_sierra_blackbox | `11` | 1.000 → 1.000 | +0.000 |  |
| tau2_sierra_blackbox | `12` | 0.000 → 0.000 | +0.000 |  |
| tau2_sierra_blackbox | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2_sierra_blackbox | `19` | 0.000 → 0.000 | +0.000 |  |
| tau2_sierra_blackbox | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2_sierra_blackbox | `23` | 0.000 → 0.000 | +0.000 |  |
| tau2_sierra_blackbox | `25` | 0.000 → 0.000 | +0.000 |  |
| tau2_sierra_blackbox | `37` | 1.000 → 1.000 | +0.000 |  |
| tau2_sierra_blackbox | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.300 → 0.300 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $10.01 over 1 iter(s)

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.100 against the baseline's 0.300 — a spread of 0.200. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | traded | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|---|
| baseline | — | `seed` | — | 0.300 | — | $0.0000 | 0s | $0.0000 | 2m22s |
| iterate | 1 | `cand_0001` | ❌ | 0.300 | +2 fixed / -2 broke | $10.0073 | 51m21s | $0.0000 | 6m36s |
| finalize | — | `seed` | — | 0.100 | — | $0.0000 | 0s | $0.0000 | 4m04s |

**Totals:** optimizer $10.0073 over 51m21s · eval $0.0000 over 13m02s
