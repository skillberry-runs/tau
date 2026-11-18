# canary / tau2 — run 44379871380

A cap-evolve benchmark run, published automatically by its CI job (`ci/benchmarks/lib/publish_results.sh`). Its row is on the [benchmark-runs dashboard](https://skillberry-runs.github.io/dashboard/).

> **Pipeline check only.** A `canary` run exists to exercise the CI path (1 task, 1 trial, 1 iteration); its numbers mean nothing.

[Actions run](https://github.com/skillberry-ai/cap-evolve/actions/runs/44379871380) · [PR #995](https://github.com/skillberry-ai/cap-evolve/pull/995) · [commit `de597c4ef`](https://github.com/skillberry-ai/cap-evolve/tree/de597c4effaa547a7d89d89a279622acdcc48e03) · [Open UI](https://skillberry-runs.github.io/dashboard/viewer/index.html?dataBase=https%3A%2F%2Fskillberry-runs.github.io%2Fdashboard%2Ftau%2Fci_ui%2F44379871380__canary-tau2#/runs/run_suite)

## Run

| | |
|---|---|
| Benchmark / tier | `tau2` / `canary` |
| Source | PR #995 |
| Date (UTC) | 2026-11-18T19:34:28Z |
| Conclusion | success |
| Agent model | `ibm-ete-int/aws/gpt-oss-120b` |
| Optimizer model | `ibm-ete/claude-opus-4-8` |
| Algorithm | `hill-climb-all` |
| Iterations / trials | 1 / 1 |
| Gate (k·SE) | 1.0 |

## Results

- **Reward:** 1.000 → 1.000 (1 task), each measured in this run against its own baseline.
- **Cost:** eval $0.0000, optimizer $3.0210.
- **Sealed test:** 1.000 → 1.000 (best candidate `seed`, Δ 0.000).
- **No held-out split:** train = val = test for this tier, so this is a fit to the tier's tasks, not a measure of generalisation.

Details per task are in `report.md`.

## Files

- [`report.md`](report.md) — the run's metrics report (also its PR comment)
- [`runmeta.json`](runmeta.json) — how the run was launched: models, tier, iterations, trials, commit
- [`metrics.jsonl`](metrics.jsonl) — one row per task: baseline vs optimized reward
- [`steps.jsonl`](steps.jsonl) — one row per iteration: cost and time
- [`final.json`](final.json) — the sealed test result
- [`capability.diff`](capability.diff) — the optimized capability vs the seed
- [`optimized_capability/`](optimized_capability/) — the optimized capability
- [`recipe/capevolve.yaml`](recipe/capevolve.yaml) — the run's cap-evolve spec
- [`recipe/split_ids.json`](recipe/split_ids.json) — the train / val / test task ids
- [`backup.json`](backup.json) — where the run's raw data archive is (backup_run.sh)
- **Raw run data** (run dir with candidates, traces and rollouts, 1 MB compressed): `user/bcarmeli/tau/44379871380__canary-tau2.tar.gz` in the `skillberry-runs-backup` archive (runner skillberry-2-capevolve: ~/skillberry-runs-backup/ (to be moved to Box)).

## Re-running it

The tier's tasks, split and overrides are committed in cap-evolve under `ci/benchmarks/tau2/canary/`. To run the same configuration again, dispatch the Benchmarks workflow on a branch at the commit above:

```bash
gh workflow run benchmarks.yml -R skillberry-ai/cap-evolve --ref <branch> -f tier=canary -f bench=tau2 \
  -f iterations=1 -f trials=1 -f agent_model=gpt-oss-120b \
  -f optimizer_model=claude-opus-4-8 -f algorithm=hill-climb-all
```

Model calls are sampled, so a re-run gives a new measurement, not the same numbers.
