"""Small local session cache for DigClaw helper scripts."""

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_SESSION_FILE = Path.home() / ".digclaw" / "session.json"
DEFAULT_CLIENT_ID = "b7bf1120a216184a9e0f4ca0e9c508bb"


def session_path(path=None):
    value = path or os.environ.get("DIGCLAW_SESSION_FILE")
    if value:
        return Path(value).expanduser()
    return DEFAULT_SESSION_FILE


def load_session(path=None):
    target = session_path(path)
    if not target.exists():
        return None
    try:
        with target.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or not data.get("access_token"):
        return None
    return data


def save_session(data, path=None):
    target = session_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(data)
    payload["cached_at"] = datetime.now(timezone.utc).isoformat()
    with target.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    try:
        os.chmod(target, 0o600)
    except OSError:
        pass
    return target


def clear_session(path=None):
    target = session_path(path)
    try:
        target.unlink()
        return True
    except FileNotFoundError:
        return False
    except OSError:
        return False


def masked_token(token):
    if not token:
        return None
    if len(token) <= 12:
        return "***"
    return token[:6] + "..." + token[-6:]


def env_account_credentials():
    account_num = os.environ.get("DIGCLAW_ACCOUNT_NUM") or os.environ.get("DIGCLAW_USERNAME")
    password = os.environ.get("DIGCLAW_PASSWORD")
    if account_num and password:
        return account_num, password
    return None, None


def extract_token(login_response):
    data = login_response.get("data") if isinstance(login_response, dict) else None
    if not isinstance(data, dict):
        return None
    return data.get("access_token") or data.get("accessToken") or data.get("token")


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


def login_with_env_credentials(base_url, clientid=DEFAULT_CLIENT_ID, timeout=60.0, session_file=None, bootstrap=False):
    account_num, password = env_account_credentials()
    if not account_num or not password:
        return None, None

    login_response = request_json(
        "POST",
        base_url,
        "/appAuth/login",
        {
            "accountNum": account_num,
            "password": password,
            "clientId": clientid,
            "grantType": "appPwd",
        },
        clientid=clientid,
        timeout=timeout,
    )
    token = extract_token(login_response)
    if not token:
        raise RuntimeError("Login response did not contain data.access_token.")

    user_info = permission = settings = None
    if bootstrap:
        user_info = request_json("GET", base_url, "/chat/user/info", token=token, clientid=clientid, timeout=timeout)
        permission = request_json("GET", base_url, "/chat/user/permission", token=token, clientid=clientid, timeout=timeout)
        settings = request_json("GET", base_url, "/chat/user/settings", token=token, clientid=clientid, timeout=timeout)

    session = {
        "base_url": base_url,
        "clientid": clientid,
        "account_num": account_num,
        "access_token": token,
        "access_token_masked": masked_token(token),
        "user_info": user_info,
        "permission": permission,
        "settings": settings,
        "source": "environment-login",
    }
    save_session(session, session_file)
    return token, session


def resolve_token(explicit_token=None, session_file=None, allow_session=True, allow_env_login=False, base_url=None, clientid=DEFAULT_CLIENT_ID, timeout=60.0):
    if explicit_token:
        return explicit_token, "argument", None
    env_token = os.environ.get("DIGCLAW_ACCESS_TOKEN")
    if env_token:
        return env_token, "environment", None
    if allow_env_login:
        token, session = login_with_env_credentials(base_url, clientid=clientid, timeout=timeout, session_file=session_file)
        if token:
            return token, "environment-login", session
    if allow_session:
        session = load_session(session_file)
        if session:
            return session["access_token"], "session", session
    return None, None, None
