# Session Cache And Next Actions

## Session Cache

`scripts/digclaw_login.py` saves a local session after successful login unless `--no-cache` is passed.

Default cache path:

```text
~/.digclaw/session.json
```

The cache contains the access token, masked token, account number, client id, user info, permissions, settings, and cache time. It does not store the password.

Helpers that automatically use the cache:

- `scripts/check_permission.py`
- `scripts/digclaw_request.py`

Resolution order:

1. `--token`
2. `DIGCLAW_ACCESS_TOKEN`
3. cached session

If the server rejects a cached token with `401` or `403`, the helper clears the cache and the agent must ask the user to log in again or run `scripts/digclaw_login.py` again with credentials.

Useful commands:

```powershell
python scripts\digclaw_login.py --account-num "<accountNum>" --password "<password>"
python scripts\check_permission.py --page project-connectivity
python scripts\digclaw_request.py --method GET --path "/chat/project-memo/list?pageNum=1&pageSize=20"
```

Use `--session-file` to isolate test sessions. Use `--no-session` when a command must ignore cached login state.

## User-Facing Next Actions

After every successful user operation, include a short "Next you can..." section. Keep it contextual and useful; do not list every system capability.

Good next actions are based on the current page and object:

- After listing projects: open a project, filter by status/leader, search by keyword, show details, summarize attachments.
- After opening a project: view meeting notes, inspect attachments, generate or view reports, run second analysis, update project status, find recommended investors.
- After listing talents: open a talent, filter by tags/status, export, add annotation, generate connection text.
- After opening a company: view members, comments, status, export, assign owner, continue search.
- After admin work: create/update users, manage account types, verify permissions with a non-master account.

For denied operations, suggest permission-safe alternatives: ask an administrator to grant the required frontend permission, switch account, or choose a page the current account can access.
