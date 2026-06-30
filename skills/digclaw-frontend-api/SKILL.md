---
name: digclaw-skill
description: Use when operating DigClaw through the same API-backed capabilities exposed by the Vue frontend, working on DigClaw frontend API calls, backend integration, request debugging, or agent tasks that need page-facing DigClaw functions without browser clicking or legacy unused endpoints.
---

# DigClaw Skill

## Overview

Use this skill to operate DigClaw through the API surface that is actually exercised by the Vue frontend. Treat the frontend pages as the source of truth, but prefer direct API calls over browser clicks.

## Base URLs

- Production chat API root: `https://v3-api.diggen.cn`
- Production insight API root: `https://v3-api.diggen.cn/insight`
- Example full request: `https://v3-api.diggen.cn/chat/talents/v2/favorite/list`
- Development uses `/chat` and `/insight` proxies that rewrite to the local backend.

For detailed environment and request behavior, read `references/frontend-context.md`.

## Workflow

1. Check for skill updates once per working session with `python scripts/check_updates.py`. Normal user and agent updates are based only on `VERSION.json.version`. If it reports a newer version and this skill is inside the official git checkout, run `python scripts/check_updates.py --pull`, then read `references/release-notes.md`.
2. When developing the next skill version or auditing page/API docs, compare the local frontend/backend source repos with `python scripts/check_source_bindings.py`, then read `references/source-bindings.md` before trusting old page/API documentation. Source bindings are developer maintenance context only; do not use them to block user installation or updates.
3. Identify the frontend page/module first, not the endpoint. Read `references/page-operation-index.md` to map UI labels, `activeMenu`, components, permission gates, and page keys.
4. Enforce the frontend permission gate with `python scripts/check_permission.py --page <page-key>`. This uses the cached login session when no token is passed. If it is denied, stop and explain that the current account cannot use the requested page or feature.
5. Read exactly one page guide for the target page: `page-smart-search.md`, `page-talent-matrix.md`, `page-project-connectivity.md`, `page-venture-directory.md`, `page-industry-analysis.md`, `page-admin-accounts.md`, `page-ai-sourcing-analysis.md`, or `page-shell-auth-files.md`.
6. Execute the operation sequence from that page guide, including polling, refresh calls, and child-dialog calls.
7. Use `references/api-details.md` only when request/response examples or field shapes are needed.
8. Use `references/api-map.md` as a compact endpoint index after the page guide, not as the primary workflow source.
9. Call endpoints directly with `scripts/digclaw_request.py` or an equivalent HTTP client.
10. Preserve the frontend request wrapper behavior: `Authorization: Bearer <access_token>`, `clientid`, JSON payloads by default, and query params for GET.
11. Verify the API response and summarize the result in user-facing terms.
12. End every successful user-facing operation with 2-4 contextual next actions so the user knows what they can do next.
13. If an endpoint is not in the page guide or current page audit, verify that a current page/component imports it before documenting or using it.

## Version Updates

Use `VERSION.json.version` as the installed skill version source. Use `scripts/check_updates.py --json` when another agent needs machine-readable update status. Source bindings in `VERSION.json` are not part of update eligibility; they are only for maintainers to know which frontend/backend commits were audited. If auto-pull is unavailable because the skill was copied rather than cloned from GitHub, report the latest version and ask the operator to reinstall or update from `https://github.com/digclaw/digclaw-skill.git`.

## API Operation

Do not use browser page clicks to operate DigClaw unless the user explicitly asks for visual inspection or UI debugging. Prefer direct API operations that mirror frontend page functions.

## Authentication

Current authenticated calls use `DIGCLAW_ACCESS_TOKEN` or `--token`. If no token is available and the user authorizes login, call the frontend-equivalent login helper:

```bash
python scripts/digclaw_login.py --account-num <accountNum> --password <password>
```

The helper posts to `/appAuth/login` with `accountNum`, `password`, `clientId`, and `grantType: appPwd`, then loads `/chat/user/info`, `/chat/user/permission`, and `/chat/user/settings`. It masks the token by default. Use `--token-only` when a follow-up command needs a token in the same shell, or `--include-token` only when the operator explicitly needs the raw token displayed.

Successful login is cached locally by default at `~/.digclaw/session.json` or `DIGCLAW_SESSION_FILE`. The cache stores token and user context, not the password. `scripts/check_permission.py` and `scripts/digclaw_request.py` automatically reuse this session until the server rejects it; on `401` or `403`, clear/recreate the session by logging in again. Read `references/session-and-next-actions.md` for details.

