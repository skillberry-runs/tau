## Smoke suite — tau2  (train-fit, no holdout)

Agent `ibm-ete/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete/claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.667 → 0.667 | +0.000 |  |
| tau2 | `11` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `12` | 0.333 → 1.000 | +0.667 |  |
| tau2 | `17` | 0.333 → 1.000 | +0.667 |  |
| tau2 | `19` | 0.333 → 1.000 | +0.667 |  |
| tau2 | `22` | 0.000 → 1.000 | +1.000 |  |
| tau2 | `23` | 0.333 → 0.667 | +0.333 |  |
| tau2 | `25` | 0.333 → 0.667 | +0.333 |  |
| tau2 | `37` | 0.667 → 1.000 | +0.333 |  |
| tau2 | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.400 → 0.800 (Δ +0.400 (+100% rel)) · best = `cand_0003` · optimizer $16.65 over 3 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | traded | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|---|
| baseline | — | `seed` | — | 0.400 | — | $0.0000 | 0s | $0.0000 | 2m40s |
| iterate | 1 | `cand_0001` | ❌ | 0.300 | — | $4.2142 | 12m08s | $0.0000 | 2m31s |
| iterate | 2 | `cand_0002` | ✅ | 0.617 | +1 fixed / -0 broke | $6.4987 | 18m31s | $0.0000 | 3m20s |
| iterate | 3 | `cand_0003` | ✅ | 0.717 | — | $5.9397 | 14m04s | $0.0000 | 3m46s |
| finalize | — | `cand_0003` | — | 0.800 | — | $0.0000 | 0s | $0.0000 | 2m41s |
| finalize_baseline | — | `seed` | — | 0.367 | — | $0.0000 | 0s | $0.0000 | 2m23s |

**Totals:** optimizer $16.6526 over 44m43s · eval $0.0000 over 17m21s
