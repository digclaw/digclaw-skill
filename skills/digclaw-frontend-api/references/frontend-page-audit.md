# DigClaw Frontend Page Audit

This audit is based on the current Vue frontend code. Use it to decide which page owns a user-visible function before choosing APIs.

## Route Shells

- Current app entry: `src/router/index.js` maps `/` to `src/views/home.vue`.
- Legacy app entry: `/home1` maps to `src/views/index.vue`. Prefer the `/` app unless the user explicitly asks about the legacy page.
- Preview routes:
  - `/preview`: `src/views/Main/Preview.vue`
  - `/memoPreview`: `src/views/Main/MemoPreview.vue`
  - `/memoAttachmentPreview`: `src/views/Home/components/MemoAttachmentPreview.vue`
- `src/views/home.vue` is the current page shell. It controls login, permissions, theme/sidebar state, current menu, user info, file management, conversation history, meeting-minute upload/generation, and opens child pages.

## Current Shell Menu

The visible current shell uses `accessibleFunctions` from `GET /chat/user/permission`.

| Menu | Component | Permission name | Notes |
|---|---|---|---|
| Smart Search | `Home/SmartSearch.vue` | `Smart Search` | Contains company search, curated list access, CSV-generated company search entry, and talent natural search. |
| Talent Matrix | `Home/Talents.vue` | `Talent Matrix` | Current talent V2 page. |
| Project Connectivity | `Home/NewMemoV3.vue` | `Project Connectivity` | Current Project Memo page plus FA collaboration and AI analysis dialogs. |
| Venture Investment Directory | `Home/Investors1.vue` | `Venture Investment Directory` | Investor directory, parsing tasks, opinions. |
| Industry Analysis | `Home/IndustryAnalyze.vue` | `Industry Analysis` | Insight event/person/opinion dashboard. |
| Account Administration | `Home/AdminAccounts.vue` | `Account Administration` or `MASTER` | Opened through account/admin action, not normal left menu. |

Hidden or mostly legacy entries in the current shell include AI Sourcing (`Home/share.vue`), file management (`activeMenu === 2`), standalone AI analysis (`Home/AiAnalyze.vue`), and FindCompany CSV upload. They still exist in the current component tree and can be used when a visible workflow opens them, but do not prioritize them over the current menu flows.

## Shell-Owned Functions

`src/views/home.vue` imports `login.js`, `share.js`, and `memo.js`.

- Login/register: `POST /appAuth/login`, `POST /appAuth/register`.
- User bootstrap: `GET /chat/user/info`, `GET /chat/user/permission`, `GET /chat/user/settings`.
- User settings/profile: `PUT /chat/user/settings`, `PUT /chat/user/updateBaseInfo`, `PUT /chat/user/updatePassword`.
- Conversation: create/list/detail/remove and streaming completion under `/chat/userConversation/...`.
- File management/meeting minutes:
  - `GET /chat/label/list`
  - `GET /chat/dict/queryDictDataList?dictType=sys_indices`
  - `GET /chat/meetingMinutes/mineList`
  - `POST /chat/meetingMinutes/create`
  - `GET /chat/meetingMinutes/info/{id}`
  - `POST /chat/meetingMinutes/batchRemove`
  - `POST /chat/meetingMinutes/edit/{id}`
  - `POST /chat/meetingMinutes/editBuy/{id}`
  - `GET /chat/meetingMinutes/unreadList`
  - `POST /chat/meetingMinutes/read/{id}`
  - `POST /chat/batch-download/download`
- Coins/orders: `GET /chat/user/accountPoint/transactions`, `GET /chat/user/accountPoint/info`, `GET /chat/product/info/{id}`, `POST /chat/order/create`.
- Upload flow: fetch `GET /chat/file/getTemporaryToken`, upload to OSS, then submit business API with returned file URLs.

## Smart Search Page

`src/views/Home/SmartSearch.vue` owns company cloud search and current search history.

Initial load:
- Permissions: `GET /chat/user/permission`
- Business tags: `GET /chat/company-vector/business-tags`
- Advanced filters: `GET /chat/company-vector/filters`
- Company status options: `GET /chat/company/contactStatus/types`
- Agent users: `GET /chat/companyMember/agentUsers`
- Statistics: `GET /chat/company-vector/statistics`
- Search history: `POST /chat/user-record/page`

Company search:
- Keyword/high-precision search: `POST /chat/company-vector/search`.
- Natural-language search: `GET /chat/company-vector/integrated-search`, then poll search history every 10 seconds until the record status becomes `请求完成` or `请求失败`.
- Advanced filters also use `POST /chat/company-vector/search` with filter fields from `/filters`.
- Further search uses `POST /chat/company-vector/filter-search` with `companyIds` and `question`, then records the refined result with `POST /chat/user-record/add`.
- History replay uses `POST /chat/company-vector/search-by-ids` for company results.
- History maintenance uses `POST /chat/user-record/add`, `PUT /chat/user-record/update`, `DELETE /chat/user-record/delete/{id}`.

