## Smoke suite — tau2  (train-fit, no holdout)

Agent `ibm-ete-int/aws/gpt-oss-120b` · optimizer Claude Code `ibm-ete-int/claude-opus-4-8` · 1 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2 | `8` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `11` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `12` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `19` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `22` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| tau2 | `23` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `25` | 0.000 → 0.000 | +0.000 |  |
| tau2 | `37` | 1.000 → 1.000 | +0.000 |  |
| tau2 | `40` | 0.000 → 0.000 | +0.000 |  |

**Suite (train-fit):** mean reward 0.333 → 0.333 (Δ +0.000 (+0% rel)) · best = seed (no candidate beat baseline) · optimizer $6.11 over 1 iter(s) · 1 task(s) infra-errored

> No candidate was accepted, so base→opt is the seed against itself and Δ is 0.000 by construction. Re-scoring those same bytes for the finalize read 0.000 against the baseline's 0.333 — a spread of 0.333. That is this tier's re-measurement **noise**, not a change in the capability, and it is the floor any real effect here would have to clear.

### Iterations

| phase | iter | candidate | accepted | reward | traded | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|---|
| baseline | — | `seed` | — | 0.333 | — | $0.0000 | 0s | $0.0000 | 2m16s |
| iterate | 1 | `cand_0001` | ❌ | 0.200 | +1 fixed / -2 broke | $6.1061 | 21m28s | $0.0000 | 4m08s |
| finalize | — | `seed` | — | 0.000 | — | $0.0000 | 0s | $0.0000 | 4m13s |

**Totals:** optimizer $6.1061 over 21m28s · eval $0.0000 over 10m37s
