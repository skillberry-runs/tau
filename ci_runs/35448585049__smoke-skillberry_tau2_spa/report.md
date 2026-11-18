## Smoke suite — skillberry_tau2_spa  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 1 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| skillberry_tau2_spa | `8` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_spa | `11` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_spa | `12` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_spa | `17` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_spa | `19` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_spa | `22` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_spa | `23` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_spa | `25` | 0.000 → 0.000 | +0.000 |  |
| skillberry_tau2_spa | `37` | 1.000 → 1.000 | +0.000 |  |
| skillberry_tau2_spa | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.100 → 0.100 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $10.29 over 1 iter(s)

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.222 against the baseline's 0.100 — a spread of 0.122. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.100 | $0.0000 | 0s | $0.0000 | 10m34s |
| iterate | 1 | `cand_0001` | ❌ | 0.300 | $10.2870 | 33m15s | $0.0000 | 6m19s |
| finalize | — | `seed` | — | 0.222 | $0.0000 | 0s | $0.0000 | 4m22s |

**Totals:** optimizer $10.2870 over 33m15s · eval $0.0000 over 21m15s
