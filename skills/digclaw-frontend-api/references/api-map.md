# DigClaw Frontend API Map

Use the production host `https://v3-api.diggen.cn` for `/chat/...` paths and `https://v3-api.diggen.cn/insight` for Insight paths.

## Auth, User, Orders, Conversation

| Feature | Function | Method | Path |
|---|---|---:|---|
| Login | `login` | POST | `/appAuth/login` |
| Register | `register` | POST | `/appAuth/register` |
| Current user | `myInfo` | GET | `/chat/user/info` |
| User permission | `userPermissionLevel` | GET | `/chat/user/permission` |
| User settings | `getUserSettingsAPI` | GET | `/chat/user/settings` |
| Update settings | `updateUserSettingsAPI` | PUT | `/chat/user/settings` |
| Update profile | `updateBaseInfoAPI` | PUT | `/chat/user/updateBaseInfo` |
| Update password | `updatePasswordAPI` | PUT | `/chat/user/updatePassword` |
| Coin balance | `coinInfo` | GET | `/chat/user/accountPoint/info` |
| Coin transactions | `transactions` | GET | `/chat/user/accountPoint/transactions` |
| Product info | `productInfoById` | GET | `/chat/product/info/{id}` |
| Create order | `createOrder` | POST | `/chat/order/create` |
| Create conversation | `messageAdd` | POST | `/chat/userConversation/create` |
| Conversation stream | `messageStream` | POST | `/chat/userConversation/{id}/completion/stream` |
| Conversation list | `conversationList` | GET | `/chat/userConversation/list` |
| Conversation detail | `conversationDetailAPI` | GET | `/chat/userConversation/message/{id}` |
| Remove conversation | `removeConversation` | POST | `/chat/userConversation/remove/{id}` |
| Dict data | `dictDataAPI` | GET | `/chat/dict/queryDictDataList` |
| OSS STS token | `getTemporaryToken` | GET | `/chat/file/getTemporaryToken` |
| Batch download | `multiDownload` | POST | `/chat/batch-download/download` |

## Meeting Minutes And Legacy Memo

| Feature | Function | Method | Path |
|---|---|---:|---|
| Create meeting minutes | `meetingcreate` | POST | `/chat/meetingMinutes/create` |
| My meeting list | `myMeetingList` | GET | `/chat/meetingMinutes/mineList` |
| Meeting detail | `minutesInfoById` | GET | `/chat/meetingMinutes/info/{id}` |
| Remove meetings | `removeMeeting` | POST | `/chat/meetingMinutes/batchRemove` |
| Rename meeting | `reNameMeeting` | POST | `/chat/meetingMinutes/edit/{id}` |
| Rename bought meeting | `reNameBuyMeeting` | POST | `/chat/meetingMinutes/editBuy/{id}` |
| Mark opened | `hanldeOpen` | POST | `/chat/meetingMinutes/open/{id}` |
| Mark bought opened | `hanldeBuyOpen` | POST | `/chat/meetingMinutes/openBuy/{id}` |
| Share meeting | `share` | POST | `/chat/meetingMinutes/share/{id}` |
| Share point text | `sharePOint` | GET | `/chat/meetingMinutes/share/{id}/getSharePointStr` |
| Buy meeting | `buy` | POST | `/chat/meetingMinutes/buy/{id}` |
| Unread list | `unreadList` | GET | `/chat/meetingMinutes/unreadList` |
| Mark read | `read` | POST | `/chat/meetingMinutes/read/{id}` |
| Edit analysis result | `editTaskResult` | POST | `/chat/meetingMinutes/editTaskResult/{id}` |
| Personal share list | `personalShareSpaceList` | GET | `/chat/meetingMinutes/personalShareList` |
| Document status list | `docLabelListAPI` | GET | `/chat/docStatus/list` |
| Active document status | `getDocStatus` | GET | `/chat/docStatus/getActive` |
| Update document status | `updateDocStatus` | POST | `/chat/docStatus/update` |
| Analysis task types | `generateTypeList` | GET | `/chat/analysis/task-types` |
| Submit analysis tasks | `submitTask` | POST | `/chat/analysis/submit-tasks` |
| Analysis task results | `taskResults` | GET | `/chat/analysis/task-results` |
| Analysis progress | `taskProgress` | GET | `/chat/analysis/task-progress` |
| Delete analysis task | `deleteTaskResult` | POST | `/chat/analysis/delete-task` |
| Meeting attachment list | `attachmentListApi` | GET | `/chat/meeting/attachment/list` |
| Upload attachment | `uploadAttachment` | POST | `/chat/meeting/attachment/upload` |
| Update attachment | `updateAttachment` | POST | `/chat/meeting/attachment/update` |
| Delete attachment | `deleteAttachment` | POST | `/chat/meeting/attachment/delete/{id}` |

