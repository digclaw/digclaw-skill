# DigClaw API Details

This file gives request parameters, examples, and response examples for the high-use frontend-backed APIs. It is intentionally focused on page operations, not every backend route.

All examples assume:

```powershell
$env:DIGCLAW_ACCESS_TOKEN = "<token>"
```

Success responses usually use:

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {}
}
```

## Talent V2

### List talents

`GET /chat/talents/v2/list`

Query params:

| Name | Type | Notes |
|---|---|---|
| `pageNum` | number | 1-based page |
| `pageSize` | number | frontend commonly uses page size from `queryParams` |
| `tag` | string/null | current selected tag; omit/null when using favorite folder |
| `keyword` | string | fuzzy search |
| `favoriteFolderId` | number | filters to a favorite folder |
| `memberId` | number | filter by assigned user |
| `scoreOrder` | number | `1` ascending, `2` descending |
| `timeOrder` | number | `1` ascending, `2` descending |
| `contactStatus` | number | talent status filter, when used |

Example:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/talents/v2/list --params '{"pageNum":1,"pageSize":20,"keyword":"AI","tag":"前沿人物"}'
```

Response example:

```json
{
  "code": 200,
  "data": {
    "records": [
      {
        "idId": 10001,
        "name": "Jane Doe",
        "tag": "AI|Robotics",
        "score": "8.6",
        "updatedAt": "2026-06-01 10:00:00",
        "talentStatus": 1,
        "members": [
          {"memberId": 1, "userId": 20, "accountNum": "agent01"}
        ]
      }
    ],
    "total": 1,
    "current": 1,
    "size": 20,
    "contactStatusCount": {
      "statusCount": [0, 1, 0, 0, 0],
      "totalCount": 1
    }
  }
}
```

### Favorite folder search task

`POST /chat/talents/v2/favorite/search-task`

Body:

| Name | Type | Notes |
|---|---|---|
| `folderName` | string | favorite folder name |
| `keyword` / search text | string | the dialog form text; exact backend field follows current frontend form |
| additional form filters | object | preserve fields submitted by the frontend form |

Example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/talents/v2/favorite/search-task --data '{"folderName":"AI人才","keyword":"AI game researcher"}'
```

Response:

```json
{
  "code": 200,
  "data": {
    "taskId": 12345,
    "folderId": 88,
    "status": "PENDING",
    "progress": 0,
    "matchedCount": 0
  }
}
```

Poll:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/talents/v2/favorite/search-task/12345
```

Poll response:

```json
{
  "code": 200,
  "data": {
    "taskId": 12345,
    "folderId": 88,
    "status": "COMPLETED",
    "progress": 100,
    "matchedCount": 32,
    "message": "completed"
  }
}
```

### Update talent status

`POST /chat/talents/v2/connection/toggleTalentStatus`

Params:

| Name | Type | Notes |
|---|---|---|
| `talentId` | number | talent primary id |
| `toggleStatus` | number | target status code from `/connection/talentStatus/types` |

Example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/talents/v2/connection/toggleTalentStatus --params '{"talentId":10001,"toggleStatus":2}'
```

## Company Search

### Keyword search

`POST /chat/company-vector/search`

Common body fields inferred from the frontend:

| Name | Type | Notes |
|---|---|---|
| `keywords` | array/string | keyword search terms |
| `businessTags` | array | selected business tags |
| `chinesePeople` | number/null | `1` Chinese, `0` non-Chinese, null all |
| filter fields | object | advanced filters from `/chat/company-vector/filters` |

Example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/company-vector/search --data '{"keywords":["AI","游戏"],"businessTags":["AI技术投入高"],"chinesePeople":1}'
```

Response:

```json
{
  "code": 200,
  "data": [
    {
      "company": {
        "companyId": 100,
        "companyName": "Example AI",
        "briefIntroduction": "AI game company",
        "keyword": "AI||Game"
      },
      "connectionStatus": {"status": 0},
      "members": []
    }
  ]
}
```

### Natural language search

`GET /chat/company-vector/integrated-search`

Query params:

| Name | Type | Notes |
|---|---|---|
| `q` / keyword text | string | frontend natural language input |
| `chinesePeople` | number/null | optional |
| `businessTags` | string/array | optional |
| `use_cache` | boolean | backend supports cache flag; frontend may omit |

Example:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/company-vector/integrated-search --params '{"q":"北大团队的AIGC公司","chinesePeople":1}'
```

### Further search

`POST /chat/company-vector/filter-search`

Body:

| Name | Type | Notes |
|---|---|---|
| `ids` / result ids | array | existing result company ids |
| `question` | string | follow-up search text |

Example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/company-vector/filter-search --data '{"ids":[100,101],"question":"只保留有海外收入的公司"}'
```

## Project Memo

### List project memos

`GET /chat/project-memo/list`

Query params:

| Name | Type | Notes |
|---|---|---|
| `pageNum` | number | page |
| `pageSize` | number | page size |
| `keyword` | string | project/company search |
| `docStatus` | number/string | status code from `/docStatus/contact-options` |
| `leaderUserIds` | array/string | owner filters |
| `favoritesOnly` | boolean | only interested projects |

