"""
AetherMesh — Command-line interface.

Provides three subcommands:

    aethermesh simulate   Run a simulated P2P testbed and measure the
                          three metrics from Section 5 of the paper.

    aethermesh info       Print version, DOI, and record information.

    aethermesh verify     Run a quick self-check (join laws, signature
                          verification, admission pipeline) without
                          a full simulation.

Usage:
    python -m aethermesh.cli simulate --nodes 50 --fanout 5
    python -m aethermesh.cli info
    python -m aethermesh.cli verify

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 5.
    Zenodo. https://doi.org/10.5281/zenodo.24038038
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Dict, List, Optional

from aethermesh.__version__ import (
    __version__,
    __author__,
    __email__,
    __doi__,
    __license__,
    __paper_version__,
    __record_id__,
)


# =============================================================================
# Info
# =============================================================================

def cmd_info(args: argparse.Namespace) -> int:
    """Print version, DOI, and record information."""
    print("=" * 60)
    print(f"AetherMesh v{__version__}")
    print("=" * 60)
    print(f"Author:          {__author__}")
    print(f"Email:           {__email__}")
    print(f"License:         {__license__}")
    print(f"Paper version:   {__paper_version__}")
    print(f"Record ID:       {__record_id__}")
    print(f"DOI:             {__doi__}")
    print(f"DOI URL:         https://doi.org/{__doi__}")
    print()
    print("AetherMesh is the decentralization layer of the Aether family:")
    print("  AetherGit  (storage)          — 10.5281/zenodo.23966896")
    print("  AetherFlow (integration)      — 10.5281/zenodo.23979129")
    print("  AetherProof (verification)    — 10.5281/zenodo.24013124")
    print("  AetherMesh (decentralization) — 10.5281/zenodo.24038038")
    print()
    print("Status: Reference implementation. Preliminary results.")
    print("        Not a production system. No real-world deployment.")
    print("=" * 60)
    return 0


# =============================================================================
# Simulate
# =============================================================================

def cmd_simulate(args: argparse.Namespace) -> int:
    """Run the full testbed and report all three metrics."""
    from aethermesh.simulation.testbed import Testbed, TestbedConfig

    print("=" * 60)
    print(f"AetherMesh v{__version__} — simulated testbed")
    print("=" * 60)
    print(f"Nodes:     {args.nodes}")
    print(f"Fanout:    {args.fanout}")
    print(f"Rounds:    {args.max_rounds}")
    print(f"Seed:      {args.seed}")
    print()

    config = TestbedConfig(
        n_nodes=args.nodes,
        fanout=args.fanout,
        max_rounds=args.max_rounds,
        seed=args.seed,
    )

    # Metric 1: convergence
    print("[1/3] Convergence latency")
    tb1 = Testbed(config)
    m1 = tb1.measure_convergence_latency(initial_delta_count=1)
    print(f"      Converged at time: {m1['converged_at_time']}")
    print(f"      Converged at round: {m1['converged_at_round']}")
    print(f"      Final fraction: {m1['final_fraction']:.2%}")
    print()

    # Metric 2: conflict overhead
    print("[2/3] Conflict resolution overhead")
    tb2 = Testbed(config)
    m2 = tb2.measure_conflict_overhead(n_conflicting_deltas=10)
    print(f"      Conflicts flagged: {m2['conflicts_flagged']}")
    print(f"      Deadlocks: {m2['deadlocks']}")
    print(f"      Throughput overhead: {m2['throughput_overhead_pct']}%")
    print()

    # Metric 3: fault resilience
    print("[3/3] Fault resilience")
    tb3 = Testbed(config)
    m3 = tb3.measure_fault_resilience(n_malformed=args.n_malformed)
    print(f"      Injected: {m3['injected']}")
    print(f"      Blocked:  {m3['blocked']}")
    print(f"      Block rate: {m3['block_rate']:.2%}")
    print()

    # Summary
    results = {
        "version": __version__,
        "config": {
            "nodes": args.nodes,
            "fanout": args.fanout,
            "max_rounds": args.max_rounds,
            "seed": args.seed,
        },
        "metric_1_convergence": m1,
        "metric_2_conflict_overhead": m2,
        "metric_3_fault_resilience": m3,
    }

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results written to {args.output}")
    else:
        print(json.dumps(results, indent=2))

    return 0


# =============================================================================
# Verify
# =============================================================================

def cmd_verify(args: argparse.Namespace) -> int:
    """Run a self-check without a full simulation."""
    print("=" * 60)
    print(f"AetherMesh v{__version__} — self-check")
    print("=" * 60)

    ok = True

    # 1. Join laws on the Figure 4 example
    print("[1/4] Join laws (Figure 4 example)")
    from aethermesh.crdt.semilattice import build_figure4_example, verify_join_laws
    lattice, elements = build_figure4_example()
    laws_ok, violations = verify_join_laws(lattice, elements)
    if laws_ok:
        print(f"      ✅ 7 elements, all 3 laws hold")
    else:
        print(f"      ❌ {len(violations)} violations")
        ok = False

    # 2. Signature verification
    print("[2/4] Ed25519 signature verification")
    from aethermesh.bft import generate_keypair, sign_delta, verify_delta_signature
    from aethermesh.models import Delta, DeltaKind
    priv, pub = generate_keypair()
    d = Delta.create(body={"op": "test"}, origin="test-agent", kind=DeltaKind.EDIT_BODY)
    d_signed = sign_delta(d, priv, "key-1")
    sig_ok = verify_delta_signature(d_signed, pub)
    if sig_ok:
        print(f"      ✅ Valid signature verified")
    else:
        print(f"      ❌ Signature verification failed")
        ok = False

    # 3. Admission pipeline
    print("[3/4] Admission pipeline")
    from aethermesh.bft import KeyRegistry
    from aethermesh.admission.pipeline import AdmissionPipeline
    from aethermesh.crdt.delta_state import DeltaStateCRDT
    registry = KeyRegistry()
    registry.register("test-agent", "key-1", pub)
    pipeline = AdmissionPipeline(registry=registry)
    crdt = DeltaStateCRDT(origin="test")
    verdict = pipeline.admit(d_signed, crdt.replica)
    if verdict.accepted:
        print(f"      ✅ Valid delta accepted")
    else:
        print(f"      ❌ Valid delta rejected: {verdict.reason}")
        ok = False

    # 4. Reject unsigned
    d_unsigned = Delta.create(body={"op": "test2"}, origin="test-agent", kind=DeltaKind.EDIT_BODY)
    verdict2 = pipeline.admit(d_unsigned, crdt.replica)
    if verdict2.verdict.value == "reject":
        print(f"      ✅ Unsigned delta rejected")
    else:
        print(f"      ❌ Unsigned delta not rejected: {verdict2.verdict.value}")
        ok = False

    print("[4/4] Summary")
    if ok:
        print("      ✅ All checks passed")
        print("=" * 60)
        return 0
    else:
        print("      ❌ Some checks failed")
        print("=" * 60)
        return 1


# =============================================================================
# Entry point
# =============================================================================

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="aethermesh",
        description=(
            f"AetherMesh v{__version__} — decentralized P2P agent synchronization"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"aethermesh {__version__}",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # info
    p_info = sub.add_parser("info", help="Print version, DOI, and record information")
    p_info.set_defaults(func=cmd_info)

    # verify
    p_verify = sub.add_parser("verify", help="Run a self-check (no simulation)")
    p_verify.set_defaults(func=cmd_verify)

    # simulate
    p_sim = sub.add_parser("simulate", help="Run the full simulated testbed")
    p_sim.add_argument("--nodes", type=int, default=50, help="Number of nodes (default: 50)")
    p_sim.add_argument("--fanout", type=int, default=5, help="Gossip fanout (default: 5)")
    p_sim.add_argument("--max-rounds", type=int, default=200, help="Max gossip rounds (default: 200)")
    p_sim.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    p_sim.add_argument("--n-malformed", type=int, default=100, help="Malformed deltas to inject (default: 100)")
    p_sim.add_argument("--output", type=str, default=None, help="Write results JSON to this file")
    p_sim.set_defaults(func=cmd_simulate)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
