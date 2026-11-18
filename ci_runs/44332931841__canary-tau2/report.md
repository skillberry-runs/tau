## Canary suite — tau2  (train-fit, no holdout)

Agent `ibm-ete-int/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete/claude-opus-4-8` · 1 iteration(s) · **all 1 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.000 → 1.000 | +1.000 |  |

**Suite (train-fit):** mean reward 0.000 → 1.000 (Δ +1.000) · best = `cand_0001` · optimizer $3.00 over 1 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | traded | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|---|
| baseline | — | `seed` | — | 0.000 | — | $0.0000 | 0s | $0.0000 | 48s |
| iterate | 1 | `cand_0001` | ✅ | 1.000 | +1 fixed / -0 broke | $3.0030 | 8m17s | $0.0000 | 22s |
| finalize | — | `cand_0001` | — | 1.000 | — | $0.0000 | 0s | $0.0000 | 21s |
| finalize_baseline | — | `seed` | — | 1.000 | — | $0.0000 | 0s | $0.0000 | 31s |

**Totals:** optimizer $3.0030 over 8m17s · eval $0.0000 over 2m02s
