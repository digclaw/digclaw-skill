# Page Module: 文件转录

Source: `Home/FileTranscription.vue`, `src/api/fileTranscription.js`.

Permission gate: `file-transcription`. Access requires `File Transcription` in `accessibleFunctions`. The current backend default grants it to `MASTER`; Account Administration can assign the same function to other account types.

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

## Parse Methods And Sources

The backend selects `parseMethod` from file metadata: image -> `ocr`, audio/video -> `asr`, document -> `document`, with text/other fallbacks.

Known source types include `MANUAL`, `PROJECT_MEMO_INIT`, `PROJECT_MEMO_AGENT`, `PROJECT_MEMO_ATTACHMENT`, `PROJECT_MEMO_REPORT_MEMO`, `PROJECT_MEMO_REPORT_FA_COLLAB`, and `AI_ANALYSIS_SECOND`. Treat other returned source values as valid server data and display them without inventing a mapping.
