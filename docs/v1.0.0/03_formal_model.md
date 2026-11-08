# AetherMesh — Formal Definitions and Mathematical Modeling (v1.0.0)

**Version:** 1.0.0
**Date:** 2026-11-08
**Status:** Formal Architecture Proposal with Simulated Evaluation
**Source:** Section 4 of the AetherMesh Research Paper (v1.0.0)
**DOI:** [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038)

---

## 1. Purpose and Scope

This section gives the formal model of AetherMesh. We first state the assumptions, because **every theorem below is conditional on them**.

Notation is collected in Appendix A of the paper.

---

## 2. Assumptions A1–A6

| ID | Assumption | Used by |
|:-:|---|:-:|
| **A1** | **Fair-lossy channels.** A message sent infinitely often between two non-faulty nodes is delivered infinitely often. (Anti-entropy retransmits implicitly, so each delta is offered repeatedly.) | T1 |
| **A2** | **Fair peer selection.** Each non-faulty node selects every other non-faulty node as a gossip partner infinitely often; for T2, selection is uniform and independent. | T1, T2 |
| **A3** | **Finite delta universe.** The set of deltas that will ever be created is finite, so the lattice has finite height. | T1 |
| **A4** | **Correct replicas.** Non-faulty nodes implement the join and the materialization function correctly and deterministically. | T1 |
| **A5** | **Cryptographic soundness.** The signature and hash schemes are unforgeable and collision-resistant, and the key registry is correct for the origins concerned. | T3 |
| **A6** | **Admission determinism.** Admission predicates are deterministic functions of the delta and its causal closure (Section 3.3.4 of the paper). | T1, T3 |

> **Note on A1.** The supplied statement of Theorem 1 uses "bounded message delay and continuous gossip activity". Bounded delay is a synchrony assumption that is **stronger than needed** for eventual consistency and is **not generally available in open networks**; fair-lossy channels (A1) with continuing gossip suffice for the qualitative convergence claim. Bounded delay becomes relevant only if one wants a **time bound**, which is the role of Section 4.5.

---

## 3. Definition 1 — Convergent State Transition

Let `A = {a₁, a₂, …, aₙ}` be a set of autonomous agents. Each agent maintains a local replica state `R_a(t)` at logical time `t`.

A transition caused by local execution or gossip reception is defined as:

```

R_a(t+1) = R_a(t) ⊔ ⨆_{m ∈ M_a} m                                    (1)

```

Where:

- `R_a(t)` — local replica state of agent `a` at logical time `t`
- `M_a` — set of incoming mutation payloads **that passed admission** during `(t, t+1)`
- `⊔` — binary join operator
- `⨆` — iterated join over the set `M_a`

By **commutativity, associativity, and idempotence**, the order and multiplicity of payloads do not matter.

---

## 4. Definition 2 — CRDT State Space

```

(S, ⊔, ⊥)  bounded join-semilattice,   s_reconciled = s_i ⊔ s_j        (2)

```

Where `⊔` is binary, commutative, associative, and idempotent.

| Property | Law | Operational consequence |
|---|---|---|
| Commutative | `sᵢ ⊔ sⱼ = sⱼ ⊔ sᵢ` | Merge order does not matter |
| Associative | `(sᵢ ⊔ sⱼ) ⊔ sₖ = sᵢ ⊔ (sⱼ ⊔ sₖ)` | Batching and grouping do not matter |
| Idempotent | `sᵢ ⊔ sᵢ = sᵢ` | Duplicate delivery is harmless |
| Inflationary (derived) | `s ⊑ s ⊔ t` | State never moves down the lattice; no rollback |

---

## 5. Definition 3 — Gossip Infection Probability

```

P_uninfected(t) ≈ e^(−β·t)                                             (3)

```

`β` is the **transmission rate constant** determined by fanout `k` and exchange frequency `r`.

---

## 6. Definition 4 — Byzantine Admission Rule

> Before a peer accepts a remote CRDT delta `Δᵢ`, local verification daemons evaluate:
>
> 1. **Cryptographic provenance**
> 2. **Structural invariants**
> 3. **Semantic compatibility matrices**
>
> Only deltas bearing **valid signatures** and satisfying **local predicates** are admitted to the local join-semilattice.

---

## 7. Theorem 1 — Eventual Consistency

### 7.1 Statement

> **Theorem 1 (Eventual Consistency)** — *Stated with proof sketch; not machine-checked; conditional on A1–A6.*
>
> Given continuous gossip activity and channels that eventually deliver, any two non-faulty agents `aᵢ`, `aⱼ` eventually reach an identical state. Given finite height (A3), the limits are attained at a finite time.