## Shared Company Data, Comments, Members

| Feature | Function | Method | Path |
|---|---|---:|---|
| Labels | `labelListAPI` | GET | `/chat/label/list` |
| Company list | `shareSpaceList` | GET | `/chat/company/list` |
| Company detail | `companyInfo` | GET | `/chat/company/detail` |
| Search filter values | `searchvalList` | GET | `/chat/search/searchval` |
| Contact status count | `contactStatusCount` | GET | `/chat/company/contactStatus/count` |
| Like status | `likeStatus` | GET | `/chat/like/status` |
| Like meeting | `like` | POST | `/chat/meetingMinutes/like/{id}` |
| Unlike meeting | `unlike` | POST | `/chat/meetingMinutes/unlike/{id}` |
| Comment list | `commentList` | GET | `/chat/comment/list` |
| Create comment | `commentCreated` | POST | `/chat/comment/create` |
| Delete comment | `deleteComment` | POST | `/chat/comment/remove/{id}` |
| Project status | `getStatus` | GET | `/chat/project/getStatus` |
| Contact project | `contactProject` | POST | `/chat/project/contact` |
| Cancel contact | `cancleContactProject` | POST | `/chat/project/cancelContact` |
| Toggle project status | `toggleProjectStatus` | POST | `/chat/project/toggleStatus` |
| Available doc members | `getUserListAPI` | GET | `/chat/docMember/available` |
| Member identity types | `getIdentityTypesAPI` | GET | `/chat/docMember/identityTypes` |
| Register doc member | `registermemberAPI` | POST | `/chat/docMember/register` |
| Doc member list | `memberListByDocId` | GET | `/chat/docMember/list` |
| Update member role | `updateMemberRole` | PUT | `/chat/docMember/updateIdentity` |
| Delete member | `deleteMember` | DELETE | `/chat/docMember/{id}` |
| Company annotation add | `annotationAddAPI` | POST | `/chat/company/annotation/add?companyId={id}` |
| Company annotation list | `getAnnotationListByIdAPI` | GET | `/chat/company/annotation/list` |
| Company export | `eliteDataExportAPI` | POST | `/chat/company/export` |

## Smart Search And Company Vector

| Feature | Function | Method | Path |
|---|---|---:|---|
| Company keyword search | `companyKeywordsAPI` | POST | `/chat/company-vector/search` |
| Company natural search | `companyNatureAPI` | GET | `/chat/company-vector/integrated-search` |
| Company filters | `filtersOptionsAPI` | GET | `/chat/company-vector/filters` |
| Company business tags | `companyFilterTagsOptionsAPI` | GET | `/chat/company-vector/business-tags` |
| Further filter search | `furtherSearchAPI` | POST | `/chat/company-vector/filter-search` |
| Search by ids | `getcompanyListByIds` | POST | `/chat/company-vector/search-by-ids` |
| Company detail | `companyDetailApi` | GET | `/chat/company-vector/detail` |
| Toggle company interest | `companyToggleInterestedAPI` | POST | `/chat/company-vector/toggle-interest` |
| Toggle connection status | `companyToggleStatusAPI` | POST | `/chat/company-vector/toggle-connection-status` |
| Search export | `searchResultExportAPI` | POST | `/chat/company-vector/export` |
| Today statistics | `todayCompanyStatisticsAPI` | GET | `/chat/company-vector/statistics` |
| Agent options | `companyAgentOptionsAPI` | GET | `/chat/companyMember/agentUsers` |
| Register company vector member | `agentVectorRegisterAPI` | POST | `/chat/company-vector/member/register` |
| Search history page | `historyDataAPI` | POST | `/chat/user-record/page` |
| Add history record | `addRecordAPI` | POST | `/chat/user-record/add` |
| Update history record | `updateSearchDataAPI` | PUT | `/chat/user-record/update` |
| Delete history record | `deleteRecordAPI` | DELETE | `/chat/user-record/delete/{id}` |
| Talent natural search | `talentSearchNatureAPI` | POST | `/chat/search/talent-search` |
| Status options | `stateOptionsAPI` | GET | `/chat/company/contactStatus/types` |

## Talent V2

