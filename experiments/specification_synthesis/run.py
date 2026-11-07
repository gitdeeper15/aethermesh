"""
Experiment 1: Specification Synthesis.

Measures the quality of LLM-generated specifications (with human review).
"""

import json
from pathlib import Path


def run_experiment() -> dict:
    """Run specification synthesis experiment."""
    # Simulated results (in a real experiment, this would use an LLM)
    results = {
        "experiment": "specification_synthesis",
        "n_specifications": 100,
        "precision": 0.892,
        "recall": 0.876,
        "f1": 0.884,
        "human_review_rate": 0.35,
        "note": "Simulated results — not real LLM output"
    }
    return results


if __name__ == "__main__":
    results = run_experiment()
    out = Path(__file__).parent / "results.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"✅ Experiment 1 results saved to {out}")
    print(f"   F1 = {results['f1']:.3f}")
