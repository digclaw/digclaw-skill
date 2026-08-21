# Page Module: App Shell, Login, User, Files

Source: `src/views/home.vue`, `src/api/login.js`, `src/utils/request.js`.

Permission gate: `shell`. File-management-only actions use `file-management`.

## Responsibilities

- Login/register and current login state.
- Permission bootstrap and default page selection.
- Global conversation list, meeting-minute list, unread reminders, coin/order/profile settings.
- OSS token and upload orchestration used by shell-level meeting minutes.

## Login State

Frontend login state is `localStorage.access_token` plus Vuex `state.user.token`. API calls add:

```text
Authorization: Bearer <access_token>
clientid: b7bf1120a216184a9e0f4ca0e9c508bb
```

## Operations

### Login And Bootstrap

1. Resolve credentials from `--token`, `DIGCLAW_ACCESS_TOKEN`, `DIGCLAW_ACCOUNT_NUM`/`DIGCLAW_USERNAME` plus `DIGCLAW_PASSWORD`, then the cached session.
2. If no credential source exists, ask the user for the DigClaw account and password.
3. `POST /appAuth/login` with `accountNum`, `password`, `clientId`, `grantType: "appPwd"` when a fresh login is needed.
4. Read `data.access_token` and `data.userId`.
5. `GET /chat/user/info`.
6. `GET /chat/user/permission`.
7. `GET /chat/user/settings`.
8. Choose the first accessible page in this order: Smart Search, AI Conversation Search, Rhizome Agent, File Transcription, Talent Matrix, Project Connectivity, Venture Investment Directory, Industry Analysis, Public Asset Summary. Admin Accounts is only for `MASTER` or `Account Administration`.

Helper:

```powershell
python scripts\digclaw_login.py --account-num "<accountNum>" --password "<password>"
python scripts\digclaw_login.py --account-num "<accountNum>" --password "<password>" --persist-credentials
```

Use `--persist-credentials` only after the user explicitly agrees to store `DIGCLAW_ACCOUNT_NUM` and `DIGCLAW_PASSWORD` in the operating-system user environment.

### Meeting-Minute Upload And List

1. `GET /chat/file/getTemporaryToken`.
2. Upload file to OSS.
3. `POST /chat/meetingMinutes/create`.
4. Refresh `GET /chat/meetingMinutes/mineList`.
5. Poll `GET /chat/meetingMinutes/unreadList` when the shell needs unread markers.

### Meeting-Minute Management

| Operation | Sequence |
|---|---|
| Detail | `GET /chat/meetingMinutes/info/{id}` |
| Rename own item | `POST /chat/meetingMinutes/edit/{id}` |
| Rename bought item | `POST /chat/meetingMinutes/editBuy/{id}` |
| Delete batch | `POST /chat/meetingMinutes/batchRemove` |
| Mark opened | `POST /chat/meetingMinutes/open/{id}` or `/openBuy/{id}` |
| Mark read | `POST /chat/meetingMinutes/read/{id}` |
| Batch download | `POST /chat/batch-download/download` |

### User/Commerce/Conversation

- Conversations: create/list/detail/remove via `/chat/userConversation/...`.
- Coin detail: `/chat/user/accountPoint/info`, `/chat/user/accountPoint/transactions`.
- Product/order: `/chat/product/info/{id}`, `/chat/order/create`.
- Profile/password: `/chat/user/updateBaseInfo`, `/chat/user/updatePassword`.
