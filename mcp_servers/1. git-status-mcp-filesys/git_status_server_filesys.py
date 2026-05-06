#!/usr/bin/env python3
"""
Ultra-minimal Git MCP Server (no subprocess, no git binary)
"""

import asyncio
import os
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult

app = Server("git-status-mcp-min")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="git_status",
            description="Minimal git status check (filesystem-based)",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Absolute path to a git repository"
                    }
                },
                "required": ["repo_path"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> CallToolResult:
    arguments = arguments or {}

    if name != "git_status":
        return CallToolResult(
            content=[TextContent(type="text", text="Unknown tool")],
            isError=True
        )

    repo_path = os.path.abspath(arguments["repo_path"])

    if not os.path.isdir(repo_path):
        return CallToolResult(
            content=[TextContent(type="text", text="Path does not exist")],
            isError=True
        )

    git_dir = os.path.join(repo_path, ".git")

    if not os.path.isdir(git_dir):
        return CallToolResult(
            content=[TextContent(type="text", text="Not a git repository")],
            isError=True
        )

    # Minimal, guaranteed output
    files = os.listdir(repo_path)

    text = (
        f"Repository: {repo_path}\n"
        f".git directory found\n"
        f"Files at root:\n" +
        "\n".join(files[:20])
    )

    return CallToolResult(
        content=[TextContent(type="text", text=text)]
    )


async def main():
    async with stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
