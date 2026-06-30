# DigClaw Business Workflows

Use these flows to operate DigClaw like the current frontend pages, without browser clicks. Each flow lists the requests in the order the UI behavior implies.

## Common Rules

- Authenticated calls need `Authorization: Bearer <token>` and `clientid`.
- Treat `code === 200` as success unless an endpoint is documented as returning an unwrapped body.
- After a mutation, refresh the same list/detail endpoint the page uses.
- For async work, submit first, then poll the task endpoint until a terminal status.
- File uploads are not a single business API call in the frontend: get OSS STS credentials with `GET /chat/file/getTemporaryToken`, upload the file to OSS, then pass `{ fileName/name, fileUrl/url }` to the business endpoint. `POST /chat/file/upload` is used by the project memo rich-text editor.
- Current page flows take precedence over helper functions that remain in `src/api/*.js` but are not imported by current pages.
- Terminal statuses:
  - Smart Search natural language history: `请求完成`, `请求失败`
  - Favorite search: `COMPLETED`, `CANCELLED`, `FAILED`
  - Investor parse: `PENDING_CONFIRM`, `CONFIRMED`, `FAILED`
  - Memo/FA report tasks: `SUCCESS`, `FAILED`
  - AI analysis progress: `progress === 100`

## App Shell, Auth, Permissions, And Files

Bootstrap after token exists:

1. `GET /chat/user/info`
2. `GET /chat/user/permission`
3. `GET /chat/user/settings`
4. Select the first accessible current menu in this order: Smart Search, Talent Matrix, Project Connectivity, Venture Investment Directory, Industry Analysis. `MASTER` or `Account Administration` can open Admin Accounts.
5. Load shell side data when needed:
   - `GET /chat/userConversation/list`
   - `GET /chat/label/list`
   - `GET /chat/dict/queryDictDataList`
   - `GET /chat/meetingMinutes/mineList`
   - `GET /chat/meetingMinutes/unreadList`

Login/register:

1. `POST /appAuth/login` or `POST /appAuth/register`.
2. For login, send the same body as the frontend: `accountNum`, `password`, `clientId`, and `grantType: "appPwd"`.
3. Read `data.access_token` and `data.userId`.
4. Store/use the token as `Authorization: Bearer <access_token>` for later requests.
5. Run the bootstrap sequence above.

Meeting-minute upload and management from the shell:

1. `GET /chat/file/getTemporaryToken`.
2. Upload audio/video/document files to OSS.
3. `POST /chat/meetingMinutes/create` with uploaded file metadata and meeting form fields.
4. Refresh `GET /chat/meetingMinutes/mineList`.
5. Poll unread reminders with `GET /chat/meetingMinutes/unreadList`; mark opened/read with `/open`, `/openBuy`, or `/read` endpoints.
6. Rename/delete/download through `POST /chat/meetingMinutes/edit/{id}`, `POST /chat/meetingMinutes/batchRemove`, and `POST /chat/batch-download/download`.

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

1. `POST /chat/talents/v2/connection/toggleTalentStatus` with `talentId` and `statusCode`.
2. Update the visible row locally.
3. Refresh `GET /chat/talents/v2/list` with the current filters to update `contactStatusCount`.

Open talent detail:

1. `GET /chat/talents/v2/detail/{id}`.
2. Load annotations with `GET /chat/talents/v2/annotation/list?talentId={id}` when the detail panel needs notes.
3. Toggle interest with `POST /chat/talents/v2/toggle-interest`.
4. Add an annotation with `POST /chat/talents/v2/annotation/add?talentId={id}`, then refresh the annotation list.

Manual talent connection:

1. Load suggested text with `GET /chat/talents/v2/connection/defaultText?talentId={id}`.
2. User edits text; send it to `POST /chat/talents/v2/connection/processText`.
3. Use returned `processedText` and `subject` to populate confirmation.
4. Confirm with `POST /chat/talents/v2/connection/confirm`.
5. Mark the row/detail as connected or refresh talent detail.

Assign talent members:

