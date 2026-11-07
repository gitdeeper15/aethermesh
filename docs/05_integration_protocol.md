# AetherProof — Document 05: Integration Protocol

**Version:** 1.0.0-draft
**Date:** 2026-11-06
**Status:** Draft for review
**Author:** Samir Baladi
**Project:** AetherProof — Autonomous Formal Verification and Invariant Synthesis for Multi-Agent Software Ecosystems

---

## 1. Purpose and Scope

This document defines the **integration protocol** between AetherProof and AetherFlow.

Its purpose is **not** to specify shared implementation, nor to couple the projects at the code level. Its purpose is to establish:

1. A **message-based protocol** for cross-system communication.
2. **Message types** for each interaction (admission, verification, remediation, escalation).
3. **Version negotiation** to allow the two systems to evolve independently.
4. **Failure semantics** when one system is unavailable.
5. **Security and trust** considerations at the boundary.
6. **Open questions** specific to cross-system integration.

This document is scoped to protocol design. Implementation details are deferred.

---

## 2. Figures

- **Figure 1** — `Fig1_Three_Layer_Architecture.png`
  The three-layer architecture showing AetherProof and AetherFlow as distinct layers.

- **Figure 2** — `Fig2_CSR_Record_Structure.png`
  CSR records are exchanged via protocol.

- **Figure 3** — `Fig3_Semantic_Relations_Graph.png`
  Semantic relations cross the protocol boundary.

- **Figure 4** — `Fig4_Two_Axis_Classification.png`
  Translation classifications cross the protocol boundary.

- **Figure 5** — `Fig5_TCB_Manifest.png`
  TCB Manifests are exchanged as proof evidence.

---

## 3. Design Principles

### 3.1 Protocol-Based, Not Code-Based

AetherProof and AetherFlow communicate via **messages**, not shared libraries.

**Rationale**: Each system can evolve independently. A change in AetherProof's internal algorithms does not break AetherFlow, as long as the protocol is respected.

### 3.2 Asynchronous, Not Blocking

Communication is **asynchronous**. Neither system blocks waiting for the other.

**Rationale**: AetherProof may take minutes to discharge an obligation; AetherFlow cannot block admission.

### 3.3 Versioned, Not Frozen

The protocol carries a **version number**. Each system declares its supported protocol versions.

**Rationale**: Allows the two systems to be upgraded independently.

### 3.4 Failure-Tolerant, Not Failure-Free

The protocol specifies **failure semantics** for every message type.

**Rationale**: Systems fail. The protocol must handle failure without corrupting state.

---

## 4. Message Types

### 4.1 Message Envelope

Every message has the form:

```

Envelope = (
version: ProtocolVersion,
message_id: Identifier,
timestamp: Timestamp,
source: SystemID,
destination: SystemID,
payload: MessagePayload
)

```

### 4.2 Message Catalogue

| # | Message | Direction | Purpose |
|---|---------|-----------|---------|
| M1 | `changeset_admitted` | AetherFlow → AetherProof | Notify AetherProof of a new changeset |
| M2 | `verification_request` | AetherFlow → AetherProof | Request proof of a property |
| M3 | `verification_result` | AetherProof → AetherFlow | Return proof verdict and evidence |
| M4 | `counterexample_found` | AetherProof → AetherFlow | Notify of a refuted property |
| M5 | `remediation_patch` | AetherProof → AetherFlow | Submit a remediation patch |
| M6 | `escalation` | AetherProof → AetherFlow | Escalate a case to human review |
| M7 | `evidence_query` | AetherFlow → AetherProof | Query for existing evidence |
| M8 | `evidence_response` | AetherProof → AetherFlow | Return existing evidence |
| M9 | `health_check` | Both | Verify liveness |
| M10 | `version_negotiation` | Both | Negotiate protocol version |

### 4.3 Payload Examples

#### M1 — `changeset_admitted`

```json
{
    "changeset_id": "cs-2026-11-06-001",
    "parent_ids": ["cs-2026-11-06-000"],
    "delta_hash": "abc123...",
    "timestamp": "2026-11-06T14:00:00Z"
}
```

M2 — verification_request

```json
{
    "obligation_id": "O-001",
    "property": "queue_length ≤ MAX",
    "assumptions": ["A1: MAX > 0"],
    "source_csr": "csr-L1-001",
    "preferred_paths": ["TLA+", "Why3", "Lean"]
}
```

M3 — verification_result

```json
{
    "obligation_id": "O-001",
    "verdict": "Proven",
    "evidence_type": "proof_term",
    "evidence_artifact": "path/to/proof",
    "tcb_manifest": {
        "tool": "TLAPS",
        "version": "1.4.0",
        "backend_provers": ["zenon", "isabelle"],
        "timestamp": "2026-11-06T14:02:00Z"
    }
}
```

M4 — counterexample_found

```json
{
    "obligation_id": "O-002",
    "counterexample": {
        "witness": "queue_length = MAX + 1",
        "refutation_evidence": "path/to/model",
        "type": "code_defect"
    }
}
```

M5 — remediation_patch

```json
{
    "counterexample_id": "C-001",
    "patch": {
        "files": ["src/main.py"],
        "diff": "...",
        "justification": "Fixed off-by-one error"
    },
    "guardrails_passed": ["test_integrity", "assertion_integrity"]
}
```

M6 — escalation

```json
{
    "escalation_id": "E-001",
    "reason": "Iteration bound reached",
    "diagnosis_history": [...],
    "patch_attempts": [...]
}
```

---

5. Version Negotiation

5.1 Protocol Version

The protocol version follows Semantic Versioning: MAJOR.MINOR.PATCH.

Version Meaning
MAJOR Breaking change (incompatible message formats)
MINOR New message types (backward-compatible)
PATCH Bug fixes (backward-compatible)

