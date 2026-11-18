## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.333 → 0.667 | +0.333 |  |
| tau2 | `11` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `12` | 0.667 → 0.000 | -0.667 | ↓ |
| tau2 | `17` | 0.000 → 0.667 | +0.667 |  |
| tau2 | `19` | 0.667 → 0.000 | -0.667 | ↓ |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 0.333 → 0.000 | -0.333 | ↓ |
| tau2 | `25` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `37` | 0.000 → 0.333 | +0.333 |  |
| tau2 | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.233 → 0.200 (Δ -0.033 (-14% rel)) · best = seed (no candidate beat baseline) · optimizer $0.00 over 3 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.233 | $0.0000 | 0s | $0.0000 | 5m23s |
| iterate | 1 | `cand_r1_policy` | ❌ | 0.267 | $0.0000 | — | — | — |
| iterate | 2 | `cand_r2_tools` | ❌ | 0.333 | $0.0000 | — | — | — |
| iterate | 3 | `cand_r3_remove` | ❌ | 0.300 | $0.0000 | — | — | — |
| finalize | — | `seed` | — | 0.200 | $0.0000 | 0s | $0.0000 | 9m49s |

**Totals:** optimizer $0.0000 over 0s · eval $0.0000 over 15m12s
