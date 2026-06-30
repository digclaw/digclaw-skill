# DigClaw Business Workflows

Use these flows to operate DigClaw like the current frontend pages, without browser clicks. Each flow lists the requests in the order the UI behavior implies.

## Common Rules

- Authenticated calls need `Authorization: Bearer <token>` and `clientid`.
- Treat `code === 200` as success unless an endpoint is documented as returning an unwrapped body.
- After a mutation, refresh the same list/detail endpoint the page uses.
- For async work, submit first, then poll the task endpoint until a terminal status.
- Terminal statuses:
  - Favorite search: `COMPLETED`, `CANCELLED`, `FAILED`
  - Investor parse: `PENDING_CONFIRM`, `CONFIRMED`, `FAILED`
  - Memo/FA report tasks: `SUCCESS`, `FAILED`
  - AI analysis progress: `progress === 100`

## Talent Matrix Page

Initial load:

1. `GET /chat/talents/v2/tags`
2. `GET /chat/talents/v2/connection/talentStatus/types`
3. `GET /chat/companyMember/agentUsers`
4. `GET /chat/talents/v2/favorite/list`
5. `GET /chat/talents/v2/list` with `pageNum`, `pageSize`, optional `tag`, `keyword`, `favoriteFolderId`, `memberId`, `scoreOrder`, `timeOrder`

Search or filter talents:

1. Reset `pageNum` to `1`.
2. Send `GET /chat/talents/v2/list`.
3. Read `data.records`, `data.total`, and `data.contactStatusCount`.
4. For infinite scroll, request the next `pageNum` and append `records`.

Switch to a favorite folder:

1. Set `tag = null`.
2. Set `favoriteFolderId`.
3. Call `GET /chat/talents/v2/list`.

Create a talent favorite folder by search:

1. `POST /chat/talents/v2/favorite/search-task` with the search form.
2. Immediately refresh favorite folders: `GET /chat/talents/v2/favorite/list`.
3. Poll `GET /chat/talents/v2/favorite/search-task/{taskId}` every ~1 second.
4. While status is `PENDING`, `RUNNING`, or `CANCELLING`, keep polling.
5. On `COMPLETED`, refresh favorite folders and then call `GET /chat/talents/v2/list?favoriteFolderId={folderId}`.
6. On `FAILED` or `CANCELLED`, stop and report the message.

Cancel a running favorite search:

1. `POST /chat/talents/v2/favorite/search-task/{taskId}/cancel`
2. Poll status once more to get the final state.
3. Refresh favorite folders.

Delete a favorite folder:

1. `DELETE /chat/talents/v2/favorite/{folderId}`
2. Refresh `GET /chat/talents/v2/favorite/list`
3. Reset talent filter to the first normal tag and refresh `GET /chat/talents/v2/list`.

Update talent connection status:

1. `POST /chat/talents/v2/connection/toggleTalentStatus` with `talentId` and `toggleStatus`.
2. Refresh the visible talent list or update that row locally.

Assign talent members:

1. Load assignable users with `GET /chat/companyMember/agentUsers`.
2. `POST /chat/talents/v2/member/register` with `talentId` and full `userIds`.
3. Refresh `GET /chat/talents/v2/list` if filtering by member or if member chips must be exact.

## Company Cloud And Smart Search

Initial load:

1. `GET /chat/user/permission` to determine access to company search and curated list.
2. `GET /chat/company-vector/business-tags`
3. `GET /chat/company-vector/statistics`
4. `GET /chat/company/contactStatus/types`
5. `GET /chat/companyMember/agentUsers`
6. `POST /chat/user-record/page` for recent search history.

Company keyword search:

1. Build a body with the text keywords, selected `businessTags`, `chinesePeople`, and any advanced filters.
2. `POST /chat/company-vector/search`
3. Show `data` as search results.
4. Save/update history with `POST /chat/user-record/add` or `PUT /chat/user-record/update`.

Company natural language search:

1. Build query params including natural language `q`/keyword text, `chinesePeople`, and optional `businessTags`.
2. `GET /chat/company-vector/integrated-search`
3. Show `data` as search results.
4. Save/update history.

Further search inside existing results:

