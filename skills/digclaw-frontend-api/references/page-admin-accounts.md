# Page Module: 账号管理

Source: `Home/AdminAccounts.vue`, `src/api/adminAccount.js`.

Permission gate: `admin-accounts`. Access requires `accountType === "MASTER"` or `Account Administration`.

## Responsibilities

- Admin user list/create/update/delete.
- Password reset and status toggle.
- Account type/template list/create/update/delete/status toggle.
- Permission function assignment through account type `accessibleFunctions`.

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
| Delete | `DELETE /chat/admin/users/{id}` | refresh user list |

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
