"""Command-line interface for AetherProof v2.0.0."""

import argparse
import sys

from aetherproof.__version__ import __version__
from aetherproof.models import CSRecord, Layer, Verdict
from aetherproof.csr.relations import SemanticRelation, RelationType
from aetherproof.obligations.generator import generate_obligations


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="aetherproof",
        description="AetherProof v2.0.0 — Reference Implementation",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # csr command
    csr = sub.add_parser("csr", help="CSR record operations")
    csr.add_argument("--layer", choices=["L1", "L2", "L3"], required=True)
    csr.add_argument("--language", required=True)
    csr.add_argument("--content", required=True)
    csr.add_argument("--role", required=True)

    # obligation command
    obl = sub.add_parser("obligation", help="Obligation operations")
    obl.add_argument("--csr-id", required=True)
    obl.add_argument("--property", required=True)

    # relation command
    rel = sub.add_parser("relation", help="Semantic relation operations")
    rel.add_argument("--source", required=True)
    rel.add_argument("--target", required=True)
    rel.add_argument(
        "--type",
        choices=[r.value for r in RelationType],
        required=True,
    )
    rel.add_argument("--loss-description")

    args = parser.parse_args(argv)

    if args.command == "csr":
        layer = Layer(args.layer)
        record = CSRecord.create(
            layer=layer,
            language=args.language,
            content=args.content,
            semantic_role=args.role,
        )
        print(f"CSR ID:        {record.csr_id}")
        print(f"Artifact Hash: {record.artifact_hash}")
        print(f"Semantic ID:   {record.semantic_id}")
        print(f"Layer:         {record.layer.value}")
        print(f"Language:      {record.language}")

    elif args.command == "obligation":
        # In a real CLI, this would fetch the CSR record
        print(f"Obligation for CSR {args.csr_id}: {args.property}")

    elif args.command == "relation":
        try:
            relation = SemanticRelation(
                source=args.source,
                target=args.target,
                relation_type=RelationType(args.type),
                loss_description=args.loss_description,
            )
            print(f"Relation created: {relation.source} "
                  f"-> {relation.target} ({relation.relation_type.value})")
        except ValueError as e:
            print(f"Error: {e}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
