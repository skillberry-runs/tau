## Smoke suite — skillberry_tau2_spa  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 2 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| skillberry_tau2_spa | `8` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| skillberry_tau2_spa | `11` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| skillberry_tau2_spa | `12` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| skillberry_tau2_spa | `17` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| skillberry_tau2_spa | `19` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| skillberry_tau2_spa | `22` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| skillberry_tau2_spa | `23` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| skillberry_tau2_spa | `25` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| skillberry_tau2_spa | `37` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| skillberry_tau2_spa | `40` | 0.000 → ⚠️ infra-error | — | ⚠️ |

**Suite (train-fit):** mean reward 0.000 → 0.000 (Δ +0.000) · best = seed (no candidate beat baseline) · optimizer $6.11 over 2 iter(s) · 10 task(s) infra-errored

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.000 against the baseline's 0.000 — a spread of 0.000. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.000 | $0.0000 | 0s | $0.0000 | 0s |
| iterate | 1 | `cand_0001` | ❌ | 0.000 | $2.8691 | 10m51s | $0.0000 | 0s |
| iterate | 2 | `cand_0002` | ❌ | 0.000 | $3.2416 | 12m02s | $0.0000 | 0s |
| finalize | — | `seed` | — | 0.000 | $0.0000 | 0s | $0.0000 | 0s |

**Totals:** optimizer $6.1106 over 22m52s · eval $0.0000 over 0s
