## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.333 → 0.000 | -0.333 | ↓ |
| tau2 | `11` | 0.333 → 0.000 | -0.333 | ↓ |
| tau2 | `12` | 0.667 → 0.667 | +0.000 |  |
| tau2 | `17` | 0.000 → 0.333 | +0.333 |  |
| tau2 | `19` | 1.000 → 0.333 | -0.667 | ↓ |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 0.667 → 0.333 | -0.333 | ↓ |
| tau2 | `25` | 0.000 → 0.333 | +0.333 |  |
| tau2 | `37` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.333 → 0.233 (Δ -0.100 (-30% rel)) · best = `cand_r2_recipe` · optimizer $0.00 over 2 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.333 | $0.0000 | 0s | $0.0000 | 3m39s |
| iterate | 1 | `cand_r1_policy` | ❌ | 0.433 | $0.0000 | — | — | — |
| iterate | 2 | `cand_r2_recipe` | ✅ | 0.467 | $0.0000 | — | — | — |
| finalize | — | `cand_r2_recipe` | — | 0.233 | $0.0000 | 0s | $0.0000 | 6m35s |
| finalize_baseline | — | `seed` | — | 0.333 | $0.0000 | 0s | $0.0000 | 5m23s |

**Totals:** optimizer $0.0000 over 0s · eval $0.0000 over 15m38s
