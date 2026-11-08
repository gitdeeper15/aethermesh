# AetherMesh — Architectural Foundations (v1.0.0)

**Version:** 1.0.0
**Date:** 2026-11-08
**Status:** Formal Architecture Proposal with Simulated Evaluation
**Source:** Section 3 of the AetherMesh Research Paper (v1.0.0)
**DOI:** [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038)

---

## 1. Purpose and Scope

AetherMesh rests on three pillars that handle, respectively, decentralized mutation, asynchronous transport, and erratic or adversarial participants.

| Pillar | Name | Function |
|:-:|---|---|
| **1** | CRDTs for Code and Metadata DAGs | Decentralized mutation over code and metadata DAGs |
| **2** | Epidemic Gossip Protocols | Asynchronous transport with low-latency, resilient propagation |
| **3** | Lightweight Byzantine Fault Tolerance | Local verification of remote deltas before admission |

This section specifies each pillar and the interfaces between them. Section 4 states the formal properties we ask of the composition.

**Figures referenced:** Figure 3 (anatomy of a node), Figure 5 (anti-entropy exchange), Figure 6 (partition healing), Figure 7 (admission pipeline).

---

## 2. Pillar 1 — CRDTs for Code and Metadata DAGs

### 2.1 State space as a join-semilattice

A replica of the shared codebase must be a value in a set `S` equipped with a join operator.

AetherMesh takes a deliberately conservative route: the replica state is the **set of admitted deltas**, where a delta is a signed, content-addressed record of one change together with pointers to its parent deltas.

Let `D` be the (possibly very large but finite, see assumption A3) universe of deltas that may ever be created. The state space is the power set of `D` ordered by inclusion, with set union as join and the empty set as bottom. This is the **grow-only-set CRDT lifted to deltas**. Its height is `|D|`, so every ascending chain is finite.

The **materialized codebase** (the files an agent actually reads) is then a deterministic function of the delta set: the deltas are linearized by a fixed rule, for example a topological order of the parent DAG with ties broken by delta identifier, and applied in that order. Because the function is deterministic, replicas that hold the same delta set materialize the same codebase.

This construction has a significant advantage and a significant cost:

- **Advantage:** the convergence argument concerns only a set lattice and does not depend on the internal structure of source files.
- **Cost:** convergence of the delta set does not make the materialized program valid. Two deltas that each yield a valid program from a common base may yield an invalid program when both are applied. This is the **semantic-merge gap** noted in Section 2.1, and in AetherMesh it is addressed by the semantic compatibility matrix of Pillar 3, not by the lattice.

Metadata, such as ownership annotations, status labels, or dependency edges, are modeled as additional lattice components, each with its own join:

- **Observed-remove sets** for membership-style metadata
- **Last-writer-wins registers** (ordered by a logical timestamp and an agent identifier as tie-breaker) for single-valued metadata
- **Grow-only maps** for append-only records

The product of join-semilattices is a join-semilattice with component-wise join, so the replica state remains a single lattice.

### 2.2 Join properties

| Property | Law | Operational consequence |
|---|---|---|
| Commutative | `s₁ ⊔ s₂ = s₂ ⊔ s₁` | Order in which two replicas are merged does not matter. |
| Associative | `(s₁ ⊔ s₂) ⊔ s₃ = s₁ ⊔ (s₂ ⊔ s₃)` | Batching and grouping of merges does not matter. |
| Idempotent | `s₁ ⊔ s₁ = s₁` | Duplicate delivery of a delta is harmless. |
| Inflationary (derived) | `s ⊆ s ⊔ t` | State never moves down the lattice; there is no rollback. |

**Figure 4** (`Fig2_CRDT_Join_Semilattice.png`) shows a seven-element example of a bounded join-semilattice as a Hasse diagram. The join of `s₁` and `s₃` is top, because the only common upper bound is top. The three join laws were verified on this example by exhaustive enumeration. The figure is an illustration of the algebra, not a model of a real codebase.

### 2.3 State-based, operation-based, and delta-state CRDTs

The choice among CRDT styles is a trade-off between bandwidth and delivery requirements.

| Style | Network requirement | Message size | Role in AetherMesh |
|---|---|---|---|
| State-based | None beyond eventual delivery | Whole state | Fallback for large divergence and for joining nodes |
| Operation-based | Causal, exactly-once delivery | Small | Not used on the wire; operations appear only inside deltas |
| **Delta-state** | Eventual delivery; duplicates and reordering allowed | Proportional to change | **Default** |

AetherMesh therefore uses **delta-state replication as its default**: nodes ship deltas that are themselves lattice elements, so duplication and reordering remain harmless, and fall back to full-state exchange only when a digest comparison indicates that incremental repair would cost more than a state transfer.