1. Load assignable users with `GET /chat/companyMember/agentUsers`.
2. `POST /chat/talents/v2/member/register` with `talentId` and full `userIds`.
3. Refresh `GET /chat/talents/v2/list` if filtering by member or if member chips must be exact.

Export talent data:

1. Build the same filter object used by the current talent list.
2. `POST /chat/talents/v2/export`.
3. Treat the response message/body as the downloadable export payload, matching frontend behavior.

## Company Cloud And Smart Search

Initial load:

1. `GET /chat/user/permission` to determine access to company search and curated list.
2. `GET /chat/company-vector/business-tags`
3. `GET /chat/company-vector/statistics`
4. `GET /chat/company-vector/filters` when advanced filters are visible.
5. `GET /chat/company/contactStatus/types`
6. `GET /chat/companyMember/agentUsers`
7. `POST /chat/user-record/page` for recent search history.

Company keyword or advanced-filter search:

1. Build a body with `keywords`, `page`, `size`, `chinesePeople`, selected `businessTags`, `establishTimeOrder`, and any advanced filters from `/chat/company-vector/filters`.
2. `POST /chat/company-vector/search`
3. Show `data` as search results.
4. Save history with `POST /chat/user-record/add`; current page stores `tab`, `searchType`, and JSON-stringified `recordData`.

Company natural language search:

1. Require non-empty natural language input.
2. `GET /chat/company-vector/integrated-search` with `q`, `use_cache: true`, `chinesePeople`, and `businessTags`.
3. The endpoint returns quickly with `data.recordId`; do not expect final company rows in this response.
4. Poll `POST /chat/user-record/page` every ~10 seconds with `{ tab: "公司", searchType: "自然语言搜索", current: 1, size: 20 }`.
5. Find the record with the returned `recordId`.
6. When `record.status === "请求完成"`, refresh history. To show rows, parse `record.recordData`, collect `company.id`, then call `POST /chat/company-vector/search-by-ids` with `{ companyIds }`.
7. When `record.status === "请求失败"`, stop polling and report failure.

Further search inside existing results:

1. Require existing result ids and a non-empty follow-up question.
2. Build `{ companyIds: tableData.map(row => row.company.id), question }`.
3. `POST /chat/company-vector/filter-search`
4. Replace visible result list with `data.data` from the wrapped response.
5. Save the new result snapshot with `POST /chat/user-record/add`.

Open company detail:

1. `GET /chat/company-vector/detail?companyId={companyId}`
2. Optionally load comments and member bindings:
   - `GET /chat/comment/company/list`
   - `GET /chat/companyMember/list`

Toggle company status:

1. `POST /chat/company-vector/toggle-connection-status` with `companyId` and `targetStatus`.
2. Refresh current result row or detail.

Assign company members from Smart Search:

1. `GET /chat/companyMember/agentUsers`
2. `POST /chat/company-vector/member/register` with `companyId` and full `userIds`.
3. Refresh the current company list/detail if member chips must be exact.

Export visible company results:

1. Collect visible `companyIds`.
2. `POST /chat/company-vector/export` with `{ companyIds }`.
3. The frontend treats `msg` as CSV text and downloads it locally.

Company CSV generation mode:

1. `GET /chat/custom-company/tasks` to decide whether to show existing generated CSV tasks.
2. If creating a task, `POST /chat/custom-company/task/submit`.
3. Refresh `GET /chat/custom-company/tasks`; delete stale tasks with `DELETE /chat/custom-company/task/delete/{id}`.

Talent natural search from Smart Search:

1. `POST /chat/search/talent-search` with the natural language query as params.
2. Save/show returned people rows as the current results for the "个人" tab.
3. Store history with `POST /chat/user-record/add` using `tab: "个人"` and `searchType: "自然语言搜索"`.

## Project Memo Page

Initial load:

1. `GET /chat/docStatus/contact-options`
2. `GET /chat/project-memo/member/available`
3. `GET /chat/project-memo/list` with filters: `pageNum`, `pageSize`, `keyword`, `docStatus`, `leaderUserIds`, `isInterested`

Create memo from a Word file:

