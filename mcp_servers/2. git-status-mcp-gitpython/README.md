# Git MCP Server

A simple Model Context Protocol (MCP) server that provides Git repository information to Claude and other MCP clients.

## What This Does

This MCP server allows Claude (or any MCP client) to:
- Check the status of a Git repository (modified, staged, and untracked files)
- View recent commit history

## Prerequisites

Before you start, make sure you have:

1. **Python 3.10 or higher** installed on your computer
   - Check by running: `python --version` or `python3 --version`
   - Download from: https://www.python.org/downloads/

2. **Git** installed on your computer
   - Check by running: `git --version`
   - Download from: https://git-scm.com/downloads

## Installation

### Step 1: Clone or Download This Repository

```bash
git clone <your-repository-url>
cd MCP_Servers
```

### Step 2: Install Required Python Packages

This server needs two Python libraries:

```bash
pip install mcp gitpython
```

Or if you're using Python 3:

```bash
pip3 install mcp gitpython
```

### Step 3: Configure Claude Desktop

To use this server with Claude Desktop, you need to add it to Claude's configuration file.

#### On Windows:

1. Open the configuration file located at:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
   
2. Add this configuration (replace `<path-to-your-server>` with the actual path):

```json
{
  "mcpServers": {
    "git-status": {
      "command": "python",
      "args": [
        "C:\\Users\\YourUsername\\Documents\\GitHub\\MCP_Servers\\git_status_server.py"
      ]
    }
  }
}
```

#### On macOS/Linux:

1. Open the configuration file located at:
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. Add this configuration:

```json
{
  "mcpServers": {
    "git-status": {
      "command": "python3",
      "args": [
        "/absolute/path/to/MCP_Servers/git_status_server.py"
      ]
    }
  }
}
```

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop for the changes to take effect.

## How to Use

Once configured, you can ask Claude to check Git repositories. For example:

- "Check the status of my repository at C:\Users\YourName\Projects\MyRepo"
- "Show me the last 5 commits in /home/user/my-project"
- "What files have changed in my repository?"

## Available Tools

### `git_status`
Shows the current status of a Git repository including:
- Current branch name
- Staged files (ready to commit)
- Modified files (not yet staged)
- Untracked files (new files not added to git)

**Example:**
```
Current branch: main
Modified files: 2
Untracked files: 1
```

### `git_log`
Shows recent commit history with:
- Commit hash (short version)
- Commit message

**Example:**
```
2414d32 Add a Read Me for basic Git MCP
a1b2c3d Fix bug in status display
```

## Troubleshooting

### "GitPython not installed" Error
Run: `pip install gitpython`

### "Not a git repository" Error
Make sure the path you provide points to a folder that contains a `.git` directory (i.e., a folder initialized with `git init`).

### Server Not Showing in Claude
1. Check that the path in `claude_desktop_config.json` is correct and absolute (full path)
2. Make sure you restarted Claude Desktop after editing the config
3. Check the Claude Desktop logs for errors

### Permission Denied Error (macOS/Linux)
Make the server executable:
```bash
chmod +x git_status_server.py
```

## How It Works

This server uses:
- **MCP (Model Context Protocol)**: A standard for connecting AI assistants to external tools
- **GitPython**: A Python library that interacts with Git repositories
- **asyncio**: For handling asynchronous operations

When Claude needs Git information, it calls this server, which reads the repository and returns the requested data.

## Contributing

Feel free to:
- Report issues
- Suggest new Git commands to support
- Submit pull requests with improvements


## Support

If you encounter any issues or have questions, please open an issue on GitHub.

This ReadMe doc is polished with help of GenAI Companions.