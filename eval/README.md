# Clone the repository
git clone <https://github.com/mims-harvard/ToolUniverse.git>

# Add all dependencies
uv sync

# 安裝額外功能

# Development tools (uv - recommended)
uv add "tooluniverse[dev]" --dev

# Embedding functionality (uv - recommended)
uv add "tooluniverse[embedding]" --dev

# All optional dependencies (uv - recommended)
uv add "tooluniverse[all]" --dev

```python
import tooluniverse
print(f"ToolUniverse version: {tooluniverse.__version__}")
print("✅ Installation successful!")
```

# Test MCP server
tooluniverse-mcp --help

# Start MCP server
python -m tooluniverse.smcp_server

### commonly used command-line flags for ToolUniverse MCP servers

```bash
tooluniverse-smcp [OPTIONS]

--port INT                     Server port (HTTP/SSE). Default: 7000
--host TEXT                    Bind host for HTTP/SSE. Default: 0.0.0.0
--transport [http|stdio|sse]   Transport protocol. Default: http
--name TEXT                    Server display name
--max-workers INT              Worker pool size for tool execution
--verbose                      Enable verbose logs

# Tool selection
--categories STR...            Include only these categories
--exclude-categories STR...    Exclude these categories
--include-tools STR...         Include only these tool names
--tools-file PATH              File with one tool name per line
--include-tool-types STR...    Include only these tool types
--exclude-tool-types STR...    Exclude these tool types
--tool-config-files TEXT       Mapping like "custom:/path/to/custom.json"

# Hooks
--hooks-enabled                Enable hooks (default: False)
--hook-type [SummarizationHook|FileSaveHook]
--hook-config-file PATH        JSON config for hooks

# ----------- stdio ---------------------------
tooluniverse-smcp-stdio [OPTIONS]

--name TEXT                    Server display name
--categories STR...            Include only these categories
--include-tools STR...         Include only these tool names
--tools-file PATH              File with one tool name per line
--include-tool-types STR...    Include only these tool types
--exclude-tool-types STR...    Exclude these tool types
--hooks                        Enable hooks (default: disabled for stdio)
--hook-type [SummarizationHook|FileSaveHook]
--hook-config-file PATH        JSON config for hooks
```

```json
{
  "mcpServers": {
    "tooluniverse": {
      "command": "tooluniverse-smcp-stdio",
      "args": ["--categories", "uniprot", "ChEMBL", "opentarget", "--hooks", "--hook-type", "SummarizationHook"]
    }
  }
}
```
