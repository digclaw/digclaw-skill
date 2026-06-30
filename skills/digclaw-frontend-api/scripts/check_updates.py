#!/usr/bin/env python3
"""Check whether the installed DigClaw skill is behind the GitHub version."""

import argparse
import json
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_LOCAL_VERSION = SKILL_DIR / "VERSION.json"
DEFAULT_LATEST_URL = (
    "https://raw.githubusercontent.com/digclaw/digclaw-skill/main/"
    "skills/digclaw-frontend-api/VERSION.json"
)
EXPECTED_REMOTE_SUFFIX = "github.com/digclaw/digclaw-skill"


def load_json(path):
    with pathlib.Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fetch_json(url, timeout):
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def version_key(version):
    parts = []
    for raw in str(version).split("."):
        digits = ""
        suffix = ""
        for char in raw:
            if char.isdigit() and not suffix:
                digits += char
            else:
                suffix += char
        parts.append((int(digits or 0), suffix))
    while len(parts) < 3:
        parts.append((0, ""))
    return parts


def find_git_root(start):
    current = pathlib.Path(start).resolve()
    for path in (current, *current.parents):
        if (path / ".git").exists():
            return path
    return None


def git_remote_matches(repo_root):
    result = subprocess.run(
        ["git", "-C", str(repo_root), "remote", "get-url", "origin"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return False, result.stderr.strip()
    remote = result.stdout.strip().rstrip(".git")
    normalized = remote.replace("git@github.com:", "https://github.com/")
    return normalized.endswith(EXPECTED_REMOTE_SUFFIX), remote


def pull_latest(repo_root, branch):
    return subprocess.run(
        ["git", "-C", str(repo_root), "pull", "--ff-only", "origin", branch],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def fetch_git_version(local):
    repo_root = find_git_root(SKILL_DIR)
    if not repo_root:
        return None, "not inside a git checkout"

    matches, remote_info = git_remote_matches(repo_root)
    if not matches:
        return None, f"origin is not the official repo ({remote_info})"

    branch = local.get("branch", "main")
    skill_path = local.get("skill_path", "skills/digclaw-frontend-api")
    fetch = subprocess.run(
        ["git", "-C", str(repo_root), "fetch", "origin", branch, "--quiet"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if fetch.returncode != 0:
        return None, (fetch.stdout + fetch.stderr).strip() or "git fetch failed"

    show = subprocess.run(
        ["git", "-C", str(repo_root), "show", f"origin/{branch}:{skill_path}/VERSION.json"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if show.returncode != 0:
        return None, (show.stdout + show.stderr).strip() or "git show failed"

    try:
        return json.loads(show.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"remote VERSION.json is invalid JSON: {exc}"


def main():
    parser = argparse.ArgumentParser(description="Check for DigClaw skill updates.")
    parser.add_argument("--local-version", default=str(DEFAULT_LOCAL_VERSION), help="Path to local VERSION.json")
    parser.add_argument("--latest-url", default=DEFAULT_LATEST_URL, help="Raw URL for latest VERSION.json")
    parser.add_argument("--timeout", type=float, default=20.0, help="Network timeout in seconds")
    parser.add_argument("--pull", action="store_true", help="If behind and inside the official git repo, run git pull --ff-only")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON only")
    args = parser.parse_args()

    try:
        local = load_json(args.local_version)
    except OSError as exc:
        raise SystemExit(f"Cannot read local version file: {exc}") from exc

    remote, git_error = fetch_git_version(local)
    remote_error = git_error
    if remote is None:
        try:
            remote = fetch_json(args.latest_url, args.timeout)
            remote_error = None
        except (urllib.error.URLError, json.JSONDecodeError) as exc:
            remote = None
            raw_error = str(exc)
            remote_error = f"git: {git_error}; raw: {raw_error}" if git_error else raw_error

    local_version = local.get("version", "0.0.0")
    remote_version = remote.get("version") if remote else None
    update_available = bool(remote_version and version_key(remote_version) > version_key(local_version))
    result = {
        "name": local.get("name"),
        "local_version": local_version,
        "remote_version": remote_version,
        "update_available": update_available,
        "local_updated_at": local.get("updated_at"),
        "remote_updated_at": remote.get("updated_at") if remote else None,
        "repo": local.get("repo"),
        "branch": local.get("branch", "main"),
        "release_notes": local.get("release_notes"),
        "remote_error": remote_error,
        "pulled": False,
        "pull_output": None,
    }

    if update_available and args.pull:
        repo_root = find_git_root(SKILL_DIR)
        if not repo_root:
            result["pull_output"] = "Cannot auto-pull: this skill is not inside a git checkout."
        else:
            matches, remote_info = git_remote_matches(repo_root)
            if not matches:
                result["pull_output"] = f"Cannot auto-pull: origin is not the official repo ({remote_info})."
            else:
                pull = pull_latest(repo_root, local.get("branch", "main"))
                result["pulled"] = pull.returncode == 0
                result["pull_output"] = (pull.stdout + pull.stderr).strip()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"Skill: {result['name']}")
    print(f"Local version: {result['local_version']} ({result['local_updated_at']})")
    if result["remote_error"]:
        print(f"Remote check failed: {result['remote_error']}")
        return
    print(f"Latest version: {result['remote_version']} ({result['remote_updated_at']})")
    print("Update available: " + ("yes" if result["update_available"] else "no"))
    if result["update_available"]:
        print(f"Repo: {result['repo']}")
        print(f"Release notes: {result['release_notes']}")
        print("To update this git checkout: python scripts/check_updates.py --pull")
    if result["pull_output"]:
        print(result["pull_output"])


if __name__ == "__main__":
    main()