### Limitations of this pillar

- The set-of-deltas lattice grows monotonically, so storage grows without bound unless compaction is added; compaction must preserve the join semantics and is **not specified here** (open question Q9).
- Convergence of delta sets does **not** entail semantic validity of the materialized program.
- Tree- and AST-structured CRDTs that merge at finer granularity than whole deltas are cited in Section 2.1 but are **not specified** in this paper.

---

## 3. Pillar 2 — Epidemic Gossip Protocols

### 3.1 Digest vector exchange

Each node periodically selects a small set of peers and reconciles with them. Reconciliation begins with a **digest**, a compact summary of which deltas the node holds.

Three digest forms are compatible with the architecture:

- **Per-origin version vector** — one counter per agent, valid when each agent's deltas are numbered consecutively
- **Merkle-style hash tree** over delta identifiers (Merkle, 1988)
- **Bloom-style probabilistic filter**

Version vectors are exact and cheap when the agent population is small and stable; hash trees locate differences in logarithmic time; filters are smallest but admit false positives, which in this setting cause a delta to be omitted from one exchange and delivered in a later one. The choice is parameterized by **D16** in Appendix C.

The exchange itself has **five steps**, shown in Figure 5:

1. **Initiator digest** — A sends its version summary
2. **Responder digest + difference list** — B replies with its digest and the list of deltas A appears to lack
3. **Delta request** — A requests the missing deltas (if B lacks A's deltas, A pushes)
4. **Delta batch** — B sends the requested deltas, each signed by its origin
5. **Local verification and join** — A verifies each delta through Steps 1–4 of the admission pipeline, then joins admitted deltas

Symmetric work happens at B for any deltas A pushed in step 3.

### 3.2 Randomized peer selection

Every gossip period, a node selects `k` peers (the **fanout**) uniformly at random from its current peer sample.

In a large network, nodes cannot hold the full membership list, so peer selection draws from a continuously refreshed **partial view**, as in peer-sampling services (Jelasity et al., 2005).

**Uniform selection** is what the dissemination analysis assumes (assumption A2); **biased selection**, for example preferring low-latency peers, may improve latency and may **violate the analysis**.

The transmission rate constant `β` in Definition 3 is determined by the fanout `k` and the exchange frequency `r`: increasing either increases `β`. The relationship in the late phase of a push epidemic is derived in Section 4.3.

### 3.3 Exponential dampening and partition healing

The practical significance of exponential dampening is that the **tail** of the dissemination time is thin: the probability that a node is still uninfected after `t` steps falls geometrically, so the time for a node to be reached grows only with the logarithm of the inverse of the tolerated failure probability.

The same mechanism provides **partition healing**:

- During a partition, each side continues to accept local deltas and to gossip internally.
- When connectivity returns, the first cross-partition digest exchange reveals missing deltas on both sides and the join combines them (Figure 6).
- The time to heal is governed by when the first cross-partition exchange occurs and then by the dissemination time inside each side.

### Limitations of this pillar

- Gossip analysis assumes **uniform random peer selection**, **independent selections**, and **reliable enough links**.
- Real networks exhibit correlated failures, non-uniform latency, and NAT and firewall effects that these assumptions do not capture.
- The digest forms listed are compatible with the architecture but **none is specified to the byte level**, and **no bandwidth analysis** is given.

---

## 4. Pillar 3 — Lightweight Byzantine Fault Tolerance

### 4.1 Cryptographic provenance

Every delta carries:

- The identifier of its **originating agent**
- A **digital signature** over the delta's content hash, which in turn covers the delta body and its parent identifiers

A signature scheme such as **Ed25519** (Bernstein et al., 2012) is representative; the architecture does not depend on a particular scheme but **does depend on its unforgeability** (assumption A5).

Each node maintains a **local registry** mapping agent identifiers to public keys. How the registry is bootstrapped, extended, and revoked is a **trust-establishment question that this paper does not settle** (Section 7.4).

Content addressing has a useful side effect: a delta **cannot be altered in transit without changing its identifier**, so tampering is detected by hash mismatch even before signature checking.

### 4.2 Structural invariants

Structural checks verify that a delta is well-formed as a node of the parent DAG:

- The identifier **equals the hash** of the content.
- Every **parent pointer** refers to a delta that the node has already admitted, or else the delta is held in a **bounded deferral buffer**.
- The pointer structure **cannot form a cycle** (guaranteed by content addressing, since a cycle would require a hash fixed point).
- **Size and fan-in bounds** hold.

A delta with **missing parents is deferred, not rejected**, because gossip may deliver a child before its parent. Deferral is bounded in size and time to prevent resource exhaustion (threat T9).

### 4.3 Semantic compatibility matrices

**Schema conformance** checks that the delta body parses against the delta schema.

**Semantic compatibility** goes further: a compatibility matrix `C` assigns to each pair of operation kinds a verdict on whether concurrent deltas of those kinds that touch overlapping targets may coexist.

**Table 3.1** (illustrative — entries are examples, not a normative specification):

| | Edit body | Rename symbol | Delete symbol | Change signature | Edit metadata |
|---|:-:|:-:|:-:|:-:|:-:|
| **Edit body** | ok | ok | conflict | ok | ok |
| **Rename symbol** | ok | resolve (deterministic rule) | conflict | conflict | ok |
| **Delete symbol** | conflict | conflict | ok (idempotent) | conflict | ok |
| **Change signature** | ok | conflict | conflict | resolve (deterministic rule) | ok |
| **Edit metadata** | ok | ok | ok | ok | resolve (LWW) |

A matrix of this kind can be evaluated **locally and cheaply**, which is what makes the admission layer lightweight. It is also **coarse**: it classifies operation kinds, not program behaviour, and it cannot detect semantic breakage that depends on program meaning.

Stronger semantic validation, such as running tests or checking proof obligations, is the province of the integration and verification layers and is **outside the admission path** (Section 6.4).

### 4.4 Admission rule and determinism

> **Admission determinism requirement (our formulation).**
>
> Each admission predicate must be a **pure, deterministic function of the delta and of its causal closure** (the delta together with all of its ancestors), and **not** of any other local state such as arrival order, local clock, or non-causal replica contents. A delta whose causal closure is not yet fully present is **deferred** until it is.

This requirement is what reconciles local verification with convergence. If predicates could depend on arbitrary local state:

- Two honest nodes could reach different verdicts on the same delta.
- They could admit different subsets.
- And they would **diverge permanently**; the lattice would then converge on different sets.

Restricting predicates to the causal closure makes verdicts identical at every honest node that has the closure, so **all honest nodes eventually hold the same admitted set**.

The cost is **expressiveness**: some useful checks, such as rate limits per origin and per-node resource policies, are inherently local. AetherMesh treats these as **delivery policies** that may delay a delta but do **not permanently reject** it, so they do not change the eventual admitted set.

### 4.5 Admission pipeline (Figure 7)

| Step | Check | Evidence required | Typical failure | Verdict on failure |
|:-:|---|---|---|---|
| 1 | **Signature** | Valid signature by a registered key over the content hash | Forged or unsigned delta; unknown origin | Reject |
| 2 | **DAG integrity** | Id equals content hash; parents present; size bounds | Hash mismatch; oversized delta; missing parents | Reject (mismatch, bounds); defer (missing parents) |
| 3 | **Schema** | Body parses against the delta schema | Malformed fields | Reject |
| 4 | **Semantics** | Compatibility matrix verdict over the causal closure | Incompatible concurrent operation | Reject or quarantine, as configured |

### Limitations of this pillar

- The admission layer detects **only violations of predicates that were specified in advance**.
- A delta that is correctly signed, well-formed, and compatible, yet **harmful**, is admitted.
- The determinism requirement is a **design constraint on predicate authors**; this paper provides **no mechanism that enforces it**, and a predicate that violates it can break convergence.
- The compatibility matrix in Table 3.1 is **illustrative**.

---

## 5. Interface Requirements

AetherMesh places only two minimal interface requirements on the layers below it:

| Layer | System | What AetherMesh requires from it |
|---|---|---|
| Storage | **AetherGit** | An **append-only changeset log** with parent pointers |
| Integration | **AetherFlow** | A **message-based protocol** over which agents submit changes and receive notifications |

**Verification (AetherProof):** Nothing mandatory. Proof evidence, if present, may be carried as delta metadata and consulted by semantic predicates.

The four layers are **methodologically independent**: AetherMesh imposes only the two minimal interface requirements above. In particular, we do **not rely on any implementation** of the sibling layers. Where the text mentions a changeset log or a message protocol, it means only the abstract interface described here.

---

## 6. Summary

| Pillar | Mechanism | Guarantee (under A1–A6) |
|:-:|---|---|
| **1** | CRDT join-semilattice | Order-independence, idempotence, eventual convergence |
| **2** | Epidemic gossip | Exponential dampening of dissemination latency |
| **3** | Lightweight BFT | Blocking of predicate-detectable invalid deltas |

Each guarantee is **conditional on stated assumptions** and is **stated with a proof sketch, not machine-checked**. See `03_formal_model.md` for the formal definitions and theorems.

---

**End of Architectural Foundations (v1.0.0).**