| Feature | Function | Method | Path |
|---|---|---:|---|
| Tags | `labelListV2API` | GET | `/chat/talents/v2/tags` |
| Talent list | `talentsListV2API` | GET | `/chat/talents/v2/list` |
| Talent detail | `talentsV2Info` | GET | `/chat/talents/v2/detail/{id}` |
| Legacy talent list | `talentsListAPI` | GET | `/chat/talents/list` |
| Legacy talent detail | `talentsInfo` | GET | `/chat/talents/detail/{id}` |
| Default connection text | `defaultTextAPIV2` | GET | `/chat/talents/v2/connection/defaultText` |
| Process connection text | `processTextAPIV2` | POST | `/chat/talents/v2/connection/processText` |
| Confirm connection | `processConfirmAPIV2` | POST | `/chat/talents/v2/connection/confirm` |
| Toggle talent status | `toggleTalentStatus` | POST | `/chat/talents/v2/connection/toggleTalentStatus` |
| Talent status options | `stateOptionsAPI` | GET | `/chat/talents/v2/connection/talentStatus/types` |
| Toggle interest | `talentToggleInterestAPI` | POST | `/chat/talents/v2/toggle-interest` |
| Annotation list | `annotationListAPI` | GET | `/chat/talents/v2/annotation/list` |
| Add annotation | `annotationUpdateAPI` | POST | `/chat/talents/v2/annotation/add?talentId={id}` |
| Add favorite folder helper (not used by current Talent page; current page creates folders through search task) | `favoriteAddAPI` | POST | `/chat/talents/v2/favorite` |
| Favorite folders | `favoriteListAPI` | GET | `/chat/talents/v2/favorite/list` |
| Delete favorite folder | `favoriteDeleteAPI` | DELETE | `/chat/talents/v2/favorite/{id}` |
| Start favorite search | `favoriteSearchStartAPI` | POST | `/chat/talents/v2/favorite/search-task` |
| Favorite search status | `favoriteSearchStatusAPI` | GET | `/chat/talents/v2/favorite/search-task/{taskId}` |
| Cancel favorite search | `favoriteSearchCancelAPI` | POST | `/chat/talents/v2/favorite/search-task/{taskId}/cancel` |
| Register member | `agentRegisterAPI` | POST | `/chat/talents/v2/member/register` |
| Export talent data | `talentDataExportAPI` | POST | `/chat/talents/v2/export` |

## Project Memo And FA Collab

| Feature | Function | Method | Path |
|---|---|---:|---|
| Contact status options | `docStatusContactOptionsAPI` | GET | `/chat/docStatus/contact-options` |
| Memo list | `projectMemoListAPI` | GET | `/chat/project-memo/list` |
| Memo detail | `projectMemoDetailAPI` | GET | `/chat/project-memo/{id}` |
| Upload/create memo | `projectMemoAddAPI` | POST | `/chat/project-memo/upload` |
| Update memo | `projectMemoUpdateAPI` | PUT | `/chat/project-memo` |
| Delete memo | `projectMemoDeleteAPI` | DELETE | `/chat/project-memo/{id}` |
| Toggle memo interest | `projectMemoToggleInterestedAPI` | POST | `/chat/project-memo/{id}/toggle-interest` |
| Update memo status | `projectMemoUpdateStatusAPI` | POST | `/chat/project-memo/{id}/update-doc-status` |
| Available members | `availableMemberAPI` | GET | `/chat/project-memo/member/available` |
| Update appointment | `appointmentTimeUpdateAPI` | PUT | `/chat/project-memo/appointment-time` |
| Attachment list | `attachmentListAPI` | GET | `/chat/project-memo/{id}/attachments` |
| Update attachment list | `updateAttachmentListAPI` | PUT | `/chat/project-memo/{id}/attachments` |
| Editor upload | `projectMemoEditorUploadAPI` | POST | `/chat/file/upload` |
| Mention agent | `projectMemoMentionAgentAPI` | POST | `/chat/project-memo/{memoId}/agent/mention` |
| Add paragraph | `paragraphsAddAPI` | POST | `/chat/project-memo/{memoId}/content-paragraphs` |
| Update paragraph | `paragraphsUpdateAPI` | PUT | `/chat/project-memo/{memoId}/content-paragraphs/{paragraphId}` |
| Delete paragraph | `paragraphsDeleteAPI` | DELETE | `/chat/project-memo/{memoId}/content-paragraphs/{paragraphId}` |
| FA meta options | `dicOptionsAPI` | GET | `/chat/project-memo/fa-collab/meta/options` |
| FA collab page | `getRecommendInvestorPageAPI` | GET | `/chat/project-memo/fa-collab/page` |
| Create FA collab | `faCollabAddAPI` | POST | `/chat/project-memo/fa-collab` |
| Update FA collab | `faCollabUpdateAPI` | PUT | `/chat/project-memo/fa-collab` |
| Sync FA collab | `faCollabAsyncAPI` | PUT | `/chat/project-memo/fa-collab/sync` |
| Delete FA collab investor | `investorDeleteAPI` | DELETE | `/chat/project-memo/fa-collab/{id}` |
| FA remark page | `remarkPageAPI` | GET | `/chat/project-memo/fa-collab/remark/page` |
| Add FA remark | `remarkAddAPI` | POST | `/chat/project-memo/fa-collab/remark` |
| FA attachment list | `collabAttachmentListAPI` | GET | `/chat/project-memo/fa-collab/attachment/list` |
| Upload FA attachment | `collabUpdateAttachmentListAPI` | POST | `/chat/project-memo/fa-collab/attachment/upload` |
| Delete FA attachment | `collabDeleteAttachmentListAPI` | DELETE | `/chat/project-memo/fa-collab/attachment/{id}` |

