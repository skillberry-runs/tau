## Smoke suite — skillberry_tau2_direct  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 1 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| skillberry_tau2_direct | `8` | 1.000 → 1.000 | +0.000 |  |
| skillberry_tau2_direct | `11` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_direct | `12` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_direct | `17` | 1.000 → 1.000 | +0.000 |  |
| skillberry_tau2_direct | `19` | 1.000 → 1.000 | +0.000 |  |
| skillberry_tau2_direct | `22` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_direct | `23` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_direct | `25` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_direct | `37` | 1.000 → 1.000 | +0.000 |  |
| skillberry_tau2_direct | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.400 → 0.400 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $4.59 over 1 iter(s)

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.333 against the baseline's 0.400 — a spread of 0.067. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.400 | $0.0000 | 0s | $0.0000 | 1m19s |
| iterate | 1 | `cand_0001` | ❌ | 0.333 | $4.5942 | 13m43s | $0.0000 | 2m01s |
| finalize | — | `seed` | — | 0.333 | $0.0000 | 0s | $0.0000 | 4m52s |

**Totals:** optimizer $4.5942 over 13m43s · eval $0.0000 over 8m12s
