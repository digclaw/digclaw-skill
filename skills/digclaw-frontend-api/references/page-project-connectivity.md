# Page Module: 项目通联

Source: `Home/NewMemoV3.vue`, `AppointmentModal.vue`, `AttachmentLIstDialog.vue`, `AIAnalyzeDialog.vue`, `InverestorSelect.vue`, `FaCooperationNotes.vue`, `MemoReportTaskHistory.vue`, `MemoReportViewDialog.vue`.

Permission gate: `project-connectivity`.

## Responsibilities

- Project memo list, detail, create/edit/delete, status, interest, leader filter.
- Memo content paragraphs and `@AI` mention tasks.
- Memo attachments and memo report generation.
- Second analysis dialog scoped by `memoId`.
- FA collaboration: recommended investors, selected investors, notes, attachments, FA reports.

## Initial Load

1. `GET /chat/docStatus/contact-options`.
2. `GET /chat/project-memo/member/available`.
3. `GET /chat/project-memo/list` with `pageNum`, `pageSize`, `keyword`, `docStatus`, `leaderUserIds`, `isInterested`.

## Memo List And Detail

### List/Search/Filter

1. Debounce keyword input.
2. Set `leaderUserIds` as comma-joined ids when leader filter changes.
3. Set `isInterested: 1` for favorites-only.
4. `GET /chat/project-memo/list`; append on infinite scroll.

### Create Or Update Memo

1. Upload file first if needed.
2. Create: `POST /chat/project-memo/upload`.
3. Update: `PUT /chat/project-memo`.
4. Refresh list or locally replace the current row.

### Open Detail

1. `GET /chat/project-memo/{id}`.
2. `GET /chat/analysis/second/all-results?memoId={id}`.
3. `GET /chat/project-memo/{id}/attachments` when attachment/report dialogs or mentions need files.

### Status, Interest, Delete

- Status: `POST /chat/project-memo/{id}/update-doc-status?statusCode={code}`.
- Appointment time if needed: `PUT /chat/project-memo/appointment-time`.
- Interest: `POST /chat/project-memo/{id}/toggle-interest`.
- Delete: `DELETE /chat/project-memo/{id}`.

## Memo Content And AI

### Paragraph CRUD

1. Add: `POST /chat/project-memo/{memoId}/content-paragraphs`.
2. Update: `PUT /chat/project-memo/{memoId}/content-paragraphs/{paragraphId}`.
3. Delete: `DELETE /chat/project-memo/{memoId}/content-paragraphs/{paragraphId}`.
4. Refresh memo detail.

### `@AI` Mention

1. Save the paragraph first.
2. Load attachments: `GET /chat/project-memo/{memoId}/attachments`.
3. `POST /chat/project-memo/{memoId}/agent/mention` with action, requester name, current paragraph title/content/text, mentioned attachments, all attachments, and other paragraphs.
4. Refresh detail after generated content is expected.

### Rich-Text Attachment Insert

1. `POST /chat/file/upload`.
2. Refresh `GET /chat/project-memo/{memoId}/attachments`.
3. If needed, `PUT /chat/project-memo/{memoId}/attachments` with the full next attachment list.

## Memo Reports

1. Confirm attachment exists via `GET /chat/project-memo/{memoId}/attachments`.
2. `POST /chat/project-memo/{memoId}/report/generate?attachmentId={attachmentId}`.
3. Poll `GET /chat/project-memo/report-task/{taskId}` every ~2.5 seconds.
4. On `SUCCESS`, refresh:
   - `GET /chat/project-memo/{memoId}/report-tasks`
   - `GET /chat/project-memo/{memoId}/reports`
   - memo detail
5. Update/delete report: `PUT` or `DELETE /chat/project-memo/{memoId}/report/{reportId}`.

## Second Analysis Dialog

1. Upload files through OSS or editor upload.
2. `POST /chat/analysis/second/submit-task` with `files`, `extraText`, `keywordText`, `memoId`.
3. Poll `GET /chat/analysis/second/task-progress?taskId={taskId}`.
4. Refresh `GET /chat/analysis/second/all-results?memoId={memoId}`.

## FA Collaboration

### Recommended Investor Panel

1. `GET /chat/project-memo/fa-collab/meta/options`.
2. `GET /chat/project-memo/fa-collab/page` with `projectId`, `pageNum`, `pageSize`, `priority`, `progressStatus`, `keyword`.
3. Load full investor list for selection: `GET /chat/investor/list`.

### Add/Sync/Update

- Add one investor: `POST /chat/project-memo/fa-collab` with `{ projectId, investorId }`.
- Sync selected investors: `PUT /chat/project-memo/fa-collab/sync` with `{ projectId, investorIds }`.
- Update progress/priority: `PUT /chat/project-memo/fa-collab` with `id` and changed fields.
- Delete collab investor: `DELETE /chat/project-memo/fa-collab/{id}`.

### Notes, Attachments, FA Reports

1. Open drawer by `collabId`.
2. Notes: `GET /chat/project-memo/fa-collab/remark/page`, then `POST /chat/project-memo/fa-collab/remark`.
3. Attachments: `GET /chat/project-memo/fa-collab/attachment/list?collabId={id}`, upload via OSS then `POST /chat/project-memo/fa-collab/attachment/upload`, delete with `DELETE /chat/project-memo/fa-collab/attachment/{id}`.
4. FA report: `POST /chat/project-memo/fa-collab/report/generate?collabId={id}&attachmentId={attachmentId}`.
5. Poll `GET /chat/project-memo/fa-collab/report-task/{taskId}`.
6. Refresh `GET /chat/project-memo/fa-collab/report-tasks?collabId={id}` and `/reports?collabId={id}`.
7. Update/delete report: `PUT` or `DELETE /chat/project-memo/fa-collab/report/{reportId}`.
