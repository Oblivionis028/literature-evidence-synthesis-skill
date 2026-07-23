# Examples

The examples demonstrate the workflow without redistributing copyrighted articles.

## Mixed literature demo

`mixed-literature-demo/` contains three short synthetic papers created only for testing:

1. a controlled experiment;
2. a qualitative interview study;
3. a machine-learning benchmark.

The reported values, themes, pages, and limitations are fictional. They are internally consistent so users can test page-level verification and validation safely.

The folder also includes a completed `evidence-matrix.xlsx`, the four underlying CSV tables, and an example cross-paper synthesis report.

Run from the repository root:

```bash
python skills/literature-evidence-synthesis/scripts/validate_evidence_matrix.py \
  --sources examples/mixed-literature-demo/sources.csv \
  --studies examples/mixed-literature-demo/studies.csv \
  --claims examples/mixed-literature-demo/claims.csv \
  --appraisals examples/mixed-literature-demo/appraisals.csv \
  --pdf-root examples/mixed-literature-demo
```

Expected result:

```text
3 sources
3 study units
8 verified claims
5 appraisal records
0 validation errors
```

Three DOI warnings are expected because these synthetic demonstration papers intentionally have no DOI.

These synthetic papers are released under CC0 for demonstration and testing.
