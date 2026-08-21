# DigClaw Skill Release Notes

Read this file when `scripts/check_updates.py` reports a newer version or when the user asks what changed.

## 0.8.1 - 2026-08-21

- Prioritized DigClaw File Transcription for audio/video speech-to-text, image OCR, document text extraction, and transcription record operations.
- Clarified the routing boundary between text extraction, generic file handling, and Rhizome file-based research.
- Added agent-executable examples for existing URLs, multipart local uploads, task start, terminal-status polling, latest-record reuse, history search, and bounded retry behavior.
- Added common failure guidance so agents do not confuse upload with transcription, submit local paths as URLs, poll indefinitely, or return previews as full text.

## 0.8.0 - 2026-08-21

- Rebound the audited frontend to `cbe06ab` and backend to `692affd`.
- Added the `File Transcription` page, permission key, upload/start flow, record filters, processing polling, detail, retry, latest lookup, soft deletion, and local text copy/download behavior.
- Documented persisted transcription records produced by project initialization, memo agents, memo/FA reports, project attachment actions, and second AI analysis.
- Updated Project Connectivity attachment workflows to locate, start, monitor, and inspect attachment transcription text.
- Documented talent-detail skill matching precedence for dynamic `顶级期刊监测` tags versus the cached `AI端侧芯片` fallback.

## 0.7.4 - 2026-08-21

- Required tag-aware frontend operations to fetch current page tag/filter options before related search or list requests.
- Added relevance-based tag selection: use only exact server-provided values when they materially match the user's request; otherwise omit the filter.
- Documented company `businessTags` behavior and talent `tag` normalization, including that displayed record tags and UI `all` values are not request-filter values.

## 0.7.3 - 2026-08-21

- Defined Rhizome Agent's primary role as answering prediction questions and research topics through reasoning and evidence-backed research.
- Added proactive company and talent keyword expansion using synonyms, bilingual variants, adjacent concepts, roles, skills, organizations, products, and locations while preserving hard constraints.
- Required relevance-based retries, later-page retrieval, cross-query deduplication, and sensible stopping conditions instead of stopping after the first successful query.

## 0.7.2 - 2026-08-20

- Added environment credential priority for authenticated helper scripts: `--token`, `DIGCLAW_ACCESS_TOKEN`, account/password environment auto-login, then cached session.
- Added optional `digclaw_login.py --persist-credentials` support for saving `DIGCLAW_ACCOUNT_NUM` and `DIGCLAW_PASSWORD` to the Windows user environment after explicit user approval.
- Updated login/session documentation to ask for DigClaw account/password when no token, credential environment variables, or cached session is available.

## 0.7.1 - 2026-08-19

- Clarified that ordinary company searches should prefer keyword/advanced-filter search first, while telling users natural-language Smart Search is available but usually slower because it runs asynchronously and requires polling.
- Expanded Project Connectivity guidance for `@智能纪要` and `@行业研究`, including action values, request payload shape, attachment context, and memo-detail polling behavior.
- Added project-scoped smart document/AI analysis examples for loading analysis tags, submitting `memoId` tasks, polling progress, and refreshing memo results.

## 0.7.0 - 2026-08-18

- Rebound source metadata to frontend `89c17667925db21ad7a8c98741b7eaa9b71f634b` and backend `3f25dad8dddc58f3d30c58ceacd2dc4c4304fcb4`.
- Added page guides and permission checks for AI Conversation Search, Rhizome Agent, and Public Asset Summary.
- Documented Rhizome Agent's external API integration, file upload, streamed research task flow, and DigClaw-native UI behavior.
- Updated Smart Search/Company Cloud export guidance for CSV URL downloads and MASTER-only curated-list export.
- Updated Account Administration docs for per-user company data restriction, search limits, and search-rate-limit clearing.
- Added Public Asset Summary asset filtering, reparse, investor extraction, and publish workflows.

## 0.6.1 - 2026-06-30

- Clarified that user and agent update checks rely only on `VERSION.json.version`.
- Marked frontend/backend source bindings as developer-only maintenance metadata that must not block skill installation or updates.

## 0.6.0 - 2026-06-30

- Added `VERSION.json.source_bindings` for the audited frontend and backend branches, remotes, and commit IDs.
- Added `references/source-bindings.md` to explain how future skill updates should compare source changes before changing API workflows.
- Added `scripts/check_source_bindings.py` to compare local frontend/backend checkouts with the bound commits.

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
