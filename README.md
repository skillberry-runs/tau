# tau

Results of [cap-evolve](https://github.com/skillberry-ai/cap-evolve) runs on **tau2**: the τ²-bench customer-service agent benchmark (airline / retail domains) and its cap-evolve variants.
One of the per-benchmark result repos in the [skillberry-runs](https://github.com/skillberry-runs) org.

**On the dashboard:** <https://skillberry-runs.github.io/dashboard/tau/>. The run rows (reward,
cost, models per run) are on the [main table](https://skillberry-runs.github.io/dashboard/) (filter
*Benchmark*); each row's **Open UI** opens that run's CapEvolve dashboard from this repo's `ci_ui/`.

## What is here

- `ci_ui/<run_id>__<tier>-<bench>/`: per-run "Open UI" data (38 runs, 2026-07-24 to 2026-10-25), moved on
  2026-11-17 from cap-evolve's `benchmark-history` branch. See [`ci_ui/README.md`](ci_ui/README.md).
- Write-ups (`*.md`) and report pages (`ui/*.html`) added here are published on the dashboard too.

| `bench` value in the run records | runs |
|---|---|
| `tau2` | 47 |
| `tau2_custom_blackbox` | 6 |
| `tau2_custom_direct` | 3 |
| `tau2_custom_spa` | 3 |
| `tau2_sierra` | 1 |
| `tau2_sierra_blackbox` | 2 |
| `tau2_blackbox` | 1 |
| `skillberry_tau2_direct` | 2 |
| `skillberry_tau2_spa` | 2 |

## Adding to it

See the dashboard's [PUBLISHING.md](https://github.com/skillberry-runs/dashboard/blob/main/PUBLISHING.md):
section B for write-ups, F for "Open UI" data.
