#!/usr/bin/env python3
"""
Experiment 2 — Conflict resolution overhead (Metric 2).

Reproduces Section 5.3 of the paper: deadlocks, CPU/memory overhead
during high-concurrency conflicting edits.

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 5.3.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aethermesh.simulation.testbed import Testbed, TestbedConfig


def main():
    results = {
        "experiment": "conflict_resolution",
        "description": "Conflict resolution overhead (deadlocks, CPU, memory)",
        "source": "Section 5.3 of AetherMesh v1.0.0",
        "runs": [],
    }

    for n_nodes in [10, 50, 100]:
        print(f"Running n_nodes={n_nodes}...", end=" ", flush=True)
        config = TestbedConfig(
            n_nodes=n_nodes,
            fanout=5,
            max_rounds=50,
            seed=42,
        )
        tb = Testbed(config)
        m2 = tb.measure_conflict_overhead(n_conflicting_deltas=10)

        result = {
            "n_nodes": n_nodes,
            "conflicts_flagged": m2["conflicts_flagged"],
            "deadlocks": m2["deadlocks"],
            "throughput_overhead_pct": m2["throughput_overhead_pct"],
        }
        results["runs"].append(result)
        print(f"deadlocks={m2['deadlocks']}, flagged={m2['conflicts_flagged']}")

    out = Path(__file__).parent / "results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results written to {out}")


if __name__ == "__main__":
    main()
