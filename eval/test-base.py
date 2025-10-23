from tooluniverse import ToolUniverse

# Initialize and test
tu = ToolUniverse()
tu.load_tools()
print(f"✅ Loaded {len(tu.all_tools)} tools successfully!")
