# Trustworthy deep-learning MPM review — reproducibility package

This public repository accompanies the Computers & Geosciences scientific review article:

**Trustworthy Deep Learning for Mineral Prospectivity Mapping under Data Scarcity: A Systematic Critical Review of Label Design, Spatial Validation, Uncertainty, and Transferability**

Author: **Amirmohammad Abhary**  
ORCID: **0009-0003-7823-5117**  
Contact: **amirabhary@ut.ac.ir**

## Purpose

This repository provides the open-source Python code, derived review-evidence tables, test fixtures, expected quick-test output, dependency records, and documentation needed to audit the quantitative summaries and reproduce the programmatic figures/tables reported in the manuscript. No proprietary software is required.

## Repository structure

- `src/generate_figures_and_tables.py` — reproduces the programmatic figures, submitted tables, and Supplementary Data S1–S6.
- `data/` — derived evidence matrices, quality scores, search/exclusion/reference registers, and review-accounting tables used by the workflow.
- `tests/quick_test.py` — lightweight reproducibility test of the core manuscript counts.
- `tests/expected_quick_test_summary.csv` — expected quick-test output.
- `tests/fixture_quality_first3.csv` — compact test fixture.
- `docs/USER_GUIDE.md` — inputs, outputs, dependencies, execution and troubleshooting.
- `examples/QUICK_TUTORIAL.md` — short worked example.
- `requirements.txt` / `environment.yml` — pip and conda dependency records.
- `CITATION.cff` — citation metadata.
- `LICENSE` — MIT license for the shared code and documentation.

Generated figures and tables are written to `outputs/` when the workflow is run. The source data required for their generation are included as individual files in this public repository; binary figure files do not need to be downloaded in advance.

## Requirements

Tested with **Python 3.11** on a standard CPU-only workstation. A GPU is not required.

### pip

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### conda

```bash
conda env create -f environment.yml
conda activate trustworthy-dl-mpm-review
```

## Quick test

Run from the repository root:

```bash
python tests/quick_test.py
```

Expected terminal message:

```text
Quick test passed: core manuscript counts match the expected summary and outputs/tables/quick_test_summary.csv was written.
```

The test independently checks the integrated corpus size and the manuscript's key reliability counts (spatial validation, spatial independence, label validity, calibration/uncertainty and reproducibility) against `tests/expected_quick_test_summary.csv`.

## Full reproduction

Run:

```bash
python src/generate_figures_and_tables.py
```

The script writes programmatic figures to `outputs/figures/`, manuscript tables to `outputs/tables/`, and Supplementary Data S1–S6 to `outputs/supplementary/`.

## Data and redistribution limits

The repository contains derived review evidence, bibliographic metadata, quality-appraisal tables, and compact fixtures. It does **not** redistribute restricted publisher PDFs, proprietary third-party datasets, or confidential source documents. Source documents remain subject to their original rights and access conditions.

## License

The source code and repository documentation are released under the MIT License. Bibliographic metadata and third-party source information remain subject to their original rights.

## Repository URL

https://github.com/abhary/trustworthy-dl-mpm-review
