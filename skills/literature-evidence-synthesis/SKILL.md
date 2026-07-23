---
name: literature-evidence-synthesis
description: Build auditable literature reviews and evidence syntheses from local PDFs or lawfully obtained full texts across research fields. Use when Codex must batch-read experimental, observational, clinical, qualitative, mixed-methods, computational or machine-learning, methods, review, meta-analysis, case, theoretical, conceptual, policy, or commentary papers; separate papers from their study or analysis units; verify numerical, statistical, qualitative, methodological, and conceptual claims against exact PDF pages; create linked evidence and appraisal matrices; or generate a cross-paper report with explicit provenance, quality boundaries, and uncertainty.
---

# Literature Evidence Synthesis

Turn a mixed paper collection into four linked evidence layers:

1. one source record per paper or document;
2. one study record per experiment, cohort, dataset, case, or analysis unit;
3. one page-verified record per substantive claim;
4. one design-aware appraisal record per quality or bias domain.

Never let an AI summary substitute for claim-level source verification.

## Required workflow

### 1. Define scope and evidence boundary

- Record the corpus folder, exact document count, languages, date limits, and inclusion logic.
- Separate available full text from citation-only records.
- State whether the corpus comes from a systematic search, a scoped search, or a convenience collection.
- Do not claim systematic-review completeness without a reproducible search and screening record.

### 2. Build a page-addressable corpus

Run:

```bash
python scripts/index_pdf_corpus.py <pdf-folder> --output <work-dir>/corpus
```

Preserve SHA-256, page count, page text, extraction status, and OCR warnings. Mark weak scans for OCR; never treat failed extraction as evidence of absence.

### 3. Classify each source and select a design module

Read [references/design-modules.md](references/design-modules.md).

- Identify the document type separately from the study design.
- Split multi-study papers into separate study rows.
- Allow non-empirical papers to have no study row; their conceptual claims still require page verification.
- Use only design-specific fields and appraisal criteria that apply.

### 4. Initialize the four evidence layers

Read [references/evidence-schema.md](references/evidence-schema.md), then run:

```bash
python scripts/init_evidence_matrix.py --output <work-dir>/evidence
```

This creates:

- `sources.csv`
- `studies.csv`
- `claims.csv`
- `appraisals.csv`

Keep common fields in the core tables. Put design-specific details in study rows or appraisal domains instead of inventing a new universal score.

### 5. Extract candidates, then verify

AI extraction creates candidates only.

For every numerical, statistical, qualitative, methodological, or conceptual conclusion:

1. return to the local PDF;
2. locate the exact PDF-reader page;
3. capture the claim with its population, comparison, timeframe, and qualifiers;
4. preserve original values, units, uncertainty, and direction;
5. store a short locator phrase plus section/table/figure identifier;
6. set `verification_status=verified` only when the PDF supports the claim.

Read [references/verification-protocol.md](references/verification-protocol.md).

Never infer a precise value or conclusion from a title, search snippet, citation context, AI summary, or secondary source.

### 6. Appraise with a design-appropriate framework

- Select appraisal domains based on the design module.
- Record the framework name and version when known.
- Store the supporting reason, not only a score or label.
- Mark unassessed domains as `not_started`, not low risk.
- Do not compare scores produced by incompatible appraisal tools.

### 7. Validate before synthesis

Run:

```bash
python scripts/validate_evidence_matrix.py \
  --sources <work-dir>/evidence/sources.csv \
  --studies <work-dir>/evidence/studies.csv \
  --claims <work-dir>/evidence/claims.csv \
  --appraisals <work-dir>/evidence/appraisals.csv \
  --pdf-root <pdf-folder>
```

Treat every error as a release blocker. Resolve or disclose every warning.

### 8. Synthesize at the right level

Read [references/synthesis-guidelines.md](references/synthesis-guidelines.md).

- Organize by research question, construct, population or material, intervention or input, comparator or context, outcome or theme, and study design.
- Keep source-level, study-level, and claim-level counts distinct.
- Consider direction, magnitude, precision, directness, consistency, bias, and transferability.
- Do not statistically pool incompatible studies.
- Do not double-count primary studies that also appear inside included reviews.
- Keep empirical findings separate from interpretations, recommendations, and theoretical propositions.

### 9. Generate deliverables

Produce:

- a PDF inventory and OCR exception list;
- linked source, study, claim, and appraisal matrices;
- a cross-paper synthesis report;
- a conflict and unverified-claim register;
- an evidence-gap and future-research section.

When available, use the PDF skill for source inspection, the spreadsheet skill for matrices, and the document skill for the report. Render and inspect final artifacts before delivery.

## Core invariants

- A verified claim always has a readable source, valid PDF page, and locator phrase.
- Original and normalized values remain distinguishable.
- Independent units remain separate from observations, repeated measures, frames, or technical replicates.
- Reviews never substitute for verification of a primary study when the primary result is asserted.
- Statistical significance never substitutes for effect magnitude, uncertainty, or practical relevance.
- Qualitative themes retain context, participant voice boundaries, and negative or divergent cases.
- Computational results retain dataset, split, metric definition, leakage checks, and external-validation status.
- Conceptual papers are synthesized as arguments or propositions, not empirical effect estimates.
- Correlation, prediction, mediation, mechanism, and causation remain distinct.

## Minimum quality gate

Do not finalize until:

- every source row has a local file or explicit unavailable status;
- every verified claim has a valid PDF page and locator;
- every study references an existing source;
- every appraisal references an existing source and, when supplied, an existing study;
- identifiers are unique;
- no page exceeds the source PDF page count;
- candidate, conflicting, and unsupported claims are excluded from definitive conclusions;
- report wording is no stronger than the verified matrix supports;
- design limitations, missing full texts, and non-transferable findings are explicit.

## Bundled resources

- `scripts/index_pdf_corpus.py` — page-level corpus and inventory.
- `scripts/init_evidence_matrix.py` — blank four-layer evidence matrix.
- `scripts/validate_evidence_matrix.py` — deterministic integrity checks.
- `references/evidence-schema.md` — universal fields and controlled terms.
- `references/design-modules.md` — design-specific extraction and appraisal routing.
- `references/verification-protocol.md` — page-level verification procedure.
- `references/synthesis-guidelines.md` — cross-study reasoning rules.
- `assets/*-template.csv` — reusable matrix templates.
- `assets/evidence-pipeline.svg` and `.png` — editable and preview-ready workflow figures.
