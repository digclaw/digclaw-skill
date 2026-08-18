# Page Module: 资料汇总

Source: `/publicAssets` route, `src/views/PublicAssets.vue`, `src/api/publicAssets.js`, and selected investor APIs from `src/api/Investors.js`.

Permission gate: `public-assets`. Access requires `Public Asset Summary` in `accessibleFunctions`.

## Responsibilities

- Summarize uploaded public assets from multiple modules: audio, file, and video.
- Filter by resource type, parse status, and AI result type.
- View original file/link and AI parsed results for events, opinions, data, and investor information.
- Reparse a selected asset.
- Start investor parsing from an asset URL, then edit/save/publish investor drafts and opinions.

## Initial Load

1. Check `public-assets` permission.
2. `GET /insight/public-assets/summary` with current filters.
3. Select the first visible item when no current selection exists.

## Summary Query

`GET /insight/public-assets/summary`

Common params:

| Param | Notes |
|---|---|
| `page` | Current page. |
| `limit` | Page size; frontend options are 40, 80, 100. |
| `keyword` | Search title, link, or content. |
| `assetType` | `audio`, `file`, `video`, or omitted for all. |
| `parseStatus` | `parsed`, `parsing`, `unparsed`, or omitted. |
| `resultType` | `event`, `opinion`, `data`, `investor`, or omitted. |

Response data is expected to include `total`, `page`, `pageSize`, `totalPages`, count maps, and `items`.

## Reparse Asset

`POST /insight/public-assets/{assetId}/reparse`

After success, refresh the summary list.

## Investor Extraction From Asset

The page reuses investor parsing APIs with the selected asset URL.

1. Start parse task:

   `POST /chat/investor/parse-task`

   Body:

   ```json
   {
     "sources": [
       {
         "url": "https://example.com/source",
         "fileName": "asset file or title"
       }
     ]
   }
   ```

2. Load investor tasks associated with the selected URL:

   `GET /insight/public-assets/investor-tasks?url={selectedAssetUrl}`

3. Poll every 3 seconds while task status is `PENDING` or `RUNNING`.

4. Edit generated investor:

   `PUT /chat/investor`

5. Edit/delete generated opinions:

   `PUT /chat/investor/opinion`

   `DELETE /chat/investor/opinion/{id}`

6. Publish selected investor info/opinions:

   `POST /chat/investor/parse-task/{taskId}/publish`

   Body:

   ```json
   {
     "publishInvestor": true,
     "publishAllOpinions": false,
     "opinionIds": [1001, 1002]
   }
   ```

## Operation Notes

- Only assets with a usable URL can start investor parsing.
- Published investor/opinion drafts should be reloaded through `/insight/public-assets/investor-tasks`.
- The page displays investor parse data both in the "投资人信息" tab and, when available, in the all-results view.
