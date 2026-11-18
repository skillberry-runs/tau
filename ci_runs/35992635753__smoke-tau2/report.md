## Smoke suite — tau2  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 1 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `11` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `12` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `19` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `22` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `23` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `25` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `37` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.500 → 0.500 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $5.88 over 1 iter(s)

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.444 against the baseline's 0.500 — a spread of 0.056. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.500 | $0.0000 | 0s | $0.0000 | 1m45s |
| iterate | 1 | `cand_0001` | ❌ | 0.750 | $5.8828 | 16m17s | $0.0000 | 1m54s |
| finalize | — | `seed` | — | 0.444 | $0.0000 | 0s | $0.0000 | 1m35s |

**Totals:** optimizer $5.8828 over 16m17s · eval $0.0000 over 5m14s
