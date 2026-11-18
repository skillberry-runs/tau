# smoke / tau2_custom_blackbox — run 36547368756

A cap-evolve benchmark run, backfilled on 2026-11-18 from its CI artifact (the run predates per-run folders, so `recipe/` is missing). Its row is on the [benchmark-runs dashboard](https://skillberry-runs.github.io/dashboard/).

[Actions run](https://github.com/skillberry-ai/cap-evolve/actions/runs/36547368756) · [commit `422cf780a`](https://github.com/skillberry-ai/cap-evolve/tree/422cf780a4b05d4a52cbec05aa735cf699feeb21)

## Run

| | |
|---|---|
| Benchmark / tier | `tau2_custom_blackbox` / `smoke` |
| Source | manual (blackbox_require_make) |
| Date (UTC) | 2026-09-29T09:10:13Z |
| Conclusion | failure |
| Agent model | `ibm-ete-int/aws/gpt-oss-120b` |
| Optimizer model | `ibm-ete-int/claude-opus-4-8` |
| Algorithm | `hill-climb-all` |
| Iterations / trials | 1 / 1 |
| Gate (k·SE) | 1.0 |

## Results

- No suite result: the run did not finish successfully (see `report.md` and the Actions run).

Details per task are in `report.md`.

## Files

- [`runmeta.json`](runmeta.json) — how the run was launched: models, tier, iterations, trials, commit
- `recipe/` was not available for this run (published from its CI artifact); the tier's definition is `ci/benchmarks/tau2_custom_blackbox/smoke/` at the commit above.

## Re-running it

The tier's tasks, split and overrides are committed in cap-evolve under `ci/benchmarks/tau2_custom_blackbox/smoke/`. To run the same configuration again, dispatch the Benchmarks workflow on a branch at the commit above:

```bash
gh workflow run benchmarks.yml -R skillberry-ai/cap-evolve --ref <branch> -f tier=smoke -f bench=tau2_custom_blackbox \
  -f iterations=1 -f trials=1 -f agent_model=ibm-ete-int/aws/gpt-oss-120b \
  -f optimizer_model=ibm-ete-int/claude-opus-4-8 -f algorithm=hill-climb-all
```

Model calls are sampled, so a re-run gives a new measurement, not the same numbers.
