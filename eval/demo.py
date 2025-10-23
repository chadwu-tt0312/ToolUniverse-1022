# 1. Install ToolUniverse
# pip install tooluniverse

# 2. Load tooluniverse
from tooluniverse import ToolUniverse

tu = ToolUniverse()
tu.load_tools()  # Load 600+ scientific tools

# Your AI scientist can reason, experiment, and collaborate in discovery using the AI-tool interaction protocol.

# 3. Use Find Tool operation to discover relevant tools
tools = tu.run(
    {
        "name": "Tool_Finder_Keyword",
        "arguments": {"description": "disease target associations", "limit": 10},
    }
)
print(tools)
print("----")

# 4. Use Call Tool operation to execute selected tool
result = tu.run(
    {
        "name": "OpenTargets_get_associated_targets_by_disease_efoId",
        "arguments": {"efoId": "EFO_0000537"},  # hypertension
    }
)
print(result)

# python demo.py
