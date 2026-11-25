## Smoke suite — tau2  (train-fit, no holdout)

Agent `ibm-ete/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete/claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.667 → 1.000 | +0.333 |  |
| tau2 | `11` | 0.333 → 0.667 | +0.333 |  |
| tau2 | `12` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `17` | 0.000 → 0.333 | +0.333 |  |
| tau2 | `19` | 0.500 → 0.667 | +0.167 |  |
| tau2 | `22` | 0.000 → 0.333 | +0.333 |  |
| tau2 | `23` | 0.000 → 0.333 | +0.333 |  |
| tau2 | `25` | 0.000 → 1.000 | +1.000 |  |
| tau2 | `37` | 0.000 → 1.000 | +1.000 |  |
| tau2 | `40` | 0.667 → 1.000 | +0.333 |  |

**Suite (train-fit):** mean reward 0.217 → 0.633 (Δ +0.417 (+192% rel)) · best = `cand_0003` · optimizer $13.66 over 3 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | traded | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|---|
| baseline | — | `seed` | — | 0.217 | — | $0.0000 | 0s | $0.0000 | 2m28s |
| iterate | 1 | `cand_0001` | ❌ | 0.233 | — | $3.8888 | 12m23s | $0.0000 | 2m16s |
| iterate | 2 | `cand_0002` | ✅ | 0.533 | +2 fixed / -0 broke | $5.6794 | 19m45s | $0.0000 | 2m28s |
| iterate | 3 | `cand_0003` | ✅ | 0.567 | +1 fixed / -0 broke | $4.0963 | 11m53s | $0.0000 | 3m09s |
| finalize | — | `cand_0003` | — | 0.633 | — | $0.0000 | 0s | $0.0000 | 3m12s |
| finalize_baseline | — | `seed` | — | 0.383 | — | $0.0000 | 0s | $0.0000 | 2m21s |

**Totals:** optimizer $13.6646 over 44m01s · eval $0.0000 over 15m55s
