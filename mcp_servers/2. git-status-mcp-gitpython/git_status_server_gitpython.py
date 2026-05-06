#!/usr/bin/env python3

"""
Above Line defines where the interpreter (python3) is located.
For Windows, it is not natively supported
"""

"""
This MCP Server is built to support basic Git functions using GitPython library
which Supports:
- git_status
- git_log
- 
- 
"""

import asyncio #Asynchronous I/O, allows other tasks to run while waiting for I/O
import os #Operating System
from typing import Any #Avoid Type Checking and allow any type to be used

from mcp.server import Server #Importing Server Class from MCP
from mcp.server.stdio import stdio_server #Application Act as Server using Std I/O
from mcp.types import Tool, TextContent, CallToolResult 

try:
    from git import Repo, InvalidGitRepositoryError
except ImportError:
    raise ImportError("GitPython not installed. Run: pip install gitpython")


#Initializing a Server named gitpython-mcp
app = Server("gitpython-mcp")


# ----------------------------
# Tools
# ----------------------------

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="git_status",
            description="Show git status (modified, staged, untracked files)",
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
        ),
        Tool(
            name="git_log",
            description="Show recent git commits",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Absolute path to a git repository"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of commits",
                        "default": 5
                    }
                },
                "required": ["repo_path"]
            }
        )
    ]


# ----------------------------
# Tool execution
# ----------------------------

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> CallToolResult:
    arguments = arguments or {}
    repo_path = os.path.abspath(arguments.get("repo_path", ""))

    if not repo_path or not os.path.isdir(repo_path):
        return error("Invalid repo_path")

    try:
        if name == "git_status":
            text = await get_status(repo_path)
        elif name == "git_log":
            limit = int(arguments.get("limit", 5))
            limit = max(1, min(limit, 20))
            text = await get_log(repo_path, limit)
        else:
            return error(f"Unknown tool: {name}")

        return CallToolResult(
            content=[TextContent(type="text", text=text)]
        )

    except InvalidGitRepositoryError:
        return error(f"Not a git repository: {repo_path}")
    except Exception as e:
        return error(f"Error: {str(e)}")


def error(msg: str) -> CallToolResult:
    return CallToolResult(
        content=[TextContent(type="text", text=msg)],
        isError=True
    )


# ----------------------------
# Git operations using GitPython
# ----------------------------

async def get_status(repo_path: str) -> str:
    """Get git status using GitPython"""
    def _get_status():
        repo = Repo(repo_path)
        
        # Get current branch
        try:
            branch = repo.active_branch.name
        except:
            branch = "HEAD (detached)"
        
        lines = [f"## {branch}"]
        
        # Changed files (modified, added, deleted)
        changed = repo.index.diff(None)  # Working directory vs index
        staged = repo.index.diff("HEAD")  # Index vs HEAD
        
        # Staged files
        for item in staged:
            if item.deleted_file:
                lines.append(f"D  {item.a_path}")
            elif item.new_file:
                lines.append(f"A  {item.a_path}")
            else:
                lines.append(f"M  {item.a_path}")
        
        # Modified but not staged
        for item in changed:
            if item.deleted_file:
                lines.append(f" D {item.a_path}")
            else:
                lines.append(f" M {item.a_path}")
        
        # Untracked files
        untracked = repo.untracked_files
        for file in untracked:
            lines.append(f"?? {file}")
        
        if len(lines) == 1:
            lines.append("(clean working directory)")
        
        return "\n".join(lines)
    
    return await asyncio.to_thread(_get_status)


async def get_log(repo_path: str, limit: int) -> str:
    """Get git log using GitPython"""
    def _get_log():
        repo = Repo(repo_path)
        commits = list(repo.iter_commits(max_count=limit))
        
        if not commits:
            return "(no commits)"
        
        lines = []
        for commit in commits:
            short_hash = commit.hexsha[:7]
            message = commit.message.split('\n')[0]  # First line only
            lines.append(f"{short_hash} {message}")
        
        return "\n".join(lines)
    
    return await asyncio.to_thread(_get_log)


# ----------------------------
# Entrypoint
# ----------------------------

async def main():
    async with stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())