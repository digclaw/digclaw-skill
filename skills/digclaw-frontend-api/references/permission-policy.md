# DigClaw Frontend Permission Policy

Agents must not bypass frontend account restrictions. Before calling a page business API, check the current account's frontend-visible capability for that page. If permission data is missing, stale, or does not allow the page, stop and explain that the current account cannot use that page.

## Permission Sources

The frontend bootstraps permissions after login with:

- `GET /chat/user/info`
- `GET /chat/user/permission`

Use the same token and headers as normal authenticated calls. The relevant fields are:

- `accountType`
- `permissionLevel`
- `accessibleFunctions`

Effective functions are `accessibleFunctions`, plus `Account Administration` when `accountType === "MASTER"`. This mirrors `src/views/home.vue`.

## Required Check

Run the helper before page-level operations:

```powershell
python scripts\check_permission.py --page smart-search
```

The helper prints JSON. Continue only when `allowed` is `true`. A denied check exits with code `2` unless `--soft` is used.

## Page Rules

| Page or feature | Helper page key | Required frontend permission |
|---|---|---|
| App shell, profile, settings, conversations | `shell` | authenticated user context |
| Smart Search page | `smart-search` | `Smart Search` |
| Smart Search company search | `smart-search.company-search` | `Smart Search` and `Company Search` |
| Smart Search curated list | `smart-search.curated-list` | `Smart Search` and `View Curated List` |
| Talent Matrix | `talent-matrix` | `Talent Matrix` |
| Project Connectivity | `project-connectivity` | `Project Connectivity` |
| Venture Investment Directory | `venture-directory` | `Venture Investment Directory` |
| Industry Analysis | `industry-analysis` | `Industry Analysis` |
| Account Administration | `admin-accounts` | `accountType === "MASTER"` or `Account Administration` |
| Hidden file management | `file-management` | `permissionLevel === 3` or `permissionLevel === 5` |
| Hidden standalone AI Analysis | `standalone-ai-analysis` | `permissionLevel === 3` |
| Hidden AI Sourcing / selected company list | `ai-sourcing` | `permissionLevel !== 0`; use only on explicit request because the menu is commented/hidden |

## Enforcement Rules

- Deny by default for unknown pages, missing token, failed permission calls, or missing required functions.
- Do not call backend APIs just because the backend accepts them. The frontend permission model is the authority for this skill.
- Re-check permissions after login, account switching, or token changes.
- For multi-step workflows, one page-level check is enough unless the workflow crosses into another page or a Smart Search subfeature.
- For Smart Search, check both the page and the specific subfeature when the action uses company search or curated-list APIs.
