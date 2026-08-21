# Page Module: AI 对话搜索

Source: `Home/AgentSearchWorkspace.vue`, `src/api/agentSearch.js`, and helper modules under `src/views/Home/agentSearch*.js`.

Permission gate: `agent-conversation-search`. Access requires `AI Conversation Search` in `accessibleFunctions`.

## Responsibilities

- Conversational company or talent search with automatic or explicit search-path selection.
- Streamed agent turns, progress/status events, ambiguity choices, keyword selection, and continuation from a previous turn.
- Conversation history list/detail/delete.
- Candidate pagination, AI check, web enrichment, profile/detail expansion, and CSV export from the visible candidate list.

## Adaptive Search Guidance

For company or talent discovery, proactively derive alternate keywords from the request and use the turn interaction/continuation flow to try them. Expand with synonyms, abbreviations, bilingual terms, adjacent domains, company/product categories, role titles, skills, organizations, and locations while preserving hard constraints. Evaluate candidate relevance after each turn. If candidates are insufficient, submit materially different keyword choices or continuation turns and request later candidate pages. Deduplicate by candidate type and stable ID. Stop when coverage is adequate or further turns/pages are repetitive or low-value.

## Initial Load

1. Check `agent-conversation-search` permission.
2. The page lists saved conversations with `GET /chat/agent-search/conversations`.
3. The left history panel can load or delete a conversation.

## Main Operations

### Start Or Continue A Search Turn

The preferred frontend path is streamed:

`POST /chat/agent-search/turn/stream`

The request is sent with normal DigClaw headers plus JSON body. Common fields include:

| Field | Notes |
|---|---|
| `message` / user text | User search request. |
| `conversationId` | Existing conversation id, or null/empty for a new conversation. |
| `targetType` / `searchPath` | `company`, `talent`, or omitted for automatic recognition. |
| `baseTurnReference` | Optional previous turn reference when continuing from a historical result set. |
| `interaction` | Response to ambiguity or keyword-selection prompts. |
| `page` / pagination fields | Used when loading additional candidates. |

The stream emits JSON events that update status, prompt for interaction, or return final turn results. If streaming fails, the page falls back to:

`POST /chat/agent-search/turn`

### Conversation History

| Operation | API |
|---|---|
| Create conversation | `POST /chat/agent-search/conversations` |
| List conversations | `GET /chat/agent-search/conversations` |
| Load conversation detail | `GET /chat/agent-search/conversations/{id}` |
| Delete conversation | `DELETE /chat/agent-search/conversations/{id}` |

Loaded conversation details hydrate messages, latest turn, current path, candidates, pagination state, and historical turn cards.

### Candidate Enrichment And Export

- Web/profile enrichment uses `POST /chat/agent-search/candidate-web-enrichment`.
- CSV export is local frontend behavior from the current visible candidate list; there is no backend export endpoint for this page.
- Candidate rows may represent either company or talent records. Preserve `type`, `id`, display fields, score/check fields, profile links, and detail payloads when summarizing or exporting.

## Operation Notes

- Do not bypass the interaction prompts: if a turn returns ambiguity choices or keyword-selection requirements, submit the user's selected choices in the next turn payload.
- AI check can run until enough qualified candidates are found. The frontend keeps rejected/checked state attached to candidates and may request more pages as needed.
- A completed turn with weak candidates should trigger alternate keyword expansion or additional candidate pages rather than immediate completion.
- Search path switching is limited once a conversation has active results; start a new conversation for a different independent search path.
