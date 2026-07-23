# Security Policy

## Supported versions

Security fixes are applied to the latest published release.

## Reporting a vulnerability

Do not open a public Issue for:

- exposed credentials or secrets;
- path traversal or unsafe file handling;
- malicious PDF behavior;
- dependency vulnerabilities with a working exploit;
- private or sensitive research data exposure.

Use GitHub Private Vulnerability Reporting if it is enabled for this repository. Otherwise, contact the maintainer through the private contact method listed on the repository owner's GitHub profile.

Include:

- affected version;
- reproduction steps;
- expected and observed behavior;
- impact assessment;
- a minimal safe proof of concept.

Do not include real credentials, restricted PDFs, participant data, or confidential datasets.

## Scope note

The project processes untrusted PDFs. Users should inspect file provenance, keep dependencies updated, and run unfamiliar documents in an appropriately isolated environment.
