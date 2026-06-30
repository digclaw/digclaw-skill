#!/usr/bin/env python3
"""Login to DigClaw like the frontend and optionally load user context."""

import argparse
import getpass
import json
import os
import sys
import urllib.error
import urllib.request

from digclaw_session import masked_token, save_session, session_path


BASE_URL = "https://v3-api.diggen.cn"
DEFAULT_CLIENT_ID = "b7bf1120a216184a9e0f4ca0e9c508bb"


def request_json(method, base_url, path, data=None, token=None, clientid=DEFAULT_CLIENT_ID, timeout=60.0):
    body = None
    headers = {
        "Accept": "application/json",
        "clientid": clientid,
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json;charset=utf-8"

    request = urllib.request.Request(
        base_url.rstrip("/") + "/" + path.lstrip("/"),
        data=body,
        headers=headers,
        method=method.upper(),
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        text = response.read().decode("utf-8", errors="replace")
    return json.loads(text)


def get_secret(value, prompt):
    if value:
        return value
    if sys.stdin.isatty():
        return getpass.getpass(prompt)
    raise SystemExit(f"{prompt.rstrip(': ')} is required. Pass it as an argument or environment variable.")


def extract_token(login_response):
    data = login_response.get("data") if isinstance(login_response, dict) else None
    if not isinstance(data, dict):
        return None
    return data.get("access_token") or data.get("accessToken") or data.get("token")


def redact_token_fields(value):
    if isinstance(value, dict):
        redacted = {}
        for key, item in value.items():
            if key in ("access_token", "accessToken", "token"):
                redacted[key] = masked_token(str(item)) if item else item
            else:
                redacted[key] = redact_token_fields(item)
        return redacted
    if isinstance(value, list):
        return [redact_token_fields(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser(description="Login to DigClaw and load frontend-equivalent user context.")
    parser.add_argument("--account-num", default=os.environ.get("DIGCLAW_ACCOUNT_NUM") or os.environ.get("DIGCLAW_USERNAME"), help="DigClaw account number; defaults to DIGCLAW_ACCOUNT_NUM or DIGCLAW_USERNAME")
    parser.add_argument("--password", default=os.environ.get("DIGCLAW_PASSWORD"), help="DigClaw password; defaults to DIGCLAW_PASSWORD")
    parser.add_argument("--base-url", default=os.environ.get("DIGCLAW_BASE_URL", BASE_URL), help="DigClaw chat API host root")
    parser.add_argument("--clientid", default=os.environ.get("DIGCLAW_CLIENT_ID", DEFAULT_CLIENT_ID), help="DigClaw clientId/clientid")
    parser.add_argument("--grant-type", default="appPwd", help="Login grantType used by the frontend")
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds")
    parser.add_argument("--no-bootstrap", action="store_true", help="Only call /appAuth/login; skip user info, permission, and settings")
    parser.add_argument("--no-cache", action="store_true", help="Do not persist the login session locally")
    parser.add_argument("--session-file", help="Override the local session cache path; defaults to DIGCLAW_SESSION_FILE or ~/.digclaw/session.json")
    parser.add_argument("--include-token", action="store_true", help="Include the raw access token in JSON output")
    parser.add_argument("--token-only", action="store_true", help="Print only the raw access token")
    args = parser.parse_args()

    account_num = get_secret(args.account_num, "accountNum: ")
    password = get_secret(args.password, "password: ")
    login_body = {
        "accountNum": account_num,
        "password": password,
        "clientId": args.clientid,
        "grantType": args.grant_type,
    }

    try:
        login_response = request_json("POST", args.base_url, "/appAuth/login", login_body, clientid=args.clientid, timeout=args.timeout)
        token = extract_token(login_response)
        if not token:
            raise SystemExit("Login response did not contain data.access_token.")

        output = {
            "login": redact_token_fields(login_response),
            "access_token_masked": masked_token(token),
            "access_token": token if args.include_token else None,
            "session_cached": False,
            "session_file": str(session_path(args.session_file)),
            "user_info": None,
            "permission": None,
            "settings": None,
        }
        if not args.no_bootstrap:
            output["user_info"] = request_json("GET", args.base_url, "/chat/user/info", token=token, clientid=args.clientid, timeout=args.timeout)
            output["permission"] = request_json("GET", args.base_url, "/chat/user/permission", token=token, clientid=args.clientid, timeout=args.timeout)
            output["settings"] = request_json("GET", args.base_url, "/chat/user/settings", token=token, clientid=args.clientid, timeout=args.timeout)

        if not args.no_cache:
            save_session({
                "base_url": args.base_url,
                "clientid": args.clientid,
                "account_num": account_num,
                "access_token": token,
                "access_token_masked": masked_token(token),
                "user_info": output["user_info"],
                "permission": output["permission"],
                "settings": output["settings"],
            }, args.session_file)
            output["session_cached"] = True

        if args.token_only:
            print(token)
            return

        print(json.dumps(output, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code} {exc.reason}", file=sys.stderr)
        print(exc.read().decode("utf-8", errors="replace"), file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc.reason}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
