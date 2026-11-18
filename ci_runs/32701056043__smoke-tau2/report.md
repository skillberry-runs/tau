## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.667 → 0.333 | -0.333 | ↓ |
| tau2 | `11` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `12` | 0.667 → 0.333 | -0.333 | ↓ |
| tau2 | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `19` | 0.333 → 0.000 | -0.333 | ↓ |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `25` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `37` | 0.000 → 0.333 | +0.333 |  |
| tau2 | `40` | 0.000 → 0.333 | +0.333 |  |

**Suite (train-fit):** mean reward 0.267 → 0.233 (Δ -0.033 (-13% rel)) · best = seed (no candidate beat baseline) · optimizer $0.00 over 2 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.267 | $0.0000 | 0s | $0.0000 | 7m15s |
| iterate | 1 | `r1_report_calc` | ❌ | 0.367 | $0.0000 | — | — | — |
| iterate | 2 | `r2_passenger_complete` | ❌ | 0.267 | $0.0000 | — | — | — |
| finalize | — | `seed` | — | 0.233 | $0.0000 | 0s | $0.0000 | 1m30s |

**Totals:** optimizer $0.0000 over 0s · eval $0.0000 over 8m45s
