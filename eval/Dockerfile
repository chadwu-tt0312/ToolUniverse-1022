FROM python:3.10-slim
# FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

RUN apt-get update && apt-get install -y libxrender1 libxext6 libx11-6 libexpat1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install tooluniverse

# RUN uv init
# RUN uv add tooluniverse

# CMD ["python", "-m", "tooluniverse.smcp_server"]
CMD ["tooluniverse-mcp", "--host", "0.0.0.0", "--port", "7000"]
