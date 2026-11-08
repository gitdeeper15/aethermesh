#!/usr/bin/env python3
"""
Experiment 1 — State convergence latency (Metric 1).

Reproduces Section 5.2 of the paper: convergence time at 99% of the
network, for 10, 50, 100, 250, 500 nodes.

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 5.2.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aethermesh.simulation.testbed import Testbed, TestbedConfig


def main():
    results = {
        "experiment": "convergence_latency",
        "description": "State convergence latency at 99% of network",
        "source": "Section 5.2 of AetherMesh v1.0.0",
        "runs": [],
    }

    for n_nodes in [10, 50, 100, 250, 500]:
        print(f"Running n_nodes={n_nodes}...", end=" ", flush=True)
        config = TestbedConfig(
            n_nodes=n_nodes,
            fanout=5,
            max_rounds=100,
            seed=42,
        )
        tb = Testbed(config)
        m1 = tb.measure_convergence_latency(initial_delta_count=1)

        result = {
            "n_nodes": n_nodes,
            "converged_at_time": m1["converged_at_time"],
            "converged_at_round": m1["converged_at_round"],
            "total_rounds": m1["total_rounds"],
            "final_fraction": m1["final_fraction"],
        }
        results["runs"].append(result)
        print(f"converged at round {m1['converged_at_round']}")

    out = Path(__file__).parent / "results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results written to {out}")


if __name__ == "__main__":
    main()
