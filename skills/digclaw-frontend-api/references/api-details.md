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
| `statusCode` | number | target status code from `/connection/talentStatus/types` |

Example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/talents/v2/connection/toggleTalentStatus --params '{"talentId":10001,"statusCode":2}'
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

Frontend behavior: this submits an async search and usually returns `data.recordId`. Poll `/chat/user-record/page` until the matching record status is `请求完成` or `请求失败`; then replay completed company ids through `/chat/company-vector/search-by-ids`.

### Further search

`POST /chat/company-vector/filter-search`

Body:

| Name | Type | Notes |
|---|---|---|
| `companyIds` | array | existing result company ids |
| `question` | string | follow-up search text |

Example:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/company-vector/filter-search --data '{"companyIds":[100,101],"question":"只保留有海外收入的公司"}'
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
| `projectId` | number | project memo id used by the current FA page |
| `pageNum` | number | page |
| `pageSize` | number | page size |
| `keyword` | string | investor/company keyword |
| `priority` | string | from meta options |
| `progressStatus` | string | from meta options |

Example:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/project-memo/fa-collab/page --params '{"projectId":2001,"pageNum":1,"pageSize":10}'
```

### Create/update FA collaboration

Create: `POST /chat/project-memo/fa-collab`

Update: `PUT /chat/project-memo/fa-collab`

Typical body:

```json
{
  "projectId": 2001,
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
  "keywordText": "市场,技术",
  "files": [
    {"fileName": "report.pdf", "url": "https://..."}
  ],
  "memoId": 2001,
  "extraText": "请关注商业化风险"
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
  "accountType": "COMPANY_AGENT",
  "accountValidUntil": "2026-12-31",
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
python scripts\digclaw_request.py --method POST --path /chat/admin/account-types --data '{"typeCode":"VC_AGENT","typeName":"VC Agent","permissionLevel":1,"accessibleFunctions":["Venture Investment Directory"],"status":1,"remark":"Investor page access"}'
```

Then refresh:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/admin/account-types
python scripts\digclaw_request.py --method GET --path /chat/admin/account-types/options
```

## Frontend-Verified Additions

These examples fill gaps found by reading the current frontend pages under `diggenai_web/src/views/home.vue` and `src/views/Home/**`.

### App shell permissions

Bootstrap sequence:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/user/info
python scripts\digclaw_request.py --method GET --path /chat/user/permission
python scripts\digclaw_request.py --method GET --path /chat/user/settings
```

Permission response shape:

```json
{
  "code": 200,
  "data": {
    "permissionLevel": "MASTER",
    "accessibleFunctions": [
      "Smart Search",
      "Talent Matrix",
      "Project Connectivity",
      "Venture Investment Directory",
      "Industry Analysis",
      "Account Administration"
    ]
  }
}
```

### Smart Search async natural language search

Submit:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/company-vector/integrated-search --params '{"q":"北大团队做具身智能的创业公司","use_cache":true,"chinesePeople":1,"businessTags":[]}'
```

Submit response:

```json
{
  "code": 200,
  "data": {
    "recordId": 91001
  }
}
```

Poll history:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/user-record/page --data '{"tab":"公司","searchType":"自然语言搜索","current":1,"size":20}'
```

Completed history response:

```json
{
  "code": 200,
  "data": {
    "records": [
      {
        "id": 91001,
        "status": "请求完成",
        "searchKeyword": "北大团队做具身智能的创业公司",
        "recordData": "[{\"company\":{\"id\":100,\"companyName\":\"Example Robotics\"}}]"
      }
    ],
    "total": 1
  }
}
```

Replay completed company ids:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/company-vector/search-by-ids --data '{"companyIds":[100,101]}'
```

Further search uses `companyIds`, not `ids`:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/company-vector/filter-search --data '{"companyIds":[100,101],"question":"只保留近期有融资信号的公司"}'
```

Toggle company status uses `targetStatus`:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/company-vector/toggle-connection-status --params '{"companyId":100,"targetStatus":2}'
```

### Talent detail and manual connection

Toggle status uses `statusCode`:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/talents/v2/connection/toggleTalentStatus --params '{"talentId":10001,"statusCode":2}'
```

Manual connection sequence:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/talents/v2/connection/defaultText --params '{"talentId":10001}'
python scripts\digclaw_request.py --method POST --path /chat/talents/v2/connection/processText --data '{"talentId":10001,"text":"请基于他的AI研究经历生成建联邮件"}'
python scripts\digclaw_request.py --method POST --path /chat/talents/v2/connection/confirm --data '{"talentId":10001,"subject":"合作沟通","finalText":"您好，想和您交流AI方向合作。"}'
```

Processed text response:

```json
{
  "code": 200,
  "data": {
    "subject": "合作沟通",
    "processedText": "您好，想和您交流AI方向合作。"
  }
}
```

Annotation:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/talents/v2/annotation/list --params '{"talentId":10001}'
python scripts\digclaw_request.py --method POST --path /chat/talents/v2/annotation/add --params '{"talentId":10001}' --data '{"content":"已邮件沟通，等待回复"}'
```

### Project Memo details, @AI, and reports

List filters:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/project-memo/list --params '{"pageNum":1,"pageSize":10,"keyword":"AI","docStatus":1,"leaderUserIds":"12,13","isInterested":1}'
```

Paragraph plus mention-agent flow:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/project-memo/2001/content-paragraphs --data '{"title":"技术判断","content":"@AI 请基于附件总结技术壁垒","contentFormat":"html"}'
python scripts\digclaw_request.py --method GET --path /chat/project-memo/2001/attachments
python scripts\digclaw_request.py --method POST --path /chat/project-memo/2001/agent/mention --data '{"action":"analyze","requesterName":"agent","currentTitle":"技术判断","currentContent":"@AI 请基于附件总结技术壁垒","currentText":"请基于附件总结技术壁垒","mentionedAttachments":[],"allAttachments":[],"otherParagraphs":[]}'
```

Memo report update/delete:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/project-memo/2001/reports
python scripts\digclaw_request.py --method PUT --path /chat/project-memo/2001/report/7001 --data '{"title":"更新后的报告标题","content":"更新后的报告正文"}'
python scripts\digclaw_request.py --method DELETE --path /chat/project-memo/2001/report/7001
```

### FA collaboration page

Current page uses `projectId`:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/project-memo/fa-collab/page --params '{"projectId":2001,"pageNum":1,"pageSize":10,"priority":"高","progressStatus":"待联系"}'
```

Add one investor or sync many investors:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/project-memo/fa-collab --data '{"projectId":2001,"investorId":501}'
python scripts\digclaw_request.py --method PUT --path /chat/project-memo/fa-collab/sync --data '{"projectId":2001,"investorIds":[501,502,503]}'
```

Notes, attachments, and report:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/project-memo/fa-collab/remark/page --params '{"collabId":9001,"pageNum":1,"pageSize":10}'
python scripts\digclaw_request.py --method POST --path /chat/project-memo/fa-collab/remark --data '{"collabId":9001,"content":"已约下周沟通"}'
python scripts\digclaw_request.py --method GET --path /chat/project-memo/fa-collab/attachment/list --params '{"collabId":9001}'
python scripts\digclaw_request.py --method POST --path /chat/project-memo/fa-collab/report/generate --params '{"collabId":9001,"attachmentId":3001}'
```

### Investor page parse refresh

Submit parse task:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/investor/parse-task --data '{"sources":[{"url":"https://example.com/profile","fileName":"社媒链接"},{"url":"https://cdn.example.com/investor.pdf","fileName":"investor.pdf"}]}'
```

The page refreshes these while tasks are running:

```powershell
python scripts\digclaw_request.py --method GET --path /chat/investor/parse-task/list
python scripts\digclaw_request.py --method GET --path /chat/investor/list --params '{"pageNum":1,"pageSize":10}'
python scripts\digclaw_request.py --method GET --path /chat/investor/opinion/page --params '{"pageNum":1,"pageSize":10}'
```

### AI second analysis

Current submit body:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/analysis/second/submit-task --data '{"files":[{"fileName":"memo.pdf","fileUrl":"https://cdn.example.com/memo.pdf"}],"extraText":"请关注商业化风险","keywordText":"市场,技术","memoId":2001}'
```

### Industry Insight

Use the Insight base URL:

```powershell
python scripts\digclaw_request.py --base insight --method GET --path /events/rank --params '{"pageNum":1,"pageSize":20,"keyword":"AI"}'
python scripts\digclaw_request.py --base insight --method GET --path /events/topRank
python scripts\digclaw_request.py --base insight --method GET --path /events/todayFocus
python scripts\digclaw_request.py --base insight --method GET --path /events/cycleDistribution
python scripts\digclaw_request.py --base insight --method GET --path /events/trend --params '{"type":"day","period":30}'
python scripts\digclaw_request.py --base insight --method GET --path /events/123
```

Paged rank response can be one of several shapes; normalize like the frontend:

```json
{
  "code": 200,
  "data": {
    "records": [
      {
        "id": 123,
        "publishDate": "2026-06-30",
        "subject": "Example Lab",
        "eventSummary": "发布新模型",
        "mentionCount": 120,
        "importanceScore": 88
      }
    ],
    "total": 1
  }
}
```

### Admin Accounts current forms

Current user form:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/admin/users --data '{"accountNum":"agent001","password":"123456","nickName":"Agent 001","accountType":"COMPANY_AGENT","status":1,"accountValidUntil":"2026-12-31"}'
python scripts\digclaw_request.py --method PUT --path /chat/admin/users/101/status --data '{"status":0}'
python scripts\digclaw_request.py --method PUT --path /chat/admin/users/101/password --data '{"password":"123456"}'
```

Current account-type form:

```powershell
python scripts\digclaw_request.py --method POST --path /chat/admin/account-types --data '{"typeCode":"COMPANY_AGENT","typeName":"企业代理人","permissionLevel":1,"accessibleFunctions":["Smart Search"],"status":1,"remark":"Smart Search only"}'
python scripts\digclaw_request.py --method PUT --path /chat/admin/account-types/1/status --data '{"status":0}'
```
