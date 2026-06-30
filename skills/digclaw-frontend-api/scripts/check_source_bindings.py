#!/usr/bin/env python3
"""Compare local DigClaw source repos with the commits bound in VERSION.json."""

import argparse
import json
import os
import pathlib
import subprocess
import sys


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_VERSION_FILE = SKILL_DIR / "VERSION.json"


def run_git(repo, args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stdout + result.stderr).strip() or "git command failed")
    return result.stdout.strip()


def find_git_root(start):
    current = pathlib.Path(start).resolve()
    for path in (current, *current.parents):
        if (path / ".git").exists():
            return path
    return None


def default_repo_path(name):
    skill_repo = find_git_root(SKILL_DIR)
    if not skill_repo:
        return None
    return skill_repo.parent / name


def load_bindings(path):
    with pathlib.Path(path).open("r", encoding="utf-8") as handle:
        version = json.load(handle)
    return version.get("source_bindings", {})


def inspect_repo(repo):
    repo_path = pathlib.Path(repo).resolve()
    status = run_git(repo_path, ["status", "--short"])
    return {
        "path": str(repo_path),
        "branch": run_git(repo_path, ["branch", "--show-current"]),
        "commit": run_git(repo_path, ["rev-parse", "HEAD"]),
        "remote": run_git(repo_path, ["remote", "get-url", "origin"]),
        "dirty": bool(status),
        "status": status.splitlines() if status else [],
    }


def compare(label, bound, repo):
    if not repo:
        return {
            "label": label,
            "ok": False,
            "reason": "repository path was not provided and no default sibling repo was found",
            "bound": bound,
            "current": None,
        }
    try:
        current = inspect_repo(repo)
    except Exception as exc:
        return {
            "label": label,
            "ok": False,
            "reason": str(exc),
            "bound": bound,
            "current": {"path": str(repo)},
        }

    mismatches = []
    for key in ("branch", "commit", "remote"):
        expected = bound.get(key)
        actual = current.get(key)
        if expected and expected != actual:
            mismatches.append({"field": key, "expected": expected, "actual": actual})

    return {
        "label": label,
        "ok": not mismatches,
        "reason": "matches bound source" if not mismatches else "branch/commit/remote mismatch",
        "bound": bound,
        "current": current,
        "mismatches": mismatches,
    }


def main():
    parser = argparse.ArgumentParser(description="Check frontend/backend repos against DigClaw skill source bindings.")
    parser.add_argument("--version-file", default=str(DEFAULT_VERSION_FILE), help="Path to VERSION.json")
    parser.add_argument("--frontend-repo", default=os.environ.get("DIGCLAW_FRONTEND_REPO"), help="Frontend repo path")
    parser.add_argument("--backend-repo", default=os.environ.get("DIGCLAW_BACKEND_REPO"), help="Backend repo path")
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    args = parser.parse_args()

    bindings = load_bindings(args.version_file)
    frontend_repo = args.frontend_repo or default_repo_path("diggenai_web")
    backend_repo = args.backend_repo or default_repo_path("diggenai")

    checks = [
        compare("frontend", bindings.get("frontend", {}), frontend_repo),
        compare("backend", bindings.get("backend", {}), backend_repo),
    ]
    output = {"ok": all(item["ok"] for item in checks), "checks": checks}

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        for item in checks:
            marker = "OK" if item["ok"] else "MISMATCH"
            current = item.get("current") or {}
            print(f"{marker} {item['label']}: {item['reason']}")
            if current:
                print(f"  path: {current.get('path')}")
                print(f"  branch: {current.get('branch')}")
                print(f"  commit: {current.get('commit')}")
                if current.get("dirty"):
                    print("  dirty worktree:")
                    for line in current.get("status", []):
                        print(f"    {line}")

    sys.exit(0 if output["ok"] else 1)


if __name__ == "__main__":
    main()
