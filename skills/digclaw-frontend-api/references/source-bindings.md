# DigClaw Source Bindings

This skill is bound to the frontend and backend source baselines below. Use this file before updating API workflows, permission rules, page maps, or request examples.

## Bound Repositories

| System | Repository | Branch | Commit | Local path used for audit | Notes |
|---|---|---|---|---|---|
| Frontend | `https://github.com/digclaw/digclaw-web.git` | `v3_dev` | `5b656899fd197fd503349cf0d7108cd12eac5bef` | `G:\digclaw_server\diggenai_web` | clean at binding time |
| Backend | `https://github.com/digclaw/digclaw-server.git` | `v3_dev` | `a07c2a3152fb2855ce539c47eaca61aabfab31a6` | `G:\digclaw_server\diggenai` | commit bound; local worktree had untracked `ruoyi-modules/vc-chat/tweitter/__pycache__/` |

Binding date: `2026-06-30`

## Update Rule

When the frontend or backend changes, do not assume this skill still matches the current system. First compare the current source repositories with `VERSION.json.source_bindings`.

Use:

```powershell
python scripts\check_source_bindings.py
```

If the output shows a branch or commit mismatch, read the changed source code before updating the skill. For frontend changes, re-check page components, page permission gates, and request chains. For backend changes, re-check endpoint paths, request parameters, response shapes, status values, and error behavior.

## Path Overrides

If the repositories are not siblings of the skill checkout, pass paths explicitly:

```powershell
python scripts\check_source_bindings.py --frontend-repo "G:\digclaw_server\diggenai_web" --backend-repo "G:\digclaw_server\diggenai"
```

Environment variables are also supported:

- `DIGCLAW_FRONTEND_REPO`
- `DIGCLAW_BACKEND_REPO`
