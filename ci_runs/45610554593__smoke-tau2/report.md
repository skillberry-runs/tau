## Smoke suite — tau2  (train-fit, no holdout)

Agent `ibm-ete/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete/claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.667 → 0.667 | +0.000 |  |
| tau2 | `11` | 0.000 → 1.000 | +1.000 |  |
| tau2 | `12` | 1.000 → 0.333 | -0.667 | ↓ |
| tau2 | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `19` | 0.333 → 1.000 | +0.667 |  |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `25` | 1.000 → 0.500 | -0.500 | ↓ |
| tau2 | `37` | 0.667 → 0.667 | +0.000 |  |
| tau2 | `40` | 0.000 → 0.333 | +0.333 |  |

**Suite (train-fit):** mean reward 0.400 → 0.483 (Δ +0.083 (+21% rel)) · best = `cand_0001` · optimizer $15.18 over 3 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | traded | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|---|
| baseline | — | `seed` | — | 0.400 | — | $0.0000 | 0s | $0.0000 | 2m59s |
| iterate | 1 | `cand_0001` | ✅ | 0.450 | — | $3.6041 | 12m20s | $0.0000 | 2m19s |
| iterate | 2 | `cand_0002` | ❌ | 0.417 | — | $4.2153 | 12m25s | $0.0000 | 3m57s |
| iterate | 3 | `cand_0003` | ❌ | 0.367 | — | $7.3630 | 20m51s | $0.0000 | 2m40s |
| finalize | — | `cand_0001` | — | 0.483 | — | $0.0000 | 0s | $0.0000 | 2m00s |
| finalize_baseline | — | `seed` | — | 0.417 | — | $0.0000 | 0s | $0.0000 | 2m28s |

**Totals:** optimizer $15.1824 over 45m35s · eval $0.0000 over 16m22s
