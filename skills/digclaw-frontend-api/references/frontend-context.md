# DigClaw Frontend Context

## Source Of Truth

This skill was derived from `diggenai_web`, a Vue 2 + Element UI frontend. The API surface is intentionally limited to functions imported by current pages/components or global stores.

Do not copy all backend controllers into this skill. Missing endpoints may be historical, backend-only, or unused.

## Environment

Production:

- `VUE_APP_BASE_API = https://v3-api.diggen.cn`
- `VUE_APP_INSIGHT_BASE_API = https://v3-api.diggen.cn/insight`
- `VUE_APP_BASE_CLIENTID = b7bf1120a216184a9e0f4ca0e9c508bb`

Development/staging:

- `VUE_APP_BASE_API = /chat`
- `VUE_APP_INSIGHT_BASE_API = /insight`
- Vue dev proxy sends both prefixes to `http://localhost:8813` and rewrites the prefix away.

Because production `VUE_APP_BASE_API` is already the host root, chat endpoints keep their `/chat/...` prefix. For example:

`favoriteListAPI` path `/chat/talents/v2/favorite/list` becomes `https://v3-api.diggen.cn/chat/talents/v2/favorite/list`.

Insight endpoints use `VUE_APP_INSIGHT_BASE_API`, so `/events/rank` becomes `https://v3-api.diggen.cn/insight/events/rank`.

## Request Wrapper

All normal calls go through `src/utils/request.js`.

- Default `Content-Type`: `application/json;charset=utf-8`
- Adds `clientid` from `VUE_APP_BASE_CLIENTID`
- Adds `Authorization: Bearer <access_token>` when local storage contains `access_token`
- GET `params` are serialized into the query string
- POST/PUT bodies use `data` unless the wrapper function explicitly uses `params`
- Default timeout is 60 seconds; selected long-running search/upload calls set longer timeouts
- Response success is application `code === 200`; `401` clears login state

## Install From GitHub

After this repository is pushed, install with:

```powershell
python C:\Users\HJD\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --repo digclaw/digclaw-skill --path skills/digclaw-frontend-api
```

Restart Codex after installation so the skill is discovered.
