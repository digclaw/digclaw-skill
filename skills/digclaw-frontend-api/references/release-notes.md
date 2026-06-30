# DigClaw Skill Release Notes

Read this file when `scripts/check_updates.py` reports a newer version or when the user asks what changed.

## 0.5.1 - 2026-06-30

- Renamed the skill metadata name from `digclaw-frontend-api` to `digclaw-skill`.
- Updated UI-facing agent metadata to display `DigClaw Skill`.
- Kept the existing `skills/digclaw-frontend-api` install path so current auto-update checks remain compatible.

## 0.5.0 - 2026-06-30

- Added `scripts/digclaw_session.py` for persistent local session caching after login.
- Updated `digclaw_login.py` to cache access token and user context by default without storing passwords.
- Updated `check_permission.py` and `digclaw_request.py` to reuse cached sessions and clear them when the server rejects a cached token.
- Added `references/session-and-next-actions.md` and required contextual next-step suggestions after successful user operations.

## 0.4.0 - 2026-06-30

- Added `references/permission-policy.md` with the frontend-derived account-type and page permission rules.
- Added `scripts/check_permission.py` so agents can verify the current token's page access before business API calls.
- Updated `SKILL.md`, page index guidance, and agent metadata so denied frontend permissions stop execution even when backend endpoints would respond.

## 0.3.0 - 2026-06-30

- Replanned the skill around frontend page modules instead of endpoint-first lookup.
- Added `page-operation-index.md` and per-page guides for Shell/Auth/Files, Smart Search, Talent Matrix, Project Connectivity, Venture Directory, Industry Analysis, Admin Accounts, and special/hidden AI Sourcing plus standalone AI Analysis pages.
- Updated `SKILL.md` so agents choose the page guide first, then use API details and the endpoint map as supporting references.

## 0.2.2 - 2026-06-30

- Added `scripts/digclaw_login.py` to call `/appAuth/login` with the same fields as the frontend.
- Documented that frontend login state is based on `localStorage.access_token` and `Authorization: Bearer <access_token>`.
- Added login examples and bootstrap calls for user info, permissions, and settings.

## 0.2.1 - 2026-06-30

- Updated `scripts/check_updates.py` to prefer `git fetch` plus `git show origin/main:.../VERSION.json` for version checks.
- Kept raw GitHub URL checking as a fallback for non-git installs.
- This makes update checks work even when GitHub raw access is unavailable but git credentials are configured.

## 0.2.0 - 2026-06-30

- Added `VERSION.json` for machine-readable skill version metadata.
- Added `scripts/check_updates.py` to compare the installed skill with the GitHub `main` version.
- Added update guidance to `SKILL.md` so agents can check for a newer skill before using stale API workflows.

## 0.1.0 - 2026-06-30

- Documented the current Vue frontend page audit.
- Expanded page-equivalent business workflows for Smart Search, Talent Matrix, Project Memo, FA collaboration, Investor Directory, AI Analysis, Industry Insight, and Admin Accounts.
- Added request examples, response examples, async polling rules, and current-page field corrections.
