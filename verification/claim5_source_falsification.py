"""Exhaustively test Claim 5's consistency quantifier on the paper tables."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
PRIMARY = DATA_DIR / "claim5_table4.csv"
INDEPENDENT = DATA_DIR / "claim5_different_seeds.csv"
EXCERPT = DATA_DIR / "claim5_source_excerpt.txt"
FID_DIVERGENCES = {"chi2", "KL", "Shannon"}
TAU_COLUMNS = ("tau_0_01_mean", "tau_1_mean", "tau_100_mean")
EXPECTED_HASHES = {
    "primary_csv_sha256": "b41cae730fe85b767a3e397d52e0aeec9982e03cd5e6a6668b0db888e7fb6d93",
    "different_seed_csv_sha256": "7e5c010ac2f28ad6b02c1781fffcdbb3a594a2c1634f75aeff869bed9e4d1223",
    "source_excerpt_sha256": "a635612f7300c6a5cca7f0f6245b64eccd92e9a3a12c805b067aaba5cd25284b",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_table(path: Path) -> list[dict]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def audit_table(rows: list[dict]) -> dict:
    names = {row["divergence"] for row in rows}
    missing = sorted(FID_DIVERGENCES - names)
    if missing:
        return {
            "complete": False,
            "missing_required_divergences": missing,
            "rows": [],
        }

    results = []
    for name in sorted(FID_DIVERGENCES):
        row = next(item for item in rows if item["divergence"] == name)
        no_jko = float(row["no_jko_mean"])
        candidates = {column: float(row[column]) for column in TAU_COLUMNS}
        best_tau, best_jko = min(candidates.items(), key=lambda item: item[1])
        delta = best_jko - no_jko
        results.append(
            {
                "divergence": name,
                "no_jko_mean_fid": no_jko,
                "best_jko_mean_fid": best_jko,
                "best_tau_column": best_tau,
                "jko_minus_no_jko": delta,
                "improved": delta < 0,
            }
        )
    return {
        "complete": True,
        "missing_required_divergences": [],
        "rows": results,
        "all_named_f_divergences_improved": all(row["improved"] for row in results),
    }


def run_contract() -> dict:
    primary_rows = read_table(PRIMARY)
    independent_rows = read_table(INDEPENDENT)
    primary = audit_table(primary_rows)
    independent = audit_table(independent_rows)
    shannon_primary = next(
        row for row in primary["rows"] if row["divergence"] == "Shannon"
    )
    shannon_independent = next(
        row for row in independent["rows"] if row["divergence"] == "Shannon"
    )
    observed_hashes = {
        "primary_csv_sha256": sha256(PRIMARY),
        "different_seed_csv_sha256": sha256(INDEPENDENT),
        "source_excerpt_sha256": sha256(EXCERPT),
    }
    integrity_passed = observed_hashes == EXPECTED_HASHES
    counterexample_valid = (
        integrity_passed
        and primary["complete"]
        and independent["complete"]
        and not primary["all_named_f_divergences_improved"]
        and not shannon_primary["improved"]
        and not shannon_independent["improved"]
    )
    return {
        "status": "FALSIFIED" if counterexample_valid else "BLOCKED",
        "scope": (
            "the exact Section 5.3 consistency assertion over all named "
            "f-divergences and all reported CIFAR-10 step sizes"
        ),
        "exact_contract": (
            "For each named f-divergence (KL, Jensen-Shannon, chi2), at least "
            "one reported JKO step size has lower mean CIFAR-10 FID than the "
            "matched no-JKO baseline."
        ),
        "primary_table": primary,
        "different_seed_table": independent,
        "counterexample": {
            "divergence": "Jensen-Shannon (paper/code label: Shannon)",
            "primary_jko_minus_no_jko": shannon_primary["jko_minus_no_jko"],
            "different_seed_jko_minus_no_jko": shannon_independent[
                "jko_minus_no_jko"
            ],
        },
        "source_integrity": {
            "paper_html_sha256": (
                "9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a"
            ),
            "authors_code_revision": (
                "6633b553a244634bd2c2e1142603aad1c1fbe55a"
            ),
            "observed_hashes": observed_hashes,
            "expected_hashes": EXPECTED_HASHES,
            "passed": integrity_passed,
        },
        "limitations": (
            "This falsifies the exact consistency quantifier using the paper's "
            "complete reported tables; it does not rerun the H100 image training "
            "or dispute that KL and chi2 improve at selected step sizes."
        ),
    }


def negative_control() -> dict:
    rows = [
        row for row in read_table(PRIMARY) if row["divergence"] != "Shannon"
    ]
    audit = audit_table(rows)
    return {
        "control": "drop the contradicting Jensen-Shannon row",
        "expected_to_fail": True,
        "completeness_audit": audit,
        "passed_as_valid_evidence": audit["complete"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    result = negative_control() if args.negative_control else run_contract()
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.negative_control:
        return 0 if result["passed_as_valid_evidence"] else 1
    return 0 if result["status"] == "FALSIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
