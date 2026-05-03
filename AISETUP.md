# AI Agent Setup Instructions

This file is intended for AI coding assistants (Claude, Copilot, Cursor, etc.) working in this repository. It covers setup, the correct Python environment to use, and how to diagnose common failures.

## First-time setup

Run once before doing anything else:

```bash
python3 setup_environment.py
```

Then use `.venv/bin/python3` for all subsequent Python commands. Do **not** use the system `python3` — it lacks the required packages.

## Generating tables

```bash
.venv/bin/python3 Analysis/run_all.py --tables
```

To run a single table:

```bash
.venv/bin/python3 Analysis/tables/<script>.py
```

## Environment details

- **Python**: `.venv/` is built from Homebrew Python 3.12 on macOS (`/opt/homebrew/bin/python3.12`), or system `python3` on Linux.
- **Stata**: macOS at `/Applications/Stata/` (SE edition), Linux at `/usr/local/stata/`. Stata is invoked via `pystata` — it runs in-process, not as a subprocess.
- **pystata path**: The venv has a `.venv/lib/python3.12/site-packages/stata.pth` file containing `/Applications/Stata/utilities`. This is what makes `import sfi` work on macOS. If the venv is deleted and recreated, `setup_environment.py` will recreate this file.
- **Stata packages required**: `estout`, `ftools`, `reghdfe`, `outreg2`, `ppmlhdfe`. These are installed by `setup_environment.py`. If a script fails because a Stata package is missing, re-run the setup script.

## Known non-fatal warning

When running on macOS, scripts print:

```
failed to set the specified Python version.
Unable to find the shared library.
```

This is Stata trying to locate its own embedded Python (the reverse direction from how we use it). It does not indicate a failure — ignore it.

## Repository structure

- `Analysis/tables/` — one `.py` per manuscript table. Each script produces one or more `.tex` files in `LaTeX/Tables/`.
- `Analysis/shared/` — shared utilities. `table_helpers.py` is the main entry point for table scripts: it initializes Stata and loads the data.
- `Analysis/Data/df4m_w.csv` — the analysis dataset. All table scripts read from this file. It is committed to the repo; no download needed.
- `LaTeX/Tables/` — generated `.tex` output files, `\input`-ed by `manuscript.tex`.
- `LaTeX/manuscript.tex` — the main LaTeX document.

## What each table script produces

| Script | Output |
|--------|--------|
| `sample_design.py` | `sampleDesign.tex` |
| `descriptive_stats.py` | `descriptive_stats.tex` |
| `descriptive_stats_by_audit.py` | `descriptive_stats_by_audit.tex` |
| `excess_adj_full_sample.py` | `excess_adj_full_sample.tex` |
| `alternative_dvs.py` | `alternative_dvs.tex` |
| `face_vs_notes.py` | `face_vs_notes.tex` |
| `procs.py` | `procs_panelA.tex`, `procs.tex`, `procs_additional.tex` |
| `value_rel.py` | `value_rel.tex` |

## Troubleshooting

**`ModuleNotFoundError: No module named 'sfi'`**
The `stata.pth` file is missing from the venv. Re-run `python3 setup_environment.py` — it will add it.

**`ModuleNotFoundError: No module named 'pandas'` (or other packages)**
You are using the system `python3` instead of `.venv/bin/python3`. Always use the venv Python.

**A Stata package is missing (`reghdfe`, `estout`, etc.)**
Re-run `python3 setup_environment.py` to reinstall Stata packages.

**Script exits with a non-zero code and no clear error**
Run the individual script directly to see full output:
```bash
.venv/bin/python3 Analysis/tables/<script>.py
```
