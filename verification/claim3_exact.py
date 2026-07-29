"""Exact contract for the Donsker–Varadhan lower-bound claim."""

from __future__ import annotations

import argparse
import json
import math

import sympy as sp


def symbolic_certificate() -> dict:
    """Prove exp(s - 1) - s >= 0 for every real s."""
    s = sp.symbols("s", real=True)
    gap = sp.exp(s - 1) - s
    derivative = sp.diff(gap, s)
    stationary = sp.solveset(derivative, s, domain=sp.S.Reals)
    second_at_stationary = sp.simplify(sp.diff(gap, s, 2).subs(s, 1))
    minimum = sp.simplify(gap.subs(s, 1))
    left_limit = sp.limit(gap, s, -sp.oo)
    right_limit = sp.limit(gap, s, sp.oo)
    passed = (
        stationary == sp.FiniteSet(1)
        and second_at_stationary == 1
        and minimum == 0
        and left_limit == sp.oo
        and right_limit == sp.oo
    )
    return {
        "identity": "DV(h)-classical(h)=exp(s-1)-s, s=log integral(exp(h)) dnu",
        "stationary_set": str(stationary),
        "second_derivative_at_1": str(second_at_stationary),
        "minimum": str(minimum),
        "limits": [str(left_limit), str(right_limit)],
        "passed": passed,
    }


def gaussian_checker() -> dict:
    """Independent continuous-measure check for affine critics.

    For nu=N(0,1), mu=N(m,1), and h(x)=a*x+b:
      log E_nu exp(h) = b + a^2/2.
    """
    cases = []
    min_gap = math.inf
    for m in [-2.0, -0.7, 0.3, 1.5]:
        for a in [-2.3, -0.5, 0.0, 0.8, 2.1]:
            for b in [-1.4, 0.0, 1.2]:
                mean_h_mu = a * m + b
                log_t = b + a * a / 2
                dv = mean_h_mu - log_t
                classical = mean_h_mu - math.exp(log_t - 1)
                gap = dv - classical
                min_gap = min(min_gap, gap)
                cases.append(
                    {
                        "m": m,
                        "a": a,
                        "b": b,
                        "dv": dv,
                        "classical": classical,
                        "gap": gap,
                    }
                )

    optimum = []
    max_opt_error = 0.0
    for m in [-2.0, -0.7, 0.3, 1.5]:
        a = m
        b = 1 - m * m / 2
        mean_h_mu = a * m + b
        log_t = b + a * a / 2
        dv = mean_h_mu - log_t
        classical = mean_h_mu - math.exp(log_t - 1)
        kl_value = m * m / 2
        error = max(abs(dv - kl_value), abs(classical - kl_value))
        max_opt_error = max(max_opt_error, error)
        optimum.append(
            {
                "m": m,
                "h_star": {"a": a, "b": b},
                "kl": kl_value,
                "dv": dv,
                "classical": classical,
                "error": error,
            }
        )
    return {
        "family": "mu=N(m,1), nu=N(0,1), h(x)=a*x+b",
        "case_count": len(cases),
        "minimum_gap": min_gap,
        "maximum_optimality_error": max_opt_error,
        "optimum_cases": optimum,
        "passed": min_gap >= -1e-12 and max_opt_error < 1e-12,
    }


def negative_control() -> dict:
    """The reversed pointwise claim must fail at s=0."""
    s = 0.0
    dv_minus_classical = math.exp(s - 1) - s
    reversed_claim_holds = dv_minus_classical <= 0
    return {
        "control": "classical(h) >= DV(h) for every h",
        "witness_s": s,
        "dv_minus_classical": dv_minus_classical,
        "passed_as_claim": reversed_claim_holds,
        "expected_to_fail": True,
    }


def run_contract() -> dict:
    symbolic = symbolic_certificate()
    independent = gaussian_checker()
    control = negative_control()
    passed = symbolic["passed"] and independent["passed"] and not control["passed_as_claim"]
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "exact_contract": (
            "For probability measures mu<<nu and every admissible bounded critic h, "
            "DV(h)>=classical(h); their suprema equal KL(mu||nu). When "
            "1+log(dmu/dnu) is admissible, both attain KL there."
        ),
        "symbolic_certificate": symbolic,
        "independent_checker": independent,
        "negative_control": control,
        "limitations": (
            "SymPy checks the scalar convex inequality exactly. The lift from "
            "s=log integral(exp(h))dnu to arbitrary probability measures is an "
            "independently reconstructed analytic derivation, not a proof-assistant "
            "formalization of measure theory."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        result = negative_control()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["passed_as_claim"] else 1
    result = run_contract()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
