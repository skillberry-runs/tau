## Canary suite — tau2  (train-fit, no holdout)

Agent `ibm-ete-int/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete/claude-opus-4-8` · 1 iteration(s) · **all 1 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 1.000 → 1.000 | +0.000 |  |

**Suite (train-fit):** mean reward 1.000 → 1.000 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $3.02 over 1 iter(s)

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 1.000 against the baseline's 1.000 — a spread of 0.000. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 1.000 | $0.0000 | 0s | $0.0000 | 40s |
| iterate | 1 | `cand_0001` | ❌ | 0.000 | $3.0210 | 9m14s | $0.0000 | 25s |
| finalize | — | `seed` | — | 1.000 | $0.0000 | 0s | $0.0000 | 36s |

**Totals:** optimizer $3.0210 over 9m14s · eval $0.0000 over 1m42s
