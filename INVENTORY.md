# AetherMesh — Complete Inventory

**Version:** 2.0.0 (reference implementation) + 1.0.0 (formal architecture)
**Release Date:** 2026-11-08
**Author:** Samir Baladi
**Email:** gitdeeper@gmail.com
**ORCID:** [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)
**License:** MIT (code) · CC-BY-4.0 (docs, manuscript, figures)
**Status:** Reference Implementation + Reproducible Experiments (published)
**Record ID:** AETHERMESH-02
**DOI (Zenodo, v2.0.0):** [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038)
**OSF Registration:** [10.17605/OSF.IO/9PE5V](https://doi.org/10.17605/OSF.IO/9PE5V)

---

## Research Status

| Item | Status |
|---|---|
| Document type | Research article + reference implementation |
| Paper (v1.0.0) | Complete (33 pages, PDF) |
| Implementation (v2.0.0) | ✅ Built (`src/aethermesh/`, 15 modules) |
| Tests | ✅ 107 passed, 79% coverage |
| Experiments | ✅ 3/3 completed |
| PyPI package | ✅ Published (`aethermesh 2.0.0`) |
| Real-world deployment | None; no deployed system has been benchmarked |
| Theorems 1–3 | Stated with proof sketches; not machine-checked; conditional on A1–A6 |
| Byzantine evaluation | Limited to malformed deltas |
| Review status | Not peer reviewed |

---

## Repository Links

| Platform | URL | Role | Status |
|----------|-----|------|--------|
| GitHub | https://github.com/gitdeeper15/aethermesh | Primary | ✅ Active |
| GitLab | https://gitlab.com/gitdeeper15/aethermesh | Mirror | ✅ Active |
| Codeberg | https://codeberg.org/gitdeeper15/aethermesh | Mirror | ✅ Active |
| Bitbucket | https://bitbucket.org/gitdeeper15/aethermesh | Mirror | ✅ Active |
| **PyPI** | https://pypi.org/project/aethermesh/2.0.0/ | Python package (`aethermesh 2.0.0`) | ✅ **Published** |
| **Zenodo** | https://doi.org/10.5281/zenodo.24038038 | DOI (v1.0.0 + v2.0.0) | ✅ **Published** |
| **OSF** | https://doi.org/10.17605/OSF.IO/9PE5V | Registration | ✅ **Published** |
| Website | https://aethermesh-web.netlify.app | Live documentation | ✅ Active |
| ORCID | https://orcid.org/0009-0003-8903-0029 | Identity | ✅ Active |

---

## Manuscript Artifact (v1.0.0)

| File | Pages | MD5 | SHA256 |
|---|---|---|---|
| `PUBLICATION/AetherMesh_Research_Paper.pdf` | 33 | `b1d7b2da6dda636871f9d5b3cddd855c` | `bf58c4c3ebb8eb1f3430a7f8fd9d15299065b699f96b61902306f95859e2b7a2` |

---

## Root Files

| File | Purpose | Status |
|------|---------|:-:|
| `.gitignore` | Git ignore rules | ✅ |
| `AUTHORS.md` | Contributors | ✅ |
| `CHANGELOG.md` | Version history (v1.0.0 + v2.0.0) | ✅ |
| `CITATION.cff` | Citation metadata (v2.0.0 + OSF DOI) | ✅ |
| `CONTRIBUTING.md` | Contribution guidelines | ✅ |
| `INVENTORY.md` | This file | ✅ |
| `LICENSE` | MIT + CC-BY-4.0 | ✅ |
| `OSF_REGISTRATION.md` | OSF registration record (DOI: 10.17605/OSF.IO/9PE5V) | ✅ |
| `PROJECT_SUMMARY.txt` | One-page summary (v2.0.0) | ✅ |
| `README.md` | Main documentation (v2.0.0) | ✅ |
| `VERSION` | `2.0.0` | ✅ |
| `manifest.json` | Project manifest (v2.0.0) | ✅ |
| `scientific_state.json` | Scientific state record (v2.0.0) | ✅ |
| `netlify.toml` | Netlify configuration | ✅ |
| `pyproject.toml` | PEP 621 build config (v2.0.0) | ✅ |
| `requirements.txt` | Python dependencies (v2.0.0) | ✅ |
| `upload_aethermesh.py` | PyPI uploader | ✅ |

---

## Directories

| Directory | Contents | Status |
|-----------|----------|:-:|
| `PUBLICATION/` | `AetherMesh_Research_Paper.pdf` (33 pages) | ✅ |
| `docs/` | Documentation | ✅ |
| `docs/figures/` | 5 figures (Fig1–Fig5) | ✅ |
| `docs/v1.0.0/` | 8 markdown files from v1.0.0 paper | ✅ |
| `src/aethermesh/` | Reference implementation (15 modules) | ✅ |
| `tests/` | Test suite (7 files, 107 tests) | ✅ |
| `experiments/` | 3 reproducible experiments | ✅ |
| `REPORTS/v2.0.0/` | Evaluation report | ✅ |
| `DATA/` | (empty) | — |
| `ANALYSIS/` | (empty) | — |
| `EXTERNAL_REVIEW/` | (empty) | — |
| `VALIDATION/` | (empty) | — |

---

## Source Code (`src/aethermesh/`)

| Module | File | Purpose |
|---|---|---|
| `__init__.py` | 1 | Package definition |
| `__version__.py` | 1 | Version info |
| `models.py` | 1 | Delta, Replica, Signature, Verdict, DeltaKind, PeerView |
| `crdt/semilattice.py` | 1 | Join-semilattice |
| `crdt/delta_state.py` | 1 | Delta-state CRDT |
| `gossip/protocol.py` | 1 | Anti-entropy exchange (5 steps) |
| `gossip/peer_sampling.py` | 1 | Randomized peer selection |
| `bft/provenance.py` | 1 | Ed25519 signatures |
| `bft/invariants.py` | 1 | Structural invariants |
| `bft/semantic_matrix.py` | 1 | Compatibility matrix |
| `admission/pipeline.py` | 1 | Four-check pipeline |
| `simulation/network.py` | 1 | Fair-lossy network model |
| `simulation/node.py` | 1 | Simulated agent |
| `simulation/testbed.py` | 1 | Full testbed |
| `cli.py` | 1 | CLI |

**Total:** 15 modules, ~1,100 lines.

---

## Test Suite (`tests/`)

| File | Tests | Coverage |
|---|:-:|:-:|
| `test_models.py` | 19 | 93% |
| `test_crdt.py` | 15 | 84% |
| `test_gossip.py` | 15 | 97% |
| `test_bft.py` | 21 | 96% |
| `test_admission.py` | 19 | 92% |
| `test_simulation.py` | 18 | 94% |
| **Total** | **107** | **79%** |

---

## Experiments (`experiments/`)

| # | Directory | Metric | Results |
|:-:|---|---|:-:|
| 1 | `convergence_latency/` | State convergence latency | ✅ `results.json` |
| 2 | `conflict_resolution/` | Conflict resolution overhead | ✅ `results.json` |
| 3 | `fault_resilience/` | Fault resilience | ✅ `results.json` |

---

## Figures

| File | Figure | Description |
|---|:-:|---|
| `docs/figures/Fig1_Tripartite_Architecture.png` | Fig 1 | Tripartite architecture |
| `docs/figures/Fig2_CRDT_Join_Semilattice.png` | Fig 4 | CRDT join-semilattice |
| `docs/figures/Fig3_Gossip_Propagation.png` | Fig 8 | (a) Dampening, (b) latency |
| `docs/figures/Fig4_BFT_Validation.png` | Fig 7 | Byzantine admission pipeline |
| `docs/figures/Fig5_Aether_Family.png` | Fig 2 | Aether family (4 layers) |

---

## Companion Works

AetherMesh is the **fourth layer** (decentralization) of the Aether family:

| Layer | System | DOI |
|---|---|---|
| Storage | AetherGit | [10.5281/zenodo.23966896](https://doi.org/10.5281/zenodo.23966896) |
| Integration | AetherFlow | [10.5281/zenodo.23979129](https://doi.org/10.5281/zenodo.23979129) |
| Verification | AetherProof | [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124) |
| **Decentralization** | **AetherMesh** (this work) | [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038) |

---

## Publication & Registration

| Platform | Identifier | Status |
|---|---|---|
| **Zenodo (DOI)** | [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038) | ✅ Published (v1.0.0 + v2.0.0) |
| **OSF Registration** | [10.17605/OSF.IO/9PE5V](https://doi.org/10.17605/OSF.IO/9PE5V) | ✅ Published |
| **PyPI package** | [aethermesh 2.0.0](https://pypi.org/project/aethermesh/2.0.0/) | ✅ Published |
| **GitHub release** | [v2.0.0](https://github.com/gitdeeper15/aethermesh/releases/tag/v2.0.0) | ✅ (tag) |
| **Website** | [aethermesh-web.netlify.app](https://aethermesh-web.netlify.app) | ✅ Active |

---

## Citation

### Software (v2.0.0)

```bibtex
@software{baladi2026aethermesh_v2,
  author       = {Baladi, Samir},
  title        = {{AetherMesh} v2.0.0: Reference Implementation of Decentralized Peer-to-Peer Agent Synchronization and State CRDTs},
  year         = {2026},
  month        = {November},
  publisher    = {PyPI},
  version      = {2.0.0},
  doi          = {10.5281/zenodo.24038038},
  url          = {https://pypi.org/project/aethermesh/},
  note         = {Reference implementation. Available via pip install aethermesh==2.0.0.}
}
```

Paper (v1.0.0)

```bibtex
@techreport{baladi2026aethermesh,
  author       = {Baladi, Samir},
  title        = {AetherMesh: Decentralized Peer-to-Peer Agent Synchronization and State CRDTs for Autonomous Multi-Agent Systems},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.24038038},
  url          = {https://doi.org/10.5281/zenodo.24038038},
  note         = {Formal Architecture Proposal with Simulated Evaluation --- No Real-World Deployment Benchmarked.}
}
```

OSF Registration

```bibtex
@misc{baladi2026aethermesh_osf,
  author       = {Baladi, Samir},
  title        = {{AetherMesh: Decentralized Peer-to-Peer Agent Synchronization and State CRDTs for Autonomous Multi-Agent Systems}},
  year         = {2026},
  month        = nov,
  day          = {8},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/9PE5V},
  url          = {https://doi.org/10.17605/OSF.IO/9PE5V},
  note         = {OSF Preregistration. Associated project: https://osf.io/n59ay}
}
```

---

Contact

· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· Zenodo DOI: 10.5281/zenodo.24038038
· OSF DOI: 10.17605/OSF.IO/9PE5V
· PyPI: pypi.org/project/aethermesh
· Website: aethermesh-web.netlify.app
· GitHub: gitdeeper15/aethermesh

---

Last Updated: 2026-11-08
Current Version: 2.0.0
