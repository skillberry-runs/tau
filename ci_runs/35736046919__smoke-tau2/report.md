## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 1 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `11` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `12` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `17` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `19` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `25` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `37` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.600 → 0.600 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $5.92 over 1 iter(s)

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.300 against the baseline's 0.600 — a spread of 0.300. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.600 | $0.0000 | 0s | $0.0000 | 2m20s |
| iterate | 1 | `cand_0001` | ❌ | 0.111 | $5.9208 | 20m45s | $0.0000 | 2m59s |
| finalize | — | `seed` | — | 0.300 | $0.0000 | 0s | $0.0000 | 3m16s |

**Totals:** optimizer $5.9208 over 20m45s · eval $0.0000 over 8m36s
