# Page Module: 账号管理

Source: `Home/AdminAccounts.vue`, `src/api/adminAccount.js`.

Permission gate: `admin-accounts`. Access requires `accountType === "MASTER"` or `Account Administration`.

## Responsibilities

- Admin user list/create/update/delete.
- Password reset and status toggle.
- Account type/template list/create/update/delete/status toggle.
- Permission function assignment through account type `accessibleFunctions`.
- Per-user company data window restriction and search rate limits.
- Clearing per-user company/talent search rate-limit counters.

## Initial Load

1. `GET /chat/admin/account-types/options`.
2. `GET /chat/admin/users` with paging/filter params.
3. `GET /chat/admin/account-types` with paging/filter params.

## User Operations

| Operation | API | Notes |
|---|---|---|
| List | `GET /chat/admin/users` | returns paged `records` |
| Create | `POST /chat/admin/users` | current form sends `accountNum`, `password`, `nickName`, `accountType`, `status`, `accountValidUntil` |
| Update | `PUT /chat/admin/users/{id}` | same form, password can be blank on edit |
| Reset password | `PUT /chat/admin/users/{id}/password` | current page resets to `{ password: "123456" }` |
| Toggle status | `PUT /chat/admin/users/{id}/status` | body `{ status: 1|0 }`; page updates row locally |
| Clear search rate limit | `POST /chat/admin/users/{id}/search-rate-limit/clear` | body `{ "type": "all" | "company" | "talent" }` |
| Delete | `DELETE /chat/admin/users/{id}` | refresh user list |

Current create/update user form also sends:

| Field | Notes |
|---|---|
| `companyDataRestrictBeforeDays` | `0` disables the company data time-window restriction; positive values restrict visible company data to that many days. |
| `companySearchMaxPerHour` | Per-user company search hourly limit; frontend defaults invalid/empty values to `50`. |
| `talentSearchMaxPerHour` | Per-user talent search hourly limit; frontend defaults invalid/empty values to `50`. |

Note: `updateAdminUserExpiry` exists in the API helper, but the current page edits expiry through `accountValidUntil` in create/update.

## Account Type Operations

| Operation | API | Notes |
|---|---|---|
| Options | `GET /chat/admin/account-types/options` | used by user form |
| List | `GET /chat/admin/account-types` | paged table |
| Create | `POST /chat/admin/account-types` | `typeCode`, `typeName`, `permissionLevel`, `accessibleFunctions`, `status`, `remark` |
| Update | `PUT /chat/admin/account-types/{id}` | same form |
| Toggle status | `PUT /chat/admin/account-types/{id}/status` | body `{ status: 1|0 }`; refresh options |
| Delete | `DELETE /chat/admin/account-types/{id}` | refresh list and options |

Current permission function options include `Smart Search`, `AI Conversation Search`, `Talent Matrix`, `Project Connectivity`, `Industry Analysis`, `Company Search`, `View Curated List`, `Venture Investment Directory`, `Investment Views Editor`, `Public Asset Summary`, `Rhizome Agent`, `File Transcription`, `Account Administration`, and legacy `AI Souring`. The current backend default grants `File Transcription` to `MASTER`.