Example:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/project-memo/list --params '{"pageNum":1,"pageSize":20,"keyword":"AI"}'
```

Response:

```json
{
  "code": 200,
  "data": {
    "records": [
      {
        "memo": {
          "id": 2001,
          "companyName": "Example Bio",
          "enterpriseIntroduction": "Project summary",
          "isInterested": false
        },
        "docStatus": 1,
        "members": []
      }
    ],
    "total": 1
  }
}
```

### Create memo

`POST /chat/project-memo/upload`

Body usually contains memo form data plus optional file info:

```json
{
  "companyName": "Example Bio",
  "enterpriseIntroduction": "Project intro",
  "financingRound": "A轮",
  "recordDate": "2026-06-30",
  "initiator": "Founder profile",
  "fileInfos": [
    {"fileName": "memo.docx", "url": "https://..."}
  ]
}
```

Example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/project-memo/upload --data '{"companyName":"Example Bio","enterpriseIntroduction":"Project intro","financingRound":"A轮"}'
```

### Update memo status

`POST /chat/project-memo/{id}/update-doc-status`

Params:

```json
{"statusCode": 1}
```

Example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/project-memo/2001/update-doc-status --params '{"statusCode":1}'
```

### Generate memo report

`POST /chat/project-memo/{memoId}/report/generate`

Params:

```json
{"attachmentId": 3001}
```

Response:

```json
{"code":200,"data":98765}
```

Poll:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/project-memo/report-task/98765
```

Poll response:

```json
{
  "code": 200,
  "data": {
    "id": 98765,
    "memoId": 2001,
    "attachmentId": 3001,
    "status": "SUCCESS",
    "progress": 100,
    "reportId": 7001,
    "errorMsg": null
  }
}
```

## FA Collaboration

### List FA collaborations

`GET /chat/project-memo/fa-collab/page`

Query params:

| Name | Type | Notes |
|---|---|---|
| `memoId` | number | project memo id |
| `pageNum` | number | page |
| `pageSize` | number | page size |
| `keyword` | string | investor/company keyword |
| `priority` | string | from meta options |
| `progressStatus` | string | from meta options |

Example:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/project-memo/fa-collab/page --params '{"memoId":2001,"pageNum":1,"pageSize":10}'
```

### Create/update FA collaboration

Create: `POST /chat/project-memo/fa-collab`

Update: `PUT /chat/project-memo/fa-collab`

Typical body:

```json
{
  "memoId": 2001,
  "investorId": 501,
  "priority": "高",
  "progressStatus": "待联系",
  "remark": "重点跟进"
}
```

### Generate FA report

`POST /chat/project-memo/fa-collab/report/generate`

Params:

```json
{"collabId": 9001, "attachmentId": 3001}
```

Poll `GET /chat/project-memo/fa-collab/report-task/{taskId}` until `SUCCESS` or `FAILED`.

## Investor Directory

### Submit parse task

`POST /chat/investor/parse-task`

Body:

```json
{
  "sources": [
    {"url": "https://example.com/profile", "fileName": "profile page"},
    {"url": "https://cdn.example.com/investor.pdf", "fileName": "investor.pdf"}
  ]
}
```

Response:

```json
{
  "code": 200,
  "data": 123456789
}
```

Poll:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/investor/parse-task/123456789
```

Poll response:

```json
{
  "code": 200,
  "data": {
    "id": 123456789,
    "status": "PENDING_CONFIRM",
    "investorId": 5001,
    "attachmentIds": "6001,6002",
    "errorMsg": null
  }
}
```

Confirm:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/investor/parse-task/123456789/confirm
```

### Investor CRUD

Create/update body:

```json
{
  "name": "Investor Name",
  "company": "Capital Firm",
  "title": "Partner",
  "rating": "高",
  "profile": "Focus on AI and SaaS"
}
```

Create:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/investor --data '{"name":"Investor Name","company":"Capital Firm","title":"Partner"}'
```

Update:

```powershell
python scripts\digclaw_request.py --method PUT --path /chat/investor --data '{"id":5001,"name":"Investor Name","company":"Capital Firm"}'
```

## AI Analysis

### Submit second analysis

`POST /chat/analysis/second/submit-task`

Body depends on selected analysis config and uploaded file metadata. Keep the same fields the frontend form submits.

Typical shape:

```json
{
  "keywords": ["市场", "技术"],
  "files": [
    {"fileName": "report.pdf", "url": "https://..."}
  ],
  "memoId": 2001
}
```

Response:

```json
{"code":200,"data":8888}
```

Poll:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/analysis/second/task-progress --params '{"taskId":8888}'
```

Poll response:

```json
{
  "code": 200,
  "data": {
    "taskId": 8888,
    "progress": 100,
    "status": 2
  }
}
```

Refresh:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/analysis/second/all-results
```

## Admin Accounts

### Create admin user

`POST /chat/admin/users`

Body:

```json
{
  "accountNum": "agent001",
  "password": "initial-password",
  "nickName": "Agent 001",
  "accountTypeId": 1,
  "validUntil": "2026-12-31",
  "status": 1
}
```

After create/update/delete/status/password/expiry changes, refresh:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/admin/users --params '{"pageNum":1,"pageSize":20}'
```

### Account types

Create:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/admin/account-types --data '{"typeName":"VC_AGENT","description":"Agent account","status":1}'
```

Then refresh:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/admin/account-types
python scripts\digclaw_request.py --method GET --path /chat/admin/account-types/options
```
