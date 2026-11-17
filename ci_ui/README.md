# ci_ui/ — per-run "Open UI" data

One folder per benchmark run: `ci_ui/<run_id>__<tier>-<bench>/`, holding that run's exported
dashboard data (the JSON files the CapEvolve viewer reads). The folder name is the same slug the
run's row on the [dashboard](https://skillberry-runs.github.io/dashboard/) uses, so a row finds its
data without a lookup table.

- **Viewer:** not stored here. One shared copy lives in
  [skillberry-runs/dashboard](https://github.com/skillberry-runs/dashboard) (`site/viewer/`); a row's
  "Open UI" opens it on this run's folder.
- **Publishing:** the dashboard's deploy copies this folder onto the public site
  (`/tau/ci_ui/<slug>/`), masking internal cluster paths and host names on the way.
- **Masking already applied here:** this repo's commits go through IBM Vault Radar. Text it reads
  as a credential was replaced before committing (every case so far was a false positive):
  tool-call ids `toolu_bdrk_…` → `toolu_masked_<hash>` (consistent, so tool calls still pair with
  their results), public OAuth client ids → `<public-oauth-client-id>`, and flagged assignment
  values → `<masked>`. See the dashboard's `scripts/mask_secrets.py`. Unmasked originals remain on
  cap-evolve's `benchmark-history` branch (`runs/<slug>/ui/data/`).
- **Adding runs:** the dashboard's `scripts/migrate_ui_snapshots.py` copies new runs from
  `benchmark-history`; see its PUBLISHING.md.

Migrated from cap-evolve's `benchmark-history` on 2026-11-17.
