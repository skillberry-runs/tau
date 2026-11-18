## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.300 → 0.500 | +0.200 |  |
| tau2 | `11` | 0.200 → 0.300 | +0.100 |  |
| tau2 | `12` | 0.500 → 0.600 | +0.100 |  |
| tau2 | `17` | 0.300 → 0.200 | -0.100 | ↓ |
| tau2 | `19` | 0.600 → 0.800 | +0.200 |  |
| tau2 | `22` | 0.000 → 0.100 | +0.100 |  |
| tau2 | `23` | 0.600 → 0.300 | -0.300 | ↓ |
| tau2 | `25` | 0.600 → 0.500 | -0.100 | ↓ |
| tau2 | `37` | 0.400 → 0.500 | +0.100 |  |
| tau2 | `40` | 0.000 → 0.700 | +0.700 |  |

**Suite (train-fit):** mean reward 0.350 → 0.450 (Δ +0.100 (+29% rel)) · best = `cand_r1_exec` · optimizer $0.00 over 1 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.350 | $0.0000 | 0s | $0.0000 | 12m59s |
| iterate | 1 | `cand_r1_exec` | ✅ | 0.440 | $0.0000 | — | — | — |
| finalize | — | `cand_r1_exec` | — | 0.450 | $0.0000 | 0s | $0.0000 | 18m44s |
| finalize_baseline | — | `seed` | — | 0.280 | $0.0000 | 0s | $0.0000 | 19m45s |

**Totals:** optimizer $0.0000 over 0s · eval $0.0000 over 51m27s
