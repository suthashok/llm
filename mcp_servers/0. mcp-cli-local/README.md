# Local MCP Client (CLI + Ollama)

A fully local, open-source **MCP (Model Context Protocol) client** that uses **Ollama-hosted LLMs** instead of cloud models.

This project explores how tools, MCP servers, and LLM reasoning actually work under the hood — with the goal of replacing **Claude Desktop** for local automation.

---

## Why This Project Exists

Claude Desktop makes MCP feel “magical”, but that magic hides a lot of important details:

- How does the model decide to call a tool?
- What happens when tools are missing?
- How does intent routing actually work?
- Can this be done **locally**, with open models?

This project answers those questions by building a minimal, transparent MCP client from scratch.

---

## What This Is

- A **CLI-based MCP client**
- Uses **local LLMs via Ollama**
- Talks to **MCP tool servers** (filesystem, git, etc.)
- Deterministic, debuggable, and vendor-free

## What This Is NOT

- ❌ A VS Code extension
- ❌ A coding assistant
- ❌ A GUI app (for now)
- ❌ Cloud-dependent

---

## Architecture Overview

```
User (CLI)
  ↓
Local MCP Client (Node.js)
  ↓
Local LLM (Ollama)
  ↓
MCP Tool Servers (filesystem, git, etc.)
  ↓
Results back to CLI
```

---

## Current Features

### MCP Client
- CLI-based interaction loop
- Strict system prompt with intent gating
- Deterministic tool invocation
- Stage-based logging for visibility

### LLM Integration
- Ollama-based local inference
- Tested with:
  - `qwen2.5:3b-instruct`
  - `phi3:mini`
- Streaming-safe response parsing
- Explicit JSON tool-call contract

### MCP Tools
- Filesystem tools:
  - `get_cwd`
  - `list_directory`
  - `read_file`
  - `write_file`

---

## Tool Calling Model

The LLM operates internally in two modes:

- **Chat Mode** – plain text
- **Tool Mode** – strict JSON only

Example tool call:

```json
{
  "tool": "get_cwd",
  "arguments": {}
}
```

---

## Lessons Learned So Far

- Prompt hardening is mandatory for local models
- Small models need explicit intent examples
- Missing tools cause refusal or hallucination
- Silence during inference ≠ hang (especially on CPU)
- Claude Desktop’s “magic” is mostly **control logic**

---

## Current Status

✅ Local MCP client  
✅ Ollama integration  
✅ Intent → tool routing  
✅ Filesystem MCP tools  
✅ Deterministic behavior  

🚧 Tool result → LLM feedback loop  
🚧 Git MCP integration  
🚧 Security sandboxing  
🚧 Streaming UX improvements  

---

## Requirements

- Node.js (v18+)
- Python 3.x
- Ollama
- Local model (e.g. `qwen2.5:3b-instruct`)

---

## Running the Project

```bash
ollama serve
ollama pull qwen2.5:3b-instruct
node index.js
```

---

## Why This Matters

This project demonstrates that:

- MCP is **LLM-agnostic**
- Local automation is practical today
- Claude Desktop can be replicated architecturally
- The hard part is **control**, not intelligence

---

## License

MIT (planned)

---

## Notes

This is an exploration-first project.
Expect rough edges, deliberate constraints, and lots of learning.
