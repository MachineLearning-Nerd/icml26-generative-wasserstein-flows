"""Build the additive, text-only Hugging Face release candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


JUDGED_REVISION = "90e3b80761e36f11697a2f3140c216842b30adb4"
TEXT_SUFFIXES = {".md", ".json", ".py", ".toml", ".lock", ".txt", ".csv"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and ".cache" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )


def copy_tree(source: Path, target: Path) -> None:
    for path in files(source):
        relative = path.relative_to(source)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def write_readme(output: Path) -> None:
    text = """---
title: "Variational Generative Wasserstein Flows — sJ7ngz2eQx"
emoji: 🌊
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-sJ7ngz2eQx
---

# Variational Generative Wasserstein Flows — current verification

Start with the [current claim index](#/index). The exact judged revision
`90e3b80761e36f11697a2f3140c216842b30adb4` is preserved and its previous
overview is labeled **Historical rejected baseline** in navigation.

Current scientific verdicts: Claims 1, 2, 3, and 6 are VERIFIED; Claims 4 and
5 are narrowly FALSIFIED under their exact contracts. These are reproduction
verdicts and a score forecast, not a new live-judge result.
"""
    (output / "README.md").write_text(text)


def write_logbook(output: Path) -> None:
    children = [
        {
            "slug": f"claim{number}",
            "title": f"Claim {number} — current verification",
            "file": f"pages/claims/claim{number}.md",
            "children": [],
        }
        for number in range(1, 7)
    ]
    children.extend(
        [
            {
                "slug": "visibility",
                "title": "Evaluator-visible evidence matrix",
                "file": "pages/visibility_matrix.md",
                "children": [],
            },
            {
                "slug": "red-team",
                "title": "Evaluator-blind red-team review",
                "file": "evidence/release/red_team_review.md",
                "children": [],
            },
            {
                "slug": "overview",
                "title": "Historical rejected baseline",
                "file": "pages/overview/page.md",
                "children": [],
            },
        ]
    )
    payload = {
        "schema_version": 1,
        "title": "Variational Generative Wasserstein Flows — current verification",
        "emoji": "🌊",
        "space_id": "DineshAI/sJ7ngz2eQx",
        "paper": "https://arxiv.org/abs/2605.31369",
        "tags": ["icml2026-repro", "paper-sJ7ngz2eQx"],
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "root": {
            "slug": "index",
            "title": "Current verification",
            "file": "pages/index.md",
            "children": children,
        },
        "agent_view_tokens": 12000,
        "revision": "release-candidate",
    }
    (output / "logbook.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judged-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing to overwrite existing {args.output}")

    args.output.mkdir(parents=True)
    copy_tree(args.judged_dir, args.output)

    history = args.output / "historical" / f"judged-{JUDGED_REVISION}"
    for relative in [Path("README.md"), Path("logbook.json"), Path("pages/index.md")]:
        destination = history / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.judged_dir / relative, destination)

    copy_tree(Path("candidate_space"), args.output)
    copy_tree(Path("verification"), args.output / "verification")
    release_evidence = args.output / "evidence" / "release"
    release_evidence.mkdir(parents=True, exist_ok=True)
    for name in ["red_team_pass1.json", "red_team_pass2.json"]:
        shutil.copy2(Path("reports/gwf_reproduction") / name, release_evidence / name)
    for relative in [
        Path("run_campaign.py"),
        Path("pyproject.toml"),
        Path("uv.lock"),
        Path(".python-version"),
    ]:
        shutil.copy2(relative, args.output / relative)

    write_readme(args.output)
    write_logbook(args.output)

    old_manifest = {
        path.relative_to(args.judged_dir).as_posix(): digest(path)
        for path in files(args.judged_dir)
    }
    preservation = []
    for relative, old_hash in old_manifest.items():
        same_path = args.output / relative
        history_path = history / relative
        if same_path.exists() and digest(same_path) == old_hash:
            preserved = same_path.relative_to(args.output).as_posix()
        elif history_path.exists() and digest(history_path) == old_hash:
            preserved = history_path.relative_to(args.output).as_posix()
        else:
            preserved = None
        preservation.append(
            {
                "original_path": relative,
                "sha256": old_hash,
                "preserved_path": preserved,
            }
        )

    manifests = args.output / "manifests"
    manifests.mkdir()
    subset = {
        "judged_revision": JUDGED_REVISION,
        "old_file_count": len(preservation),
        "subset_pass": all(row["preserved_path"] for row in preservation),
        "files": preservation,
    }
    (manifests / "judged_subset.json").write_text(
        json.dumps(subset, indent=2) + "\n"
    )

    candidate_manifest = {
        path.relative_to(args.output).as_posix(): digest(path)
        for path in files(args.output)
        if path.parent != manifests
    }
    (manifests / "candidate_sha256.json").write_text(
        json.dumps(candidate_manifest, indent=2, sort_keys=True) + "\n"
    )

    original_hashes = {
        relative: old_hash for relative, old_hash in old_manifest.items()
    }
    allowlist = []
    for path in files(args.output):
        relative = path.relative_to(args.output).as_posix()
        if relative.startswith("manifests/"):
            allowlist.append(relative)
            continue
        is_text = path.suffix in TEXT_SUFFIXES or path.name == ".python-version"
        changed = original_hashes.get(relative) != digest(path)
        if is_text and changed:
            allowlist.append(relative)
    allowlist.append("manifests/text_upload_allowlist.txt")
    (manifests / "text_upload_allowlist.txt").write_text(
        "\n".join(sorted(set(allowlist))) + "\n"
    )

    print(
        json.dumps(
            {
                "output": str(args.output),
                "subset_pass": subset["subset_pass"],
                "candidate_files": len(files(args.output)),
                "text_upload_files": len(set(allowlist)),
            },
            indent=2,
        )
    )
    return 0 if subset["subset_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
