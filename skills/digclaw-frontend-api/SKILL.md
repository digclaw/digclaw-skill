---
name: digclaw-frontend-api
description: Use when working on DigClaw frontend pages, Vue API calls, backend integration, request debugging, or agent tasks that need the current DigClaw page-facing API surface without relying on legacy unused endpoints.
---

# DigClaw Frontend API

## Overview

Use this skill to work with the API surface that is actually exercised by the DigClaw Vue frontend. Treat the frontend pages as the source of truth; do not assume every backend controller or historical API is still active.

## Base URLs

- Production chat API root: `https://v3-api.diggen.cn`
- Production insight API root: `https://v3-api.diggen.cn/insight`
- Example full request: `https://v3-api.diggen.cn/chat/talents/v2/favorite/list`
- Development uses `/chat` and `/insight` proxies that rewrite to the local backend.

For detailed environment and request behavior, read `references/frontend-context.md`.

## Workflow

1. Identify the frontend page or component being changed.
2. Find the imported API functions from `src/api/*.js`.
3. Use only the matching function and endpoint entries in `references/api-map.md`.
4. Preserve the existing request wrapper behavior: `Authorization: Bearer <access_token>`, `clientid`, JSON payloads by default, and query params for GET.
5. If an endpoint is not in the frontend-facing map, verify that a page imports it before documenting or using it.
6. When adding a new page feature, update the frontend API wrapper first, then update `references/api-map.md`.

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

## Guardrails

- Do not add backend-only or legacy endpoints unless a current page/component imports the API function.
- Do not hard-code a user's token. Read `access_token` from runtime context or ask the operator to provide one.
- Use `https://v3-api.diggen.cn` for `/chat/...` endpoints and `https://v3-api.diggen.cn/insight` for insight endpoints.
- Keep endpoint docs concise: method, path, frontend function, and page feature are enough unless the page code proves a required payload shape.
