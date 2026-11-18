## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.000 → 1.000 | +1.000 |  |
| tau2 | `11` | 0.333 → 0.667 | +0.333 |  |
| tau2 | `12` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `17` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `19` | 0.667 → 0.667 | +0.000 |  |
| tau2 | `22` | 0.000 → 0.333 | +0.333 |  |
| tau2 | `23` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `25` | 0.333 → 1.000 | +0.667 |  |
| tau2 | `37` | 0.000 → 1.000 | +1.000 |  |
| tau2 | `40` | 0.500 → 1.000 | +0.500 |  |

**Suite (train-fit):** mean reward 0.283 → 0.667 (Δ +0.383 (+135% rel)) · best = `cand_0003` · optimizer $20.56 over 3 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.283 | $0.0000 | 0s | $0.0000 | 9m29s |
| iterate | 1 | `cand_0001` | ✅ | 0.483 | $5.1088 | 17m56s | $0.0000 | 3m59s |
| iterate | 2 | `cand_0002` | ❌ | 0.567 | $7.4261 | 17m03s | $0.0000 | 3m20s |
| iterate | 3 | `cand_0003` | ✅ | 0.667 | $8.0267 | 17m36s | $0.0000 | 4m22s |
| finalize | — | `cand_0003` | — | 0.667 | $0.0000 | 0s | $0.0000 | 49s |
| finalize_baseline | — | `seed` | — | 0.350 | $0.0000 | 0s | $0.0000 | 1m53s |

**Totals:** optimizer $20.5616 over 52m36s · eval $0.0000 over 23m53s
