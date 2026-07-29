"""Falsify the assertion that Equation 18 avoids discriminator optimization."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


DATA_DIR = Path(__file__).parent / "data"
PAPER_EXCERPT = DATA_DIR / "claim4_paper_excerpt.txt"
CODE_EXCERPT = DATA_DIR / "claim4_authors_code_excerpt.py"
EXPECTED_HASHES = {
    "paper_excerpt_sha256": (
        "cd8c0aa0b09741c605951ba359dfb5c741b2d37fd7f18b47209524bc4ba314d1"
    ),
    "authors_code_excerpt_sha256": (
        "18a5eafabe048418b9026b9b6b65a345df708317d65dd2e709c0fcfab0ec33c0"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_audit() -> dict:
    paper = PAPER_EXCERPT.read_text()
    code = CODE_EXCERPT.read_text()
    observed = {
        "paper_excerpt_sha256": sha256(PAPER_EXCERPT),
        "authors_code_excerpt_sha256": sha256(CODE_EXCERPT),
    }
    required_paper = [
        "max_phi min_T",
        "solved using an adversarial",
        "argmax_phi",
        "explicitly updates",
    ]
    required_code = [
        "Optimise discriminator",
        "args.D_steps",
        "optimizerD.step()",
        "--divergence MMD --JKO",
    ]
    return {
        "observed_hashes": observed,
        "expected_hashes": EXPECTED_HASHES,
        "hashes_match": observed == EXPECTED_HASHES,
        "paper_requirements": {
            item: item in paper for item in required_paper
        },
        "code_requirements": {
            item: item in code for item in required_code
        },
        "paper_html_sha256": (
            "9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a"
        ),
        "authors_code_revision": (
            "6633b553a244634bd2c2e1142603aad1c1fbe55a"
        ),
    }


def finite_counterexample() -> dict:
    """Solve a valid nondegenerate Equation-18 instance exhaustively.

    Let mu=delta_1, nu=delta_0, T_t(1)=t, phi in [0,1], and use the PSD
    linear kernel k_phi(x,y)=(phi*x)(phi*y). The Equation-18 objective is
    0.5*(1-t)^2 + phi^2*t^2.
    """
    phi_grid = np.linspace(0.0, 1.0, 1001)
    t_minimizers = 1.0 / (1.0 + 2.0 * phi_grid**2)
    minimized_values = (
        0.5 * (1.0 - t_minimizers) ** 2
        + phi_grid**2 * t_minimizers**2
    )
    maximizing_index = int(np.argmax(minimized_values))
    phi_star = float(phi_grid[maximizing_index])
    t_star = float(t_minimizers[maximizing_index])
    no_discriminator_t = float(t_minimizers[0])
    analytic_phi_star = 1.0
    analytic_t_star = 1.0 / 3.0
    return {
        "domain": (
            "mu=delta_1, nu=delta_0, T_t(1)=t, phi in [0,1], "
            "k_phi(x,y)=phi^2*x*y (positive semidefinite)"
        ),
        "objective": "max_phi min_t 0.5*(1-t)^2 + phi^2*t^2",
        "grid_points": len(phi_grid),
        "grid_phi_star": phi_star,
        "grid_t_star": t_star,
        "analytic_phi_star": analytic_phi_star,
        "analytic_t_star": analytic_t_star,
        "t_with_phi_fixed_at_zero": no_discriminator_t,
        "generator_solution_shift_without_discriminator": abs(
            no_discriminator_t - analytic_t_star
        ),
        "passed": (
            abs(phi_star - analytic_phi_star) < 1e-12
            and abs(t_star - analytic_t_star) < 1e-12
            and abs(no_discriminator_t - analytic_t_star) > 0.5
        ),
    }


def run_contract() -> dict:
    audit = source_audit()
    counterexample = finite_counterexample()
    source_complete = (
        audit["hashes_match"]
        and all(audit["paper_requirements"].values())
        and all(audit["code_requirements"].values())
    )
    falsified = source_complete and counterexample["passed"]
    return {
        "status": "FALSIFIED" if falsified else "BLOCKED",
        "scope": (
            "the imported Equation-18 conjunct that the JKO-regularized "
            "MMD-GAN does not require explicit discriminator optimization"
        ),
        "exact_contract": (
            "Equation 18 can be implemented without optimizing its phi "
            "embedding/discriminator while still solving the stated max-min problem."
        ),
        "source_audit": audit,
        "independent_checker": counterexample,
        "counterexample": (
            "Equation 18 itself contains max_phi; Appendix D.4 gives an "
            "argmax_phi update; Algorithm 2 and the authors' implementation "
            "execute discriminator optimizer steps."
        ),
        "limitations": (
            "This falsifies only the no-discriminator conjunct attached to "
            "Equation 18. The paper correctly says that fixed-kernel Algorithm 1 "
            "has a closed-form witness, and the broader IPM/MMD extension remains valid."
        ),
    }


def negative_control() -> dict:
    fixed_kernel_only = (
        "Algorithm 1 has no adversarial scheme because its witness is closed form."
    )
    required_eq18_markers = ["max_phi", "Equation 18", "argmax_phi"]
    complete = all(item in fixed_kernel_only for item in required_eq18_markers)
    return {
        "control": (
            "substitute the fixed-kernel Algorithm 1 statement for Equation 18"
        ),
        "required_eq18_markers": required_eq18_markers,
        "complete_for_equation_18": complete,
        "expected_to_fail": True,
        "passed_as_valid_evidence": complete,
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
