# smoke / tau2 — run 45614993743

A cap-evolve benchmark run, published automatically by its CI job (`ci/benchmarks/lib/publish_results.sh`). Its row is on the [benchmark-runs dashboard](https://skillberry-runs.github.io/dashboard/).

[Actions run](https://github.com/skillberry-ai/cap-evolve/actions/runs/45614993743) · [commit `d0363e5c0`](https://github.com/skillberry-ai/cap-evolve/tree/d0363e5c0d5ace112f6e80ef635bf7c5132bdd83) · [Open UI](https://skillberry-runs.github.io/dashboard/viewer/index.html?dataBase=https%3A%2F%2Fskillberry-runs.github.io%2Fdashboard%2Ftau%2Fci_ui%2F45614993743__smoke-tau2#/runs/run_suite)

## Run

| | |
|---|---|
| Benchmark / tier | `tau2` / `smoke` |
| Source | manual (feat/agent-harness-capability) |
| Date (UTC) | 2026-11-25T14:38:30Z |
| Conclusion | success |
| Agent model | `ibm-ete/aws/gpt-oss-120b` |
| Optimizer model | `ibm-ete/claude-opus-4-8` |
| Algorithm | `hill-climb-all` |
| Iterations / trials | 3 / 3 |
| Gate (k·SE) | 1.0 |

## Results

- **Reward:** 0.217 → 0.633 (10 tasks), each measured in this run against its own baseline.
- **Cost:** eval $0.0000, optimizer $13.6646.
- **Sealed test:** 0.383 → 0.633 (best candidate `cand_0003`, Δ 0.250).
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
- **Raw run data** (run dir with candidates, traces and rollouts, 18 MB compressed): `user/eranra/tau/45614993743__smoke-tau2.tar.gz` in the `skillberry-runs-backup` archive (on runner skillberry-2-capevolve in ~/skillberry-runs-backup/, to be moved to Box).

## Re-running it

The tier's tasks, split and overrides are committed in cap-evolve under `ci/benchmarks/tau2/smoke/`. To run the same configuration again, dispatch the Benchmarks workflow on a branch at the commit above:

```bash
gh workflow run benchmarks.yml -R skillberry-ai/cap-evolve --ref <branch> -f tier=smoke -f bench=tau2 \
  -f iterations=3 -f trials=3 -f agent_model=ibm-ete/aws/gpt-oss-120b \
  -f optimizer_model=claude-opus-4-8 -f algorithm=hill-climb-all
```

Model calls are sampled, so a re-run gives a new measurement, not the same numbers.
