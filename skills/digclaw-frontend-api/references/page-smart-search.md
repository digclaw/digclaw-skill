# Page Module: 智能搜索 / 公司云库

Source: `Home/SmartSearch.vue`, `FindCompany.vue`, `FindCompanyResultList.vue`, `ElitedCompany.vue`, `ComapnyPanel.vue`, `TalentCard.vue`.

Permission gate: `smart-search`. For company search operations also check `smart-search.company-search`; for curated-list operations also check `smart-search.curated-list`.

## Responsibilities

- Company keyword search, natural-language search, advanced filters, business tags, China/non-China filters.
- Company search history, replay, further search, export.
- Company detail, interest, connection status, member assignment, comments.
- Talent natural search inside the same page.
- CSV/custom-company generation task entry.

## Search Choice Guidance

When a user asks to search companies, prefer Company Keyword Search when the request can be expressed as keywords, tags, China/non-China scope, or advanced filters. Tell the user that the current Smart Search natural-language mode can take longer because it submits an async task and requires history polling, but it remains available when they want semantic query expansion or a less structured query.

Before the first request, derive multiple plausible keyword formulations from the user's intent. Search the strongest formulation first, assess actual record relevance, then use alternate synonyms, bilingual terms, abbreviations, adjacent categories, product names, or relaxed non-essential constraints when the initial results are insufficient. Preserve explicit hard constraints. For each useful formulation, request subsequent `page` values while more records remain and additional coverage is valuable; merge and deduplicate results by company ID. A successful but irrelevant first response is not a stopping condition.

## Initial Load

1. `GET /chat/user/permission`.
2. `GET /chat/company-vector/business-tags`.
3. `GET /chat/company-vector/statistics`.
4. `GET /chat/company-vector/filters` when advanced filter is opened.
5. `GET /chat/company/contactStatus/types`.
6. `GET /chat/companyMember/agentUsers`.
7. `POST /chat/user-record/page` with current tab/search type.

## Main Operations

### Company Keyword Search

Use this first for normal company search requests. It returns result rows directly and matches the faster current frontend path.

1. Build body with `keywords`, `page`, `size`, `chinesePeople`, `businessTags`, `establishTimeOrder`, and optional advanced filter values.
2. `POST /chat/company-vector/search`.
3. Display returned rows.
4. `POST /chat/user-record/add` with `tab: "公司"`, `searchType: "关键词搜索"`, and JSON `recordData`.
5. When more rows are available, increment `page` and repeat; append and deduplicate records rather than replacing previously relevant matches.

### Company Natural-Language Search

Before using this path, tell the user it usually takes longer than keyword search because it submits an async backend task and the page polls history about every 10 seconds. Use it when the user's query is exploratory, broad, or hard to translate into keywords/filters.

1. `GET /chat/company-vector/integrated-search` with `q`, `use_cache: true`, `chinesePeople`, `businessTags`.
2. Read `data.recordId`.
3. Poll every ~10 seconds: `POST /chat/user-record/page` with `{ tab: "公司", searchType: "自然语言搜索", current: 1, size: 20 }`.
4. On status `请求完成`, refresh history. To show result rows, parse `recordData`, collect `company.id`, then `POST /chat/company-vector/search-by-ids` with `{ companyIds }`.
5. On status `请求失败`, stop and report failure.

### Further Search

1. Collect current result `companyIds`.
2. `POST /chat/company-vector/filter-search` with `{ companyIds, question }`.
3. Replace visible rows with `data.data`.
4. Save a new history snapshot with `POST /chat/user-record/add`.

### History

| Operation | API |
|---|---|
| List history | `POST /chat/user-record/page` |
| Save history | `POST /chat/user-record/add` |
| Update history | `PUT /chat/user-record/update` |
| Delete history | `DELETE /chat/user-record/delete/{id}` |
| Replay company rows | `POST /chat/company-vector/search-by-ids` |

### Company Detail And Actions

1. Detail: `GET /chat/company-vector/detail?companyId={id}`.
2. Interest: `POST /chat/company-vector/toggle-interest`.
3. Connection status: `POST /chat/company-vector/toggle-connection-status` with `companyId`, `targetStatus`.
4. Smart Search member assign: `POST /chat/company-vector/member/register` with `companyId`, full `userIds`.
5. Detail panel may also load comments/member bindings from `/chat/comment/company/*` and `/chat/companyMember/*`.

### Export And CSV Task

- Export visible search-result companies: `POST /chat/company-vector/export` with `{ companyIds }`; frontend treats response `msg` as a downloadable CSV URL and downloads it in the browser.
- Company Cloud curated-list export is available only to `MASTER` in the current `ElitedCompany.vue` UI. It uses `POST /chat/company/export` with `{ query }`, where `query` is the current company cloud filter/search params reset to `pageNum: 1`. The backend exports all rows matching that query and returns a CSV URL in `msg`.
- CSV generation mode: `GET /chat/custom-company/tasks`, `POST /chat/custom-company/task/submit`, delete with `/chat/custom-company/task/delete`.

### Talent Search Inside Smart Search

1. `POST /chat/search/talent-search` with params `{ inputText, mode: "result" }`.
2. Display `data.data`.
3. Refresh/save history for `tab: "个人"`.
4. If results do not satisfy the request, retry with expanded role, skill, organization, domain, and bilingual keyword variants. Merge and deduplicate people across searches; use a paginated talent surface when broader coverage is required and this endpoint does not expose continuation.
