# Contributing

Thank you for helping improve Literature Evidence Synthesis.

## Good first contributions

- report a reproducible bug;
- improve a design-specific extraction checklist;
- add a new study-design module;
- contribute a lawful, redistributable demonstration corpus;
- improve validation messages or test coverage;
- document a real use case without uploading restricted full text.

## Before opening an issue

1. Search existing issues and discussions.
2. Confirm the problem occurs with the latest release.
3. Remove confidential information, copyrighted PDFs, API keys, and personal data.
4. Prepare the smallest reproducible example.

## Proposing a study-design module

Describe:

- the research design and disciplines that use it;
- the minimum extraction fields;
- the main bias or quality domains;
- which existing module is closest and why it is insufficient;
- at least one openly accessible methodological reference;
- a synthetic or openly licensed test case.

Do not force incompatible research traditions into a universal numeric quality score.

## Pull requests

1. Keep the core invariant intact: verified substantive claims require a readable source, valid PDF page, and relocation phrase.
2. Keep `SKILL.md` concise and route detailed material into `references/`.
3. Test changed scripts on a small corpus.
4. Update relevant examples and documentation.
5. Do not add restricted article PDFs.
6. Explain the scientific or workflow impact of the change.

## Style

- Use clear, evidence-bounded language.
- Separate source facts, evidence, inference, recommendation, and uncertainty.
- Preserve original values and units before adding normalized values.
- Use lowercase kebab-case filenames where practical.
- Keep templates machine-readable.

## Questions

Use GitHub Discussions for usage questions and early ideas. Use Issues for reproducible bugs and scoped feature requests.
