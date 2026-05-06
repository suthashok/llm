# Minimal Filesystem-Based Git MCP Server

> A beginner-friendly introduction to writing an MCP (Model Context Protocol) server — **without invoking Git binaries or subprocesses**.

---

## Why this project exists

If you are new to MCP, it is very tempting to start by building a *"real"* tool — for example, a Git MCP server that runs commands like `git status` or `git log`.

In practice, this quickly becomes frustrating:

* MCP servers do **not** run in your terminal context
* Relative paths like `.` are unreliable
* On Windows, `git` + `subprocess` + `stdio` can hang silently
* You end up debugging OS behavior instead of learning MCP

This repository exists to **remove those distractions**.

It gives you a **minimal, reliable MCP server** that:

* Always responds
* Demonstrates the MCP lifecycle clearly
* Uses Git repositories *only as a filesystem concept*
* Is safe for beginners on Windows, macOS, and Linux

---

## What this project is

✅ A minimal MCP server written in Python

✅ Uses filesystem inspection to detect Git repositories (`.git` directory)

✅ Demonstrates:

* Tool discovery (`list_tools`)
* Tool execution (`call_tool`)
* Returning structured MCP responses

✅ Designed to be read, modified, and extended by beginners

---

## What this project is NOT

❌ This is **not** a full Git MCP server

❌ It does **not** run:

* `git status`
* `git log`
* `git diff`

❌ It does **not** invoke:

* Git binaries
* Shell commands
* Subprocesses

❌ It does **not** support remote repositories

This is intentional.

---

## Why filesystem-based Git detection?

A Git repository is, at its core, just a directory containing a `.git` folder.

By checking:

```
<repo_path>/.git
```

we can reliably determine whether a path is a Git repository **without**:

* depending on Git being installed
* worrying about pagers or prompts
* dealing with OS-specific subprocess behavior

This makes the MCP behavior:

* deterministic
* fast
* beginner-safe

---

## How MCP works (plain English)

An MCP server:

1. Starts as a background process
2. Advertises the tools it supports
3. Receives tool execution requests
4. Returns structured responses

Unlike CLI tools:

* There is **no current directory** you can rely on
* There is **no interactive terminal**
* All context must be passed explicitly

This project is designed to teach exactly that mental model.

---

## The provided tool

### `git_status`

**What it does:**

* Accepts an absolute path to a directory
* Checks if `.git` exists
* Returns basic repository information

**What it proves:**

* MCP tool invocation works
* Arguments are passed correctly
* Responses are rendered by the client

### Example MCP call

```json
{
  "name": "git_status",
  "arguments": {
    "repo_path": "C:\\path\\to\\your\\repo"
  }
}
```

---

## Common beginner traps (learned the hard way)

This project intentionally avoids the following traps:

### 1. Using `.` as a default path

In MCP:

* `.` does **not** mean "your project"
* It means "wherever the server process started"

Always pass absolute paths.

---

### 2. Calling external commands too early

Subprocesses introduce:

* OS-specific behavior
* Silent hangs
* Hard-to-debug failures

Learn MCP first. Add subprocesses later.

---

### 3. Mixing too many concepts at once

MCP + async Python + Git + Windows quirks is **too much** for a first project.

This repo keeps the scope intentionally small.

---

## Where to go next

Once you are comfortable with this server, you can:

* Add real Git commands using `gitmcp`
* Run MCP servers inside WSL
* Use socket-based transports instead of stdio
* Experiment with non-Git tools first

This repository is meant to be a **starting point**, not a destination.

---

## Who this is for

* Beginners learning MCP
* Developers frustrated by hanging Git MCP examples
* Anyone who wants to understand MCP *before* optimizing functionality

---

## Final note

If this repository saves you even a few hours of confusion — it has done its job.

Clarity beats cleverness.
