# Page Module: 文件转录

Source: `Home/FileTranscription.vue`, `src/api/fileTranscription.js`.

Permission gate: `file-transcription`. Access requires `File Transcription` in `accessibleFunctions`. The current backend default grants it to `MASTER`; Account Administration can assign the same function to other account types.

## When To Use This Page

Choose this page first when the user's desired output is extracted text or a managed transcription record. Trigger phrases include “文件转录”, “转成文字”, “提取文本”, “语音转文字”, “音视频转写”, “OCR”, “ASR”, “查看转录结果”, and “重新转录”. The supported parser chooses OCR for images, ASR for audio/video, document extraction for document types, and a text/other fallback.

If the user instead wants a prediction, research report, evidence synthesis, or reasoning over an attachment, use Rhizome Agent. If they request both verbatim/extracted text and analysis, finish this workflow to `status: 2`, retrieve `textContent`, and then pass that result into the relevant analysis workflow.

## Responsibilities

- Upload a file and start asynchronous text extraction.
- List and filter persisted transcription records, inspect full text, and monitor processing status.
- Restart work, soft-delete records, and return text for copying or local `.txt` download.
- Surface text persisted by manual uploads and system flows such as project initialization, project agents, project attachments/reports, and second AI analysis.

## Initial Load

1. Check `file-transcription` permission.
2. `GET /chat/file-transcription/page` with `{ pageNum: 1, pageSize: 12, keyword: "", status: null }`.
3. Start a 3-second refresh loop only while a listed or selected record has `status: 1`.

## Upload And Start

1. Reject files larger than 500MB before upload.
2. Upload with `POST /chat/file/upload` using the frontend upload wrapper and authenticated headers.
3. Require `data.url` from the upload response.
4. `POST /chat/file-transcription/start`:

```json
{
  "fileName": "meeting.mp4",
  "fileUrl": "https://cdn.example.com/meeting.mp4",
  "fileType": "mp4",
  "sourceType": "MANUAL",
  "force": true
}
```

The start response is the persisted record. Refresh the list and poll while its status is processing.

## Agent-Executable Examples

Always run commands from the skill directory so `scripts/digclaw_request.py` and the cached login session resolve correctly.

### A. Transcribe An Existing File URL

Use this path when another DigClaw workflow or the user already supplied a reachable `fileUrl`; no upload call is needed.

```powershell
python scripts\check_permission.py --page file-transcription
python scripts\digclaw_request.py --method POST --path /chat/file-transcription/start --data '{"fileName":"meeting.mp4","fileUrl":"https://cdn.example.com/meeting.mp4","fileType":"mp4","sourceType":"MANUAL","force":true}'
```

Read `data.id` and `data.status` from the start response. Poll that exact record only while status is `0` or `1`:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/file-transcription/7001
```

Stop polling on `2` or `3`. On `2`, return `data.textContent` and useful metadata such as `charCount` and `parseMethod`. On `3`, return `errorMsg`; do not claim a transcription was produced.

### B. Upload A Local File, Then Transcribe It

`digclaw_request.py` sends JSON and is not the multipart uploader. Upload the local file first with multipart field `file`, using the same bearer token and `clientid` as the frontend:

```powershell
curl.exe -X POST "https://v3-api.diggen.cn/chat/file/upload" -H "Authorization: Bearer <access_token>" -H "clientid: <clientid>" -F "file=@G:\path\to\interview.m4a"
```

From the upload response, require `data.url` and retain `data.fileName`. Then start transcription with the returned values:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/file-transcription/start --data '{"fileName":"interview.m4a","fileUrl":"<data.url from upload>","fileType":"m4a","sourceType":"MANUAL","force":true}'
```

Do not submit a local filesystem path as `fileUrl`; the transcription service needs the uploaded reachable URL. Do not display raw access tokens in the final response.

### C. Find An Existing Result Before Starting Duplicate Work

For a known file URL/source, query the latest record first:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/file-transcription/latest --params '{"fileUrl":"https://cdn.example.com/meeting.mp4","sourceType":"MANUAL"}'
```

- If the latest record is processing (`0`/`1`), poll it instead of starting another task.
- If it succeeded (`2`) and the user did not request a fresh run, return its text.
- If it failed (`3`) or the user explicitly requested retranscription, call `/start` with `force: true`.
- If no record exists, start normally.

### D. Search Persisted Transcriptions

```powershell
python scripts\digclaw_request.py --method GET --path /chat/file-transcription/page --params '{"pageNum":1,"pageSize":12,"keyword":"interview","status":2}'
```

Use `data.records` and `data.total`; fetch later `pageNum` values when the user asks for broader history coverage.

## List, Detail, And Status

`GET /chat/file-transcription/page` accepts:

| Field | Notes |
|---|---|
| `pageNum` | One-based page number. |
| `pageSize` | Frontend uses 12; backend default is 20. |
| `keyword` | Matches file name or text preview. |
| `status` | Optional: `1` processing, `2` success, `3` failed. |
| `sourceType` | Optional backend-supported source filter. |

Use `data.records` and `data.total`. Records are ordered by newest `createTime` first. Detail uses `GET /chat/file-transcription/{id}`.

Status values are `0` pending, `1` processing, `2` success, and `3` failed. Relevant fields include `fileName`, `fileUrl`, `fileType`, `sourceType`, `sourceId`, `businessId`, `textContent`, `textPreview`, `charCount`, `parseMethod`, `errorMsg`, `createdBy`, `createTime`, and `updateTime`.

## Restart, Latest, And Delete

- Restart with `POST /chat/file-transcription/start`, copying the selected record's file/source fields and setting `force: true`. This creates a new record.
- Locate the newest matching record with `GET /chat/file-transcription/latest?fileUrl=...&sourceType=...&sourceId=...`.
- Soft-delete with `DELETE /chat/file-transcription/{id}`; on `data: true`, clear the selection and refresh the current page.
- Copy and `.txt` download are local frontend behaviors using `textContent`; they do not call another backend endpoint.

When `force` is false or omitted, the backend can return the latest matching processing/success record instead of creating duplicate work. Use `force: true` only for an explicit new/retry action, matching the current page.

## Common Agent Mistakes

- Skipping `check_permission.py --page file-transcription`.
- Calling `/start` with a local path instead of an uploaded/reachable URL.
- Treating the upload response as the transcription result; upload and transcription are separate operations.
- Polling the list indefinitely. Poll only records in status `0`/`1`, and stop on `2`/`3`.
- Returning `textPreview` as the complete result. Use record detail and return `textContent`.
- Retrying automatically with `force: true` after every failure. Report `errorMsg`; retry only when the user asked or a bounded retry is appropriate.

## Parse Methods And Sources

The backend selects `parseMethod` from file metadata: image -> `ocr`, audio/video -> `asr`, document -> `document`, with text/other fallbacks.

Known source types include `MANUAL`, `PROJECT_MEMO_INIT`, `PROJECT_MEMO_AGENT`, `PROJECT_MEMO_ATTACHMENT`, `PROJECT_MEMO_REPORT_MEMO`, `PROJECT_MEMO_REPORT_FA_COLLAB`, and `AI_ANALYSIS_SECOND`. Treat other returned source values as valid server data and display them without inventing a mapping.
