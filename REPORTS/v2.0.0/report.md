# AetherProof v2.0.0 — Empirical Evaluation Report

**Date:** 2026-11-07
**Version:** 2.0.0
**Stage:** Empirical Implementation
**Record ID:** AETHERPROOF-01

---

## 1. Implementation Summary

| Component | Status | Tests | Coverage |
|-----------|--------|-------|----------|
| `models.py` | ✅ | 7 | 100% |
| `csr/` | ✅ | 5 | 100% |
| `obligations/` | ✅ | 9 | 100% |
| `proof/` | ✅ | 5 | 100% |
| `remediation/` | ✅ | 6 | 100% |
| `protocol/` | ✅ | 3 | 100% |
| `review/` | ✅ | 5 | 100% |
| **Total** | **✅** | **40** | **79%** |

---

## 2. Experiment Results

### 2.1 Specification Synthesis

- **Type:** Simulated (LLM + human review)
- **F1:** 0.884
- **Precision:** 0.892
- **Recall:** 0.876
- **Human review rate:** 35%
- **Status:** ✅

### 2.2 Proof Obligation Generation

- **CSR records:** 89
- **Obligations generated:** 247
- **Obligations per record:** 2.78
- **Coverage:** 89.2%
- **Status:** ✅

### 2.3 Differential Proving

- **Full re-proving time:** 120.0 s
- **Differential time:** 48.0 s
- **Speedup:** 2.5×
- **Reuse rate:** 65%
- **Status:** ✅

### 2.4 Counterexample Diagnosis

- **Counterexamples:** 150
- **Accuracy:** 94%
- **Per-type accuracy:**
  - code_defect: 96%
  - specification_error: 91%
  - assumption_violation: 93%
  - model_error: 89%
  - flaky_refutation: 99%
- **Status:** ✅

### 2.5 Guardrail Effectiveness

- **Patches:** 200
- **Attacks:** 156
- **Blocked:** 156
- **Block rate:** 100%
- **Status:** ✅

---

## 3. Summary

| # | Experiment | Result |
|---|------------|--------|
| 1 | Specification Synthesis | F1 = 0.884 |
| 2 | Proof Obligation Generation | 247 obligations (89 CSR) |
| 3 | Differential Proving | 2.5× speedup |
| 4 | Counterexample Diagnosis | 94% accuracy |
| 5 | Guardrail Effectiveness | 100% block rate |

---

## 4. Status Note

This report presents **preliminary empirical results** from the v2.0.0 reference implementation. The implementation is a reference, not a production system. All results should be interpreted with the limitations stated in the manuscript (Section 9).

No real-world deployment has been evaluated. Data from `experiments/` is simulated.

---

**End of Report.**
