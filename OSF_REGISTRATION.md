# AetherProof: Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems

---

**Registration DOI:** [10.17605/OSF.IO/SRM2P](https://doi.org/10.17605/OSF.IO/SRM2P)
**Registration Type:** OSF Preregistration
**Registry:** OSF Registries
**Date Created:** Nov 7, 2026, 4:59 AM
**Date Registered:** Nov 7, 2026, 4:59 AM
**Associated Project:** [https://osf.io/atcgp](https://osf.io/atcgp)
**Internet Archive:** [https://archive.org/details/osf-registrations-srm2p-v1](https://archive.org/details/osf-registrations-srm2p-v1)
**License:** CC-By Attribution 4.0 International
**Contributor:** Samir Baladi

---

## Data / Analytic Code / Materials / Papers / Supplements

The following files were attached to this registration:

- `AetherProof_Research_Paper.pdf`
- `README.md`

---

## Overview

### Research questions or hypotheses

AetherProof is a formal architecture proposal, not an empirical study. The research is organized around one central question and five supporting questions, none of which are empirically testable in the current stage (v1.0.0). The questions are stated to define the research frontier, not to be evaluated in this registration.

CENTRAL QUESTION (Q0)
How can heterogeneous specification languages (TLA+, Why3/Lean, SMT-LIB) express different levels of system behavior while preserving semantic consistency, traceability, and verifiable relationships across their respective proof obligations?

SUPPORTING QUESTIONS (from the 50 open questions documented in the manuscript)

Q1. Under what conditions is a translation between specification representations sound with respect to a given property?

Q2. What is a mathematically precise definition of semantic consistency between two CSR records?

Q3. What is the minimal CSR structure that preserves semantic identity across translations?

Q4. How should assumption dependency graphs be structured to support incremental invalidation?

Q5. When is an approximation "good enough" for a given requirement?

Q6. How should proof portability interact with tool diversity?

Q7. Can the three identities of a CSR record (Record / Artifact / Semantic) be reconciled mechanically?

The full list of 50 open questions (Q1–Q50) is documented in Appendix B of the manuscript.

NOTE ON STATUS
No hypothesis is stated as testable in the current stage. The architecture is specified, not implemented. No empirical evaluation is performed. The questions are analytical and formal, not experimental. Future stages (v2.0.0+) may operationalize some questions as testable hypotheses.

### Foreknowledge of data or evidence

Data does not yet exist. No part of the data that will be used for this analysis plan exists, and no part will be generated until after this plan is registered.

### Explanation of foreknowledge and managing unintended influences

No data exists for this registration. AetherProof v1.0.0 is a formal architecture proposal with no implementation and no empirical evaluation. The manuscript specifies three functional layers, a Canonical Specification Representation (CSR), a Proof Dependency Graph (PDG), and a counterexample-guided remediation protocol.

The open questions (Q1–Q50) are analytical and formal, not experimental. They are documented to define the research frontier, not to be tested in this stage.

Future stages (v2.0.0+) will:
1. Implement the reference architecture (src/aetherproof/).
2. Generate synthetic and real-world data for the five experiments.
3. Operationalize some open questions as testable hypotheses.
4. Pre-register any empirical analyses before data collection.

No unintended influences on analysis plans are possible at this stage because no data exists and no analyses are planned. The registration serves to document the formal architecture and its research agenda, not to pre-register an empirical study.

---

## Research Design

### Study type

Other

### Intention for causal interpretation

No causal relationship inferred: This study is not intended to inform a causal relationship.

### Blinding of experimental treatments

No blinding is involved.

### Additional blinding during research or analysis

Not applicable. This is a formal architecture proposal with no experimental treatments, no subjects, and no data collection. Blinding is not relevant.

### Study design

Not applicable. AetherProof v1.0.0 is a formal architecture proposal, not an empirical study. There are no treatments, no conditions, no subjects, and no data collection.

The contribution is a formal specification of:
- Three functional layers (TLA+, Why3/Lean, SMT-LIB/Z3)
- A Canonical Specification Representation (CSR) with three identities
- A Proof Dependency Graph (PDG)
- A counterexample-guided remediation protocol
- An integration protocol with AetherFlow
- A human review protocol
- A threat catalogue (15 threats)

The study design is a "formal specification" design, not an experimental, observational, or simulation design.

For details, see the manuscript: `PUBLICATION/AetherProof_Research_Paper.pdf` (46 pages).

### Randomization

Not applicable. No randomization is involved. This is a formal architecture proposal, not an empirical study.

---

## Sampling

### Data collection procedures

Not applicable. AetherProof v1.0.0 is a formal architecture proposal, not an empirical study. No data is collected, no sample is drawn, and no participants are recruited.

The "data" for this registration consists of the formal artifacts of the architecture:
- 9 design documents (docs/)
- 5 conceptual figures (docs/figures/)
- 1 manuscript (PUBLICATION/AetherProof_Research_Paper.pdf)

These artifacts are not empirical data. They are the output of formal specification work, not of data collection.

If a future stage (v2.0.0+) performs empirical evaluation, a separate pre-registration will be created before any data is collected.

### Sample size

Not applicable. No sample size is defined because no data is collected.

If a future stage (v2.0.0+) performs empirical evaluation, the sample size will be specified in a separate pre-registration before data collection begins.

### Sample size rationale

Not applicable. No sample size rationale is needed because no data is collected.

The number of artifacts in this registration (9 documents, 5 figures, 1 manuscript) is determined by the scope of the formal architecture, not by a sampling strategy or power analysis.

### Starting and stopping rules

Not applicable. There are no starting or stopping rules because no data collection is performed.

The formal architecture was developed iteratively across 9 design documents. The final document (08_research_status_statement.md) marks the completion of v1.0.0.

Future work (v2.0.0+) will define starting and stopping rules for empirical evaluation in a separate pre-registration.

---

## Variables

### Manipulated variables

None. AetherProof v1.0.0 is a formal architecture proposal, not an empirical study. There are no manipulated variables, no treatment arms, and no randomization.

### Measured variables

None. No variables are measured because no data is collected and no empirical study is performed.

AetherProof v1.0.0 specifies a formal architecture. Its "variables" are formal objects, not measured quantities:
- CSR records (formal data structure)
- Semantic relations (formal relations)
- Translation classifications (two orthogonal axes)
- Proof obligations (formal tuples)
- PDG nodes and edges (formal graph)
- Counterexamples (formal tuples)
- TCB manifests (formal records)
- Trust levels (formal classification)

These are not measured variables in the empirical sense. They are formal artifacts of the architecture, defined in the 9 design documents (docs/).

If a future stage (v2.0.0+) performs empirical evaluation, the measured variables (e.g., proof time, throughput, attribution precision) will be specified in a separate pre-registration before data collection begins.

### Indices

Not applicable. No indices or derived variables are constructed because no empirical data is collected.

AetherProof v1.0.0 defines formal objects (CSR records, PDG, proof obligations, counterexamples), but these are not indices derived from measured variables. They are formal constructs specified in the design documents.

If a future stage (v2.0.0+) performs empirical evaluation, the indices (e.g., proof coverage, assumption density, mutation score) will be specified in a separate pre-registration before data collection begins.

---

## Analysis Plan

### Statistical models

Not applicable. AetherProof v1.0.0 is a formal architecture proposal, not an empirical study. No statistical models are used because no data is collected and no empirical analysis is performed.

The "analysis" in this registration is formal, not statistical:
- Formal definitions (6)
- Propositions stated as design requirements (10)
- Architectural pillars (6)
- Open questions (50)
- Design decisions (52)
- Threat catalogue (15)

None of these involve statistical models, hypothesis testing, or empirical data analysis.

If a future stage (v2.0.0+) performs empirical evaluation, the statistical models (e.g., regression for proof time, ANOVA for attribution accuracy, etc.) will be specified in a separate pre-registration before data collection begins.

### Transformations

Not applicable. No data is collected, so no transformations are performed.

The formal objects in AetherProof (CSR records, proof obligations, PDG nodes, counterexamples) are defined by the architecture, not transformed from raw data.

### Inference criteria

Not applicable. No inference criteria are defined because no empirical data is analyzed.

The inferences in AetherProof v1.0.0 are formal, not statistical:
- Propositions P1–P10 are stated as design requirements.
- Open questions Q1–Q50 are stated as open (not answered).
- No p-values, Bayes factors, or model fit indices are used.

If a future stage (v2.0.0+) performs empirical evaluation, the inference criteria (e.g., significance thresholds, effect size cutoffs, multiple comparison corrections) will be specified in a separate pre-registration before data collection begins.

### Data inclusion and exclusion

Not applicable. No data is collected, so no inclusion or exclusion criteria are defined.

The formal artifacts (9 documents, 5 figures, 1 manuscript) are all included by design, not by a selection process.

### Missing data

Not applicable. No data is collected, so missing data is not a concern.

The formal architecture is complete as specified in v1.0.0. No data points are missing.

### Other planned analysis

Not applicable. No other analyses are planned for v1.0.0.

Future stages (v2.0.0+) may include:
- Empirical evaluation of the five experiments (specification synthesis, proof obligation generation, differential proving, counterexample diagnosis, guardrail effectiveness).
- Performance benchmarking of the reference implementation.
- Usability study of the human review protocol.

These will be pre-registered separately before data collection begins.

---

## Other

### Context and additional information

AetherProof v1.0.0 is the third layer in the Aether family, above AetherGit (storage) and AetherFlow (integration). It is a formal architecture proposal with no implementation and no empirical evaluation.

RELATION TO PRIOR WORK
- AetherGit (storage layer): DOI 10.5281/zenodo.23966896
- AetherFlow (integration layer): DOI 10.5281/zenodo.23979129
- Scion position paper (prior work): DOI 10.5281/zenodo.23934465

AetherProof is self-contained: a reader who has not seen the other two papers needs only the definitions in the manuscript and the protocol summary.

CENTRAL COMMITMENT
The hard problem of AetherProof is not making TLA+, Why3, Lean, and SMT-LIB exchange data; it is proving that what these languages mean remains consistent when a specification moves from one representation to another. Semantic consistency (Q2) is an open question that this paper frames but does not solve.

EVIDENTIARY STATUS
No implementation is built. No benchmark is executed. No empirical evaluation is performed. Propositions P1–P10 are design requirements, not formally proven theorems. All numerical values are design targets, not measurements.

DOCUMENT STRUCTURE
The manuscript is accompanied by 9 design documents:
- 01_specification_language.md
- 02_proof_obligations.md
- 03_incremental_proof_engine.md
- 04_counterexample_remediation.md
- 05_integration_protocol.md
- 06_human_review_protocol.md
- 07_threats_and_limitations.md
- 08_research_status_statement.md
- system_architecture.md

These are available in the project repository (github.com/gitdeeper15/aetherproof) and on Zenodo (DOI 10.5281/zenodo.24013124).

NEXT STAGE
v2.0.0 (planned): implementation of the reference architecture and execution of five experiments. A separate pre-registration will be created before any data is collected.

CONTACT
Samir Baladi — gitdeeper@gmail.com — ORCID 0009-0003-8903-0029
Ronin Institute / Rite of Renaissance

---

## Metadata

### Contributors

Samir Baladi

### Resource type

No resource type

### Description

AetherProof is a formal architecture for specification-driven proof construction, incremental differential proving, and counterexample-guided remediation in multi-agent software ecosystems. It is the verification layer of the Aether family, above AetherGit (storage) and AetherFlow (integration).

The paper specifies three functional layers (TLA+, Why3/Lean, SMT-LIB/Z3), a Canonical Specification Representation (CSR) with three distinct identities (record, artifact, semantic), a Proof Dependency Graph (PDG), and a counterexample-guided remediation protocol.

Keywords: AetherProof · Formal Verification · Multi-Agent Systems · Differential Verification · Invariant Synthesis · TLA+ · Why3 · Lean · SMT-LIB · Z3 · CSR Record · TCB Manifest · Semantic Relations · Compatibility Matrices · Requirement-driven Proof Trace · Specification Languages · Proof Obligations · Incremental Proving · Counterexample-Guided Remediation · Agentic Software Engineering.

Status: Formal Architecture Proposal — No Implementation Benchmarked. No empirical evaluation is performed. Propositions P1–P10 are design requirements, not formally proven theorems. Semantic consistency (Q2) remains an open question.

DOI (Zenodo): 10.5281/zenodo.24013124
Record ID: AETHERPROOF-01
Version: 1.0.0 — November 2026
Author: Samir Baladi — ORCID 0009-0003-8903-0029
License: MIT (code) + CC-BY-4.0 (docs)

### Registration Type

OSF Preregistration

### Registry

OSF Registries

### Associated project

https://osf.io/atcgp

### Date Created

Nov 7, 2026, 4:59 AM

### Date registered

Nov 7, 2026, 4:59 AM

### Subjects

- Software Engineering
- Computer Sciences
- Mathematics
- Physical Sciences and Mathematics
- Logic and Foundations
- Programming Languages and Compilers

### Tags

- AetherProof
- Agentic Software Engineering
- Compatibility Matrices
- Counterexample-Guided Remediation
- CSR Record
- Differential Verification
- Formal Methods
- Formal Verification
- Functional Contracts
- Incremental Proving
- Invariant Synthesis
- Lean
- Logical Constraints
- Multi-Agent Systems
- Proof Obligations
- Proof Trace
- Semantic Relations
- SMT-LIB
- Specification Languages
- System-Level Properties
- TCB Manifest
- TLA+
- Trusted Computing Base
- Why3
- Z3

### Affiliated Institutions

No affiliated institutions

### Funder Names

No information

### Language

No language

### Associated project

https://osf.io/atcgp

### Internet Archive link

https://archive.org/details/osf-registrations-srm2p-v1

### License

CC-By Attribution 4.0 International

### Registration DOI

10.17605/OSF.IO/SRM2P

---

## Citations

### APA

Baladi, S. (2026, November 7). AetherProof: Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems. OSF. https://doi.org/10.17605/OSF.IO/SRM2P

### MLA

Baladi, Samir. "AetherProof: Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems." OSF, 7 Nov. 2026. Web.

### Chicago

Baladi, Samir. 2026. "AetherProof: Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems." OSF. November 7. doi:10.17605/OSF.IO/SRM2P.

### BibTeX

```bibtex
@misc{baladi2026aetherproof_osf,
  author       = {Baladi, Samir},
  title        = {{AetherProof: Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems}},
  year         = {2026},
  month        = nov,
  day          = {7},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/SRM2P},
  url          = {https://doi.org/10.17605/OSF.IO/SRM2P},
  note         = {OSF Preregistration. Associated project: https://osf.io/atcgp}
}
```

---

Source: Center for Open Science · OSF Registries
Retrieved: 2026-11-07