### 7.2 Proof sketch

1. Each agent's state evolves monotonically upward in a finite-height lattice (A3).
2. Anti-entropy gossip with fair-lossy channels (A1) and fair peer selection (A2) ensures that every delta eventually reaches every non-faulty node.
3. Correct replicas (A4) implement the join deterministically.
4. Admission determinism (A6) ensures that every honest node admits the same deltas.
5. Therefore, all non-faulty nodes converge to the same supremum:

```

lim_{t→∞} R_{aᵢ}(t) = lim_{t→∞} R_{aⱼ}(t) = ⨆_{m ∈ M*} m

```

where `M*` is the set of all deltas admitted by some non-faulty node.

### 7.3 What the sketch does **not** show

- No **time bound** is given.
- Presumes `M*` is finite (or "eventually" is read relative to a fixed prefix).
- Presumes A6, which a predicate author could violate.
- Concerns **non-faulty nodes only**.
- Says nothing about **semantic validity** of the materialized program.
- Treats the **agent set as fixed**.

---

## 8. Theorem 2 — Exponential Dampening of Gossip Latency

### 8.1 Statement

> **Theorem 2 (Exponential Dampening)** — *Stated with proof sketch; not machine-checked; conditional on A2.*
>
> Under the constant-hazard model, `P_uninfected(t) = (1−p)^t ≈ e^(−βt)` with `β = −ln(1−p) ≈ p` for small `p`. A statement about the **tail** of the dissemination.

### 8.2 Proof sketch

In each gossip step a node participates in exchanges with randomly chosen peers. Under independence, the probability of not being infected in a step is `1 − p`, and over `t` independent steps:

```

(1 − p)^t = exp(t · ln(1 − p)) = e^(−βt)   with   β = −ln(1 − p)

```

### 8.3 Interpretation and the limits of the model

The constant-hazard model is an **approximation**: in a real epidemic the per-step infection probability of an uninfected node depends on the infected fraction `i(t)`, which starts near zero.

In a push protocol with fanout `k` and `n` nodes:

- An uninfected node escapes all `k·i·n` pushes of a step with probability `(1 − 1/n)^(k·i·n) = e^(−k·i)`.
- So the hazard is `1 − e^(−k·i)`.
- In the **late phase**, when `i` is close to 1, the uninfected fraction is multiplied by approximately `e^(−k)` per step, which identifies `β = k` per step for push gossip (Pittel, 1987; Demers et al., 1987).
- **Push-pull** exchanges can shrink the uninfected fraction faster than geometrically in the late phase (Karp et al., 2000).
- In the **early phase**, the infected population grows roughly by a factor of `(1 + k)` per step, so reaching a constant fraction takes about `log_{1+k} n` steps.

**Theorem 2 should therefore be read as a statement about the tail** of the dissemination. The curves in Figure 8(a), drawn for `β = 0.3, 0.5, 0.8`, are analytic illustrations of Equation (3), **not data**.

---

## 9. Theorem 3 — Byzantine Fault Tolerance Bound

### 9.1 Statement

> **Theorem 3 (Byzantine Fault Tolerance Bound)** — *Stated with proof sketch; not machine-checked; conditional on A5, A6.*
>
> If the number of Byzantine agents `f` satisfies `f < n/3`, then the local verification predicates at each honest node block all **predicate-detectable** invalid deltas with probability approaching 1.

"Invalid" here means **predicate-detectable**: failing at least one predicate of Definition 4.

### 9.2 Proof sketch — Part (a): deterministic filtering

Each honest node evaluates the predicates independently on each received delta.

- By **A5**, a delta without a valid signature from a registered key cannot be produced by a node that lacks the key.
- By **content addressing**, any alteration is detected.
- By **A6**, the structural and semantic verdicts are the same at every honest node.

A predicate-detectable invalid delta is therefore rejected at every honest node with probability 1, **independently of `f`**.

### 9.3 Proof sketch — Part (b): the role of `f < n/3`

The bound `n > 3f` of classical Byzantine agreement (Lamport et al., 1982; Castro and Liskov, 1999) enters when a decision **cannot be made locally** and must rely on a **quorum**, for example when key-registry updates or non-locally-checkable semantic predicates are decided by attestations from a committee.

Suppose a committee of `m` members is drawn uniformly at random and a delta is accepted on a **majority** of attestations. If each member is Byzantine with probability at most `1/3` independently (an approximation that is accurate when `m ≪ n`), the **Chernoff–Hoeffding bound** gives:

