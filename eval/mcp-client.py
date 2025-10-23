import requests

# Discover tools
tools = requests.get("http://127.0.0.1:8000/mcp/tools").json()

# Execute a tool
payload = {"name": "UniProt_get_entry_by_accession", "arguments": {"accession": "P04637"}}
result = requests.post("http://127.0.0.1:8000/mcp/run", json=payload).json()
print(result)
