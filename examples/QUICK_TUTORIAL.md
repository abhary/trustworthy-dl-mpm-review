# Quick tutorial

This example verifies the core review counts before running the full figure/table workflow.

1. Create the environment using either `requirements.txt` or `environment.yml`.
2. From the repository root, run:

```bash
python tests/quick_test.py
```

3. Open `outputs/tables/quick_test_summary.csv`. The expected values are:

- integrated studies: 32
- secure-core studies: 25
- strong spatial validation in the integrated set: 4
- no demonstrated spatial independence in the integrated set: 25
- strong negative/unlabeled-sample validity: 6
- strong calibration/uncertainty/stability: 9
- strong reproducibility: 8

4. Reproduce the programmatic figures and tables:

```bash
python src/generate_figures_and_tables.py
```

5. Compare the regenerated files under `outputs/` with the reference outputs committed in the repository.
