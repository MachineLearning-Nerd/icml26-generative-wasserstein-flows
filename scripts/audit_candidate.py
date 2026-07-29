"""Evaluator-blind traversal and release-gate audit for a candidate Space."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote


LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
VERDICTS = {
    1: "VERIFIED",
    2: "VERIFIED",
    3: "VERIFIED",
    4: "FALSIFIED",
    5: "FALSIFIED",
    6: "VERIFIED",
}
TEXT_SUFFIXES = {".md", ".json", ".py", ".toml", ".lock", ".txt", ".csv"}
SECRET_VALUE = re.compile(
    r"(?i)(api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{16,}"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_target(root: Path, source: Path, target: str) -> Path | None:
    target = unquote(target.strip().split("#", 1)[0])
    if not target or target.startswith(("http://", "https://", "mailto:", "/")):
        return None
    resolved = (source.parent / target).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        raise ValueError(f"link escapes candidate: {source}: {target}")
    return resolved


def traverse(root: Path) -> tuple[list[str], list[str]]:
    entrypoints = [root / "README.md", root / "logbook.json", root / "pages/index.md"]
    queue = deque(entrypoints)
    opened: list[str] = []
    errors: list[str] = []
    seen: set[Path] = set()
    while queue:
        path = queue.popleft().resolve()
        if path in seen:
            continue
        seen.add(path)
        if not path.is_file():
            errors.append(f"missing reachable file: {path.relative_to(root.resolve())}")
            continue
        relative = path.relative_to(root.resolve()).as_posix()
        opened.append(relative)
        if path.suffix not in TEXT_SUFFIXES and path.name != ".python-version":
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            errors.append(f"reachable file is not text: {relative}")
            continue
        if path.suffix == ".md":
            for raw_target in LINK.findall(text):
                try:
                    target = local_target(root, path, raw_target)
                except ValueError as exc:
                    errors.append(str(exc))
                    continue
                if target is not None:
                    queue.append(target)
        if path.name == "logbook.json":
            payload = json.loads(text)

            def enqueue_pages(node: dict) -> None:
                queue.append((root / node["file"]).resolve())
                for child in node.get("children", []):
                    enqueue_pages(child)

            enqueue_pages(payload["root"])
    return opened, errors


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def audit(root: Path) -> dict:
    opened, errors = traverse(root)
    opened_set = set(opened)
    for number, verdict in VERDICTS.items():
        page_name = f"pages/claims/claim{number}.md"
        require(page_name in opened_set, f"claim {number} page not reachable", errors)
        if page_name not in opened_set:
            continue
        page = (root / page_name).read_text()
        for term in [
            f"Verdict: {verdict}",
            "Exact claim",
            "assumption",
            "uv run --frozen python run_campaign.py",
            "negative control",
            "Limitation",
            "Git SHA",
            "cpu-upgrade",
            "seconds",
            "seed",
        ]:
            require(
                term.lower() in page.lower(),
                f"claim {number} page missing visible term: {term}",
                errors,
            )
        required = [
            f"evidence/claim{number}/claim_contract.json",
            f"evidence/claim{number}/source_audit.md",
            f"evidence/claim{number}/method.md",
            f"evidence/claim{number}/raw_result.json",
            f"evidence/claim{number}/checker_output.json",
            f"evidence/claim{number}/negative_control_output.json",
        ]
        for relative in required:
            require(relative in opened_set, f"claim {number} unreachable: {relative}", errors)
        require(
            any(
                name.startswith(f"verification/claim{number}") and name.endswith(".py")
                for name in opened_set
            ),
            f"claim {number} verifier source not reachable",
            errors,
        )

    matrix = root / "pages/visibility_matrix.md"
    matrix_text = matrix.read_text() if matrix.is_file() else ""
    require("PENDING" not in matrix_text, "visibility matrix contains PENDING", errors)
    require(matrix.relative_to(root).as_posix() in opened_set, "matrix is unreachable", errors)
    for number in VERDICTS:
        require(f"| {number} |" in matrix_text, f"matrix missing claim {number}", errors)

    for relative in ["run_campaign.py", "pyproject.toml", "uv.lock", ".python-version"]:
        require(relative in opened_set, f"environment/command file unreachable: {relative}", errors)

    subset_path = root / "manifests/judged_subset.json"
    subset = json.loads(subset_path.read_text())
    require(subset.get("subset_pass") is True, "judged file subset check failed", errors)
    for row in subset["files"]:
        preserved = root / row["preserved_path"]
        require(preserved.is_file(), f"missing judged file: {row['original_path']}", errors)
        if preserved.is_file():
            require(
                sha256(preserved) == row["sha256"],
                f"judged hash mismatch: {row['original_path']}",
                errors,
            )

    allowlist_path = root / "manifests/text_upload_allowlist.txt"
    allowlist = [line for line in allowlist_path.read_text().splitlines() if line]
    require(
        "manifests/text_upload_allowlist.txt" in allowlist,
        "upload allowlist does not include itself",
        errors,
    )
    for relative in allowlist:
        path = root / relative
        require(path.is_file(), f"allowlisted path missing: {relative}", errors)
        if path.is_file():
            require(
                path.suffix in TEXT_SUFFIXES or path.name == ".python-version",
                f"allowlisted path is not text: {relative}",
                errors,
            )

    all_text = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and (
            path.suffix in TEXT_SUFFIXES or path.name == ".python-version"
        ):
            try:
                all_text.append((path.relative_to(root).as_posix(), path.read_text()))
            except UnicodeDecodeError:
                errors.append(f"text extension is not UTF-8: {path.relative_to(root)}")
    for relative, text in all_text:
        require(
            SECRET_VALUE.search(text) is None,
            f"possible secret value in {relative}",
            errors,
        )

    numeric_checks = {
        "pages/claims/claim1.md": ["4.44e-14"],
        "pages/claims/claim2.md": ["1.25e-8", "0.02374"],
        "pages/claims/claim3.md": ["8.326672684688674e-17", "0.01783465805601825"],
        "pages/claims/claim4.md": ["phi*=1", "t*=1/3", "2/3"],
        "pages/claims/claim5.md": ["14.60", "15.23", "16.84", "16.87"],
        "pages/claims/claim6.md": ["0.9833", "0.001215", "1.831428"],
    }
    for relative, values in numeric_checks.items():
        text = (root / relative).read_text()
        for value in values:
            require(value in text, f"displayed evidence missing: {relative}: {value}", errors)

    return {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "candidate_root": str(root.resolve()),
        "entrypoints": ["README.md", "logbook.json", "pages/index.md"],
        "opened_files": opened,
        "conclusions_not_verified": errors,
        "visibility_complete": not errors,
        "reviewer_verdict": "PASS" if not errors else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    result = audit(args.candidate)
    text = json.dumps(result, indent=2) + "\n"
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(text)
    print(text, end="")
    return 0 if result["visibility_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
