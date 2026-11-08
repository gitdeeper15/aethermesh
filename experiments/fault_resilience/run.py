#!/usr/bin/env python3
"""
Experiment 3 — Fault resilience (Metric 3).

Reproduces Section 5.4 of the paper: blocking of malformed deltas.

Reference:
    Baladi, S. (2026). AetherMesh v1.0.0. Section 5.4.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aethermesh.simulation.testbed import Testbed, TestbedConfig


def main():
    results = {
        "experiment": "fault_resilience",
        "description": "Blocking of malformed deltas",
        "source": "Section 5.4 of AetherMesh v1.0.0",
        "runs": [],
    }

    for n_malformed in [10, 50, 100, 500]:
        print(f"Running n_malformed={n_malformed}...", end=" ", flush=True)
        config = TestbedConfig(
            n_nodes=20,
            fanout=5,
            max_rounds=20,
            seed=42,
        )
        tb = Testbed(config)
        m3 = tb.measure_fault_resilience(n_malformed=n_malformed)

        result = {
            "n_malformed": n_malformed,
            "injected": m3["injected"],
            "blocked": m3["blocked"],
            "block_rate": m3["block_rate"],
        }
        results["runs"].append(result)
        print(f"block_rate={m3['block_rate']:.2%}")

    out = Path(__file__).parent / "results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results written to {out}")


if __name__ == "__main__":
    main()
