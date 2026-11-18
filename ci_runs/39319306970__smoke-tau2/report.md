## Smoke suite — tau2  (train-fit, no holdout)

Agent `ibm-ete-int/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete-int/claude-opus-4-8` · 3 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.667 → 0.667 | +0.000 |  |
| tau2 | `11` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `12` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `19` | 0.667 → 0.667 | +0.000 |  |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `25` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `37` | 0.333 → 0.333 | +0.000 |  |
| tau2 | `40` | 0.500 → 0.500 | +0.000 |  |

**Suite (train-fit):** mean reward 0.317 → 0.317 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $29.21 over 3 iter(s)

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.300 against the baseline's 0.317 — a spread of 0.017. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | traded | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|---|
| baseline | — | `seed` | — | 0.317 | — | $0.0000 | 0s | $0.0000 | 13m22s |
| iterate | 1 | `cand_0001` | ❌ | 0.417 | — | $10.3971 | 25m38s | $0.0000 | 20m25s |
| iterate | 2 | `cand_0002` | ❌ | 0.433 | — | $7.7362 | 19m25s | $0.0000 | 11m41s |
| iterate | 3 | `cand_0003` | ❌ | 0.433 | — | $11.0804 | 29m56s | $0.0000 | 21m20s |
| finalize | — | `seed` | — | 0.300 | — | $0.0000 | 0s | $0.0000 | 30m28s |

**Totals:** optimizer $29.2137 over 74m58s · eval $0.0000 over 97m16s
