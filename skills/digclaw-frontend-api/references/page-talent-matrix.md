# Page Module: 人才矩阵

Source: `Home/Talents.vue`, `AddCustomerFavorite.vue`, `TalentPanelType1/2/3.vue`, `TalentConnect.vue`.

Permission gate: `talent-matrix`.

## Responsibilities

- Talent V2 list, tags, status filters, member filters, sorting, infinite scroll.
- Favorite folders and async favorite-folder search.
- Talent detail panels, interest, annotations.
- Manual connection text generation and confirmation.
- Talent member assignment and export.

## Adaptive Search Guidance

Do not treat the user's wording as the only valid `keyword`. Derive role-title variants, seniority terms, skills, technologies, research fields, employer types/names, locations, and Chinese/English equivalents that retain the user's hard constraints. Start with high-signal combinations; if returned people are sparse or irrelevant, try materially different expansions or relax only non-essential terms. Continue through `pageNum` while `data.total` shows more records and later pages may improve coverage. Merge and deduplicate by talent ID, and stop when useful coverage is reached or new pages/queries become repetitive.

Always fetch `GET /chat/talents/v2/tags` before the first talent list/search request. Compare the returned labels with the user's requested profile and set `tag` to one exact returned value only when it is a meaningful constraint. Otherwise send `tag: null`; the frontend's `all` value is UI state and is converted to `null` for the API. Do not infer valid filter values from the “人才标签” shown on individual result rows. When both keyword and tag could apply, use the tag only if it improves precision without hiding plausible matches; for broad discovery, search without a tag first and optionally use a relevant tag in a refinement pass.

## Initial Load

1. `GET /chat/talents/v2/tags`, then decide whether one returned exact value should be sent as `tag`; otherwise use `null`.
2. `GET /chat/talents/v2/connection/talentStatus/types`.
3. `GET /chat/companyMember/agentUsers`.
4. `GET /chat/talents/v2/favorite/list`.
5. `GET /chat/talents/v2/list` with `pageNum`, `pageSize`, `tag`, `keyword`, `favoriteFolderId`, `memberId`, `scoreOrder`, `timeOrder`.

## Main Operations

### List/Search/Filter

1. Reset `pageNum` to `1` and normalize the tag selection: one relevant exact server-provided tag, or `null` for no tag/“all”.
2. `GET /chat/talents/v2/list`.
3. Use `data.records`, `data.total`, `data.contactStatusCount`.
4. For infinite scroll, increment `pageNum` and append `records`.
5. Continue keyword variants and pages as needed to satisfy the user's requested coverage; do not stop solely because the first API call returned successfully.

### Favorite Folder Search

1. `POST /chat/talents/v2/favorite/search-task` with the dialog form.
2. Refresh `GET /chat/talents/v2/favorite/list`.
3. Poll `GET /chat/talents/v2/favorite/search-task/{taskId}` every ~1 second.
4. Running statuses: `PENDING`, `RUNNING`, `CANCELLING`.
5. On `COMPLETED`, refresh favorite list and list talents by `favoriteFolderId`.
6. Cancel: `POST /chat/talents/v2/favorite/search-task/{taskId}/cancel`.
7. Delete folder: `DELETE /chat/talents/v2/favorite/{id}`, then refresh.

### Talent Detail

1. `GET /chat/talents/v2/detail/{id}`.
2. `GET /chat/talents/v2/annotation/list?talentId={id}`.
3. Toggle interest: `POST /chat/talents/v2/toggle-interest`.
4. Add annotation: `POST /chat/talents/v2/annotation/add?talentId={id}`.

### Connection Status

1. `POST /chat/talents/v2/connection/toggleTalentStatus` with `talentId`, `statusCode`.
2. Update row locally.
3. Refresh `GET /chat/talents/v2/list` to update `contactStatusCount`.

### Manual Connection Text

1. `GET /chat/talents/v2/connection/defaultText?talentId={id}`.
2. `POST /chat/talents/v2/connection/processText`.
3. Confirm with `POST /chat/talents/v2/connection/confirm`.
4. Mark the row/detail connected or refresh the detail.

### Assignment And Export

- Assign members: `POST /chat/talents/v2/member/register` with `talentId` and full `userIds`.
- Export current filtered talent data: `POST /chat/talents/v2/export`.
