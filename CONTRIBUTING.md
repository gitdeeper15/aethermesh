# Contributing to AetherProof

**AetherProof: Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems**

---

## Status

This project is a **formal architecture paper** (`v1.0.0`). The framework is specified through six formal definitions, ten propositions, and six architectural pillars. No implementation has been built and no empirical evaluation has been performed.

Contributions at this stage are welcome in:

- **Formalization**: Critical review of Definitions 1–6 and Propositions P1–P10.
- **Architecture**: Proposals for the six pillars (three-layer specification, CSR, PDG, remediation, integration, human review).
- **Open questions**: Proposals addressing Q1–Q50.
- **Documentation**: Clarifying the manuscript, adding examples, or improving figure quality.

**Not accepted at this stage:**

- Empirical claims presented as findings (no empirical work has been performed).
- New architectural commitments that bypass the sequential formalization discipline.
- Changes to the formal definitions or propositions without a documented rationale.

For extensions, open an issue first to discuss scope.

---

## Reporting Issues

Open an issue with:

- A one-sentence description.
- The affected file (e.g., `docs/01_specification_language.md`).
- A minimal reproduction or screenshot.
- Expected vs. actual behavior.

---

## Submitting Changes

```bash
git checkout -b feature/short-description
# make changes
git commit -m "feat: short description"
git push origin feature/short-description
```

Then open a pull request. Each PR should address one concern.

---

Code Standards

Language Standard
Python PEP 8, black (88 chars), isort, flake8
Markdown markdownlint (MD013 disabled)
YAML yamllint

Reproducibility: every documentation change must preserve the sequential formalization discipline and the negative commitments.

---

Data Provenance

All figures and diagrams are original to this project. No third-party imagery was used. The architectural diagrams were constructed from the formal description in the manuscript.

---

Review Process

· All changes are reviewed by the maintainer (Samir Baladi).
· Changes to the manuscript, figures, or formal definitions require explicit documentation in CHANGELOG.md with rationale.
· Adoption of any new formal construct requires an explicit version increment.

---

Contact

· Email: gitdeeper@gmail.com
· ORCID: https://orcid.org/0009-0003-8903-0029
· Zenodo DOI: https://doi.org/10.5281/zenodo.24013124
· Website: https://aether-proof.netlify.app

---

Thank you for helping improve the formal analysis of autonomous formal verification and invariant synthesis.