5.2 Negotiation

1. Both systems declare their supported versions on startup.
2. The highest common MAJOR.MINOR is selected.
3. If no common version exists, the systems refuse to communicate.

5.3 Backward Compatibility

· MINOR versions: New messages are ignored by systems that do not support them.
· PATCH versions: No compatibility impact.
· MAJOR versions: Require negotiation or fallback.

---

6. Failure Semantics

6.1 Failure Modes

Failure Detection Response
AetherProof unavailable Health check timeout AetherFlow continues without proof (degraded)
AetherFlow unavailable Health check timeout AetherProof queues messages (bounded)
Message lost No acknowledgment Retry with exponential backoff
Message corrupted Hash mismatch Reject and log
Version mismatch Negotiation failure Refuse communication

6.2 Degraded Mode

If AetherProof is unavailable:

· AetherFlow continues admission and verification (its core function).
· Proof obligations are queued in AetherProof's inbox.
· When AetherProof returns, queued obligations are processed.

No data loss: messages are durably stored.

6.3 Bounded Queues

Both systems maintain bounded queues. If a queue is full:

· New messages are rejected.
· The sender is notified (backpressure).
· The sender retries later.

---

7. Security and Trust

7.1 Authentication

· Messages are signed by the sender's key.
· The receiver verifies the signature before processing.

7.2 Authorization

· AetherProof can only submit remediation patches (it cannot modify code directly).
· AetherFlow can only request verification (it cannot modify CSR records).
· Human review is required for specification changes (Document 04, §4.3).

7.3 Audit

· Every message is logged with sender, timestamp, and hash.
· The audit log is append-only and tamper-evident.
· Audit logs are shared between AetherProof and AetherFlow.

7.4 Trust Boundaries

Boundary Trust Level
AetherFlow ↔ AetherProof Medium (protocol-based, authenticated)
AetherProof ↔ External tools Low (tools are treated as untrusted)
AetherProof ↔ Human High (human review is authoritative)
AetherProof ↔ CSR Store High (CSR Store is a trusted component)

---

8. Integration Examples

8.1 Example 1: Successful Verification

```
1. AetherFlow admits cs-001.
2. AetherFlow sends M1 (changeset_admitted) to AetherProof.
3. AetherProof identifies an affected obligation O-001.
4. AetherProof sends M2 (verification_request) to itself (internal).
5. AetherProof discharges O-001 via TLA+.
6. AetherProof sends M3 (verification_result) to AetherFlow.
7. AetherFlow records the verified status.
```

8.2 Example 2: Refuted Obligation

```
1. AetherFlow admits cs-002.
2. AetherProof identifies O-002 is affected.
3. AetherProof discharges O-002 and gets Refuted.
4. AetherProof sends M4 (counterexample_found) to AetherFlow.
5. AetherProof diagnoses the counterexample (code_defect).
6. AetherProof sends M5 (remediation_patch) to AetherFlow.
7. AetherFlow admits the patch as a new changeset.
8. AetherProof re-verifies O-002 on the patched code.
```

8.3 Example 3: Escalation

```
1. AetherProof cannot resolve a counterexample within 3 iterations.
2. AetherProof sends M6 (escalation) to AetherFlow.
3. AetherFlow notifies a human reviewer.
4. Human reviews the counterexample and the patch attempts.
5. Human provides a decision (accept/reject/revise/defer).
6. AetherFlow relays the decision to AetherProof.
```

---

9. Open Questions

ID Question Status
Q31 What is the minimum protocol version that supports all needed messages? Open
Q32 How should backpressure be communicated between systems? Open
Q33 What is the maximum message size that both systems support? Open
Q34 How should audit logs be merged when the systems are temporarily disconnected? Open
Q35 Can the protocol be extended to support multiple AetherProof instances? Open
Q36 What is the latency SLA for each message type? Open

---

10. Design Decisions and Deferred Commitments

10.1 Decisions Made

ID Decision Rationale
D35 Protocol-based integration, not code-based Methodological independence
D36 Asynchronous communication No blocking
D37 Versioned protocol Independent evolution
D38 Bounded queues Prevents unbounded memory growth
D39 Signed messages Authentication
D40 Shared audit log Accountability
D41 Human review as first-class message Preserves judgment

10.2 Decisions Deferred

ID Deferred Question Deferred To
DD29 Full message schema (JSON Schema) Future work
DD30 Implementation details Future work
DD31 Performance benchmarks Future work
DD32 Deployment architecture Future work
DD33 Multi-instance protocol Future work

---

11. Summary

This document establishes:

1. A message-based protocol for cross-system communication.
2. Message types for each interaction (10 messages).
3. Version negotiation for independent evolution.
4. Failure semantics for degraded mode.
5. Security and trust at the boundary.
6. Integration examples for common scenarios.
7. Open questions specific to cross-system integration.

The governing question of this document is:

What is the minimal message-based protocol that allows AetherProof and AetherFlow to integrate without coupling, while preserving auditability, security, and failure tolerance?

This question is answered structurally by the protocol. Its empirical answer requires future work.

---

Appendix A — Glossary

Term Definition
Envelope The wrapper around every message
Message ID Unique identifier for a message
Protocol version SemVer-compatible version of the protocol
Degraded mode Operation when one system is unavailable
Backpressure Notification that a queue is full

---

Appendix B — References

· Document 01: Specification Language (AetherProof, 2026).
· Document 02: Proof Obligations (AetherProof, 2026).
· Document 03: Incremental Proof Engine (AetherProof, 2026).
· Document 04: Counterexample Remediation (AetherProof, 2026).
· AetherFlow (Baladi, 2026b).
· AetherGit (Baladi, 2026c).

---

End of Document 05 (v1.0.0-draft).
