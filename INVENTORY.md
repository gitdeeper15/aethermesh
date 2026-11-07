# AetherProof — Complete Inventory

**Version:** 2.0.0 (manuscript revision) / 0.1.0a1 (PyPI package)
**Release Date:** 2026-11-07
**Author:** Samir Baladi
**Email:** gitdeeper@gmail.com
**ORCID:** [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)
**License:** MIT (code) · CC-BY-4.0 (docs, manuscript, figures)
**Status:** Empirical Implementation · Reference implementation · Preliminary results
**Record ID:** AETHERPROOF-01
**DOI (Zenodo):** [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124)
**DOI (OSF):** [10.17605/OSF.IO/SRM2P](https://doi.org/10.17605/OSF.IO/SRM2P)

---

## Repository Links

| Platform | URL | Role | Status |
|----------|-----|------|--------|
| GitHub | https://github.com/gitdeeper15/aetherproof | Primary | ✅ Active |
| GitLab | https://gitlab.com/gitdeeper15/aetherproof | Mirror | ✅ Active |
| Codeberg | https://codeberg.org/gitdeeper15/aetherproof | Mirror | ✅ Active |
| Bitbucket | https://bitbucket.org/gitdeeper15/aetherproof | Mirror | ✅ Active |
| PyPI | https://pypi.org/project/aetherproof/ | Python package | ✅ **Published (0.1.0a1)** |
| Zenodo | https://doi.org/10.5281/zenodo.24013124 | DOI (manuscript) | ✅ Published |
| OSF | https://doi.org/10.17605/OSF.IO/SRM2P | Registration | ✅ Published |
| Website | https://aetherproof-arch.netlify.app | Live documentation | ✅ Active |
| ORCID | https://orcid.org/0009-0003-8903-0029 | Identity | ✅ Active |

> **PyPI note:** Published as `aetherproof` version `0.1.0a1` (alpha). Install with
> `pip install aetherproof==0.1.0a1`. The alpha status signals that the API may
> change before `1.0.0`. This is a reference implementation, not a production system.

---

## Root Files

| File | Purpose |
|------|---------|
| `.gitignore` | Git ignore rules |
| `AUTHORS.md` | Contributors (AetherProof) |
| `CHANGELOG.md` | Version history (v2.0.0) |
| `CITATION.cff` | Citation metadata (v2.0.0) |
| `CONTRIBUTING.md` | Contribution guidelines (AetherProof) |
| `INVENTORY.md` | Complete inventory (this file) |
| `LICENSE` | MIT + CC-BY-4.0 |
| `PROJECT_SUMMARY.txt` | One-page summary (AetherProof v2.0.0) |
| `README.md` | Main documentation (v2.0.0) |
| `VERSION` | 2.0.0 |
| `manifest.json` | Project manifest (v2.0.0) |
| `scientific_state.json` | Scientific state record (v2.0.0) |
| `requirements.txt` | Python deps |
| `pyproject.toml` | PEP 621 build config (v0.1.0a1) |
| `upload_aetherproof.py` | PyPI uploader script |
| `netlify.toml` | Netlify configuration (for future site) |
| `OSF_REGISTRATION.md` | OSF registration document (published) |

---

## Directories

| Directory | Purpose |
|-----------|---------|
| `src/aetherproof/` | Reference implementation (v2.0.0) |
| `tests/` | Test suite (40 tests, 79% coverage) |
| `experiments/` | 5 experiment protocols + results |
| `docs/` | Formal documents (9 files) + figures |
| `docs/figures/` | Conceptual diagrams (5) |
| `PUBLICATION/` | Manuscript (PDF) |
| `REPORTS/v2.0.0/` | v2.0.0 evaluation report |
| `DATA/` | Future data (empty) |
| `ANALYSIS/` | Future analysis (empty) |
| `EXTERNAL_REVIEW/` | Future review records (empty) |
| `VALIDATION/` | Future validation (empty) |

---

## Source Code Structure (v2.0.0)

| Module | Purpose |
|--------|---------|
| `models.py` | CSRecord, Obligation, Counterexample, Verdict, Layer |
| `csr/record.py` | CSR Record (Definition 1) |
| `csr/relations.py` | Semantic Relations (Definition 2, 7 types) |
| `obligations/generator.py` | Obligation Generator (Section 4.2) |
| `obligations/odg.py` | ODG (Section 4.3) |
| `proof/pdg.py` | PDG (Definition 5) |
| `proof/invalidation.py` | Invalidation Rules (Section 5.3) |
| `proof/engine.py` | Differential Proof Engine (Section 5) |
| `remediation/diagnosis.py` | Diagnosis Protocol (Section 6.3) |
| `remediation/guardrails.py` | Guardrails (Section 6.5) |
| `remediation/cycle.py` | Remediation Cycle (Section 6.2) |
| `protocol/messages.py` | M1-M10 (Section 7.2) |
| `review/roles.py` | 5 Roles + Authority Matrix (Section 8.1) |
| `cli.py` | Command-line interface |

---

## Test Suite (v2.0.0)

| Test File | Tests |
|-----------|-------|
| `test_models.py` | 7 |
| `test_csr.py` | 5 |
| `test_obligations.py` | 9 |
| `test_proof.py` | 5 |
| `test_remediation.py` | 6 |
| `test_protocol.py` | 3 |
| `test_review.py` | 5 |
| **Total** | **40 tests, 79% coverage** |

---

## Experiments (v2.0.0)

| # | Experiment | Result | Status |
|---|------------|--------|--------|
| 1 | Specification Synthesis | F1 = 0.884 | ✅ |
| 2 | Proof Obligation Generation | 247 obligations (89 CSR) | ✅ |
| 3 | Differential Proving | 2.5× speedup | ✅ |
| 4 | Counterexample Diagnosis | 94% accuracy | ✅ |
| 5 | Guardrail Effectiveness | 100% block rate | ✅ |

> **Status note:** Experiments use simulated data. No real-world deployment evaluated.

---

## Documentation (9 files)

| # | File | Version | Status |
|---|------|---------|--------|
| 01 | `docs/01_specification_language.md` | 1.0.1-draft | ✅ Draft |
| 02 | `docs/02_proof_obligations.md` | 1.0.0-draft | ✅ Draft |
| 03 | `docs/03_incremental_proof_engine.md` | 1.0.0-draft | ✅ Draft |
| 04 | `docs/04_counterexample_remediation.md` | 1.0.0-draft | ✅ Draft |
| 05 | `docs/05_integration_protocol.md` | 1.0.0-draft | ✅ Draft |
| 06 | `docs/06_human_review_protocol.md` | 1.0.0-draft | ✅ Draft |
| 07 | `docs/07_threats_and_limitations.md` | 1.0.0-draft | ✅ Draft |
| 08 | `docs/08_research_status_statement.md` | 1.0.0-final | ✅ Final |
| — | `docs/system_architecture.md` | 1.0.0-draft | ✅ Draft |

---

## Formal Definitions (6)

| # | Definition | Statement | Status |
|---|------------|-----------|--------|
| 1 | CSR Record | `csr = (csr_id, artifact_hash, semantic_id, layer, language, content, semantic_role, requirements_refs, assumptions, relations, version, provenance)` | ✅ Defined |
| 2 | Semantic Relation | Seven typed relations: refines, instantiates, approximates, implies, contradicts, depends_on, supersedes | ✅ Defined |
| 3 | Translation Classification | Two orthogonal axes: Axis A (Semantic Relationship), Axis B (Verification Property) | ✅ Defined |
| 4 | Proof Obligation | `O = (id, property, assumptions, source_csr, discharged_by, verdict)` | ✅ Defined |
| 5 | Proof Dependency Graph (PDG) | `PDG = (Obligations ∪ Evidence ∪ Assumptions, Edges)` | ✅ Defined |
| 6 | Counterexample | `C = (id, obligation, witness, refutation_evidence, type, provenance)` | ✅ Defined |

---

## Propositions (10)

| # | Proposition | Status |
|---|-------------|--------|
| P1 | Non-Substitutability | ✅ Stated (design requirement) |
| P2 | Orthogonality of Translation Axes | ✅ Stated (design requirement) |
| P3 | ODG Acyclicity | ✅ Stated (design requirement) |
| P4 | PDG Extends ODG | ✅ Stated (design requirement) |
| P5 | Invalidation via derives_from | ✅ Stated (design requirement) |
| P6 | Bounded Remediation | ✅ Stated (design requirement) |
| P7 | Specification Changes Require Human Review | ✅ Stated (design requirement) |
| P8 | Separation of Duties | ✅ Stated (design requirement) |
| P9 | Human Discharge Only When Automation Cannot | ✅ Stated (design requirement) |
| P10 | Trust Is Explicit | ✅ Stated (design requirement) |

> **Note:** Propositions P1–P10 are **design requirements**, not formally proven theorems.

---

## Architectural Pillars (6)

| # | Pillar | Status |
|---|--------|--------|
| 1 | Three-Layer Functional Specification (TLA+, Why3/Lean, SMT-LIB) | ✅ Specified |
| 2 | Canonical Specification Representation (CSR) | ✅ Specified |
| 3 | Proof Dependency Graph (PDG) | ✅ Specified |
| 4 | Counterexample-Guided Remediation | ✅ Specified |
| 5 | Protocol-Based Integration (with AetherFlow) | ✅ Specified |
| 6 | Human Review Protocol | ✅ Specified |

---

## Open Questions (50)

| Range | Topic | Document |
|-------|-------|----------|
| Q1–Q7 | Specification language | 01 |
| Q8–Q12 | Proof obligations | 02 |
| Q13–Q18 | Differential proving | 03 |
| Q19–Q24 | Counterexample remediation | 04 |
| Q25–Q30 | System architecture | System Architecture |
| Q31–Q36 | Integration protocol | 05 |
| Q37–Q42 | Human review | 06 |
| Q43–Q50 | Threats and limitations | 07 |

> **Q2** (semantic consistency) is the most consequential open question.

---

## Design Decisions (52)

52 design decisions (D1–D52) documented across the eight documents.

---

## Threats (15)

| ID | Threat | Category | Severity | Residual Risk |
|----|--------|----------|----------|---------------|
| T1 | Unsound proof artifact | Soundness | High | Low |
| T2 | Incomplete TCB manifest | Trust | High | Medium |
| T3 | Specification does not reflect intent | Specification | High | Medium |
| T4 | Silent assumption change | Trust | High | Low |
| T5 | Guardrail bypass | Process | High | Low |
| T6 | Toolchain compromise | Toolchain | High | Medium |
| T7 | Reviewer conflict of interest | Human | Medium | Low |
| T8 | Incomplete completeness proof | Completeness | Medium | Medium |
| T9 | Semantic inconsistency between layers | Trust | Medium | Medium |
| T10 | Counterexample flakiness | Soundness | Medium | Low |
| T11 | Model over-approximation | Completeness | Medium | Medium |
| T12 | Hypothesis-testing bias | Human | Medium | Medium |
| T13 | Denial of service on proof engine | Process | Low | Low |
| T14 | Audit-log tampering | Process | High | Low |
| T15 | LLM-generated specification error | Specification | High | Medium |

---

## Figures (5)

| # | Figure | File | Size |
|---|--------|------|------|
| 1 | Three-Layer Architecture | `docs/figures/Fig1_Three_Layer_Architecture.png` | 349 KB |
| 2 | CSR Record Structure | `docs/figures/Fig2_CSR_Record_Structure.png` | 211 KB |
| 3 | Semantic Relations Graph | `docs/figures/Fig3_Semantic_Relations_Graph.png` | 275 KB |
| 4 | Two-Axis Classification | `docs/figures/Fig4_Two_Axis_Classification.png` | 317 KB |
| 5 | TCB Manifest | `docs/figures/Fig5_TCB_Manifest.png` | 363 KB |

---

## Publication

| File | Description | Size |
|------|-------------|------|
| `PUBLICATION/AetherProof_Research_Paper.pdf` | Full manuscript (46 pages) | 1.3 MB |

---

## Reports

| File | Description | Size |
|------|-------------|------|
| `REPORTS/v2.0.0/report.md` | v2.0.0 evaluation report | 94 lines |

---

## References (27)

27 references (see Section "References" of the manuscript, pages 44–45).

Key related identifiers:
- **Zenodo DOI (this manuscript):** [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124)
- **OSF Registration:** [10.17605/OSF.IO/SRM2P](https://doi.org/10.17605/OSF.IO/SRM2P)
- **PyPI Package:** [pypi.org/project/aetherproof](https://pypi.org/project/aetherproof/)
- **AetherGit (storage layer, related work):** [10.5281/zenodo.23966896](https://doi.org/10.5281/zenodo.23966896)
- **AetherFlow (integration layer, related work):** [10.5281/zenodo.23979129](https://doi.org/10.5281/zenodo.23979129)
- **Scion position paper (prior work):** [10.5281/zenodo.23934465](https://doi.org/10.5281/zenodo.23934465)

---

## Dependencies

### Python (runtime — v2.0.0)

- `numpy >= 1.24.0`

### Python (dev)

- `pytest >= 7.0`
- `pytest-cov >= 4.0`
- `ruff >= 0.1`
- `mypy >= 1.0`

### Python (experiments — optional)

- `scikit-learn >= 1.3`
- `matplotlib >= 3.7`

### External APIs

- None (reference implementation; no API calls).

---

## Completion Summary

```

Project:              AetherProof — Autonomous Formal Verification and
Invariant Synthesis for Multi-Agent Software Ecosystems
Version:              2.0.0 (manuscript) / 0.1.0a1 (PyPI package)
Status:               Empirical Implementation · Reference implementation
Formal Definitions:   6
Propositions:         10 (design requirements; not formally proven)
Architectural Pillars: 6
Figures:              5
References:           27
Open Questions:       50 (Q1–Q50)
Design Decisions:     52 (D1–D52)
Threats:              15 (T1–T15)
Documentation:        9 files (docs/)
Source files:         22 (src/aetherproof/)
Tests:                40 passed, 79% coverage
Experiments:          5/5 completed
Manuscript:           Complete (46 pages, PDF)
PyPI package:         ✅ Published (aetherproof 0.1.0a1)
Real-world deployment: ❌ Not evaluated
Causal Claims:        None (formal analysis only)
License:              MIT (code) + CC-BY-4.0 (manuscript, figures, docs)
DOI (Zenodo):         10.5281/zenodo.24013124
DOI (OSF):            10.17605/OSF.IO/SRM2P
Website:              https://aetherproof-arch.netlify.app

```

---

## Citation

### Primary Manuscript (AetherProof v1.0.0)

```bibtex
@techreport{baladi2026aetherproof,
  author       = {Baladi, Samir},
  title        = {AetherProof: Autonomous Formal Verification and Invariant
                  Synthesis for Multi-Agent Software Ecosystems},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.24013124},
  url          = {https://doi.org/10.5281/zenodo.24013124},
  note         = {Formal Architecture Proposal --- Formalization Stage.
                  Six formal definitions, six architectural pillars,
                  ten propositions with proofs. No empirical results.}
}
```

Software Archive (PyPI + Zenodo)

```bibtex
@software{baladi2026aetherproof_v2,
  author       = {Baladi, Samir},
  title        = {{AetherProof} v2.0.0: Empirical Implementation of Autonomous
                  Formal Verification and Invariant Synthesis},
  year         = {2026},
  month        = {November},
  publisher    = {PyPI},
  version      = {0.1.0a1},
  doi          = {10.5281/zenodo.24013124},
  url          = {https://pypi.org/project/aetherproof/},
  note         = {Reference implementation.
                  Available via pip install aetherproof==0.1.0a1.}
}
```

---

Generated: 2026-11-07
Inventory Version: 2.0.0
