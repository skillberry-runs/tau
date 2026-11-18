## Smoke suite — tau2_custom_spa  (train-fit, no holdout)

Agent `aws/gpt-oss-120b` · optimizer Claude Code `claude-opus-4-8` · 1 iteration(s) · **all 10 tasks optimized together** · `train==val==test` (FIT metric, not a generalization/held-out claim).

| bench | task | reward (base→opt) | Δ | note |
|---|---|---|---|:--:|
| tau2_custom_spa | `8` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_spa | `11` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_spa | `12` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_spa | `17` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_spa | `19` | 1.000 → 1.000 | +0.000 |  |
| tau2_custom_spa | `22` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| tau2_custom_spa | `23` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_spa | `25` | 0.000 → ⚠️ infra-error | — | ⚠️ |
| tau2_custom_spa | `37` | 0.000 → 0.000 | +0.000 |  |
| tau2_custom_spa | `40` | 0.000 → ⚠️ infra-error | — | ⚠️ |

**Suite (train-fit):** mean reward 0.111 → 0.250 (Δ +0.139 (+125% rel)) · best = `cand_0001` · optimizer $4.07 over 1 iter(s) · 3 task(s) infra-errored

### Iterations

| phase | iter | candidate | accepted | reward | optimizer $ | optimizer time | eval $ | eval time |
|---|:--:|---|:--:|---|---|---|---|---|
| baseline | — | `seed` | — | 0.111 | $0.0000 | 0s | $0.0000 | 4m08s |
| iterate | 1 | `cand_0001` | ✅ | 0.500 | $4.0695 | 10m45s | $0.0000 | 2m49s |
| finalize | — | `cand_0001` | — | 0.250 | $0.0000 | 0s | $0.0000 | 1m19s |
| finalize_baseline | — | `seed` | — | 0.222 | $0.0000 | 0s | $0.0000 | 2m37s |

**Totals:** optimizer $4.0695 over 10m45s · eval $0.0000 over 10m52s