## Reports And AI Analysis

| Feature | Function | Method | Path |
|---|---|---:|---|
| Submit second analysis | `submitTaskAPI` | POST | `/chat/analysis/second/submit-task` |
| Second analysis progress | `taskProgressAPI` | GET | `/chat/analysis/second/task-progress` |
| Second analysis results | `allResultTableAPI`, `getTaskListAPI` | GET | `/chat/analysis/second/all-results` |
| Analysis keywords | `keywordsAPI` | GET | `/chat/analysis/keywords` |
| Delete second analysis | `deleteTaskAPI` | POST | `/chat/analysis/second/delete-task` |
| Generate memo report | `submitMemoReportTaskAPI` | POST | `/chat/project-memo/{memoId}/report/generate` |
| Memo report task status | `reportTaskStatusAPI` | GET | `/chat/project-memo/report-task/{taskId}` |
| Memo report task list | `memoReportTaskListAPI` | GET | `/chat/project-memo/{memoId}/report-tasks` |
| Memo report list | `memoReportListAPI` | GET | `/chat/project-memo/{memoId}/reports` |
| Update memo report | `memoReportUpdateAPI` | PUT | `/chat/project-memo/{memoId}/report/{reportId}` |
| Delete memo report | `memoReportDeleteAPI` | DELETE | `/chat/project-memo/{memoId}/report/{reportId}` |
| Generate FA report | `submitFaCollabReportTaskAPI` | POST | `/chat/project-memo/fa-collab/report/generate` |
| FA report task status | `faCollabReportTaskStatusAPI` | GET | `/chat/project-memo/fa-collab/report-task/{taskId}` |
| FA report task list | `faCollabReportTaskListAPI` | GET | `/chat/project-memo/fa-collab/report-tasks` |
| FA report list | `faCollabReportListAPI` | GET | `/chat/project-memo/fa-collab/reports` |
| Update FA report | `faCollabReportUpdateAPI` | PUT | `/chat/project-memo/fa-collab/report/{reportId}` |
| Delete FA report | `faCollabReportDeleteAPI` | DELETE | `/chat/project-memo/fa-collab/report/{reportId}` |

## Investors

| Feature | Function | Method | Path |
|---|---|---:|---|
| Submit parse task | `submitParseTaskAPI` | POST | `/chat/investor/parse-task` |
| Parse task status | `taskStatusAPI` | GET | `/chat/investor/parse-task/{id}` |
| Confirm parse task | `taskStatusConfirmAPI` | POST | `/chat/investor/parse-task/{id}/confirm` |
| Parse task list | `parseTaskListAPI` | GET | `/chat/investor/parse-task/list` |
| Delete parse task | `parseTaskDeleteAPI` | DELETE | `/chat/investor/parse-task/{id}` |
| Upload investor attachment | `attachmentUploadAPI` | POST | `/chat/investor/attachment/upload` |
| Investor attachment list | `attachmentlistAPI` | GET | `/chat/investor/attachment/list` |
| Delete investor attachment | `attachmentDeleteAPI` | DELETE | `/chat/investor/attachment/{id}` |
| Create investor | `investorAddAPI` | POST | `/chat/investor` |
| Update investor | `investorUpdatePI` | PUT | `/chat/investor` |
| Investor list | `investorListAPI` | GET | `/chat/investor/list` |
| Investor detail | `investorDetailAPI` | GET | `/chat/investor/{id}` |
| Delete investor | `investorDeleteAPI` | DELETE | `/chat/investor/{id}` |
| Opinion page | `opinionPageAPI` | GET | `/chat/investor/opinion/page` |
| Create opinion | `opinionCreateAPI` | POST | `/chat/investor/opinion` |
| Update opinion | `opinionUpdateAPI` | PUT | `/chat/investor/opinion` |
| Delete opinion | `opinionDeleteAPI` | DELETE | `/chat/investor/opinion/{id}` |

