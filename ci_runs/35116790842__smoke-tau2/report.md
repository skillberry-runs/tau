## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 2 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.500 → 0.500 | +0.000 |  |
| tau2 | `11` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `12` | 0.500 → 1.000 | +0.500 |  |
| tau2 | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `19` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `25` | 0.500 → 0.500 | +0.000 |  |
| tau2 | `37` | 0.000 → 1.000 | +1.000 |  |
| tau2 | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.250 → 0.400 (Δ +0.150 (+60% rel)) · best = `cand_0001` · optimizer $9.63 over 2 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.250 | $0.0000 | 0s | $0.0000 | 2m51s |
| iterate | 1 | `cand_0001` | ✅ | 0.450 | $4.5594 | 15m06s | $0.0000 | 6m19s |
| iterate | 2 | `cand_0002` | ❌ | 0.450 | $5.0699 | 18m09s | $0.0000 | 5m47s |
| finalize | — | `cand_0001` | — | 0.400 | $0.0000 | 0s | $0.0000 | 6m45s |
| finalize_baseline | — | `seed` | — | 0.450 | $0.0000 | 0s | $0.0000 | 2m15s |

**Totals:** optimizer $9.6292 over 33m15s · eval $0.0000 over 23m57s