1. Upload the file first if needed through `/chat/file/upload` or OSS helper.
2. `POST /chat/project-memo/upload` with memo metadata and file info.
3. Refresh `GET /chat/project-memo/list`.
4. Open the new item with `GET /chat/project-memo/{id}` when the user needs details.

Open memo detail:

1. `GET /chat/project-memo/{id}`
2. `GET /chat/analysis/second/all-results?memoId={id}` for second-analysis history.
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

1. User creates/updates a paragraph containing an `@AI` mention.
2. Load current attachments with `GET /chat/project-memo/{memoId}/attachments`.
3. Add/update the paragraph first.
4. `POST /chat/project-memo/{memoId}/agent/mention` with `action`, `requesterName`, current paragraph title/content/text, mentioned attachments, all attachments, and other paragraphs.
5. Refresh memo detail after the generated content or notification is expected.

Edit memo paragraphs:

1. Add: `POST /chat/project-memo/{memoId}/content-paragraphs`
2. Update: `PUT /chat/project-memo/{memoId}/content-paragraphs/{paragraphId}`
3. Delete: `DELETE /chat/project-memo/{memoId}/content-paragraphs/{paragraphId}`
4. Refresh `GET /chat/project-memo/{memoId}`.

Insert attachment from memo editor:

1. Upload with `POST /chat/file/upload`.
2. Refresh `GET /chat/project-memo/{memoId}/attachments`.
3. If the uploaded file is not already present, call `PUT /chat/project-memo/{memoId}/attachments` with the full next attachment list.
4. Insert the uploaded file URL/name into the editor content.

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
2. `GET /chat/project-memo/fa-collab/page` with `projectId`, paging, priority, progress status, keyword.
3. If adding new investors, load investor list with `GET /chat/investor/list`.

Create one FA collaboration after manually adding an investor:

1. Select investor(s) from `GET /chat/investor/list`.
2. `POST /chat/project-memo/fa-collab` with `{ projectId, investorId }`.
3. Refresh `GET /chat/project-memo/fa-collab/page`.

Update FA collaboration status/priority:

1. `PUT /chat/project-memo/fa-collab` with updated collab fields.
2. Refresh the FA collab page.

Sync FA collaboration investors:

1. Keep selected investor ids across all investor-list pages.
2. `PUT /chat/project-memo/fa-collab/sync` with `{ projectId, investorIds }`.
3. Refresh `GET /chat/project-memo/fa-collab/page`.

Delete FA collaboration investor:

1. `DELETE /chat/project-memo/fa-collab/{id}`.
2. Refresh `GET /chat/project-memo/fa-collab/page`.

Add FA remark:

1. Open notes drawer with a `collabId`.
2. `GET /chat/project-memo/fa-collab/remark/page` with `collabId`.
3. `POST /chat/project-memo/fa-collab/remark`
4. Refresh `GET /chat/project-memo/fa-collab/remark/page`.

FA attachment and report:

1. Open notes drawer with a `collabId`.
2. Upload to OSS when using a file picker.
3. Register attachment with `POST /chat/project-memo/fa-collab/attachment/upload`.
4. Refresh `GET /chat/project-memo/fa-collab/attachment/list?collabId={collabId}`.
5. Generate report with `POST /chat/project-memo/fa-collab/report/generate?collabId={collabId}&attachmentId={attachmentId}`.
6. Poll `GET /chat/project-memo/fa-collab/report-task/{taskId}` every ~2.5 seconds.
7. While status is `PENDING` or `RUNNING`, refresh report task/list metadata.
8. On `SUCCESS`, refresh:
   - `GET /chat/project-memo/fa-collab/report-tasks?collabId={collabId}`
   - `GET /chat/project-memo/fa-collab/reports?collabId={collabId}`
9. Update/delete reports with `PUT` or `DELETE /chat/project-memo/fa-collab/report/{reportId}`, then refresh report list.

## Investor Directory

Initial load:

1. `GET /chat/file/getTemporaryToken` for OSS upload credentials.
2. `GET /chat/investor/parse-task/list`
3. `GET /chat/investor/list`
4. `GET /chat/investor/opinion/page`
5. Start two frontend-style refresh loops when a page is open:
   - parse tasks and investor list every ~30 seconds while tasks are `PENDING` or `RUNNING`
   - opinion page every ~30 seconds

