# AetherProof — Changelog

All notable changes to this research project will be documented in this file.

## [2.0.0] — 2026-11-07

### Empirical Implementation

First implementation of AetherProof formal architecture.
Also published on **PyPI** as `aetherproof` (alpha release).

### Added — Source Code

- `src/aetherproof/` package with 7 modules (22 files):
  - `models.py` — CSRecord, Obligation, Counterexample, Verdict, Layer
  - `csr/` — CSR Record + Semantic Relations (7 typed relations)
  - `obligations/` — Obligation Generator + ODG
  - `proof/` — PDG + Invalidation + ProofEngine
  - `remediation/` — Diagnosis + Guardrails + RemediationCycle
  - `protocol/` — Message (M1-M10) + Envelope
  - `review/` — Role (5 roles) + Authority Matrix (45 entries)
- `pyproject.toml` — PEP 621 compliant
- 40 tests, 79% coverage

### Added — Experiments (all 5 completed)

| # | Experiment | Result |
|---|------------|--------|
| 1 | Specification Synthesis | F1 = 0.884 |
| 2 | Proof Obligation Generation | 247 obligations (89 CSR) |
| 3 | Differential Proving | 2.5× speedup |
| 4 | Counterexample Diagnosis | 94% accuracy |
| 5 | Guardrail Effectiveness | 100% block rate |

### Added — Reports

- `REPORTS/v2.0.0/report.md` — full evaluation report

### Added — PyPI Publication

- Package: `aetherproof` on **PyPI**
- Version: `0.1.0a1` (alpha — API may change)
- URL: https://pypi.org/project/aetherproof/
- Install: `pip install aetherproof==0.1.0a1`

### Changed

- `VERSION`: 1.0.0 → 2.0.0
- `CITATION.cff`: 1.0.0 → 2.0.0 (version + date)
- `manifest.json`: 1.0.0 → 2.0.0
- `scientific_state.json`: 1.0.0 → 2.0.0
- `PROJECT_SUMMARY.txt`: 1.0.0 → 2.0.0
- `INVENTORY.md`: 1.0.0 → 2.0.0
- `README.md`: added PyPI badges, Installation section, v2.0.0 status
- `CHANGELOG.md`: this entry

### Technical Notes

- `pyproject.toml` uses PEP 621
- Python 3.9+ required
- `scikit-learn` moved to `[experiments]` extras
- PyPI package version `0.1.0a1` is separate from manuscript `VERSION=2.0.0`

### Related Identifiers

- **Zenodo DOI**: [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124)
- **OSF Registration**: [10.17605/OSF.IO/SRM2P](https://doi.org/10.17605/OSF.IO/SRM2P)
- **PyPI**: [pypi.org/project/aetherproof](https://pypi.org/project/aetherproof/)
- **GitHub Release**: [v2.0.0](https://github.com/gitdeeper15/aetherproof/releases/tag/v2.0.0)

### Status

| Dimension | Status |
|-----------|--------|
| Manuscript | Complete (46 pages, PDF) |
| Formal Definitions | 6 |
| Propositions | 10 (design requirements) |
| Architectural Pillars | 6 |
| Figures | 5 |
| Open Questions | 50 |
| Design Decisions | 52 |
| Threats | 15 |
| Implementation | ✅ Built (`src/aetherproof/`) |
| Tests | ✅ 40 passed, 79% coverage |
| Experiments | ✅ 5/5 completed |
| PyPI Package | ✅ Published (0.1.0a1) |
| Real-world deployment | ❌ Not evaluated |
| Causal claims | None (formal analysis only) |

---

## [1.0.0] — 2026-11-07

### Initial Program Manuscript

First public release: formal architecture proposal, 46-page PDF, 6 definitions, 10 propositions, 6 architectural pillars, 5 figures, 27 references.

No implementation, no empirical results.

---

**Last Updated:** 2026-11-07
**Current Version:** 2.0.0 (manuscript) / 0.1.0a1 (PyPI)
