## Smoke suite — tau2_custom_blackbox  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 1 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2_custom_blackbox | `8` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_blackbox | `11` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_blackbox | `12` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_blackbox | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_blackbox | `19` | 1.000 → 1.000 | +0.000 |  |
| tau2_custom_blackbox | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_blackbox | `23` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_blackbox | `25` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_blackbox | `37` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_blackbox | `40` | 1.000 → 1.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.200 → 0.200 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $5.84 over 1 iter(s)

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.300 against the baseline's 0.200 — a spread of 0.100. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.200 | $0.0000 | 0s | $0.0000 | 3m23s |
| iterate | 1 | `cand_0001` | ❌ | 0.100 | $5.8424 | 18m21s | $0.0000 | 3m26s |
| finalize | — | `seed` | — | 0.300 | $0.0000 | 0s | $0.0000 | 4m25s |

**Totals:** optimizer $5.8424 over 18m21s · eval $0.0000 over 11m14s
