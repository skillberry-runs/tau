# smoke / skillberry_tau2_direct — run 35111801588

A cap-evolve benchmark run, backfilled on 2026-11-18 from its CI artifact (the run predates per-run folders, so `recipe/` is missing). Its row is on the [benchmark-runs dashboard](https://skillberry-runs.github.io/dashboard/).

[Actions run](https://github.com/skillberry-ai/cap-evolve/actions/runs/35111801588) · [commit `164710695`](https://github.com/skillberry-ai/cap-evolve/tree/1647106954a5c3c2b45822e0c2db0930d70b5810) · [Open UI](https://skillberry-runs.github.io/dashboard/viewer/index.html?dataBase=https%3A%2F%2Fskillberry-runs.github.io%2Fdashboard%2Ftau%2Fci_ui%2F35111801588__smoke-skillberry_tau2_direct#/runs/run_suite)

## Run

| | |
|---|---|
| Benchmark / tier | `skillberry_tau2_direct` / `smoke` |
| Source | manual (ci_skillberry_benchmarks_tau2_2) |
| Date (UTC) | 2026-09-16T15:39:53Z |
| Conclusion | cancelled |
| Agent model | `aws/gpt-oss-120b` |
| Optimizer model | `claude-opus-4-8` |
| Algorithm | `hill-climb-all` |
| Iterations / trials | 2 / 2 |
| Gate (k·SE) | 1.0 |

## Results

- No suite result: the run did not finish successfully (see `report.md` and the Actions run).

Details per task are in `report.md`.

## Files

- [`runmeta.json`](runmeta.json) — how the run was launched: models, tier, iterations, trials, commit
- [`metrics.jsonl`](metrics.jsonl) — one row per task: baseline vs optimized reward
- `recipe/` was not available for this run (published from its CI artifact); the tier's definition is `ci/benchmarks/skillberry_tau2_direct/smoke/` at the commit above.

## Re-running it

The tier's tasks, split and overrides are committed in cap-evolve under `ci/benchmarks/skillberry_tau2_direct/smoke/`. To run the same configuration again, dispatch the Benchmarks workflow on a branch at the commit above:

```bash
gh workflow run benchmarks.yml -R skillberry-ai/cap-evolve --ref <branch> -f tier=smoke -f bench=skillberry_tau2_direct \
  -f iterations=2 -f trials=2 -f agent_model=aws/gpt-oss-120b \
  -f optimizer_model=claude-opus-4-8 -f algorithm=hill-climb-all
```

Model calls are sampled, so a re-run gives a new measurement, not the same numbers.