```

P[Byzantine majority] ≤ exp(−m · D(1/2 ‖ 1/3))

```

where:

```

D(1/2 ‖ 1/3) = ½ ln(3/2) + ½ ln(3/4) = 0.0589

```

### 9.4 Committee bound table (Table 4.1)

| Committee size `m` | Upper bound on P[Byzantine majority] |
|:-:|:-:|
| 25 | 2.29e-01 |
| 50 | 5.26e-02 |
| 100 | 2.77e-03 |
| 200 | 7.67e-06 |
| 400 | 5.88e-11 |

*Values are the output of a formula under stated assumptions, **not simulation results**.*

### 9.5 What the sketch does **not** show

- Does **not** show that invalid deltas **outside** the predicates are blocked — harmful but well-formed deltas from a signed, registered, Byzantine agent are **admitted**.
- Does **not** address colluding Byzantine agents that control a committee.
- Does **not** address **Sybil identities** (Douceur, 2002).
- Does **not** address **key compromise**.
- Does **not** address **denial of service by flooding**.
- **Assumes** the registry (A5) is correct, which is itself a trust-establishment problem.

The supplied sketch connects the statement to the classical `n/3` threshold by saying that honest nodes "form a majority"; we regard the two-part form above as a **more accurate reading**, and we note that this reading makes the `n/3` bound relevant **only to quorum-based decisions**.

---

## 10. Latency Bound (Section 4.5)

For a network of `n` nodes with fanout `k` and gossip round frequency `r` (rounds per second), the **supplied heuristic estimate** of the expected convergence time is:

```

T_convergence = (ln n) / (k · r)                                       (4)

```

With `n = 250`, `k = 5`, and `r = 10 Hz`:

```

T_convergence = ln(250) / (5 · 10) = 0.11 s = 110 ms

```

### 10.1 Two limitations

This is a **scaling estimate, not a theorem**, and it has two limitations:

1. **Dimensional.** It is dimensionally a count of `ln n` over `k` rounds divided by `r`, and it **omits the dependence on the early-phase growth factor**: the standard analysis of push gossip gives a round count of approximately `ln n · (1/ln(1+k) + 1/k)`, the sum of the early and late phases.
2. **Omissions.** It omits network delay, processing time, and the admission pipeline's latency, which Section 5 shows to be **not negligible** in the simulation.

### 10.2 Comparison with reported simulation values (Table 4.2)

| Nodes `n` | Reported (simulation), ms | Eq. (4), ms | Refined push estimate, ms | Reported / Eq. (4) |
|:-:|:-:|:-:|:-:|:-:|
| 10 | 45 | 46 | 175 | 1.0× |
| 50 | 120 | 78 | 297 | 1.5× |
| 100 | 210 | 92 | 349 | 2.3× |
| 250 | 420 | 110 | 419 | 3.8× |
| 500 | 680 | 124 | 471 | 5.5× |

*Eq. (4): `T ≈ (ln n)/(k·r)` with illustrative `k = 5`, `r = 10 Hz`. Computed by us from the formulas; **not simulation output**.*

The table shows that the supplied Equation (4):

- **agrees with the first reported point** (n=10)
- **underestimates the rest** by an increasing factor
- up to **5.5× at n = 500**

The **refined estimate** happens to coincide with the reported value at `n = 250` (419 ms versus 420 ms), but it does **not** track the reported values at other sizes (175 ms against 45 ms at n=10; 471 ms against 680 ms at n=500). We regard the coincidence at one point as **uninformative** and do **not** use it as support.

---

## 11. Summary of formal results

| Item | Statement | Status | Assumptions |
|:-:|---|---|:-:|
| **T1** | Eventual Consistency | Proof sketch, not machine-checked | A1–A6 |
| **T2** | Exponential Dampening | Proof sketch, not machine-checked | A2 |
| **T3** | Byzantine Bound | Proof sketch, not machine-checked | A5, A6 |
| **Eq. (4)** | Latency heuristic | Not a theorem; **does not match** reported values across sizes | — |

### Limitations of this section

- The three theorems are **proof sketches**.
- None has been checked mechanically, and a mechanized proof of Theorem 1 over a specified model of channels and fairness would be a natural next step (**Q1**).
- The constant-hazard model of Theorem 2 is an **idealization**.
- Theorem 3 is conditional on a predicate set that is **not enumerated here**, on a correct key registry, and, in part (b), on an independence approximation for committee sampling.
- The latency estimate is **heuristic** and, as Table 4.2 shows, does **not reproduce** the reported simulation values across sizes.

---

**End of Formal Definitions and Mathematical Modeling (v1.0.0).**
