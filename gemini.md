# Gemini AI Guidelines - Facebook Ads MCP Server

This file contains strictly enforced rules for any AI agent (like Gemini CLI) interacting with this codebase. These rules are designed to prevent accidental over-writes, logic bypasses, or safety violations.

## 🛡️ Code Integrity & Safety

1.  **Do Not Overwrite Error Handling**: The error handling logic in `server.py` (specifically within `_make_graph_api_call`) must NEVER be simplified or reverted to generic HTTP error reporting. It is designed to extract specific Facebook API error details for better debugging.
2.  **No Tool Bypassing**: Always use the defined MCP tools (e.g., `list_ad_accounts`, `get_ad_insights`) to access data. Do not create temporary scripts that perform direct API calls unless user explicitly requested for one-time debugging.
3.  **Strict Pagination**: All tools that fetch collections must follow the established `paging.next` pattern. Never return truncated results without a clear pagination path.

## 🔑 Security & Credentials

1.  **Never Hardcode Tokens**: AI agents must never write or suggest code that hardcodes Facebook Access Tokens.
2.  **Follow Credential Patterns**: Always use the established patterns for token access:
    - `--fb-token` command-line argument.
    - `FB_ACCESS_TOKEN` environment variable.
    - `.env` file (if applicable and safe).

## 🛠️ Development Practices

1.  **Concise Communication**: When announcing actions, be brief (e.g., "Finding tools to see which is suitable"). 
2.  **Preserve Helper Functions**: Helper functions like `_prepare_params` and `_fetch_edge` are core to the server's stability and should be respected when adding new tools.

