# DigClaw Page Operation Index

Use this index first. The current frontend is route `/` -> `src/views/home.vue`; it switches sidebar pages by `activeMenu`. Treat each page as a business module with its own operations and request chains.

## Current Route And Page Map

| UI page | `activeMenu` | Current component | Permission label | Page guide |
|---|---:|---|---|---|
| App shell, login, user, files | shell | `src/views/home.vue` | login-dependent | `page-shell-auth-files.md` |
| 智能搜索 / 公司云库 | 9 | `Home/SmartSearch.vue` | `Smart Search` | `page-smart-search.md` |
| 人才矩阵 | 7 | `Home/Talents.vue` + talent panels | `Talent Matrix` | `page-talent-matrix.md` |
| 项目通联 | 4 | `Home/NewMemoV3.vue` + memo dialogs | `Project Connectivity` | `page-project-connectivity.md` |
| 创投名录 | 12 | `Home/Investors1.vue` + investor dialogs | `Venture Investment Directory` | `page-venture-directory.md` |
| 行业探析 | 11 | `Home/IndustryAnalyze.vue` + tabs/dialogs | `Industry Analysis` | `page-industry-analysis.md` |
| 账号管理 | 13 | `Home/AdminAccounts.vue` | `MASTER` or `Account Administration` | `page-admin-accounts.md` |
| Special/hidden pages | 2, 3, 8 | file management, `Home/share.vue`, `Home/AiAnalyze.vue` | permission/commented menu | `page-ai-sourcing-analysis.md` |

## Secondary Routes

- `/preview`: meeting/project preview page.
- `/memoPreview`: memo preview page.
- `/memoAttachmentPreview`: memo attachment preview route used by attachment/report dialogs.
- `/home1`: legacy shell (`src/views/index.vue`); do not document new operations from it unless the user explicitly asks about legacy behavior.
- `activeMenu === 6` opens `FindCompany.vue` directly; in the current visible flow it is usually reached from Smart Search or AI Sourcing CSV task entry.

## Page-First Usage Rule

1. Identify the page from the user's wording or the UI label.
2. Read that page guide before using `api-map.md`.
3. Execute the page operation sequence, including polling and refresh calls.
4. Use `api-details.md` only for parameter examples and response examples.
5. If an API helper exists but is not imported by the current page or its active child components, treat it as legacy or backend-only.

## Shared Operation Rules

- Authenticated requests need `Authorization: Bearer <access_token>` and `clientid`.
- When no token is available and login is authorized, use `scripts/digclaw_login.py`.
- File uploads usually require `GET /chat/file/getTemporaryToken`, OSS upload, then a page-specific register/update API.
- Mutations should refresh the same list/detail data the page refreshes.
- Async work should be submitted, polled to terminal state, then followed by page refresh calls.
