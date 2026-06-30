# Page Module: 行业探析

Source: `Home/IndustryAnalyze.vue`, `LeaderPeopleTab.vue`, `ViewPointsTab.vue`, `EventDetailDialog.vue`, `LeaderDetailDialog.vue`, `OpinionDetailDialog.vue`.

## Responsibilities

- Industry event dashboard and event rank/search/pagination.
- Event top rank, today's focus, cycle distribution, trend chart.
- Leader/person rank, detail, history.
- Opinion rank, summary, sentiment distribution, trend, detail.

Insight endpoints use base URL `https://v3-api.diggen.cn/insight`.

## Initial Load

1. `GET /insight/events/rank` with `pageNum`, `pageSize`, optional `keyword`.
2. `GET /insight/events/topRank`.
3. `GET /insight/events/todayFocus`.
4. `GET /insight/events/cycleDistribution`.
5. `GET /insight/events/trend` with `{ type: "day", period: 30 }` or `{ type: "month", period: 12 }`.

## Event Rank/Search

1. Reset `pageNum` to `1` when keyword changes.
2. `GET /insight/events/rank`.
3. Normalize page data from one of: top-level `rows`, `data.rows`, `data.list`, `data.records`, or array `data`.
4. If current page is beyond max page after filtering, retry the max valid page.

## Event Detail

- Open dialog: `GET /insight/events/{id}`.

## Leader People Tab

| Operation | API |
|---|---|
| Rank/list | `GET /insight/persons/rank` |
| Detail | `GET /insight/persons/{pid}` |
| History | `GET /insight/persons/history/{pid}` |

## Viewpoints Tab

| Operation | API |
|---|---|
| Opinion rank | `GET /insight/opinions/rank` |
| Summary | `GET /insight/opinions/summary` |
| Sentiment distribution | `GET /insight/opinions/sentimentDistribution` |
| Trend | `GET /insight/opinions/trend` |
| Detail | `GET /insight/opinions/{id}` |
