#!/usr/bin/env python3
"""Create a blank four-layer literature evidence matrix."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_FIELDS = [
    "source_id",
    "title",
    "authors",
    "first_author",
    "year",
    "venue",
    "doi",
    "source_file",
    "document_type",
    "research_domain",
    "language",
    "scope_or_abstract",
    "record_status",
    "notes",
]

STUDY_FIELDS = [
    "study_id",
    "source_id",
    "study_label",
    "study_design",
    "objective_or_question",
    "setting",
    "population_or_material",
    "intervention_exposure_or_input",
    "comparator_or_context",
    "outcomes_or_themes",
    "data_source",
    "timeframe",
    "unit_of_analysis",
    "sample_or_corpus_size",
    "analysis_method",
    "key_finding",
    "limitations",
    "study_status",
]

CLAIM_FIELDS = [
    "claim_id",
    "source_id",
    "study_id",
    "claim_nature",
    "claim_text",
    "value_original",
    "value_normalized",
    "unit_original",
    "comparison_context",
    "section",
    "table_or_figure",
    "pdf_page",
    "locator_phrase",
    "verification_status",
    "extraction_method",
    "notes",
]

APPRAISAL_FIELDS = [
    "appraisal_id",
    "source_id",
    "study_id",
    "tool_or_framework",
    "domain",
    "judgment",
    "supporting_reason",
    "pdf_page",
    "locator_phrase",
    "appraisal_status",
    "notes",
]


def write_blank(path: Path, fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle).writerow(fields)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    tables = {
        "sources.csv": SOURCE_FIELDS,
        "studies.csv": STUDY_FIELDS,
        "claims.csv": CLAIM_FIELDS,
        "appraisals.csv": APPRAISAL_FIELDS,
    }
    for filename, fields in tables.items():
        write_blank(args.output / filename, fields)
        print(f"Created {args.output / filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
