---
name: digclaw-frontend-api
description: Use when operating DigClaw through the same API-backed capabilities exposed by the Vue frontend, working on DigClaw frontend API calls, backend integration, request debugging, or agent tasks that need page-facing DigClaw functions without browser clicking or legacy unused endpoints.
---

# DigClaw Frontend API

## Overview

Use this skill to operate DigClaw through the API surface that is actually exercised by the Vue frontend. Treat the frontend pages as the source of truth, but prefer direct API calls over browser clicks.

## Base URLs

- Production chat API root: `https://v3-api.diggen.cn`
- Production insight API root: `https://v3-api.diggen.cn/insight`
- Example full request: `https://v3-api.diggen.cn/chat/talents/v2/favorite/list`
- Development uses `/chat` and `/insight` proxies that rewrite to the local backend.

For detailed environment and request behavior, read `references/frontend-context.md`.

## Workflow

1. Check for skill updates once per working session with `python scripts/check_updates.py`. If it reports a newer version and this skill is inside the official git checkout, run `python scripts/check_updates.py --pull`, then read `references/release-notes.md`.
2. Identify the user-facing DigClaw function: search, talent, memo, investor, industry, admin account, report, comment, member, payment, or settings.
3. Read `references/frontend-page-audit.md` when unsure which current page owns a function or whether a page is current versus legacy.
4. Read `references/business-workflows.md` first for execution. Page actions often require multiple calls, polling, and a final refresh.
5. Read `references/api-details.md` for request parameters, request examples, response examples, and status meanings.
6. Use `references/api-map.md` only as the compact endpoint index.
7. Call endpoints directly with `scripts/digclaw_request.py` or an equivalent HTTP client.
8. Preserve the frontend request wrapper behavior: `Authorization: Bearer <access_token>`, `clientid`, JSON payloads by default, and query params for GET.
9. Verify the API response and summarize the result in user-facing terms.
10. If an endpoint is not in the frontend-facing map, verify that a current page imports it before documenting or using it.

## Version Updates

Use `VERSION.json` as the installed skill version source. Use `scripts/check_updates.py --json` when another agent needs machine-readable update status. If auto-pull is unavailable because the skill was copied rather than cloned from GitHub, report the latest version and ask the operator to reinstall or update from `https://github.com/digclaw/digclaw-skill.git`.

## API Operation

Do not use browser page clicks to operate DigClaw unless the user explicitly asks for visual inspection or UI debugging. Prefer direct API operations that mirror frontend page functions.

## Authentication

Current authenticated calls use `DIGCLAW_ACCESS_TOKEN` or `--token`. If no token is available and the user authorizes login, call the frontend-equivalent login helper:

```bash
python scripts/digclaw_login.py --account-num <accountNum> --password <password>
```

The helper posts to `/appAuth/login` with `accountNum`, `password`, `clientId`, and `grantType: appPwd`, then loads `/chat/user/info`, `/chat/user/permission`, and `/chat/user/settings`. It masks the token by default. Use `--token-only` when a follow-up command needs a token in the same shell, or `--include-token` only when the operator explicitly needs the raw token displayed.

Use the bundled request helper:

```bash
python scripts/digclaw_request.py --method GET --path /chat/talents/v2/favorite/list
```

For authenticated requests, set `DIGCLAW_ACCESS_TOKEN` in the environment or pass `--token`. For JSON body and query examples, run:

```bash
python scripts/digclaw_request.py --help
```

## Page Domains

- Auth, user profile, settings, coins, orders, conversations, meeting minutes
- Shared/company data, comments, document members, company annotations
- Smart search for companies and talent
- Talent V2 list, detail, favorites, annotations, connection status, export
- Project Memo, attachments, content paragraphs, FA collaboration, report tasks
- Investor parsing, investor CRUD, attachments, opinions
- AI analysis second-task workflows
- Industry Insight event, person, and opinion dashboards
- Admin account and account-type management

## References

- `references/business-workflows.md`: page-equivalent multi-request business flows
- `references/api-details.md`: parameters, examples, response shapes, and polling statuses
- `references/frontend-page-audit.md`: current route/page/component audit and ownership notes
- `references/frontend-context.md`: project context, inferred API roots, request wrapper behavior
- `references/api-map.md`: frontend-used API functions grouped by page feature
- `references/release-notes.md`: version changes to read after `check_updates.py` reports an update
- `VERSION.json`: machine-readable installed skill version metadata
- `scripts/check_updates.py`: compare/pull the latest GitHub skill version
- `scripts/digclaw_login.py`: frontend-equivalent login and user context helper
- `scripts/digclaw_request.py`: direct HTTP helper for page-equivalent API operations

## Guardrails

- Do not use browser clicks as the default way to perform DigClaw actions.
- Do not treat a single endpoint as a complete page action until checking `business-workflows.md`.
- Do not add backend-only or legacy endpoints unless a current page/component imports the API function.
- Do not hard-code a user's token. Read `access_token` from runtime context or ask the operator to provide one.
- Use `https://v3-api.diggen.cn` for `/chat/...` endpoints and `https://v3-api.diggen.cn/insight` for insight endpoints.
- Keep endpoint docs concise: method, path, frontend function, and page feature are enough unless the page code proves a required payload shape.