Use the bundled request helper:

```bash
python scripts/digclaw_request.py --method GET --path /chat/talents/v2/favorite/list
```

For authenticated requests, set `DIGCLAW_ACCESS_TOKEN` in the environment or pass `--token`. For JSON body and query examples, run:

```bash
python scripts/digclaw_request.py --help
```

## Permission Enforcement

Frontend-visible permissions are mandatory. Before calling page business APIs, use:

```bash
python scripts/check_permission.py --page <page-key>
```

Read `references/permission-policy.md` for the page-key map and special subfeature rules. Never call backend APIs to bypass a page that the current account type cannot see in the frontend.

## Next Actions

After each successful operation, suggest 2-4 relevant next actions based on the current page and object. Prefer concrete actions like opening a record, filtering a list, viewing attachments, generating a report, changing status, exporting, or running analysis. For denied operations, suggest permission-safe alternatives. See `references/session-and-next-actions.md`.

## Page Domains

- Shell/Auth/Files: login, user profile, settings, conversations, meeting minutes, file tokens
- Smart Search / Company Cloud: company and talent search, history, detail, members, export, CSV tasks
- Talent Matrix: talent list/detail, favorites, annotations, connection status, connection text, export
- Project Connectivity: project memo list/detail, paragraphs, attachments, reports, second analysis, FA collaboration
- Venture Investment Directory: investor parse tasks, investor CRUD, attachments, opinions
- Industry Analysis: insight events, leader people, viewpoints
- Account Administration: admin users and account types
- Special/hidden pages: AI Sourcing, standalone AI Analysis, selected company list, direct CSV task entry

## References

- `references/page-operation-index.md`: page-first map from UI labels/routes to operation guides
- `references/permission-policy.md`: frontend account-type and page permission enforcement rules
- `references/session-and-next-actions.md`: local login session reuse and user-facing next-action prompts
- `references/source-bindings.md`: developer-only bound frontend/backend branches and commit IDs for this skill version
- `references/page-shell-auth-files.md`: shell login, bootstrap, meeting minutes, user/system utilities
- `references/page-smart-search.md`: Smart Search and Company Cloud operations
- `references/page-talent-matrix.md`: Talent Matrix operations
- `references/page-project-connectivity.md`: Project Connectivity, memo, FA, and reports
- `references/page-venture-directory.md`: Venture Investment Directory operations
- `references/page-industry-analysis.md`: Industry Insight page operations
- `references/page-admin-accounts.md`: Account Administration operations
- `references/page-ai-sourcing-analysis.md`: special/hidden AI Sourcing and standalone AI Analysis operations
- `references/business-workflows.md`: page-equivalent multi-request business flows
- `references/api-details.md`: parameters, examples, response shapes, and polling statuses
- `references/frontend-page-audit.md`: current route/page/component audit and ownership notes
- `references/frontend-context.md`: project context, inferred API roots, request wrapper behavior
- `references/api-map.md`: frontend-used API functions grouped by page feature
- `references/release-notes.md`: version changes to read after `check_updates.py` reports an update
- `VERSION.json`: machine-readable installed skill version metadata
- `scripts/check_updates.py`: compare/pull the latest GitHub skill version
- `scripts/check_source_bindings.py`: compare local frontend/backend repos with developer-only `VERSION.json` source bindings
- `scripts/check_permission.py`: enforce frontend page permission gates before API calls
- `scripts/digclaw_session.py`: shared local session cache support for helper scripts
- `scripts/digclaw_login.py`: frontend-equivalent login and user context helper
- `scripts/digclaw_request.py`: direct HTTP helper for page-equivalent API operations

## Guardrails

- Do not use browser clicks as the default way to perform DigClaw actions.
- Do not bypass frontend permission/account-type gates; if `check_permission.py` denies access, stop before any business API call.
- Deny by default when permission data is unavailable, stale, or does not include the requested page feature.
- Do not treat a single endpoint as a complete page action until checking `business-workflows.md`.
- Do not add backend-only or legacy endpoints unless a current page/component imports the API function.
- Do not hard-code a user's token. Read `access_token` from runtime context or ask the operator to provide one.
- Do not store passwords in the session cache. Persist only token and user context.
- Do not end a successful operation without giving the user practical next-step options.
- Use `https://v3-api.diggen.cn` for `/chat/...` endpoints and `https://v3-api.diggen.cn/insight` for insight endpoints.
- Keep endpoint docs concise: method, path, frontend function, and page feature are enough unless the page code proves a required payload shape.
