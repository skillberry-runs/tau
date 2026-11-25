# smoke / tau2_sierra_blackbox — run 45593725145

A cap-evolve benchmark run, published automatically by its CI job (`ci/benchmarks/lib/publish_results.sh`). Its row is on the [benchmark-runs dashboard](https://skillberry-runs.github.io/dashboard/).

[Actions run](https://github.com/skillberry-ai/cap-evolve/actions/runs/45593725145) · [commit `0e50c7f57`](https://github.com/skillberry-ai/cap-evolve/tree/0e50c7f57c5a40b491d9b11d6a3c50b95bb63cbb)

## Run

| | |
|---|---|
| Benchmark / tier | `tau2_sierra_blackbox` / `smoke` |
| Source | manual (main) |
| Date (UTC) | 2026-11-25T10:22:57Z |
| Conclusion | failure |
| Agent model | `gpt-oss-120b` |
| Optimizer model | `claude-opus-4-8` |
| Algorithm | `hill-climb-all` |
| Iterations / trials | 3 / 3 |
| Gate (k·SE) | 1.0 |

## Results

- No suite result: the run did not finish successfully (see `report.md` and the Actions run).

Details per task are in `report.md`.

## Files

- [`runmeta.json`](runmeta.json) — how the run was launched: models, tier, iterations, trials, commit
- [`backup.json`](backup.json) — where the run's raw data archive is (backup_run.sh)
- **Raw run data** (run dir with candidates, traces and rollouts, 0 MB compressed): `user/aviweit/tau/45593725145__smoke-tau2_sierra_blackbox.tar.gz` in the `skillberry-runs-backup` archive (on runner skillberry-2-capevolve in ~/skillberry-runs-backup/, to be moved to Box).
- `recipe/` was not available for this run (published from its CI artifact); the tier's definition is `ci/benchmarks/tau2_sierra_blackbox/smoke/` at the commit above.

## Re-running it

The tier's tasks, split and overrides are committed in cap-evolve under `ci/benchmarks/tau2_sierra_blackbox/smoke/`. To run the same configuration again, dispatch the Benchmarks workflow on a branch at the commit above:

```bash
gh workflow run benchmarks.yml -R skillberry-ai/cap-evolve --ref <branch> -f tier=smoke -f bench=tau2_sierra_blackbox \
  -f iterations=3 -f trials=3 -f agent_model=gpt-oss-120b \
  -f optimizer_model=claude-opus-4-8 -f algorithm=hill-climb-all
```

Model calls are sampled, so a re-run gives a new measurement, not the same numbers.
