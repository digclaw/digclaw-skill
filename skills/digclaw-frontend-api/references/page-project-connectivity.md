# Page Module: 项目通联

Source: `Home/NewMemoV3.vue`, `AppointmentModal.vue`, `AttachmentLIstDialog.vue`, `AIAnalyzeDialog.vue`, `InverestorSelect.vue`, `FaCooperationNotes.vue`, `MemoReportTaskHistory.vue`, `MemoReportViewDialog.vue`.

Permission gate: `project-connectivity`.

## Responsibilities

- Project memo list, detail, create/edit/delete, status, interest, leader filter.
- Memo content paragraphs and agent mention tasks for `@智能纪要` and `@行业研究`.
- Memo attachments and memo report generation.
- Smart document/AI second-analysis dialog scoped by `memoId`.
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

### Agent Mentions: 智能纪要 And 行业研究

The current editor mention menu exposes two agent actions:

| User mention | Action value | Use when |
|---|---|---|
| `@智能纪要` | `smart_memo` | Generate a memo/summary from the current card, project context, and attachments. |
| `@行业研究` | `industry_research` | Generate an industry research card with market, competitors, financing, and risk context. |

1. Save the paragraph first through paragraph create/update.
2. Load attachments: `GET /chat/project-memo/{memoId}/attachments`.
3. Extract linked attachments from paragraph content as `mentionedAttachments`; send all project attachments as `allAttachments`.
4. Send one `POST /chat/project-memo/{memoId}/agent/mention` per action. A paragraph that contains both mentions triggers both actions.
5. Include `userInstruction` as the paragraph plain text with the mention text removed.
6. Send `otherParagraphs` from current project paragraphs, excluding the current paragraph and generated agent paragraphs.
7. Refresh `GET /chat/project-memo/{memoId}` every ~2.5 seconds while generated content contains progress markers such as `## 生成进度`, `## Agent 实时执行记录`, `正在生成`, `正在调用 DeepResearch`, or `正在判断现有资料`.

Smart memo request example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/project-memo/2001/agent/mention --data '{"action":"smart_memo","requesterName":"agent","currentTitle":"会议纪要","currentContent":"@智能纪要 请结合附件总结本项目核心进展、待办和风险","currentText":"@智能纪要 请结合附件总结本项目核心进展、待办和风险","userInstruction":"请结合附件总结本项目核心进展、待办和风险","mentionedAttachments":[{"fileName":"memo.docx","fileUrl":"https://cdn.example.com/memo.docx","type":"DOCX"}],"allAttachments":[{"fileName":"memo.docx","fileUrl":"https://cdn.example.com/memo.docx","type":"DOCX"}],"otherParagraphs":[{"id":3001,"title":"项目背景","content":"<p>...</p>","text":"..."}]}'
```

Industry research request example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/project-memo/2001/agent/mention --data '{"action":"industry_research","requesterName":"agent","currentTitle":"行业研究","currentContent":"@行业研究 请分析具身智能赛道规模、代表公司、融资趋势和主要风险","currentText":"@行业研究 请分析具身智能赛道规模、代表公司、融资趋势和主要风险","userInstruction":"请分析具身智能赛道规模、代表公司、融资趋势和主要风险","mentionedAttachments":[],"allAttachments":[],"otherParagraphs":[]}'
```

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

This is the project-scoped smart document/AI analysis feature opened from Project Connectivity. It can analyze uploaded PDF, Word, and Excel files plus free-text instructions, then stores results under the current `memoId`.

1. Load analysis tags: `GET /chat/analysis/keywords`.
2. Upload files through the frontend OSS flow (`GET /chat/file/getTemporaryToken`, then multipart upload) and keep each uploaded `{ fileName, fileUrl }`.
3. Require at least one file or non-empty `extraText`.
4. Require at least one selected analysis tag; join selected tags as comma-separated `keywordText`.
5. `POST /chat/analysis/second/submit-task` with `files`, `extraText`, `keywordText`, `memoId`.
6. Poll `GET /chat/analysis/second/task-progress?taskId={taskId}` until `progress === 100`.
7. Refresh `GET /chat/analysis/second/all-results?memoId={memoId}` or open the page's history dialog.

Example:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/analysis/keywords
python scripts\digclaw_request.py --method POST --path /chat/analysis/second/submit-task --data '{"files":[{"fileName":"project.xlsx","fileUrl":"https://cdn.example.com/project.xlsx"}],"extraText":"请提炼商业模式、竞争格局和风险点","keywordText":"市场,商业和竞争,发展风险","memoId":2001}'
python scripts\digclaw_request.py --method GET --path /chat/analysis/second/task-progress --params '{"taskId":8888}'
python scripts\digclaw_request.py --method GET --path /chat/analysis/second/all-results --params '{"memoId":2001}'
```

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