Parse investor from URLs/files:

1. Upload files to OSS first if the user supplied files.
2. Build `sources` from uploaded files and URLs. Each item includes `url` and `fileName`; social link text is sent as a source URL named `社媒链接`.
3. `POST /chat/investor/parse-task` with `{ "sources": [...] }`.
4. Save returned task id.
5. Poll `GET /chat/investor/parse-task/{taskId}`.
6. If status is `PENDING` or `RUNNING`, keep polling.
7. If status is `PENDING_CONFIRM`, show generated investor and attachment data; require confirm.
8. Confirm with `POST /chat/investor/parse-task/{taskId}/confirm`.
9. Refresh:
   - `GET /chat/investor/parse-task/list`
   - `GET /chat/investor/list`
   - `GET /chat/investor/opinion/page`
10. If status is `FAILED`, show `errorMsg`.

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
2. `POST /chat/analysis/second/submit-task` with `files`, `extraText`, `keywordText`, and optional `memoId`.
3. Save returned task id.
4. Poll `GET /chat/analysis/second/task-progress?taskId={taskId}` every ~5 seconds.
5. When `data.progress === 100`, stop polling.
6. Refresh `GET /chat/analysis/second/all-results`.

Delete analysis result:

1. `POST /chat/analysis/second/delete-task` with `taskId`.
2. Refresh `GET /chat/analysis/second/all-results`.

## Industry Analysis

Initial load:

1. `GET /insight/events/rank` with `pageNum`, `pageSize`, optional `keyword`.
2. `GET /insight/events/topRank`.
3. `GET /insight/events/todayFocus`.
4. `GET /insight/events/cycleDistribution`.
5. `GET /insight/events/trend` with `{ type: "day", period: 30 }` or `{ type: "month", period: 12 }`.

Search and paginate event rank:

1. Reset `pageNum` to `1` when keyword changes.
2. `GET /insight/events/rank`.
3. Read the paged payload from `data.records`, `data.rows`, `data.list`, or top-level `rows`, matching the frontend normalizer.
4. If the current page is beyond max page after filtering, retry the max valid page.

Open event/person/opinion detail:

1. Event: `GET /insight/events/{id}`.
2. Person rank/detail/history when a person tab/dialog is used:
   - `GET /insight/persons/rank`
   - `GET /insight/persons/{pid}`
   - `GET /insight/persons/history/{pid}`
3. Opinion widgets and detail:
   - `GET /insight/opinions/rank`
   - `GET /insight/opinions/summary`
   - `GET /insight/opinions/sentimentDistribution`
   - `GET /insight/opinions/trend`
   - `GET /insight/opinions/{id}`

## Admin Accounts

Initial load:

1. `GET /chat/admin/users` with paging/filter params.
2. `GET /chat/admin/account-types/options`
3. `GET /chat/admin/account-types`

Create/update user:

1. Load account type options first.
2. Create with `POST /chat/admin/users` or update with `PUT /chat/admin/users/{id}`. Current page sends `accountNum`, optional `password`, `nickName`, `accountType`, `status`, and `accountValidUntil`.
3. Reset password with `PUT /chat/admin/users/{id}/password` and `{ password: "123456" }`.
4. Toggle status with `PUT /chat/admin/users/{id}/status` and `{ status: 1|0 }`; the page updates the row locally.
5. Delete with `DELETE /chat/admin/users/{id}`.
6. Refresh `GET /chat/admin/users` after create/update/delete.
7. The API helper has `/expiry`, but the current Admin Accounts page edits expiry through `accountValidUntil` in create/update, so do not call `/expiry` for page-equivalent behavior.

Manage account types:

1. List with `GET /chat/admin/account-types`.
2. Create/update with `typeCode`, `typeName`, `permissionLevel`, `accessibleFunctions`, `status`, and `remark`.
3. Toggle status with `PUT /chat/admin/account-types/{id}/status` and `{ status: 1|0 }`.
4. Delete with `DELETE /chat/admin/account-types/{id}`.
5. Refresh account type list and options after create/update/status/delete.
