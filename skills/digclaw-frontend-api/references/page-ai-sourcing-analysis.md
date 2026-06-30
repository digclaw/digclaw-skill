# Page Module: Special Pages - AI Sourcing And Standalone AI Analysis

Source: `Home/share.vue`, `Home/ElitedCompany.vue`, `Home/AiAnalyze.vue`, `FindCompany.vue`, `FindCompanyResultList.vue`.

These entries still exist in current code, but their sidebar menu items are commented or permission-hidden in `home.vue`. Use them only when the user explicitly asks about AI Sourcing, selected/legacy company lists, standalone AI analysis, file management, or old preview flows. For the visible company search experience, prefer `page-smart-search.md`.

Permission gates: `ai-sourcing` for AI Sourcing / selected company list, `standalone-ai-analysis` for standalone AI Analysis, and `file-management` for file management actions.

## AI Sourcing / Selected Company List

Current components: `Share.vue`, `ElitedCompany.vue`, `ComapnyPanel.vue`, `soucingDetailPanel.vue`.

### Responsibilities

- Shared/selected company list with filters and status counts.
- Company detail and status operations.
- Like/unlike, comments, member assignment.
- Legacy CSV/company discovery task entry.
- Preview route for generated files.

### Initial/List Flow

1. `GET /chat/label/list`.
2. `GET /chat/search/searchval`.
3. `GET /chat/company/contactStatus/count` when counts are needed.
4. `GET /chat/company/list` with filters such as label, team, area, business point, found date, status, paging.
5. For CSV task entry: `GET /chat/custom-company/tasks`.

### Row Detail And Actions

| Operation | API |
|---|---|
| Detail | `GET /chat/company/detail` or current vector detail in child panel |
| Toggle project status | `POST /chat/project/toggleStatus` |
| Contact/cancel contact | `POST /chat/project/contact`, `POST /chat/project/cancelContact` |
| Like/unlike | `POST /chat/company/like`, `POST /chat/company/unlike` |
| Company comments | `/chat/comment/company/list`, `/create` |
| Company annotation | `/chat/company/annotation/list`, `/add?companyId={id}` |
| Assign member | `POST /chat/companyMember/register` |
| Export selected company data | `POST /chat/company/export` |

## Standalone AI Analysis

Current component: `Home/AiAnalyze.vue`. Project-scoped analysis from Project Connectivity uses `AIAnalyzeDialog.vue`; prefer that page guide when a `memoId` is involved.

### Initial Load

1. `GET /chat/file/getTemporaryToken`.
2. `GET /chat/analysis/keywords`.
3. `GET /chat/analysis/second/all-results`.
4. Start a refresh loop for task result rows until all `status === 2`.

### Submit Analysis

1. Upload files to OSS.
2. `POST /chat/analysis/second/submit-task` with `files`, `extraText`, `keywordText`.
3. Poll `GET /chat/analysis/second/task-progress?taskId={id}` every ~5 seconds.
4. Refresh `GET /chat/analysis/second/all-results`.
5. Delete result: `POST /chat/analysis/second/delete-task`.
