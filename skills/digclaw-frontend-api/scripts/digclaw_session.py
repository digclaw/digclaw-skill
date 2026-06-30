"""Small local session cache for DigClaw helper scripts."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_SESSION_FILE = Path.home() / ".digclaw" / "session.json"


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


def resolve_token(explicit_token=None, session_file=None, allow_session=True):
    if explicit_token:
        return explicit_token, "argument", None
    env_token = os.environ.get("DIGCLAW_ACCESS_TOKEN")
    if env_token:
        return env_token, "environment", None
    if allow_session:
        session = load_session(session_file)
        if session:
            return session["access_token"], "session", session
    return None, None, None
