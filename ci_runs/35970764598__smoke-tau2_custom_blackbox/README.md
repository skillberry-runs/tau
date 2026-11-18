# smoke / tau2_custom_blackbox — run 35970764598

A cap-evolve benchmark run, backfilled on 2026-11-18 from its CI artifact (the run predates per-run folders, so `recipe/` is missing). Its row is on the [benchmark-runs dashboard](https://skillberry-runs.github.io/dashboard/).

[Actions run](https://github.com/skillberry-ai/cap-evolve/actions/runs/35970764598) · [commit `90e0d0bfa`](https://github.com/skillberry-ai/cap-evolve/tree/90e0d0bfad7cc28b7be2303aff0ecaf890554815) · [Open UI](https://skillberry-runs.github.io/dashboard/viewer/index.html?dataBase=https%3A%2F%2Fskillberry-runs.github.io%2Fdashboard%2Ftau%2Fci_ui%2F35970764598__smoke-tau2_custom_blackbox#/runs/run_suite)

## Run

| | |
|---|---|
| Benchmark / tier | `tau2_custom_blackbox` / `smoke` |
| Source | manual (rename_intervention_spa_to_blackbox) |
| Date (UTC) | 2026-09-24T08:14:12Z |
| Conclusion | success |
| Agent model | `aws/gpt-oss-120b` |
| Optimizer model | `claude-opus-4-8` |
| Algorithm | `hill-climb-all` |
| Iterations / trials | 1 / 1 |
| Gate (k·SE) | 1.0 |

## Results

- **Reward:** 0.300 → 0.300 (10 tasks), each measured in this run against its own baseline.
- **Cost:** eval $0.0000, optimizer $5.2697.

Details per task are in `report.md`.

## Files

- [`report.md`](report.md) — the run's metrics report (also its PR comment)
- [`runmeta.json`](runmeta.json) — how the run was launched: models, tier, iterations, trials, commit
- [`metrics.jsonl`](metrics.jsonl) — one row per task: baseline vs optimized reward
- [`steps.jsonl`](steps.jsonl) — one row per iteration: cost and time
- [`capability.diff`](capability.diff) — the optimized capability vs the seed
- [`optimized_capability/`](optimized_capability/) — the optimized capability
- `recipe/` was not available for this run (published from its CI artifact); the tier's definition is `ci/benchmarks/tau2_custom_blackbox/smoke/` at the commit above.

## Re-running it

The tier's tasks, split and overrides are committed in cap-evolve under `ci/benchmarks/tau2_custom_blackbox/smoke/`. To run the same configuration again, dispatch the Benchmarks workflow on a branch at the commit above:

```bash
gh workflow run benchmarks.yml -R skillberry-ai/cap-evolve --ref <branch> -f tier=smoke -f bench=tau2_custom_blackbox \
  -f iterations=1 -f trials=1 -f agent_model=aws/gpt-oss-120b \
  -f optimizer_model=claude-opus-4-8 -f algorithm=hill-climb-all
```

Model calls are sampled, so a re-run gives a new measurement, not the same numbers.