1. Require existing result ids and a non-empty follow-up question.
2. `POST /chat/company-vector/filter-search`
3. Replace visible result list with returned `data`.
4. Save/update history if the UI is preserving this search.

Open company detail:

1. `GET /chat/company-vector/detail?companyId={companyId}`
2. Optionally load comments and member bindings:
   - `GET /chat/comment/company/list`
   - `GET /chat/companyMember/list`

Toggle company status:

1. `POST /chat/company-vector/toggle-connection-status` with `companyId` and `toggleStatus`.
2. Refresh current result row or detail.

Assign company members:

1. `GET /chat/companyMember/agentUsers`
2. `POST /chat/companyMember/register` with `companyId`, `userIds`, and identity.
3. Refresh `GET /chat/companyMember/list?companyId={companyId}` or the current company list.

## Project Memo Page

Initial load:

1. `GET /chat/docStatus/contact-options`
2. `GET /chat/project-memo/member/available`
3. `GET /chat/project-memo/list` with filters: `pageNum`, `pageSize`, `keyword`, `docStatus`, `leaderUserIds`, `favoritesOnly`

Create memo from a Word file:

1. Upload the file first if needed through `/chat/file/upload` or OSS helper.
2. `POST /chat/project-memo/upload` with memo metadata and file info.
3. Refresh `GET /chat/project-memo/list`.
4. Open the new item with `GET /chat/project-memo/{id}` when the user needs details.

Open memo detail:

1. `GET /chat/project-memo/{id}`
2. `GET /chat/analysis/second/all-results?memoId={id}`
3. `GET /chat/project-memo/{id}/attachments`
4. Optionally load reports:
   - `GET /chat/project-memo/{id}/report-tasks`
   - `GET /chat/project-memo/{id}/reports`

Update memo:

1. `PUT /chat/project-memo`
2. Refresh `GET /chat/project-memo/{id}`.
3. Refresh list if fields shown on cards changed.

Update memo contact status:

1. `POST /chat/project-memo/{id}/update-doc-status?statusCode={code}`
2. Refresh list/detail.
3. If status requires appointment time, call `PUT /chat/project-memo/appointment-time`.

Toggle memo interest:

1. `POST /chat/project-memo/{id}/toggle-interest`
2. Refresh list or update row.

Mention agent in memo content:

1. User writes content containing an agent mention.
2. `POST /chat/project-memo/{memoId}/agent/mention`
3. Refresh memo detail if generated content or notifications matter.

Edit memo paragraphs:

1. Add: `POST /chat/project-memo/{memoId}/content-paragraphs`
2. Update: `PUT /chat/project-memo/{memoId}/content-paragraphs/{paragraphId}`
3. Delete: `DELETE /chat/project-memo/{memoId}/content-paragraphs/{paragraphId}`
4. Refresh `GET /chat/project-memo/{memoId}`.

## Memo Report Generation

Generate a report from a memo attachment:

1. Confirm attachment exists with `GET /chat/project-memo/{memoId}/attachments`.
2. `POST /chat/project-memo/{memoId}/report/generate?attachmentId={attachmentId}`
3. Save returned `taskId`.
4. Poll `GET /chat/project-memo/report-task/{taskId}` every ~2.5 seconds.
5. While status is `PENDING` or `RUNNING`, keep polling.
6. On `SUCCESS`, refresh:
   - `GET /chat/project-memo/{memoId}/report-tasks`
   - `GET /chat/project-memo/{memoId}/reports`
7. On `FAILED`, stop and report `errorMsg`/message.

Update or delete a generated memo report:

1. List reports with `GET /chat/project-memo/{memoId}/reports`.
2. Update: `PUT /chat/project-memo/{memoId}/report/{reportId}`
3. Delete: `DELETE /chat/project-memo/{memoId}/report/{reportId}`
4. Refresh report list.

## FA Collaboration

Open recommended investor panel:

1. `GET /chat/project-memo/fa-collab/meta/options`
2. `GET /chat/project-memo/fa-collab/page` with `memoId`, paging, priority, progress status, keyword.
3. If adding new investors, load investor list with `GET /chat/investor/list`.

Create FA collaboration:

