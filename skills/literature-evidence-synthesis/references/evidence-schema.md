# Universal evidence schema

## Relationship model

```text
source 1 ── 0..n study units
source 1 ── 0..n claims
study  1 ── 0..n claims
source/study ── 0..n appraisal domains
```

A source is a paper or document. A study is an empirical or analytical unit inside that source. Non-empirical sources may have claims and appraisals without a study row.

## `sources.csv`

| Field | Meaning |
|---|---|
| `source_id` | Stable local identifier such as `S0001` |
| `title`, `authors`, `first_author`, `year`, `venue`, `doi` | Verified bibliographic record |
| `source_file` | Local PDF path relative to the corpus root |
| `document_type` | Original research, review, methods, protocol, theoretical, guideline, report, and so on |
| `research_domain` | User-defined discipline or topic |
| `language` | Main document language |
| `scope_or_abstract` | Short source-level scope |
| `record_status` | `verified`, `partial`, or `full_text_unavailable` |
| `notes` | Retraction, correction, supplement, or access notes |

## `studies.csv`

One row represents an experiment, cohort, survey, dataset evaluation, case, qualitative sample, or other analysis unit.

| Field | Meaning |
|---|---|
| `study_id` | Stable identifier such as `ST0001` |
| `source_id` | Parent source |
| `study_label` | “Experiment 2”, “Validation cohort”, or a local label |
| `study_design` | Design selected from `design-modules.md` |
| `objective_or_question` | Study-level objective |
| `setting` | Laboratory, clinic, field, online, archival, simulation, and so on |
| `population_or_material` | Participants, organisms, specimens, texts, devices, datasets, or cases |
| `intervention_exposure_or_input` | Treatment, exposure, predictor, model input, or not applicable |
| `comparator_or_context` | Control, reference, baseline, social context, or not applicable |
| `outcomes_or_themes` | Outcomes, endpoints, themes, or performance targets |
| `data_source` | Recruitment, database, instrument, corpus, benchmark, or archive |
| `timeframe` | Follow-up, exposure, observation, publication, or analysis window |
| `unit_of_analysis` | Independent unit used by the analysis |
| `sample_or_corpus_size` | Participants, clusters, cases, records, documents, images, or datasets |
| `analysis_method` | Statistical, qualitative, computational, or argumentative method |
| `key_finding` | Bounded study-level summary |
| `limitations` | Main design and transferability limits |
| `study_status` | `verified`, `partial`, or `not_applicable` |

Use `not_applicable`, not zero, when a field genuinely does not apply.

## `claims.csv`

One row represents one auditable assertion.

| Field | Meaning |
|---|---|
| `claim_id` | Stable identifier such as `C000001` |
| `source_id`, `study_id` | Provenance; `study_id` may be blank for source-level arguments |
| `claim_nature` | Controlled term below |
| `claim_text` | Concise, contextualized assertion |
| `value_original` | Value exactly as reported |
| `value_normalized` | Optional converted or harmonized value |
| `unit_original` | Original unit |
| `comparison_context` | Population, contrast, model, timeframe, and direction |
| `section`, `table_or_figure` | Structural locator |
| `pdf_page` | PDF-reader page number |
| `locator_phrase` | Short, non-substitutive phrase used to relocate evidence |
| `verification_status` | `candidate`, `verified`, `conflict`, `unsupported`, `not_applicable` |
| `extraction_method` | Manual, AI-assisted, table extraction, OCR, or combined |
| `notes` | Conversion, ambiguity, supplement, or conflict details |

Controlled `claim_nature` values:

- `quantitative_result`
- `statistical_result`
- `qualitative_finding`
- `model_performance`
- `method_description`
- `conceptual_proposition`
- `causal_claim`
- `association_claim`
- `recommendation`
- `limitation`
- `background`

## `appraisals.csv`

Use one row per appraisal domain.

| Field | Meaning |
|---|---|
| `appraisal_id` | Stable identifier |
| `source_id`, `study_id` | Appraisal target |
| `tool_or_framework` | Named tool, local framework, or `custom` |
| `domain` | Selection, measurement, confounding, analysis, reflexivity, leakage, synthesis, and so on |
| `judgment` | Tool-appropriate label; do not force a universal numeric scale |
| `supporting_reason` | Evidence-based rationale |
| `pdf_page`, `locator_phrase` | Primary supporting location when applicable |
| `appraisal_status` | `not_started`, `partial`, `complete`, `not_applicable` |
| `notes` | Reviewer assumptions or unresolved questions |

Do not convert unlike appraisal judgments into a pooled score.
