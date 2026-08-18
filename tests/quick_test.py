from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

required_files = {
    "integrated": DATA / "standardized_integrated_evidence_matrix.csv",
    "secure_quality": DATA / "adjudicated_consensus_quality.csv",
    "sensitivity_quality": DATA / "sensitivity_consensus_scores.csv",
    "domain_profile": DATA / "domain_profile.csv",
    "fixture": ROOT / "tests" / "fixture_quality_first3.csv",
    "expected": ROOT / "tests" / "expected_quick_test_summary.csv",
}
missing = [str(path) for path in required_files.values() if not path.exists()]
if missing:
    raise FileNotFoundError("Missing required files: " + "; ".join(missing))

integrated = pd.read_csv(required_files["integrated"])
secure = pd.read_csv(required_files["secure_quality"])
sensitivity = pd.read_csv(required_files["sensitivity_quality"])
domain = pd.read_csv(required_files["domain_profile"])
fixture = pd.read_csv(required_files["fixture"])
expected = pd.read_csv(required_files["expected"])

for name, frame in [("integrated", integrated), ("secure_quality", secure), ("sensitivity_quality", sensitivity), ("domain_profile", domain), ("fixture", fixture)]:
    if frame.empty:
        raise ValueError(f"{name} is empty")

q_cols = [f"Q{i}" for i in range(1, 13)]
for frame_name, frame in [("secure_quality", secure), ("sensitivity_quality", sensitivity)]:
    missing_q = [c for c in q_cols if c not in frame.columns]
    if missing_q:
        raise ValueError(f"{frame_name} lacks reliability columns: " + ", ".join(missing_q))

quality_all = pd.concat([secure[q_cols], sensitivity[q_cols]], ignore_index=True)
summary = pd.DataFrame({
    "metric": [
        "integrated_studies",
        "secure_core_studies",
        "reliability_domains",
        "fixture_rows",
        "strong_spatial_validation_integrated",
        "no_spatial_independence_integrated",
        "strong_label_validity_integrated",
        "strong_calibration_uq_integrated",
        "strong_reproducibility_integrated",
    ],
    "value": [
        len(integrated),
        len(secure),
        len(q_cols),
        len(fixture),
        int((quality_all["Q5"] == 2).sum()),
        int((quality_all["Q5"] == 0).sum()),
        int((quality_all["Q4"] == 2).sum()),
        int((quality_all["Q10"] == 2).sum()),
        int((quality_all["Q12"] == 2).sum()),
    ],
})
summary.to_csv(OUT / "quick_test_summary.csv", index=False)

actual = summary.sort_values("metric").reset_index(drop=True)
expected = expected.sort_values("metric").reset_index(drop=True)
if not actual.equals(expected):
    comparison = actual.merge(expected, on="metric", how="outer", suffixes=("_actual", "_expected"))
    raise AssertionError("Quick-test summary differs from expected values:\n" + comparison.to_string(index=False))

print("Quick test passed: core manuscript counts match the expected summary and outputs/tables/quick_test_summary.csv was written.")
