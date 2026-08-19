#!/usr/bin/env python3
"""Verify the committed publication contract for this repository."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_STATUS = (
    "PARTIAL_C1_C2_C3_C6_VERIFIED_C4_C5_NARROWLY_FALSIFIED_HISTORICAL_SCORE_5_OF_12_NO_CURRENT_SCORE"
)
EXPECTED_BRANCHES = {
    "audit/c1-vwgf-s-jko-equivalence",
    "audit/c2-wasserstein-jko-update",
    "audit/c3-donsker-varadhan-bound",
    "audit/c4-eq18-discriminator",
    "audit/c5-fid-consistency",
    "audit/c6-parametric-flow",
    "historical/judged-baseline-5-of-12",
    "release/c1-evaluator-evidence",
    "release/c2-evaluator-evidence",
    "release/c3-evaluator-evidence",
    "release/c4-evaluator-evidence",
    "release/c5-evaluator-evidence",
    "release/c6-evaluator-evidence",
    "release/cumulative-candidate",
    "release/final-publication-package",
    "main",
}
EXPECTED_COMMITS = 39
CANONICAL_IDENTITY = "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
CLAIM_IDS = ["C1", "C2", "C3", "C4", "C5", "C6"]


def load(name: str):
    return json.loads((ROOT / name).read_text())


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"verification failed: {message}")


def published_branches() -> set[str]:
    remote = {
        name.removeprefix("origin/")
        for name in git(
            "for-each-ref", "refs/remotes/origin", "--format=%(refname:short)"
        ).splitlines()
        if name.startswith("origin/") and name != "origin/HEAD"
    }
    if remote:
        return remote
    return set(git("for-each-ref", "refs/heads", "--format=%(refname:short)").splitlines())


def main() -> None:
    claims = load("claims.json")
    verdicts = load("reproduction_verdicts.json")
    manifest = load("EVIDENCE_MANIFEST.json")
    state = load("AUTONOMOUS_STATE.json")
    logbook = load("release_candidate_space/logbook.json")
    red_team = load("release_candidate_space/evidence/release/red_team_pass4.json")
    claim5 = load("release_candidate_space/evidence/claim5/checker_output.json")
    claim6 = load("release_candidate_space/evidence/claim6/checker_output.json")

    require(claims["overall_status"] == EXPECTED_STATUS, "claims overall status")
    require(state["overall_status"] == EXPECTED_STATUS, "autonomous state overall status")
    require(verdicts["overall_verdict"] == "PARTIAL_C1_C2_C3_C6_VERIFIED_C4_C5_NARROWLY_FALSIFIED", "overall verdict")
    require([claim["id"] for claim in claims["claims"]] == CLAIM_IDS, "claim ordering")
    expected_statuses = {
        "C1": "VERIFIED_SCOPED",
        "C2": "VERIFIED_SCOPED",
        "C3": "VERIFIED_SCOPED",
        "C4": "FALSIFIED_SCOPED",
        "C5": "FALSIFIED_SCOPED",
        "C6": "VERIFIED_SCOPED",
    }
    require({claim["id"]: claim["status"] for claim in claims["claims"]} == expected_statuses, "claim statuses")
    require(verdicts["claim_statuses"] == expected_statuses, "verdict statuses")
    require(all((ROOT / path).exists() for path in manifest["required_paths"]), "manifest paths")

    require(logbook["space_id"] == "DineshAI/sJ7ngz2eQx", "Space identity")
    require(red_team["reviewer_verdict"] == "PASS", "red team verdict")
    require(red_team["visibility_complete"] is True, "visibility gate")
    require(claim5["all_named_f_divergences_improved_primary"] is False, "primary table falsification")
    require(claim5["all_named_f_divergences_improved_different_seeds"] is False, "different-seed falsification")
    require(claim6["passed"] is True, "claim 6 checker")
    require(claim6["small_tau_implicit_residual_loglog_slope"] > 0.9, "claim 6 residual slope")
    require(claim6["minimum_metric_eigenvalue"] > 0.2, "claim 6 metric")
    require(claim6["minimum_absolute_metric_off_diagonal"] > 0.7, "claim 6 off-diagonal metric")

    require(verdicts["historical_external_result"]["live_judge_score"] == "5/12", "historical score")
    require(verdicts["historical_external_result"]["current_score_claim"] is False, "current score claim")
    require(verdicts["publication"]["publication_allowed"] is False, "publication state")
    require(verdicts["publication"]["author_endorsement_claimed"] is False, "author endorsement state")

    branches = published_branches()
    require(branches == EXPECTED_BRANCHES, "published branches")
    require(not any(branch.startswith("orx/") for branch in branches), "legacy orx branch")
    require(int(git("rev-list", "--all", "--count")) == EXPECTED_COMMITS, "reachable commit count")
    identities = git("log", "--all", "--format=%an <%ae>\n%cn <%ce>").splitlines()
    require(identities and all(identity == CANONICAL_IDENTITY for identity in identities), "canonical commit identity")

    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={len(branches)} commits={EXPECTED_COMMITS} "
        "claims=C1:C3_C6_verified_scoped,C4:C5_falsified_scoped "
        "historical_score=5/12 current_score_claim=false publication_allowed=false"
    )


if __name__ == "__main__":
    main()
