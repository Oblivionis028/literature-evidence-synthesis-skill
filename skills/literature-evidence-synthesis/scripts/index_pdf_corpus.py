#!/usr/bin/env python3
"""Create a page-addressable corpus and source inventory from a PDF directory."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_folder", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--weak-text-threshold", type=int, default=80)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.pdf_folder.resolve()
    output = args.output.resolve()
    if not root.is_dir():
        raise SystemExit(f"PDF folder not found: {root}")

    corpus_dir = output / "corpus"
    corpus_dir.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(
        (path for path in root.rglob("*.pdf") if path.is_file()),
        key=lambda path: str(path.relative_to(root)).lower(),
    )
    inventory: list[dict[str, object]] = []

    for number, pdf_path in enumerate(pdfs, start=1):
        source_id = f"S{number:04d}"
        page_records: list[dict[str, object]] = []
        errors: list[str] = []
        try:
            reader = PdfReader(str(pdf_path))
            for page_number, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text() or ""
                except Exception as exc:
                    text = ""
                    errors.append(f"page {page_number}: {exc}")
                page_records.append(
                    {"source_id": source_id, "page": page_number, "text": text}
                )
        except Exception as exc:
            errors.append(str(exc))

        text_chars = sum(len(str(row["text"])) for row in page_records)
        page_count = len(page_records)
        mean_chars = text_chars / page_count if page_count else 0
        if errors and not page_records:
            status = "read_error"
        elif mean_chars < args.weak_text_threshold:
            status = "ocr_required"
        else:
            status = "text_extracted"

        corpus_path = corpus_dir / f"{source_id}.jsonl"
        with corpus_path.open("w", encoding="utf-8", newline="\n") as handle:
            for record in page_records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")

        inventory.append(
            {
                "source_id": source_id,
                "filename": pdf_path.name,
                "relative_path": str(pdf_path.relative_to(root)),
                "page_count": page_count,
                "sha256": sha256(pdf_path),
                "text_chars": text_chars,
                "extraction_status": status,
                "errors": " | ".join(errors),
            }
        )

    fields = [
        "source_id",
        "filename",
        "relative_path",
        "page_count",
        "sha256",
        "text_chars",
        "extraction_status",
        "errors",
    ]
    output.mkdir(parents=True, exist_ok=True)
    with (output / "inventory.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(inventory)

    summary = {
        "pdf_root": str(root),
        "source_count": len(inventory),
        "page_count": sum(int(row["page_count"]) for row in inventory),
        "ocr_required": sum(
            row["extraction_status"] == "ocr_required" for row in inventory
        ),
        "read_errors": sum(
            row["extraction_status"] == "read_error" for row in inventory
        ),
    }
    (output / "corpus_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if not summary["read_errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
