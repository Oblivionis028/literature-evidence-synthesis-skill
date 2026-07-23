# Page-level verification protocol

## Verification unit

Verify one claim at a time. Split sentences containing multiple values, comparisons, outcomes, or inferential steps into separate claim rows.

## Procedure

1. Open the local full text, not a search snippet.
2. Confirm the source identity using title, author, year, and DOI when available.
3. Use the PDF-reader page number; also record printed page, section, table, figure, or supplement when useful.
4. Capture a short locator phrase, not a long copyrighted passage.
5. Preserve the original value, unit, precision, sign, denominator, uncertainty, and comparison.
6. Add the population/material, setting, timeframe, model, and qualifiers needed to interpret the claim.
7. Store conversions in `value_normalized`; never overwrite `value_original`.
8. Assign one status:
   - `verified`: the local source supports the claim;
   - `candidate`: extracted but not checked;
   - `conflict`: source locations disagree;
   - `unsupported`: the claimed conclusion is not supported;
   - `not_applicable`: no evidentiary claim is being made.

## Claim-specific checks

### Quantitative or statistical

- numerator, denominator, unit, scale, and time point;
- estimate versus raw observation;
- comparison, reference group, and direction;
- uncertainty interval, test, statistic, degrees of freedom, multiplicity adjustment, and model covariates when reported;
- missing-data population and analysis set.

### Qualitative

- participant/source context;
- whether the statement is a participant account, coded theme, author interpretation, or reviewer inference;
- deviant or negative cases;
- limits on transferability.

### Computational or model performance

- dataset and exact split;
- preprocessing and leakage boundary;
- metric definition and averaging convention;
- baseline, ablation, random seeds, uncertainty, and external validation;
- public benchmark result versus local/project performance.

### Methods

- intended use and operating conditions;
- comparator or reference method;
- accuracy, reliability, robustness, and failure conditions;
- software/version or protocol details needed for reproduction.

### Conceptual, policy, or theoretical

- whether the statement is a premise, definition, argument, prediction, recommendation, or empirical assertion;
- cited evidence versus the author's own reasoning;
- boundary conditions and acknowledged alternatives;
- normative statements kept separate from empirical claims.

### Review or meta-analysis

- whether the number is a source count, study count, participant count, effect estimate, or subgroup result;
- model, effect measure, heterogeneity, dependency handling, and sensitivity analysis;
- primary-study overlap across reviews.

## Stop conditions

Do not mark a claim verified when:

- only a citation, abstract, or secondary summary is available;
- OCR is unreliable around the evidence;
- the source page cannot be determined;
- a table or figure cannot be interpreted with its caption and denominator;
- the claim merges incompatible populations, studies, outcomes, or time points;
- the study unit or comparison remains ambiguous.

Record the ambiguity instead of resolving it by guess.