1. Select investor(s) from `GET /chat/investor/list`.
2. `POST /chat/project-memo/fa-collab`
3. Refresh `GET /chat/project-memo/fa-collab/page`.

Update FA collaboration status/priority:

1. `PUT /chat/project-memo/fa-collab` with updated collab fields.
2. Refresh the FA collab page.

Sync FA collaboration investors:

1. `PUT /chat/project-memo/fa-collab/sync`
2. Refresh `GET /chat/project-memo/fa-collab/page`.

Add FA remark:

1. `POST /chat/project-memo/fa-collab/remark`
2. Refresh `GET /chat/project-memo/fa-collab/remark/page`.

FA attachment and report:

1. Upload/register attachment with `POST /chat/project-memo/fa-collab/attachment/upload`.
2. Refresh `GET /chat/project-memo/fa-collab/attachment/list`.
3. Generate report with `POST /chat/project-memo/fa-collab/report/generate?collabId={collabId}&attachmentId={attachmentId}`.
4. Poll `GET /chat/project-memo/fa-collab/report-task/{taskId}`.
5. On `SUCCESS`, refresh:
   - `GET /chat/project-memo/fa-collab/report-tasks?collabId={collabId}`
   - `GET /chat/project-memo/fa-collab/reports?collabId={collabId}`

## Investor Directory

Initial load:

1. `GET /chat/investor/parse-task/list`
2. `GET /chat/investor/list`
3. `GET /chat/investor/opinion/page`

Parse investor from URLs/files:

1. Build `sources` from uploaded files and URLs. Each item usually includes `url` and optional `fileName`.
2. `POST /chat/investor/parse-task` with `{ "sources": [...] }`.
3. Save returned task id.
4. Poll `GET /chat/investor/parse-task/{taskId}`.
5. If status is `PENDING` or `RUNNING`, keep polling.
6. If status is `PENDING_CONFIRM`, show generated investor and attachment data; require confirm.
7. Confirm with `POST /chat/investor/parse-task/{taskId}/confirm`.
8. Refresh:
   - `GET /chat/investor/parse-task/list`
   - `GET /chat/investor/list`
   - `GET /chat/investor/opinion/page`
9. If status is `FAILED`, show `errorMsg`.

Manual investor CRUD:

1. Create: `POST /chat/investor`
2. Update: `PUT /chat/investor`
3. Delete: `DELETE /chat/investor/{id}`
4. Refresh `GET /chat/investor/list`.

Investor attachments:

1. Register/upload attachment with `POST /chat/investor/attachment/upload`.
2. Refresh `GET /chat/investor/attachment/list?investorId={id}`.
3. Delete with `DELETE /chat/investor/attachment/{id}` and refresh list.

Investor opinions:

1. List: `GET /chat/investor/opinion/page`
2. Create: `POST /chat/investor/opinion`
3. Update: `PUT /chat/investor/opinion`
4. Delete: `DELETE /chat/investor/opinion/{id}`
5. Refresh opinion page.

## AI Analysis Page

Initial load:

1. `GET /chat/analysis/keywords`
2. `GET /chat/analysis/second/all-results`

Submit analysis task:

1. Upload files through OSS or `/chat/file/upload`.
2. `POST /chat/analysis/second/submit-task` with selected files and keywords/config.
3. Save returned task id.
4. Poll `GET /chat/analysis/second/task-progress?taskId={taskId}` every ~5 seconds.
5. When `data.progress === 100`, stop polling.
6. Refresh `GET /chat/analysis/second/all-results`.

Delete analysis result:

1. `POST /chat/analysis/second/delete-task` with `taskId`.
2. Refresh `GET /chat/analysis/second/all-results`.

## Admin Accounts

Initial load:

1. `GET /chat/admin/users` with paging/filter params.
2. `GET /chat/admin/account-types/options`
3. `GET /chat/admin/account-types`

Create/update user:

1. Load account type options first.
2. Create with `POST /chat/admin/users` or update with `PUT /chat/admin/users/{id}`.
3. If needed, update password, status, or expiry with the dedicated endpoint.
4. Refresh `GET /chat/admin/users`.

Manage account types:

1. List with `GET /chat/admin/account-types`.
2. Create/update/delete/status-change with the matching endpoint.
3. Refresh account type list and options.
