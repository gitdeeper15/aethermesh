<div align="center">

# 🕸️ AetherGovern

### A Falsification-First Investigation of Governance in the Aether Family

*A Falsification-First Investigation of Authority, Policy, and Accountability in Multi-Agent Software Ecosystems*

<br>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24054524.svg)](https://doi.org/10.5281/zenodo.24054524)
[![License: MIT + CC-BY-4.0](https://img.shields.io/badge/License-MIT%20%2B%20CC--BY--4.0-crimson.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--8903--0029-a6ce39?logo=orcid&logoColor=white)](https://orcid.org/0009-0003-8903-0029)
[![Release](https://img.shields.io/badge/Release-v0.1.0-orange)](https://github.com/gitdeeper15/aethergovern/releases/tag/v0.1.0)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://python.org)

[![Status](https://img.shields.io/badge/Status-Hypothesis%20Under%20Investigation-orange)](README.md)
[![Propositions](https://img.shields.io/badge/Propositions-2%20(proof%20sketches)-blue)](README.md)
[![Failure Conditions](https://img.shields.io/badge/Failure%20Conditions-F1–F5-red)](README.md)
[![Open Questions](https://img.shields.io/badge/Open%20Questions-Q1–Q20-yellow)](README.md)

[![Zenodo](https://img.shields.io/badge/Zenodo-Published-blue)](https://doi.org/10.5281/zenodo.24054524)
[![Record ID](https://img.shields.io/badge/Record%20ID-AETHERGOVERN--01-orange)](https://doi.org/10.5281/zenodo.24054524)
[![OSF](https://img.shields.io/badge/OSF-Pending-lightgrey)](https://osf.io/)
[![Website](https://img.shields.io/badge/Website-aethergovern.netlify.app-00C7B7?logo=netlify&logoColor=white)](https://aethergovern.netlify.app)
[![Aether Family](https://img.shields.io/badge/Aether%20Family-5%20dimensions%20(4%20confirmed%20%2B%201%20hypothesis)-orange)](https://aethergovern.netlify.app)

<br>

**[📄 Paper](https://doi.org/10.5281/zenodo.24054524)** ·
**[🌐 Website](https://aethergovern.netlify.app)** ·
**[📦 Releases](https://github.com/gitdeeper15/aethergovern/releases)** ·
**[📖 Citation](#-citation)**

</div>

---

> [!WARNING]
> **Status: v0.1.0 — Architectural Hypothesis Under Investigation.**
> This is **not** a committed project. It is a **structured investigation** of whether a governance gap genuinely exists in the Aether family.
> **No implementation is claimed.** **No real-world deployment has been evaluated.**
> Propositions 1–2 are stated with **proof sketches**, not machine-checked.
> The five failure conditions (F1–F5) are the author's proposals; F1–F4 are **not falsified by argument**, F5 is **untested**.
> The final project structure (single, dual, or triple project) is **undetermined**.
> See [Threats and Limitations](#-threats-and-limitations) and the [Research Status Statement](#-research-status-statement).

> *"AetherGovern is a candidate, not a result."*
> — AetherGovern v0.1.0, Section 8.5

> *"The investigation found that the question 'who is authorized to do what, under which policy?' is not answered by the four existing Aether preprints, and that a decentralized answer is not ruled out by the determinism requirement."*
> — AetherGovern v0.1.0, Section 8.5

---

## 📑 Table of Contents

- [Overview](#-overview)
- [v0.1.0 at a Glance](#-v010-at-a-glance)
- [The Central Question](#-the-central-question)
- [The Five Functional Dimensions](#-the-five-functional-dimensions)
- [The Falsification-First Methodology](#-the-falsification-first-methodology)
- [Failure Conditions F1–F5](#-failure-conditions-f1f5)
- [The Three Candidate Capabilities](#-the-three-candidate-capabilities)
- [AetherGovern: Architecture](#-aethergovern-architecture)
- [Propositions](#-propositions)
- [Interfaces with the Aether Family](#-interfaces-with-the-aether-family)
- [Evaluation (Proposed)](#-evaluation-proposed)
- [Threats and Limitations](#-threats-and-limitations)
- [Research Status Statement](#-research-status-statement)
- [Platforms & Mirrors](#-platforms--mirrors)
- [Project Structure](#️-project-structure)
- [Version History](#-version-history)
- [Citation](#-citation)
- [Author](#-author)
- [License](#️-license)

---

## 🔭 Overview

**AetherGovern** is the **fifth functional dimension** of the Aether family (under investigation) — a candidate architecture for **authority, policy, accountability, revocation, and dispute resolution** in multi-agent software ecosystems.

The Aether family currently comprises **four foundational dimensions**, each published as a preprint on Zenodo (**not peer-reviewed**):

| Dimension | Focus | Question |
|---|---|---|
| **AetherGit** | Storage and versioning | How are changes stored and versioned? |
| **AetherFlow** | Integration and operational verification | How are changes integrated and verified? |
| **AetherProof** | Specification and formal evidence | How is correctness proven? |
| **AetherMesh** | Distribution and eventual consistency | How is state synchronized without a central coordinator? |

AetherGovern asks whether a **fifth dimension** is needed:

> **Who is authorized to do what, under which policy, with what accountability, and how is authority revoked?**

The investigation follows a **falsification-first methodology**: before describing the candidate, it states **five failure conditions (F1–F5)** whose satisfaction would show that the candidate does not deserve to exist as a separate dimension.

---

## 📊 v0.1.0 at a Glance

| Dimension | Status |
|---|---|
| Manuscript | Complete (33 pages, PDF) |
| Formal definitions | 4 (Authorization, Policy, Accountability, Revocation, Dispute Resolution — as layers) |
| Propositions | 2 (determinism of causal-authority admission; monotonicity of revocation) — **proof sketches** |
| Failure conditions | 5 (F1–F5) — **the author's proposals** |
| Open questions | 20 (Q1–Q20) |
| Figures | 5 (Fig1–Fig5) + 2 supplementary |
| Implementation | ❌ Not built |
| Real-world deployment | ❌ Not evaluated |
| Causal claims | None (argument only) |
| Project structure | ⏳ Undetermined (single, dual, or triple) |

<p align="center">
  <img src="docs/figures/Fig1_Five_Dimensions.png"
       alt="AetherGovern — The Five Functional Dimensions of the Aether Family"
       width="100%">
</p>

<p align="center">
  <em>Figure 1 — The Five Functional Dimensions of the Aether Family (AetherGit, AetherFlow, AetherProof, AetherMesh, and the proposed hypothesis AetherGovern). The fifth dimension (AetherGovern) is a hypothesis under investigation, not a confirmed dimension.</em>
</p>

### Contributions to the Investigation

| # | Contribution | Kind |
|:-:|---|---|
| 1 | A falsification-first procedure with five failure conditions and a decision rule, stated before the candidate is described | Methodology |
| 2 | A comparison of three candidate capabilities that could fill a gap beside the four dimensions: orchestration, governance, and runtime assurance | Analysis |
| 3 | A hypothesized five-layer governance architecture, including a policy lifecycle, a scoped delegation model with revocation, and a statement of how governance differs from verification | Specification (hypothesis) |
| 4 | Two propositions with proof sketches that bear directly on F4: causal-authority admission preserves the determinism requirement of AetherMesh, and revocation leaves an irreducible exposure window | Analysis (proof sketches) |
| 5 | A provisional assessment of F1–F5 based on argument alone, with residual weaknesses stated, and an evaluation design that specifies in advance what outcomes would count as failure | Evaluation design |
| 6 | Twenty open questions (Q1–Q20) | Catalogue |

---

## ❓ The Central Question

> **Is there a body of authorization, policy, accountability, revocation, and dispute-resolution requirements for multi-agent software ecosystems that (i) is not already specified by the four existing dimensions, (ii) is not reducible to verification or to orchestration, (iii) can be specified without reintroducing a central authority, and (iv) yields an observable benefit over existing mechanisms?**

The four clauses correspond to failure conditions F1, F2 and F3 (clause ii), F4, and F5. A negative answer to any clause would show that governance, as a separate dimension, is not warranted. A positive answer to all four, supported by evidence, would show that it is a candidate.

---

## 🏛️ The Five Functional Dimensions

*The word "dimension" is chosen deliberately. Earlier descriptions used "layer", which suggests a vertical stack. The relationships among the five works are not strictly hierarchical.*

| # | Dimension | Focus | Question | DOI |
|:-:|---|---|---|---|
| 1 | **AetherGit** | Storage and versioning | How are changes stored and versioned? | [10.5281/zenodo.23966896](https://doi.org/10.5281/zenodo.23966896) |
| 2 | **AetherFlow** | Integration and operational verification | How are changes integrated and verified? | [10.5281/zenodo.23979129](https://doi.org/10.5281/zenodo.23979129) |
| 3 | **AetherProof** | Specification and formal evidence | How is correctness proven? | [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124) |
| 4 | **AetherMesh** | Distribution and eventual consistency | How is state synchronized without a central coordinator? | [10.5281/zenodo.24053492](https://doi.org/10.5281/zenodo.24053492) |
| 5 | **AetherGovern** *(hypothesis)* | Authority and policy | Who is authorized to do what, under which policy? | [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524) |

---

## 🔬 The Falsification-First Methodology

A typical architecture paper begins from a conviction that a component is needed and then specifies it. The risk is circular: the specification is judged against the author's own framing of the problem, and the framing was chosen to make the component look necessary.

AetherGovern adopts a **falsification-first methodology**:

1. **No prior assumption** that the gap exists.
2. **No prior assumption** that AetherGovern should be a separate project.
3. **Every claim** is tested against failure conditions (F1–F5).
4. **The final structure** (single project, dual project, triple project, or integration protocol) is determined **after** comparison.

---

## 🧭 Failure Conditions F1–F5

*Each condition is stated as a condition whose satisfaction would show that the candidate fails.*

| ID | Claim under test | Falsified if | Status |
|:-:|---|---|:-:|
| **F1** | Non-redundancy | Every requirement R1–R6 is met by existing mechanisms or by a bounded extension of a single existing dimension | 🟡 Not falsified (R1, R3, R5) |
| **F2** | Orthogonality to verification | Every authorization decision and every trust anchor can be encoded as a verified proposition | 🟡 Not falsified (narrowly) |
| **F3** | Boundary with orchestration | Governance reduces to task assignment plus conventional access control | 🟡 Not falsified (decentralized setting) |
| **F4** | Decentralizability | Any design preserving the required properties needs a central authority or strong consistency | 🟡 Not falsified (with residuals) |
| **F5** | Observable benefit | No scenario class can be constructed in which the best existing baseline fails and governance succeeds | 🔴 **Untested** |

**Requirement list R1–R6 (used by F1):**

| ID | Requirement |
|:-:|---|
| **R1** | Scoped, attenuating delegation: an agent can grant a subset of its authority to another, and no agent can grant more than it holds. |
| **R2** | Authorized policy change: the rules that decide authorization can themselves be changed only by agents authorized to change them. |
| **R3** | Revocation with dependents: withdrawing a grant also withdraws grants derived from it. |
| **R4** | Attribution: each admitted action can be traced to the chain of agents responsible for it. |
| **R5** | Dispute handling: conflicting authority claims are resolved by a deterministic rule or an explicit escalation. |
| **R6** | Partition tolerance: authority checks can be made at a node that is temporarily disconnected, with a stated safety consequence. |

---

## 🎯 The Three Candidate Capabilities

| Candidate | Focus | Central question | Closest existing dimension | Redundancy risk |
|---|---|---|---|---|
| **AetherOrchestrate** | Task scheduling and workflow | What should agents do next? | AetherFlow (integration) | Medium |
| **AetherGovern** | Authority, accountability, revocation | Who may act, under which policy? | AetherMesh (key registry), AetherProof (review roles) | Medium |
| **AetherRuntime** | Live monitoring and rollback | Are agents behaving acceptably while running? | AetherFlow (operational verification) | High |

**AetherGovern is a candidate for addressing the authorization gap, provided it passes the falsification criteria (F1–F5).** No claim is made that the other two candidates are weaker.

---

## 🏛️ AetherGovern: Architecture

*All of this is hypothesis: a specification-level description of what a governance dimension might contain.*

### The Five Governance Layers

<p align="center">
  <img src="docs/figures/Fig2_Governance_Layers.png"
       alt="AetherGovern — The Five Layers"
       width="100%">
</p>

<p align="center">
  <em>Figure 2 — The five layers of AetherGovern (hypothesis). Ordering reflects conceptual dependency, not an enforcement hierarchy.</em>
</p>

| Layer | Question | Objects | Operations | Design requirement (hypothesis) |
|:-:|---|---|---|---|
| **1 — Authorization** | Who may act? | Agent identity; action; resource; scope; delegation certificate | grant, present, verify | Every admitted action carries a verifiable chain of authority for its scope |
| **2 — Policy** | Under which rules? | Policy document; policy version; approval record | propose, approve, enforce, supersede | Policy changes are themselves actions subject to authorization |
| **3 — Accountability** | Who is responsible? | Action record; chain of authority; signature; hash link | record, link, query | Each admitted action can be attributed to a chain of agents after the fact |
| **4 — Revocation** | How is authority withdrawn? | Revocation record; revocation frontier; epoch | revoke, propagate, cascade | Revocation is monotone and dependent grants lapse with their parents |
| **5 — Dispute Resolution** | How are conflicts resolved? | Conflicting claims; precedence rule; escalation record | detect, apply rule, escalate | Conflicts are resolved by a deterministic rule or an explicit escalation |

### The Policy Lifecycle

<p align="center">
  <img src="docs/figures/Fig3_Policy_Lifecycle.png"
       alt="AetherGovern — The Policy Lifecycle"
       width="100%">
</p>

<p align="center">
  <em>Figure 3 — The policy lifecycle in AetherGovern (hypothesis): creation, approval, enforcement, revocation. Schematic; not a protocol specification.</em>
</p>

### Authority Delegation

<p align="center">
  <img src="docs/figures/Fig4_Authority_Delegation.png"
       alt="AetherGovern — Authority Delegation"
       width="100%">
</p>

<p align="center">
  <em>Figure 4 — Authority delegation via cryptographic signature chains in AetherGovern (hypothesis). Verification includes scope attenuation, expiry, and a revocation check.</em>
</p>

### Governance vs. Verification

<p align="center">
  <img src="docs/figures/Fig5_Governance_vs_Verification.png"
       alt="AetherGovern — Governance vs. Verification"
       width="100%">
</p>

<p align="center">
  <em>Figure 5 — Governance versus verification in the Aether family. Orthogonality is a hypothesis tested as failure condition F2; the figure was redrawn for this record.</em>
</p>

---

## 📜 Propositions

> [!NOTE]
> *Status: Stated with proof sketches; **not machine-checked**.*

| # | Proposition | Statement | Bears on |
|:-:|---|---|:-:|
| **P1** | Determinism of Causal-Authority Admission | If the admission predicate for an action consists of signature, attenuation, expiry, root recognition, and revocation checks evaluated at the revocation frontier cited by the action, and the cited frontier and policy version are in the action's causal closure, then the verdict is a deterministic function of the action and its causal closure, and the predicate satisfies assumption A6 of AetherMesh. | F4 |
| **P2** | Monotonicity of Revocation | Let `valid(c, F)` denote "chain c is valid at frontier F". If `F ≤ F'` then `valid(c, F') ⇒ valid(c, F)`. Equivalently, validity is antitone in the revocation frontier, and the revocation set can be maintained as a grow-only set whose join is union. | F4 |

<details>
<summary><b>What the proof sketches do <u>not</u> show</b></summary>

- **P1** assumes that the root-of-authority set is common knowledge among honest nodes and is itself part of the closure. It guarantees determinism, not security: an action that cites a stale frontier is admitted at every honest node even if a later revocation exists. It does not address clock manipulation.
- **P2** is good news for decentralization, because revocation requires no coordination to record. The cost is in timeliness: an exposure window remains (Section 5.3.2).

</details>

---

## 🔗 Interfaces with the Aether Family

| Dimension | Requires from it | Provides to it | Coupling |
|---|---|---|---|
| **AetherGit** | Fields for authority and policy references; append-only governance records | Authorship authorization verdict | Low-medium |
| **AetherFlow** | Admission hook before verification; role for remediation | Authorization verdicts; remediation authority | Medium |
| **AetherProof** | Designation of governed specification changes | Authority for specification change; checkable policies | Medium |
| **AetherMesh** | Delta replication of governance records; determinism-compatible predicate | Registry with delegation, rotation, revocation | High |

**Minimal interface (four artifacts, one rule):** a delegation certificate record, a revocation record, an authority-frontier reference carried in each action, and the requirement that the authorization predicate satisfy Proposition 1.

> [!IMPORTANT]
> If the minimal interface is all that is needed, the whole contribution might be an extension of AetherMesh. The case for a standalone dimension rests on the layers beyond the minimal interface (policy, accountability, dispute resolution) being separable and valuable. That is a hypothesis for which this paper has no evidence.

---

## 📊 Evaluation (Proposed)

> [!IMPORTANT]
> **No evaluation has been performed.** This section specifies how the candidate would be evaluated, in a form that fixes in advance what outcomes would count as failure. Every metric, baseline, and threshold is a proposal.

### Evaluation Metrics

| ID | Metric | Definition | Direction |
|:-:|---|---|---|
| **M1** | Unauthorized-action admission rate | Fraction of actions by agents lacking valid authority that are admitted | Lower is better |
| **M2** | Exposure count | Number of actions citing revoked authority that are admitted after the revocation is issued | Lower is better |
| **M3** | Exposure duration | Time from revocation issue to its receipt at each honest node (median, 99th percentile) | Lower is better |
| **M4** | Attribution completeness | Fraction of admitted actions for which the responsible chain can be recovered | Higher is better |
| **M5** | Attribution accuracy | Fraction of recovered chains that match the ground truth | Higher is better |
| **M6** | False-rejection rate | Fraction of legitimate actions rejected by governance checks | Lower is better |
| **M7** | Dispute handling | Median time to resolve conflicting claims | Lower is better |
| **M8** | Admission overhead | Added admission latency, CPU, storage per action | Lower is better |
| **M9** | Convergence preservation | Count of runs in which honest nodes end with different admitted sets | Must be zero if P1 holds |

### Baselines

| ID | Baseline | What it tests |
|---|---|---|
| **B1** | No authority checks beyond AetherMesh admission | Value of any governance mechanism |
| **B2** | Static registry with periodic refresh | Whether simple key rotation suffices (F1) |
| **B3** | Centralized access control | Cost and benefit of decentralization vs. central authority (F4) |
| **B4** | Expiring bearer grants without revocation | Whether expiry alone bounds the exposure window |
| **B5** | Minimal-interface governance | Whether layers beyond the minimal interface add value |

---

## ⚠️ Threats and Limitations

### Threats to Validity

| Type | Threat | Status |
|---|---|---|
| **Internal** | Same author proposes the candidate, the failure conditions, the baselines, and the thresholds | Pre-registration; invite external review |
| **Internal** | Weak or straw-man baselines | Include B2, B4, B5; report B3 as a ceiling |
| **Construct** | "Unauthorized action" and "harm" are simulated by the experimenter | State explicitly; M1–M2 count policy violations, not harm |
| **Construct** | Attribution accuracy (M5) measured against a ground truth that exists only in simulation | Report as an upper bound |
| **External** | Simulated network, simplified adversary, synthetic workload | No generalization claimed |
| **Conclusion** | Few scenario classes; thresholds are proposals | Report all outcomes |
| **Literature** | Access-control literature not reviewed | Acknowledge; review needed before any strong claim (Q2) |

### Architectural Limitations

- The architecture provides **eventual, not strong**, consistency.
- It offers **no global order**.
- It filters only **predicate-detectable** invalid deltas.
- It assumes a **trustworthy key registry**.
- It **grows without compaction**.

### Design Limitations

- The **compatibility matrix**, **digest form**, **fanout policy**, **forwarding policy**, and **compaction** are **underspecified**.
- The **determinism requirement** is **not enforced mechanically**.
- **Dynamic membership**, **access control beyond key registration**, **privacy of deltas**, and **integration with the other layers** are not treated.

### When **Not** to Use AetherGovern

| Scenario | Reason |
|---|---|
| **Small, co-located teams or few agents** | A conventional central repository has lower complexity. |
| **Strong consistency requirements** | Unique-name allocation, exactly-once external effects, release gating, and any operation that needs a global order are not expressible as join-semilattice updates. |
| **Validity must hold before visibility** | If a merged program must be known to be correct before any agent can observe it, a gate before merge is required; AetherGovern admits deltas on syntactic and compatibility grounds only. |
| **Adversarial settings beyond the stated threat model** | Where colluding or well-funded adversaries are expected, a lightweight filter is insufficient. |
| **Constrained nodes** | Because the delta set grows without compaction (Q9), nodes with small storage budgets may not be able to hold replicas. |

---

## 📋 Research Status Statement

| Item | Status |
|---|---|
| Document type | Research article: structured investigation of an architectural hypothesis |
| Version / record | 0.1.0, November 2026 · AETHERGOVERN-01 · DOI 10.5281/zenodo.24054524 |
| Project status | **Not a committed project**; final structure (single, dual, or triple) undetermined |
| Implementation | None claimed |
| Real-world deployment | None; none evaluated |
| Empirical results | None reported |
| Propositions 1–2 | Stated with proof sketches; not machine-checked |
| F1–F4 | **Not falsified by argument alone**, with residual weaknesses; provisional |
| F5 | **Untested** |
| AetherGovern | **A candidate** for addressing the authorization gap, provided it passes F1–F5; **not a confirmed dimension** |
| Review status | Not peer reviewed; the four companion papers are likewise unreviewed preprints |

<details>
<summary><b>Reconciliation notes</b></summary>

1. **Failure conditions.** The brief named F1–F5 but did not define them. The definitions, the requirement list R1–R6, and the decision rule are the writer's proposals and should be confirmed or replaced by the author.
2. **AetherMesh DOI.** The supplied reference list gave `10.5281/zenodo.24053492` for AetherMesh (v2.0.0), whereas the DOI supplied for the AetherMesh paper was `10.5281/zenodo.24038038` (v1.0.0). The latter is used throughout; the author should confirm which is correct.
3. **Reference check.** All 25 entries correspond to the intended publications.
4. **Figures.** The five supplied figures were redrawn under their supplied filenames.
5. **Layers versus dimensions.** The supplied text calls the five items "dimensions" and the governance sub-components "layers"; this usage is kept.
6. **Format.** The brief requested Markdown; this record is a PDF, as requested separately.

</details>

**Catalogues:** 20 open questions (Q1–Q20) across authorization, policy, accountability, revocation, dispute resolution, interfaces, and evaluation method. See Appendix C of the [paper](https://doi.org/10.5281/zenodo.24054524).

---

## 🌍 Platforms & Mirrors

| Platform | URL | Role | Status |
|---|---|---|:-:|
| **GitHub** | [gitdeeper15/aethergovern](https://github.com/gitdeeper15/aethergovern) | Source code, issues, PRs | ✅ Active |
| **GitLab** | [gitlab.com/gitdeeper15/aethergovern](https://gitlab.com/gitdeeper15/aethergovern) | Mirror repository | ✅ Active |
| **Codeberg** | [codeberg.org/gitdeeper15/aethergovern](https://codeberg.org/gitdeeper15/aethergovern) | Mirror repository | ✅ Active |
| **Bitbucket** | [bitbucket.org/gitdeeper15/aethergovern](https://bitbucket.org/gitdeeper15/aethergovern) | Mirror repository | ✅ Active |
| **Zenodo** | [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524) | Citable DOI, paper archive | ✅ Published |
| **OSF** | Pending registration | Registration | ⏳ Pending |
| **Website** | [aethergovern.netlify.app](https://aethergovern.netlify.app) | Live documentation | ⏳ (planned) |
| **ORCID** | [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) | Author identity | ✅ Active |

> [!NOTE]
> **PyPI:** Not published. AetherGovern is a hypothesis under investigation; no implementation is claimed.

---

## 🗂️ Project Structure

<details>
<summary><b>Click to expand the repository tree</b></summary>

```text
AetherGovern/
├── docs/
│   ├── figures/
│   │   ├── Fig1_Five_Dimensions.png
│   │   ├── Fig2_Governance_Layers.png
│   │   ├── Fig3_Policy_Lifecycle.png
│   │   ├── Fig4_Authority_Delegation.png
│   │   └── Fig5_Governance_vs_Verification.png
│   └── fifth-layer-study/
│       ├── 01_orchestrate_study.md
│       ├── 02_govern_study.md
│       ├── 03_runtime_study.md
│       └── 04_comparison.md
├── PUBLICATION/
│   ├── AetherMesh_Research_Paper.pdf       (reference)
│   └── AetherGovern_Research_Paper.pdf    (this work)
├── AUTHORS.md
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── INVENTORY.md
├── LICENSE
├── PROJECT_SUMMARY.txt
├── README.md
├── VERSION
├── manifest.json
└── scientific_state.json
```

</details>

---

🕓 Version History

Version Release Focus Status
v0.1.0 2026-11-08 (release) Architectural Hypothesis Under Investigation: 4 definitions, 2 propositions (proof sketches), 5 failure conditions, 20 open questions ✅ Released
(planned) 2027+ Comparative study of the three candidate capabilities; evaluation design; decision on project structure ⏳ Not executed

v0.1.0: hypothesis under investigation. No implementation, no experiment, no measurement. 33-page PDF, 5 figures, 25 references, 20 open questions.

---

📖 Citation

Primary Manuscript — AetherGovern v0.1.0

```bibtex
@techreport{baladi2026aethergovern,
  author       = {Baladi, Samir},
  title        = {AetherGovern: A Falsification-First Investigation of Governance in the Aether Family},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.24054524},
  url          = {https://doi.org/10.5281/zenodo.24054524},
  note         = {Architectural Hypothesis Under Investigation --- Not a committed project.}
}
```

<details>
<summary><b>Related work — AetherGit (Storage Dimension)</b></summary>

```bibtex
@software{baladi2026aethergit,
  author       = {Baladi, Samir},
  title        = {{AetherGit}: Scalable Source Control for Autonomous AI Agents},
  year         = {2026},
  month        = {November},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.23966896},
  url          = {https://doi.org/10.5281/zenodo.23966896}
}
```

</details>

<details>
<summary><b>Related work — AetherFlow (Integration Dimension)</b></summary>

```bibtex
@techreport{baladi2026aetherflow,
  author       = {Baladi, Samir},
  title        = {AetherFlow: Automated Post-Merge Verification and Dynamic Conflict Resolution in Multi-Agent Programming Environments},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.23979129},
  url          = {https://doi.org/10.5281/zenodo.23979129}
}
```

</details>

<details>
<summary><b>Related work — AetherProof (Verification Dimension)</b></summary>

```bibtex
@techreport{baladi2026aetherproof,
  author       = {Baladi, Samir},
  title        = {AetherProof: Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.24013124},
  url          = {https://doi.org/10.5281/zenodo.24013124}
}
```

</details>

<details>
<summary><b>Related work — AetherMesh (Decentralization Dimension)</b></summary>

```bibtex
@software{baladi2026aethermesh,
  author       = {Baladi, Samir},
  title        = {{AetherMesh}: Decentralized Peer-to-Peer Agent Synchronization and State CRDTs},
  year         = {2026},
  month        = {November},
  version      = {2.0.0},
  doi          = {10.5281/zenodo.24053492},
  url          = {https://doi.org/10.5281/zenodo.24053492}
}
```

</details>

---

👤 Author

Samir Baladi
Interdisciplinary AI Researcher — Ronin Institute / Rite of Renaissance

 
Research Area Distributed Systems / Software Engineering / Institutional Analysis
Research Domain Governance, Authority, Policy, Accountability, Revocation, Dispute Resolution, Multi-Agent Systems, Falsification-First Methodology
Research Type Architectural Hypothesis Under Investigation (v0.1.0)
📧 Email gitdeeper@gmail.com
🔗 ORCID 0009-0003-8903-0029
🐙 GitHub gitdeeper15/aethergovern
🦊 GitLab gitlab.com/gitdeeper15/aethergovern
🟦 Codeberg codeberg.org/gitdeeper15/aethergovern
🪣 Bitbucket bitbucket.org/gitdeeper15/aethergovern
🌐 Official Site aethergovern.netlify.app (planned)

---

⚖️ License

Scope License
Code MIT License — Copyright © 2026 Samir Baladi
Documentation, manuscript, and figures CC-BY-4.0

<details>
<summary><b>MIT License — full text</b></summary>

```text
MIT License

Copyright (c) 2026 Samir Baladi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

</details>

---

<div align="center">

AetherGovern — Program Manuscript v0.1.0 (Architectural Hypothesis Under Investigation)

© 2026 Samir Baladi — Ronin Institute / Rite of Renaissance — MIT (code) + CC-BY-4.0 (docs)

Zenodo ·
Website (planned) ·
OSF: pending

</div>
