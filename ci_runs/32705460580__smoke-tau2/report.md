## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `11` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `12` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `19` | 0.333 → 1.000 | +0.667 |  |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 0.667 → 0.333 | -0.333 | ↓ |
| tau2 | `25` | 0.000 → 1.000 | +1.000 |  |
| tau2 | `37` | 0.000 → 0.333 | +0.333 |  |
| tau2 | `40` | 0.000 → 0.333 | +0.333 |  |

**Suite (train-fit):** mean reward 0.167 → 0.367 (Δ +0.200 (+120% rel)) · best = `r1_exec` · optimizer $0.00 over 3 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.167 | $0.0000 | 0s | $0.0000 | 6m06s |
| iterate | 1 | `r1_exec` | ✅ | 0.467 | $0.0000 | — | — | — |
| iterate | 2 | `r2_exec` | ❌ | 0.333 | $0.0000 | — | — | — |
| iterate | 3 | `r3_exec` | ❌ | 0.367 | $0.0000 | — | — | — |
| finalize | — | `r1_exec` | — | 0.367 | $0.0000 | 0s | $0.0000 | 3m08s |
| finalize_baseline | — | `seed` | — | 0.300 | $0.0000 | 0s | $0.0000 | 4m17s |

**Totals:** optimizer $0.0000 over 0s · eval $0.0000 over 13m31s
