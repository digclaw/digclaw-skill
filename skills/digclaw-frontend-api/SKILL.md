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

1. Identify the user-facing DigClaw function: search, talent, memo, investor, admin account, report, comment, member, payment, or settings.
2. Read `references/api-map.md` and select the endpoint that backs the matching frontend page capability.
3. Call the endpoint directly with `scripts/digclaw_request.py` or an equivalent HTTP client.
4. Preserve the frontend request wrapper behavior: `Authorization: Bearer <access_token>`, `clientid`, JSON payloads by default, and query params for GET.
5. Verify the API response and summarize the result in user-facing terms.
6. If an endpoint is not in the frontend-facing map, verify that a current page imports it before documenting or using it.

## API Operation

Do not use browser page clicks to operate DigClaw unless the user explicitly asks for visual inspection or UI debugging. Prefer direct API operations that mirror frontend page functions.

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

- `references/frontend-context.md`: project context, inferred API roots, request wrapper behavior
- `references/api-map.md`: frontend-used API functions grouped by page feature
- `scripts/digclaw_request.py`: direct HTTP helper for page-equivalent API operations

## Guardrails

- Do not use browser clicks as the default way to perform DigClaw actions.
- Do not add backend-only or legacy endpoints unless a current page/component imports the API function.
- Do not hard-code a user's token. Read `access_token` from runtime context or ask the operator to provide one.
- Use `https://v3-api.diggen.cn` for `/chat/...` endpoints and `https://v3-api.diggen.cn/insight` for insight endpoints.
- Keep endpoint docs concise: method, path, frontend function, and page feature are enough unless the page code proves a required payload shape.