Company result actions:
- Open company detail: `GET /chat/company-vector/detail?companyId={id}`.
- Toggle connection: `POST /chat/company-vector/toggle-connection-status` with `companyId` and `targetStatus`.
- Toggle interest: `POST /chat/company-vector/toggle-interest` with `companyId`.
- Assign agents from result rows: `POST /chat/company-vector/member/register` with `companyId` and `userIds`.
- Export visible results: `POST /chat/company-vector/export` with `companyIds`; response `msg` is a CSV URL.

Other Smart Search subflows:
- Talent natural search uses `POST /chat/search/talent-search` with `inputText` and `mode: "result"`.
- CSV company generation entry checks `GET /chat/custom-company/tasks`, then opens the generated result list or upload dialog. Submit/delete use `POST /chat/custom-company/task/submit` and `POST /chat/custom-company/task/delete`.
- Curated list support is gated by `Company Search` and `View Curated List` permission names.

## Talent Matrix Page

`src/views/Home/Talents.vue` owns current talent V2 lists, favorites, assignments, export, and high-level detail routing.

Initial load:
- `GET /chat/talents/v2/tags`
- `GET /chat/talents/v2/connection/talentStatus/types`
- `GET /chat/companyMember/agentUsers`
- `GET /chat/talents/v2/favorite/list`
- `GET /chat/talents/v2/list`

List actions:
- Filters and infinite scroll call `GET /chat/talents/v2/list`.
- Assignment uses `POST /chat/talents/v2/member/register` after the row select closes.
- Status toggle uses `POST /chat/talents/v2/connection/toggleTalentStatus`, then refreshes status counts by reloading the list.
- Export uses `POST /chat/talents/v2/export` with `talentIds`; response `msg` is a CSV URL.
- Favorite folders list/delete/search use `GET /favorite/list`, `DELETE /favorite/{id}`, and the async search-task endpoints.

Detail panels:
- `TalentPanelType1/2/3.vue` open by talent `type` and fetch `GET /chat/talents/v2/detail/{id}`.
- Manual talent connection is a chain: `GET /connection/defaultText`, `POST /connection/processText`, user confirms final text, then `POST /connection/confirm`.
- Talent interest: `POST /chat/talents/v2/toggle-interest`.
- Talent annotations: `GET /chat/talents/v2/annotation/list`, `POST /chat/talents/v2/annotation/add?talentId={id}`.

## Project Connectivity Page

`src/views/Home/NewMemoV3.vue` owns current Project Memo.

Initial load:
- `GET /chat/docStatus/contact-options`
- `GET /chat/project-memo/member/available`
- `GET /chat/project-memo/list`

List actions:
- Filter/search/leader/favorite toggles call `GET /chat/project-memo/list`.
- Create memo calls `POST /chat/project-memo/upload`, then resets paging and reloads list.
- Edit memo calls `PUT /chat/project-memo`; leader changes also update via the same endpoint when the select closes.
- Delete memo calls `DELETE /chat/project-memo/{id}` and removes the row locally.
- Toggle interest calls `POST /chat/project-memo/{id}/toggle-interest`.
- Status toggle calls `POST /chat/project-memo/{id}/update-doc-status?statusCode={code}`.

Detail actions:
- Open detail: `GET /chat/project-memo/{id}`.
- Load AI analysis result list: `GET /chat/analysis/second/all-results?memoId={id}`.
- View attachments: `GET /chat/project-memo/{id}/attachments`; attachment dialog also refreshes report task and report metadata.
- Paragraph add/update/delete: `/chat/project-memo/{memoId}/content-paragraphs...`, then refresh detail.
- If paragraph content mentions `@智能纪要` or `@行业研究`, the page calls `POST /chat/project-memo/{memoId}/agent/mention` with action, paragraph text, mentioned attachments, all attachments, and other paragraphs.
- Editor file insert uploads through `/chat/file/upload` helper and then registers the file in `PUT /chat/project-memo/{id}/attachments`.

## Memo Attachments And Reports

`AttachmentLIstDialog.vue` owns memo attachments and memo report generation.

- Opening the dialog calls `GET /chat/project-memo/{memoId}/attachments`, `GET /chat/project-memo/{memoId}/report-tasks`, and `GET /chat/project-memo/{memoId}/reports`.
- It refreshes task/report metadata every 5 seconds while open.
- Upload flow: `GET /chat/file/getTemporaryToken`, OSS multipart upload, then `PUT /chat/project-memo/{memoId}/attachments`.
- Delete attachment rebuilds the attachment array and calls `PUT /chat/project-memo/{memoId}/attachments`.
- Generate report: `POST /chat/project-memo/{memoId}/report/generate?attachmentId={attachmentId}`, poll `GET /chat/project-memo/report-task/{taskId}` every 2.5 seconds, refresh task/report lists, and refresh memo detail on success.
- Report view dialog can update/delete reports through `PUT`/`DELETE /chat/project-memo/{memoId}/report/{reportId}`.

## FA Collaboration

`InverestorSelect.vue` and `FaCooperationNotes.vue` own FA collaboration under a Project Memo.

