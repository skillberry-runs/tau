## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.400 → 0.500 | +0.100 |  |
| tau2 | `11` | 0.300 → 0.400 | +0.100 |  |
| tau2 | `12` | 0.300 → 0.300 | +0.000 |  |
| tau2 | `17` | 0.100 → 0.700 | +0.600 |  |
| tau2 | `19` | 0.300 → 0.900 | +0.600 |  |
| tau2 | `22` | 0.000 → 0.700 | +0.700 |  |
| tau2 | `23` | 0.100 → 0.200 | +0.100 |  |
| tau2 | `25` | 0.600 → 0.600 | +0.000 |  |
| tau2 | `37` | 0.200 → 0.100 | -0.100 | ↓ |
| tau2 | `40` | 0.100 → 0.500 | +0.400 |  |

**Suite (train-fit):** mean reward 0.240 → 0.490 (Δ +0.250 (+104% rel)) · best = `r1_ops_bag` · optimizer $9.05 over 1 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.240 | $0.0000 | 0s | $0.0000 | 14m50s |
| iterate | 1 | `r1_ops_bag` | ✅ | 0.580 | $0.0000 | — | — | — |
| finalize | — | `r1_ops_bag` | — | 0.490 | $0.0000 | 0s | $0.0000 | 13m08s |
| finalize_baseline | — | `seed` | — | 0.290 | $0.0000 | 0s | $0.0000 | 18m34s |

**Totals:** optimizer $0.0000 over 0s · eval $0.0000 over 46m33s
