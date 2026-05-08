#!/bin/bash


LOG_FILE="mcp-proxy.log"
echo "Starting MCP Proxy..."
uvx mcp-proxy --named-server-config config.json --host 0.0.0.0 --allow-origin "*" --port 8001 --stateless 2>&1 | tee -a "${LOG_FILE}"