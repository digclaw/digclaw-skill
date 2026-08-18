# Page Module: Rhizome Agent

Source: `Home/RhizomeAgent.vue`.

Permission gate: `rhizome-agent`. Access requires `Rhizome Agent` in `accessibleFunctions`. `MASTER` receives this function in the default backend account-type template, and other account types can receive it through Account Administration.

## Responsibilities

- DigClaw-native page for running the deployed Rhizome agent at `VUE_APP_RHIZOME_AGENT_URL` or `https://rhizome.diggen.cn/`.
- Health check, optional file upload, task submission, streamed execution logs, and final answer display.
- The page is not an iframe. It calls Rhizome API endpoints directly from the frontend, so Rhizome UI style changes do not change the DigClaw page.

## Rhizome API Base

Default base URL:

```text
https://rhizome.diggen.cn/
```

The frontend constructs absolute API URLs from that base.

## Initial Load

1. Check `rhizome-agent` permission.
2. `GET {rhizomeBase}/api/health`.
3. If `default_config` matches one of the frontend workflow options, select it.

## Workflow Options

| Frontend label | `config_file_name` |
|---|---|
| 联网搜索 | `agent_qwen_web_search` |
| 附件 / 网页读取 | `agent_qwen_web` |
| 多智能体分析 | `agent_qwen_multi` |
| Claude 文件读取 | `agent_quickstart_reading` |

## Upload

`POST {rhizomeBase}/api/files`

Multipart form field:

| Field | Notes |
|---|---|
| `file` | Selected user file. Rhizome currently reports max upload size in `/api/health`; observed default is 100MB. |

Response fields used by the frontend:

| Field | Notes |
|---|---|
| `filename` | Display name. |
| `task_file_name` | Value to pass into the research request. |
| `size_bytes` | Optional display/debug info. |

## Run Task

Preferred endpoint:

`POST {rhizomeBase}/api/research/stream`

Body:

```json
{
  "task": "请先联网搜索最新资料，再分析未来一个月显卡价格走势，并给出主要依据和结论。",
  "config_file_name": "agent_qwen_web_search",
  "task_file_name": "optional uploaded task file name",
  "task_id": "digclaw_1720000000000",
  "timeout_seconds": 900
}
```

Stream handling:

- `type: "start"`: mark task started.
- `type: "log"` with `content`: append to the scrollable execution stream.
- `type: "error"` with `message`: show error and final answer text.
- `type: "result"`: use `boxed_answer` when present; otherwise show completion/failure message.
- `data: [DONE]`: stream end marker.

## UI Behavior Notes

- Rhizome Agent uses normal sidebar width. The AI Conversation Search auto-collapse behavior does not apply to `activeMenu === 15`.
- The page hides the Rhizome service address in normal UI.
- Streamed logs are contained in a fixed-height scrollable event container so long runs do not stretch the page.
- The "原页面" action opens the external Rhizome URL in a new tab.