- Open FA panel: `GET /chat/project-memo/fa-collab/meta/options`, then `GET /chat/project-memo/fa-collab/page`; the current page passes the opened memo id as `projectId`.
- Add one new investor to collaboration: create or choose investor, then `POST /chat/project-memo/fa-collab` with `projectId` and `investorId`.
- Bulk sync selected investors: `PUT /chat/project-memo/fa-collab/sync` with `projectId` and `investorIds`.
- Change priority/progress: `PUT /chat/project-memo/fa-collab` with `id` plus `priority` or `progressStatus`.
- Delete recommended investor: `DELETE /chat/project-memo/fa-collab/{id}`.
- Notes drawer:
  - Remarks: `GET /chat/project-memo/fa-collab/remark/page?collabId={id}`, `POST /chat/project-memo/fa-collab/remark`.
  - Attachments: `GET /chat/project-memo/fa-collab/attachment/list?collabId={id}`, upload through OSS then `POST /chat/project-memo/fa-collab/attachment/upload`, delete with `DELETE /chat/project-memo/fa-collab/attachment/{id}`.
  - FA reports: submit, poll, list, update, and delete through `/chat/project-memo/fa-collab/report...`.

## Investor Directory

`src/views/Home/Investors1.vue` owns the current investor directory.

Initial load:
- `GET /chat/file/getTemporaryToken`
- `GET /chat/investor/list`
- `GET /chat/investor/opinion/page`
- `GET /chat/investor/parse-task/list`

Task refresh:
- The page refreshes parse tasks and investor list every 30 seconds until all tasks are `PENDING_CONFIRM` or `CONFIRMED`.
- Opinion list also refreshes every 30 seconds.

Parse flow:
- Upload files through OSS or provide a social link.
- `POST /chat/investor/parse-task` with `sources`.
- Poll/list tasks with `GET /chat/investor/parse-task/list`; inspect a task with `GET /chat/investor/parse-task/{id}`.
- When a task is `PENDING_CONFIRM`, open investor editor and confirm with `POST /chat/investor/parse-task/{id}/confirm`.
- Delete tasks with `DELETE /chat/investor/parse-task/{id}`.

Investor and opinion actions:
- Investor list/search/sort: `GET /chat/investor/list`.
- Investor detail/create/update/delete: `GET /chat/investor/{id}`, `POST /chat/investor`, `PUT /chat/investor`, `DELETE /chat/investor/{id}`.
- Attachments: `POST /chat/investor/attachment/upload`, `GET /chat/investor/attachment/list`, `DELETE /chat/investor/attachment/{id}`.
- Opinions: `GET /chat/investor/opinion/page`, `POST /chat/investor/opinion`, `PUT /chat/investor/opinion`, `DELETE /chat/investor/opinion/{id}`.

## AI Analysis

There are two current AI analysis surfaces.

- Standalone `Home/AiAnalyze.vue` loads `GET /chat/analysis/keywords` and `GET /chat/analysis/second/all-results`, submits `POST /chat/analysis/second/submit-task`, polls `GET /chat/analysis/second/task-progress?taskId={id}`, and deletes with `POST /chat/analysis/second/delete-task`.
- Project Memo detail opens `AIAnalyzeDialog.vue`, which uses the same second-analysis APIs but includes `memoId`, file metadata, `keywordText`, and optional `extraText`.

## Industry Analysis

`src/views/Home/IndustryAnalyze.vue` and child tabs use the Insight base URL `https://v3-api.diggen.cn/insight`.

Initial event dashboard:
- `GET /events/rank`
- `GET /events/topRank`
- `GET /events/todayFocus`
- `GET /events/cycleDistribution`
- `GET /events/trend`

Event detail:
- `GET /events/{id}`

Leader people tab:
- `GET /persons/rank`
- `GET /persons/{pid}`
- `GET /persons/history/{pid}`

Viewpoints tab:
- `GET /opinions/rank`
- `GET /opinions/summary`
- `GET /opinions/sentimentDistribution`
- `GET /opinions/trend`
- `GET /opinions/{id}`

Collect/share/copy actions in the dialogs are local UI actions, not backend calls in the current code.

## Admin Accounts

`src/views/Home/AdminAccounts.vue` owns account and permission-template management.

- Initial load: `GET /chat/admin/account-types/options`, `GET /chat/admin/users`, `GET /chat/admin/account-types`.
- Users:
  - Create: `POST /chat/admin/users`.
  - Update: `PUT /chat/admin/users/{id}`.
  - Reset password: `PUT /chat/admin/users/{id}/password` with `{ "password": "123456" }`.
  - Toggle status: `PUT /chat/admin/users/{id}/status` with `{ "status": 1 | 0 }`.
  - Delete: `DELETE /chat/admin/users/{id}`.
- Account types:
  - Create: `POST /chat/admin/account-types`.
  - Update: `PUT /chat/admin/account-types/{id}`.
  - Toggle status: `PUT /chat/admin/account-types/{id}/status`.
  - Delete: `DELETE /chat/admin/account-types/{id}`.
  - After type changes, refresh both account type list and options.
