## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 10 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.300 → 0.200 | -0.100 | ↓ |
| tau2 | `11` | 0.300 → 0.800 | +0.500 |  |
| tau2 | `12` | 0.800 → 0.600 | -0.200 | ↓ |
| tau2 | `17` | 0.100 → 0.400 | +0.300 |  |
| tau2 | `19` | 0.700 → 0.400 | -0.300 | ↓ |
| tau2 | `22` | 0.000 → 0.300 | +0.300 |  |
| tau2 | `23` | 0.400 → 0.400 | +0.000 |  |
| tau2 | `25` | 0.600 → 0.900 | +0.300 |  |
| tau2 | `37` | 0.500 → 0.400 | -0.100 | ↓ |
| tau2 | `40` | 0.100 → 0.900 | +0.800 |  |

**Suite (train-fit):** mean reward 0.380 → 0.530 (Δ +0.150 (+39% rel)) · best = `cand4` · optimizer $16.63 over 4 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.380 | $0.0000 | 0s | $0.0000 | 9m28s |
| iterate | 1 | `cand1` | ❌ | 0.400 | $0.0000 | — | — | — |
| iterate | 2 | `cand2` | ❌ | 0.430 | $0.0000 | — | — | — |
| iterate | 3 | `cand3` | ❌ | 0.370 | $0.0000 | — | — | — |
| iterate | 4 | `cand4` | ✅ | 0.530 | $0.0000 | — | — | — |
| finalize | — | `cand4` | — | 0.530 | $0.0000 | 0s | $0.0000 | 18m19s |
| finalize_baseline | — | `seed` | — | 0.400 | $0.0000 | 0s | $0.0000 | 16m55s |

**Totals:** optimizer $0.0000 over 0s · eval $0.0000 over 44m42s
