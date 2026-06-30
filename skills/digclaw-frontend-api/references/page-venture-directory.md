# Page Module: 创投名录

Source: `Home/Investors1.vue`, `InvestorAdd.vue`, `InvestorAttachments.vue`, `OpinionAdd.vue`, `OpinionEdit.vue`, `OpinionSelectInvestor.vue`, `InvestoParseTaskData.vue`.

Permission gate: `venture-directory`.

## Responsibilities

- Investor parse tasks from uploaded files or social links.
- Investor list/detail/create/update/delete.
- Investor attachments.
- Investor opinions and links to investors.
- Periodic refresh while parse tasks/opinions are active.

## Initial Load

1. `GET /chat/file/getTemporaryToken` for OSS credentials.
2. `GET /chat/investor/list`.
3. `GET /chat/investor/opinion/page`.
4. `GET /chat/investor/parse-task/list`.
5. Start refresh loops:
   - parse tasks and investor list every ~30 seconds while tasks are `PENDING` or `RUNNING`
   - opinion page every ~30 seconds

## Parse Investor

1. If files are supplied, upload them to OSS.
2. If a social link is supplied, add it to `sources` as `{ url, fileName: "社媒链接" }`.
3. `POST /chat/investor/parse-task` with `{ sources }`.
4. Poll `GET /chat/investor/parse-task/{id}` or refresh `GET /chat/investor/parse-task/list`.
5. Running statuses: `PENDING`, `RUNNING`.
6. Confirmation status: `PENDING_CONFIRM`; confirm with `POST /chat/investor/parse-task/{id}/confirm`.
7. Refresh parse tasks, investor list, and opinion page.
8. Delete parse task: `DELETE /chat/investor/parse-task/{id}`.

## Investor CRUD

| Operation | API |
|---|---|
| List | `GET /chat/investor/list` |
| Detail | `GET /chat/investor/{id}` |
| Create | `POST /chat/investor` |
| Update | `PUT /chat/investor` |
| Delete | `DELETE /chat/investor/{id}` |

## Investor Attachments

1. Upload to OSS.
2. Register: `POST /chat/investor/attachment/upload`.
3. List: `GET /chat/investor/attachment/list?investorId={id}`.
4. Delete: `DELETE /chat/investor/attachment/{id}`.

## Opinions

| Operation | API |
|---|---|
| List | `GET /chat/investor/opinion/page` |
| Create | `POST /chat/investor/opinion` |
| Update | `PUT /chat/investor/opinion` |
| Delete | `DELETE /chat/investor/opinion/{id}` |

After opinion create/update/delete, refresh `GET /chat/investor/opinion/page`.
