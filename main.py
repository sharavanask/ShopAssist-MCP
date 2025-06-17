#!/usr/bin/env python3
"""
Amazon Product Search MCP Server
Main entry point for the MCP server.
"""

import asyncio
from server.buy import mcp

def main():
    """Run the MCP server."""
    print("🚀 Starting Amazon Product Search MCP Server...")
    print("Available tools:", [tool.name for tool in mcp.tools])
    mcp.run()

if __name__ == "__main__":
    main()
