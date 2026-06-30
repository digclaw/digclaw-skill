#!/usr/bin/env python3
"""Check whether the current DigClaw account can use a frontend page feature."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


BASE_URL = "https://v3-api.diggen.cn"
DEFAULT_CLIENT_ID = "b7bf1120a216184a9e0f4ca0e9c508bb"

PAGE_RULES = {
    "shell": {"kind": "login"},
    "smart-search": {"functions": ["Smart Search"]},
    "smart-search.company-search": {"functions": ["Smart Search", "Company Search"]},
    "smart-search.curated-list": {"functions": ["Smart Search", "View Curated List"]},
    "talent-matrix": {"functions": ["Talent Matrix"]},
    "project-connectivity": {"functions": ["Project Connectivity"]},
    "venture-directory": {"functions": ["Venture Investment Directory"]},
    "industry-analysis": {"functions": ["Industry Analysis"]},
    "admin-accounts": {"kind": "admin"},
    "file-management": {"permission_levels": [3, 5]},
    "standalone-ai-analysis": {"permission_levels": [3]},
    "ai-sourcing": {"permission_level_not": [0]},
}


def request_json(method, base_url, path, token, clientid, timeout):
    headers = {
        "Accept": "application/json",
        "clientid": clientid,
        "Authorization": "Bearer " + token,
    }
    request = urllib.request.Request(
        base_url.rstrip("/") + "/" + path.lstrip("/"),
        headers=headers,
        method=method.upper(),
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        text = response.read().decode("utf-8", errors="replace")
    return json.loads(text)


def unwrap_data(response):
    if isinstance(response, dict) and isinstance(response.get("data"), dict):
        return response["data"]
    if isinstance(response, dict):
        return response
    return {}


def normalize_functions(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        try:
            decoded = json.loads(text)
            if isinstance(decoded, list):
                return [str(item) for item in decoded if str(item)]
        except json.JSONDecodeError:
            pass
        return [part.strip() for part in text.split(",") if part.strip()]
    return [str(value)]


def normalize_permission_level(value):
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


def first_present(*values):
    for value in values:
        if value is not None and value != "":
            return value
    return None


def build_context(user_info_response, permission_response):
    user_info = unwrap_data(user_info_response)
    permission = unwrap_data(permission_response)

    account_type = first_present(permission.get("accountType"), user_info.get("accountType"))
    permission_level = normalize_permission_level(
        first_present(permission.get("permissionLevel"), user_info.get("permissionLevel"))
    )
    accessible_functions = normalize_functions(
        first_present(permission.get("accessibleFunctions"), user_info.get("accessibleFunctions"))
    )
    effective_functions = list(dict.fromkeys(accessible_functions))

    if account_type == "MASTER" and "Account Administration" not in effective_functions:
        effective_functions.append("Account Administration")

    return {
        "accountType": account_type,
        "permissionLevel": permission_level,
        "accessibleFunctions": accessible_functions,
        "effectiveFunctions": effective_functions,
    }


def decide(page, context):
    rule = PAGE_RULES.get(page)
    if not rule:
        return False, "Unknown page key. Deny by default."

    if rule.get("kind") == "login":
        return True, "Authenticated user context is available."

    functions = set(context["effectiveFunctions"])
    account_type = context["accountType"]
    permission_level = context["permissionLevel"]

    if rule.get("kind") == "admin":
        allowed = account_type == "MASTER" or "Account Administration" in functions
        reason = "Requires MASTER accountType or Account Administration."
        return allowed, reason

    required_functions = rule.get("functions", [])
    if required_functions:
        missing = [name for name in required_functions if name not in functions]
        if missing:
            return False, "Missing frontend accessibleFunctions: " + ", ".join(missing)
        return True, "Required frontend accessibleFunctions are present."

    if "permission_levels" in rule:
        allowed = permission_level in rule["permission_levels"]
        reason = "Requires permissionLevel in " + json.dumps(rule["permission_levels"])
        return allowed, reason

    if "permission_level_not" in rule:
        denied_levels = rule["permission_level_not"]
        allowed = permission_level is not None and permission_level not in denied_levels
        reason = "Requires permissionLevel not in " + json.dumps(denied_levels)
        return allowed, reason

    return False, "No rule matched. Deny by default."


def main():
    parser = argparse.ArgumentParser(description="Enforce DigClaw frontend page permission gates before API use.")
    parser.add_argument("--page", required=True, choices=sorted(PAGE_RULES.keys()), help="Frontend page or subfeature key")
    parser.add_argument("--token", default=os.environ.get("DIGCLAW_ACCESS_TOKEN"), help="Bearer token; defaults to DIGCLAW_ACCESS_TOKEN")
    parser.add_argument("--base-url", default=os.environ.get("DIGCLAW_BASE_URL", BASE_URL), help="DigClaw chat API host root")
    parser.add_argument("--clientid", default=os.environ.get("DIGCLAW_CLIENT_ID", DEFAULT_CLIENT_ID), help="DigClaw clientid header")
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds")
    parser.add_argument("--soft", action="store_true", help="Always exit 0 after printing JSON, even when denied")
    args = parser.parse_args()

    if not args.token:
        print(json.dumps({
            "page": args.page,
            "allowed": False,
            "reason": "DIGCLAW_ACCESS_TOKEN or --token is required before checking permissions.",
        }, ensure_ascii=False, indent=2))
        sys.exit(0 if args.soft else 2)

    try:
        user_info = request_json("GET", args.base_url, "/chat/user/info", args.token, args.clientid, args.timeout)
        permission = request_json("GET", args.base_url, "/chat/user/permission", args.token, args.clientid, args.timeout)
        context = build_context(user_info, permission)
        allowed, reason = decide(args.page, context)
        print(json.dumps({
            "page": args.page,
            "allowed": allowed,
            "reason": reason,
            **context,
        }, ensure_ascii=False, indent=2))
        if not allowed and not args.soft:
            sys.exit(2)
    except urllib.error.HTTPError as exc:
        print(json.dumps({
            "page": args.page,
            "allowed": False,
            "reason": f"Permission request failed with HTTP {exc.code}.",
            "body": exc.read().decode("utf-8", errors="replace"),
        }, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(json.dumps({
            "page": args.page,
            "allowed": False,
            "reason": "Permission request failed: " + str(exc.reason),
        }, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
