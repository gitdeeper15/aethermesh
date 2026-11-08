# Contributing to AetherMesh

**AetherMesh: Decentralized Peer-to-Peer Agent Synchronization and State CRDTs for Autonomous Multi-Agent Systems**

---

## Status

This project is a **formal architecture proposal with simulated evaluation** (`v1.0.0`). The framework is specified through four formal definitions, three theorems (stated with proof sketches, not machine-checked), six assumptions (A1–A6), and three architectural pillars.

**No implementation has been built. No real-world deployment has been evaluated.** All numerical results come from a simulated P2P testbed (10–500 nodes). The paper is not peer reviewed.

Contributions at this stage are welcome in:

- **Formalization**: Critical review of Definitions 1–4, Theorems 1–3, and Assumptions A1–A6.
- **Architecture**: Proposals for the three pillars (CRDTs, epidemic gossip, lightweight BFT).
- **Open questions**: Proposals addressing Q1–Q50 (Appendices B and C of the paper).
- **Threat analysis**: Extensions to the 15-threat taxonomy (T1–T15) across six classes.
- **Documentation**: Clarifying the manuscript, adding examples, or improving figure quality.
- **Simulation**: Reproducing or extending the simulated evaluation (see *Reproducibility* below).

**Not accepted at this stage:**

- Empirical claims presented as findings (no real-world deployment has been evaluated).
- New architectural commitments that bypass the sequential formalization discipline.
- Changes to the formal definitions, theorems, or assumptions without a documented rationale.
- Claims that the simulator source, seeds, or raw traces are included in the record — they are not.

For extensions, open an issue first to discuss scope.

---

## Reporting Issues

Open an issue with:

- A one-sentence description.
- The affected file (e.g., `README.md`, `docs/figures/Fig1_Tripartite_Architecture.png`, or a section reference like "Section 3.3.4").
- A minimal reproduction or screenshot.
- Expected vs. actual behavior.
- For scientific claims: cite the specific definition, theorem, or assumption affected.

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

Standards

Language Standard
Markdown markdownlint (MD013 disabled)
YAML yamllint
JSON valid JSON (verify with python3 -m json.tool)
BibTeX / CITATION.cff valid CFF 1.2.0

No Python code standards apply — this project claims no implementation. If a future version adds a reference implementation, Python standards (PEP 8, black, isort, flake8) will apply to that version.

---

Scientific Integrity Requirements

Because this is a research record with a published DOI, contributions must preserve:

1. Evidentiary status. No claim may be strengthened beyond what the manuscript supports. Simulated results must never be described as measurements of a deployed system. Theorems must remain labeled as proof sketches (not machine-checked).
2. Assumption transparency. Any theorem or claim that depends on A1–A6 must state which assumptions it relies on.
3. Limitation disclosure. Contributions that add results must also add the corresponding threats to validity (internal, external, construct, conclusion) in the style of Section 7.8.
4. Negative commitments. The following must remain explicit in all derived documents:
   · No real-world deployment has been evaluated.
   · No implementation is claimed.
   · The Byzantine model is limited to malformed deltas.
   · Simulator source, seeds, and raw traces are not included in the record.
   · The paper is not peer reviewed.
5. No silent corrections to published records. The Zenodo DOI 10.5281/zenodo.24038038 archives the v1.0.0 manuscript. Corrections must be issued as a new version with its own DOI, not by silently replacing the archived PDF.

---

Reproducibility

The record for v1.0.0 does not include the simulator source, random seeds, or raw traces. The paper states this explicitly (Section 5.1 and Research Status Statement).

If you submit work that reproduces or extends the simulation, please include in your PR:

· Simulator source code (Python + NumPy or equivalent).
· Random seeds used.
· Raw output traces (CSV or JSON).
· The exact command line to reproduce each reported number.
· Number of independent runs and variance/confidence intervals (the v1.0.0 record does not report these).

This is the recommended path to addressing Q43 (reproducibility package) from Appendix B.

---

Data Provenance

All figures and diagrams in docs/figures/ are original to this project or were redrawn from the author's own drafts. No third-party imagery was used. Figures 6–9 are supplementary and have no supplied counterpart in the draft material (see Reconciliation notes, paper p. 32).

The reference list in the paper was assembled from the author's knowledge of the literature, not by live bibliographic lookup. Bibliographic details (volumes, pages, venues) should be verified before submission to a peer-reviewed venue.

---

Review Process

· All changes are reviewed by the maintainer (Samir Baladi).
· Changes to the manuscript, figures, formal definitions, theorems, or assumptions require explicit documentation in CHANGELOG.md with rationale.
· Adoption of any new formal construct requires an explicit version increment.
· Changes that affect the published manuscript must be coordinated with a new Zenodo version, not a silent edit.

---

Contact

· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· Zenodo DOI: 10.5281/zenodo.24038038
· OSF Registration: Pending
· Website: aethermesh-web.netlify.app
· GitHub: gitdeeper15/aethermesh

---

Thank you for helping improve the formal analysis of decentralized peer-to-peer agent synchronization.
