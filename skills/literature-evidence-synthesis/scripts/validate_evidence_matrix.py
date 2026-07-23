#!/usr/bin/env python3
"""Validate linked source, study, claim, and appraisal matrices."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from pypdf import PdfReader


SOURCE_REQUIRED = {
    "source_id",
    "title",
    "authors",
    "year",
    "venue",
    "source_file",
    "document_type",
    "research_domain",
    "record_status",
}
STUDY_REQUIRED = {
    "study_id",
    "source_id",
    "study_design",
    "objective_or_question",
    "population_or_material",
    "outcomes_or_themes",
    "unit_of_analysis",
    "sample_or_corpus_size",
    "analysis_method",
    "key_finding",
    "study_status",
}
CLAIM_REQUIRED = {
    "claim_id",
    "source_id",
    "study_id",
    "claim_nature",
    "claim_text",
    "value_original",
    "pdf_page",
    "locator_phrase",
    "verification_status",
}
APPRAISAL_REQUIRED = {
    "appraisal_id",
    "source_id",
    "study_id",
    "tool_or_framework",
    "domain",
    "judgment",
    "supporting_reason",
    "appraisal_status",
}

VALID_RECORD_STATUS = {"verified", "partial", "full_text_unavailable"}
VALID_STUDY_STATUS = {"verified", "partial", "not_applicable"}
VALID_CLAIM_STATUS = {
    "candidate",
    "verified",
    "conflict",
    "unsupported",
    "not_applicable",
}
VALID_APPRAISAL_STATUS = {"not_started", "partial", "complete", "not_applicable"}
NUMERIC_CLAIM_NATURES = {
    "quantitative_result",
    "statistical_result",
    "model_performance",
}


def read_csv(path: Path) -> tuple[list[dict[str, str]], set[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
        return rows, set(reader.fieldnames or [])


def resolve_source(value: str, pdf_root: Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else pdf_root / path


def duplicate_or_blank(values: list[str], label: str, errors: list[str]) -> None:
    for value, count in Counter(values).items():
        if not value or count > 1:
            errors.append(f"invalid or duplicate {label}: {value!r} count={count}")


def validate_page(
    row_id: str,
    source_id: str,
    page_value: str,
    locator: str,
    page_counts: dict[str, int],
    errors: list[str],
) -> None:
    try:
        page = int(page_value)
    except ValueError:
        errors.append(f"{row_id}: invalid pdf_page")
        return
    if page < 1:
        errors.append(f"{row_id}: pdf_page must be >= 1")
    maximum = page_counts.get(source_id)
    if maximum is None:
        errors.append(f"{row_id}: cannot verify page without readable PDF")
    elif page > maximum:
        errors.append(f"{row_id}: pdf_page {page} exceeds page count {maximum}")
    if not locator:
        errors.append(f"{row_id}: verified record lacks locator_phrase")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", required=True, type=Path)
    parser.add_argument("--studies", required=True, type=Path)
    parser.add_argument("--claims", required=True, type=Path)
    parser.add_argument("--appraisals", required=True, type=Path)
    parser.add_argument("--pdf-root", required=True, type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    sources, source_fields = read_csv(args.sources)
    studies, study_fields = read_csv(args.studies)
    claims, claim_fields = read_csv(args.claims)
    appraisals, appraisal_fields = read_csv(args.appraisals)

    for filename, required, actual in [
        ("sources.csv", SOURCE_REQUIRED, source_fields),
        ("studies.csv", STUDY_REQUIRED, study_fields),
        ("claims.csv", CLAIM_REQUIRED, claim_fields),
        ("appraisals.csv", APPRAISAL_REQUIRED, appraisal_fields),
    ]:
        missing = sorted(required - actual)
        if missing:
            errors.append(f"{filename} missing fields: {missing}")

    source_ids = [row.get("source_id", "") for row in sources]
    study_ids = [row.get("study_id", "") for row in studies]
    claim_ids = [row.get("claim_id", "") for row in claims]
    appraisal_ids = [row.get("appraisal_id", "") for row in appraisals]
    duplicate_or_blank(source_ids, "source_id", errors)
    duplicate_or_blank(study_ids, "study_id", errors)
    duplicate_or_blank(claim_ids, "claim_id", errors)
    duplicate_or_blank(appraisal_ids, "appraisal_id", errors)

    source_map = {row.get("source_id", ""): row for row in sources}
    study_map = {row.get("study_id", ""): row for row in studies}
    page_counts: dict[str, int] = {}

    for row in sources:
        source_id = row.get("source_id", "")
        status = row.get("record_status", "")
        if status not in VALID_RECORD_STATUS:
            errors.append(f"{source_id}: invalid record_status {status!r}")
        if status == "full_text_unavailable":
            continue
        source = resolve_source(row.get("source_file", ""), args.pdf_root)
        if not source.is_file():
            errors.append(f"{source_id}: source PDF not found: {source}")
            continue
        try:
            page_counts[source_id] = len(PdfReader(str(source)).pages)
        except Exception as exc:
            errors.append(f"{source_id}: cannot read PDF: {exc}")
        if not row.get("doi"):
            warnings.append(f"{source_id}: DOI missing or not applicable")

    for row in studies:
        study_id = row.get("study_id", "")
        source_id = row.get("source_id", "")
        if source_id not in source_map:
            errors.append(f"{study_id}: unknown source_id {source_id!r}")
        status = row.get("study_status", "")
        if status not in VALID_STUDY_STATUS:
            errors.append(f"{study_id}: invalid study_status {status!r}")

    verified_claims = 0
    for row in claims:
        claim_id = row.get("claim_id", "")
        source_id = row.get("source_id", "")
        study_id = row.get("study_id", "")
        status = row.get("verification_status", "")
        if source_id not in source_map:
            errors.append(f"{claim_id}: unknown source_id {source_id!r}")
            continue
        if study_id and study_id not in study_map:
            errors.append(f"{claim_id}: unknown study_id {study_id!r}")
        elif study_id and study_map[study_id].get("source_id") != source_id:
            errors.append(f"{claim_id}: study_id belongs to a different source")
        if status not in VALID_CLAIM_STATUS:
            errors.append(f"{claim_id}: invalid verification_status {status!r}")
        if not row.get("claim_text"):
            errors.append(f"{claim_id}: claim_text is empty")
        if (
            row.get("claim_nature") in NUMERIC_CLAIM_NATURES
            and not row.get("value_original")
        ):
            errors.append(f"{claim_id}: numerical claim lacks value_original")
        if status == "verified":
            verified_claims += 1
            validate_page(
                claim_id,
                source_id,
                row.get("pdf_page", ""),
                row.get("locator_phrase", ""),
                page_counts,
                errors,
            )
        elif status == "candidate":
            warnings.append(f"{claim_id}: candidate claim is not ready for synthesis")

    for row in appraisals:
        appraisal_id = row.get("appraisal_id", "")
        source_id = row.get("source_id", "")
        study_id = row.get("study_id", "")
        status = row.get("appraisal_status", "")
        if source_id not in source_map:
            errors.append(f"{appraisal_id}: unknown source_id {source_id!r}")
            continue
        if study_id and study_id not in study_map:
            errors.append(f"{appraisal_id}: unknown study_id {study_id!r}")
        elif study_id and study_map[study_id].get("source_id") != source_id:
            errors.append(f"{appraisal_id}: study_id belongs to a different source")
        if status not in VALID_APPRAISAL_STATUS:
            errors.append(f"{appraisal_id}: invalid appraisal_status {status!r}")
        if status == "complete" and not row.get("supporting_reason"):
            errors.append(f"{appraisal_id}: completed appraisal lacks supporting_reason")
        if row.get("pdf_page"):
            validate_page(
                appraisal_id,
                source_id,
                row.get("pdf_page", ""),
                row.get("locator_phrase", ""),
                page_counts,
                errors,
            )

    result = {
        "sources": len(sources),
        "studies": len(studies),
        "claims": len(claims),
        "verified_claims": verified_claims,
        "appraisals": len(appraisals),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