## Company Member Binding

| Feature | Function | Method | Path |
|---|---|---:|---|
| Like company | `like` | POST | `/chat/company/like` |
| Unlike company | `unlike` | POST | `/chat/company/unlike` |
| Company comment list | `commentList` | GET | `/chat/comment/company/list` |
| Create company comment | `commentCreated` | POST | `/chat/comment/company/create` |
| Agent user options | `agentUsersListAPI` | GET | `/chat/companyMember/agentUsers` |
| Bind agent to company | `bindAgentUserToCompanyAPI` | POST | `/chat/companyMember/register` |
| Bound agent list | `bindingAgentListAPI` | GET | `/chat/companyMember/list` |
| Unbind agent | `deleteAgentUserAPI` | DELETE | `/chat/companyMember/{id}` |
| Update agent identity | `updateAgentUserToCompanyAPI` | POST | `/chat/companyMember/updateIdentity` |

## Industry Insight

Insight paths use `https://v3-api.diggen.cn/insight`.

| Feature | Function | Method | Path |
|---|---|---:|---|
| Event rank | `queryEventRankList` | GET | `/events/rank` |
| Event top rank | `queryEventTopRank` | GET | `/events/topRank` |
| Event detail | `queryEventDetail` | GET | `/events/{id}` |
| Today focus | `queryTodayFocus` | GET | `/events/todayFocus` |
| Event cycle distribution | `queryEventCycleDistribution` | GET | `/events/cycleDistribution` |
| Event trend | `queryEventTrend` | GET | `/events/trend` |
| Leader person rank | `queryLeaderPeopleRankList` | GET | `/persons/rank` |
| Leader person detail | `queryLeaderPeopleDetail` | GET | `/persons/{pid}` |
| Leader person history | `queryLeaderPeopleHistory` | GET | `/persons/history/{pid}` |
| Opinion rank | `queryOpinionsRank` | GET | `/opinions/rank` |
| Opinion summary | `queryOpinionsSummary` | GET | `/opinions/summary` |
| Opinion sentiment distribution | `queryOpinionsDistribution` | GET | `/opinions/sentimentDistribution` |
| Opinion trend | `queryOpinionsTrend` | GET | `/opinions/trend` |
| Opinion detail | `queryOpinionsDetail` | GET | `/opinions/{id}` |

## Admin Accounts

| Feature | Function | Method | Path |
|---|---|---:|---|
| Admin users | `listAdminUsers` | GET | `/chat/admin/users` |
| Admin user detail | `getAdminUser` | GET | `/chat/admin/users/{id}` |
| Create admin user | `createAdminUser` | POST | `/chat/admin/users` |
| Update admin user | `updateAdminUser` | PUT | `/chat/admin/users/{id}` |
| Reset admin password | `resetAdminUserPassword` | PUT | `/chat/admin/users/{id}/password` |
| Update admin status | `updateAdminUserStatus` | PUT | `/chat/admin/users/{id}/status` |
| Update admin expiry helper (not used by current Admin Accounts page; current page sends `accountValidUntil` in create/update) | `updateAdminUserExpiry` | PUT | `/chat/admin/users/{id}/expiry` |
| Delete admin user | `deleteAdminUser` | DELETE | `/chat/admin/users/{id}` |
| Account types | `listAccountTypes` | GET | `/chat/admin/account-types` |
| Account type options | `accountTypeOptions` | GET | `/chat/admin/account-types/options` |
| Create account type | `createAccountType` | POST | `/chat/admin/account-types` |
| Update account type | `updateAccountType` | PUT | `/chat/admin/account-types/{id}` |
| Update account type status | `updateAccountTypeStatus` | PUT | `/chat/admin/account-types/{id}/status` |
| Delete account type | `deleteAccountType` | DELETE | `/chat/admin/account-types/{id}` |

## System Bootstrap

These are imported by global app bootstrap/store code, not by DigClaw business pages.

| Feature | Function | Method | Path |
|---|---|---:|---|
| Runtime config key | `getConfigKey` | GET | `/system/config/configKey/{key}` |
| Dict type values | `getDicts` | GET | `/system/dict/data/type/{dictType}` |
| Routers | `getRouters` | GET | `/getRouters` |
