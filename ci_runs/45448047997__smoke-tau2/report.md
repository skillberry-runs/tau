## Smoke suite — tau2  (train-fit, no holdout)

Agent `ibm-ete/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete/claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.667 → 0.333 | -0.333 | ↓ |
| tau2 | `11` | 0.667 → 1.000 | +0.333 |  |
| tau2 | `12` | 0.667 → 1.000 | +0.333 |  |
| tau2 | `17` | 0.000 → 0.667 | +0.667 |  |
| tau2 | `19` | 0.000 → 0.667 | +0.667 |  |
| tau2 | `22` | 0.000 → 0.667 | +0.667 |  |
| tau2 | `23` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `25` | 0.667 → 1.000 | +0.333 |  |
| tau2 | `37` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `40` | 0.333 → 1.000 | +0.667 |  |

**Suite (train-fit):** mean reward 0.333 → 0.667 (Δ +0.333 (+100% rel)) · best = `cand_0003` · optimizer $13.87 over 3 iter(s)

### Iterations

| phase | iter | candidate | accepted | reward | traded | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|---|
| baseline | — | `seed` | — | 0.333 | — | $0.0000 | 0s | $0.0000 | 2m46s |
| iterate | 1 | `cand_0001` | ✅ | 0.467 | — | $5.4724 | 12m49s | $0.0000 | 3m59s |
| iterate | 2 | `cand_0002` | ✅ | 0.567 | — | $3.8092 | 12m29s | $0.0000 | 2m36s |
| iterate | 3 | `cand_0003` | ✅ | 0.700 | — | $4.5875 | 15m58s | $0.0000 | 2m49s |
| finalize | — | `cand_0003` | — | 0.667 | — | $0.0000 | 0s | $0.0000 | 5m02s |
| finalize_baseline | — | `seed` | — | 0.433 | — | $0.0000 | 0s | $0.0000 | 7m35s |

**Totals:** optimizer $13.8691 over 41m16s · eval $0.0000 over 24m47s
