# Does assurance improve the quality and value relevance of non-GAAP earnings?

**Nicholas J. Hallman** (University of Texas at Austin) · **Jaime J. Schmidt** (University of Texas at Austin) · **Anne M. Thompson** (University of Illinois at Urbana-Champaign)

---

## Abstract

Standard-setters and regulators worldwide have expressed concern about the quality and consistency of non-GAAP reporting. To address these concerns, stakeholder groups have encouraged standard-setters to require assurance over, and reporting of, non-GAAP earnings in the financial statements. We test whether non-GAAP earnings reported within the scope of the audited financial statements (i.e., on the income statement or within the footnotes) are more value relevant and higher quality than non-GAAP earnings reported elsewhere in the annual report. Among a sample of U.K. companies, we find that non-GAAP earnings are more value relevant and higher quality when they are audited and reported within the financial statements. We find no difference in value relevance or quality between non-GAAP earnings that are reported on the income statement versus disclosed in the footnotes. However, non-GAAP earnings are less value relevant when reported as a column on the income statement rather than in rows. Our results are consistent with stakeholders' suggestions to require assurance of non-GAAP reporting and provide evidence on the formatting and placement of non-GAAP earnings within the financial statements.

---

## Repository Structure

```
├── Analysis/
│   ├── prepare_data.py           # Builds df4m_w.csv from raw inputs (requires raw data; see below)
│   ├── run_all.py                # Orchestrator: runs all table scripts
│   ├── llm_extraction_prompt.md  # Full LLM prompt used to extract non-GAAP data (Appendix B, Section IX)
│   ├── Data/
│   │   └── df4m_w.csv            # Final analysis dataset (firm-year-measure)
│   ├── tables/                   # One script per table
│   └── shared/                   # Shared utilities (paths, Stata setup, LaTeX formatting)
├── LaTeX/
│   ├── manuscript.tex         # Main manuscript
│   ├── preamble.sty           # LaTeX formatting
│   ├── variables.sty          # Variable macros
│   ├── references.bib         # Bibliography
│   ├── Tables/                # Generated LaTeX table files (\input-ed by manuscript)
│   └── Figures/               # Figures referenced by manuscript
├── setup_environment.py       # One-time setup: venv + Python packages + Stata packages
└── AISETUP.md                 # Instructions for AI agents
```

---

## Data

### Final analysis dataset

`Analysis/Data/df4m_w.csv` is included in this repository. It is a firm-year-measure panel of UK-listed companies. All tables can be reproduced from this file alone — no external data access is required to run the analysis scripts.

### Raw data sources (required only to re-run `prepare_data.py`)

The raw inputs used to construct `df4m_w.csv` are not included in this repository:

| Source | Access |
|--------|--------|
| Compustat Global (fundamentals, prices, exchange rates, security linking) | [WRDS](https://wrds-www.wharton.upenn.edu/) subscription required |
| IBES Summary Statistics (EPS forecasts) | [WRDS](https://wrds-www.wharton.upenn.edu/) subscription required |
| Hand-collected data (firm IDs, non-GAAP measure classification, KAM audit procedures) | Available from the authors upon request |
| LLM-extracted data (non-GAAP measure presence, KAM indicators from annual reports) | Available from the authors upon request |

---

## Reproducing the Results

### Prerequisites

- **Python 3.9+**
  - macOS: [Homebrew](https://brew.sh) Python 3.12 is recommended (`brew install python@3.12`) and will be used automatically by the setup script if present.
  - Linux: the system `python3` is used.
- **Stata SE 17+** — must be installed separately (proprietary; not included).
  - macOS: expected at `/Applications/Stata/`
  - Linux: expected at `/usr/local/stata/`
- **LaTeX** — required only to compile `manuscript.tex` into a PDF; not needed to regenerate the table `.tex` files. [TeX Live](https://www.tug.org/texlive/) or [MacTeX](https://www.tug.org/mactex/) (macOS) are recommended. Compile with `pdflatex` + `biber` (two passes).

### Step 1: One-time environment setup

```bash
python3 setup_environment.py
```

This script:
1. Creates a `.venv/` virtual environment using Python 3.12 (Homebrew) on macOS, or the system `python3` on Linux.
2. Installs required Python packages into the venv: `pandas`, `numpy`, `openpyxl`, `stata_setup`.
3. Writes a `stata.pth` file into the venv so that Stata's `pystata` module is importable (critical on macOS).
4. Installs required Stata packages via pystata: `estout`, `ftools`, `reghdfe`, `outreg2`, `ppmlhdfe`.

The script is idempotent — safe to re-run; it skips steps that are already complete.

### Step 2: Generate all tables

```bash
.venv/bin/python3 Analysis/run_all.py --tables
```

This reads `Analysis/Data/df4m_w.csv` and writes all `.tex` table files to `LaTeX/Tables/`. Each script in `Analysis/tables/` corresponds to one table in the manuscript and can also be run individually, e.g.:

```bash
.venv/bin/python3 Analysis/tables/excess_adj_full_sample.py
```

### Re-running data preparation (optional)

If you have access to the raw data files, place them under `Analysis/Data/` following the structure in `prepare_data.py`, then:

```bash
.venv/bin/python3 Analysis/prepare_data.py
```

---

## How the Code Works

Each table script in `Analysis/tables/` follows the same pattern:

1. Imports `load_data()` from `shared/table_helpers.py`, which initializes Stata via `pystata` and loads `df4m_w.csv` into Stata memory.
2. Runs Stata estimation commands via `pystata`'s `stata.run()`.
3. Exports results to `LaTeX/Tables/<tablename>.tex` using `estout` (for regression tables) or direct file writes (for descriptive tables).

The `shared/` directory contains:
- `paths.py` — detects the repo root and defines `tables_dir`, `data_dir`, `figures_dir`.
- `stata_setup.py` — initializes `pystata` with the correct Stata path for macOS or Linux.
- `table_helpers.py` — convenience wrappers: `load_data()`, `tables_dir`, `format_latex()`.
- `latex_utils.py` — post-processing to clean up Stata's LaTeX output.

### Known non-fatal warning

When running scripts on macOS, Stata may print:

```
failed to set the specified Python version.
Unable to find the shared library.
```

This is Stata trying to configure its own embedded Python (the reverse direction) and can be ignored. The scripts complete successfully despite this message.

---

## Contact

Nicholas Hallman — nh9686@eid.utexas.edu
