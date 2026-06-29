#!/usr/bin/env python3
"""Call DigClaw frontend-backed API endpoints without browser automation."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


CHAT_BASE_URL = "https://v3-api.diggen.cn"
INSIGHT_BASE_URL = "https://v3-api.diggen.cn/insight"
DEFAULT_CLIENT_ID = "b7bf1120a216184a9e0f4ca0e9c508bb"


def parse_json_arg(value, name):
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{name} must be valid JSON: {exc}") from exc


def build_url(base_url, path, params):
    if path.startswith("http://") or path.startswith("https://"):
        url = path
    else:
        url = base_url.rstrip("/") + "/" + path.lstrip("/")
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        separator = "&" if urllib.parse.urlparse(url).query else "?"
        url = url + separator + query
    return url


def pretty_print_response(status, headers, body):
    content_type = headers.get("Content-Type", "")
    text = body.decode("utf-8", errors="replace")
    if "application/json" in content_type or text[:1] in ("{", "["):
        try:
            print(json.dumps(json.loads(text), ensure_ascii=False, indent=2))
            return
        except json.JSONDecodeError:
            pass
    print(text)


def main():
    parser = argparse.ArgumentParser(description="Call DigClaw API endpoints that mirror frontend page functions.")
    parser.add_argument("--method", required=True, help="HTTP method, such as GET, POST, PUT, DELETE")
    parser.add_argument("--path", required=True, help="Endpoint path, for example /chat/talents/v2/favorite/list")
    parser.add_argument("--base", choices=["chat", "insight"], default="chat", help="Known production API base")
    parser.add_argument("--base-url", help="Override the API base URL")
    parser.add_argument("--params", help="JSON object encoded as query params")
    parser.add_argument("--data", help="JSON request body")
    parser.add_argument("--token", default=os.environ.get("DIGCLAW_ACCESS_TOKEN"), help="Bearer token; defaults to DIGCLAW_ACCESS_TOKEN")
    parser.add_argument("--clientid", default=os.environ.get("DIGCLAW_CLIENT_ID", DEFAULT_CLIENT_ID), help="DigClaw clientid header")
    parser.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds")
    args = parser.parse_args()

    params = parse_json_arg(args.params, "--params")
    data = parse_json_arg(args.data, "--data")
    if params is not None and not isinstance(params, dict):
        raise SystemExit("--params must be a JSON object")

    base_url = args.base_url or (INSIGHT_BASE_URL if args.base == "insight" else CHAT_BASE_URL)
    body = None
    headers = {
        "Accept": "application/json",
        "clientid": args.clientid,
    }
    if args.token:
        headers["Authorization"] = "Bearer " + args.token
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json;charset=utf-8"

    url = build_url(base_url, args.path, params)
    request = urllib.request.Request(url, data=body, headers=headers, method=args.method.upper())

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            pretty_print_response(response.status, response.headers, response.read())
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code} {exc.reason}", file=sys.stderr)
        pretty_print_response(exc.code, exc.headers, exc.read())
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc.reason}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
