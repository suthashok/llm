# MCP Local Sandbox with LLM Integration

This repository provides a **safe, sandboxed environment** for running Local LLM commands (currently using `llama3:8b-instruct-q4_K_M` via Ollama SDK v0.6.1) for **filesystem and automation tasks**, without risking critical system files.

It’s designed for developers, testers, or team members who want to experiment with **MCP (Managed Code/Content Processing) operations** safely and efficiently.

---

## 🛠 Features

- **Sandboxed filesystem operations**: Read, write, and list files in a designated folder.
    
- **Security**: All operations are restricted to allowed paths to prevent accidental system changes.
    
- **LLM-driven command generation**: The LLM generates commands like `write file`, `read file`, and `list folder` which are automatically cleaned and executed.
    
- **Ollama SDK v0.6.1 compatible**: Uses local `llama3:8b-instruct-q4_K_M` model and handles paths with spaces and special characters.
    
- **Extensible**: Ready to integrate **Git commands** (`clone`, `commit`, `push`) or cloud operations.
    

---

## 📂 Folder Structure

Plaintext

```
MCP_Servers/
├── main.py          # Main session script (LLM → tool_router)
├── tools/
│   ├── __init__.py
│   └── fs_tools.py  # Safe filesystem operations
├── config/
│   └── config.py    # Configurable paths, settings
├── test/
│   └── temp/        # Sandbox folder for testing commands
└── README.md
```

---

## ⚡ Quick Start

### 1. Install Dependencies

Bash

```
pip install ollama
```

_Ensure Ollama Desktop is installed with the `llama3:8b-instruct-q4_K_M` model downloaded._

### 2. Configure Allowed Paths

Edit `tools/fs_tools.py`:

Python

```
from pathlib import Path

ALLOWED_PATHS = [
    Path(r"C:\path\to\MCP_Servers\test\temp").resolve()
]
```

_All read/write operations will be restricted to these paths._

### 3. Run the Main Session

Bash

```
python main.py
```

---

## 🔍 Expected Behavior & Output

The LLM will generate a write command, read back the content, and list the files in the sandbox.

**Example Output:**

- **LLM Command**: `write file "C:\MCP_Servers\test\temp\LLM File.txt" "Hello from LLM in sandbox"`
    
- **Result**: Wrote to `C:\MCP_Servers\test\temp\LLM File.txt`
    
- **Read Result**: `Hello from LLM in sandbox`
    

---

## 📝 Best Practices

- Always run commands inside the sandbox folder.
    
- Use quotes for paths with spaces.
    
- **LLM Instruction**: _"Do not remove or change any spaces or characters in folder/file names."_
    

---

## 🔧 Next Steps

- Integrate Git operations: `clone`, `branch`, `commit`, `push`.
    
- Add cloud drive support: Google Drive, OneDrive.
    
- Multi-step MCP pipelines for automation.
    

---

## 📌 References

- [Ollama Docs](https://ollama.ai/)
    
- Python 3.9+ (`pathlib.Path.is_relative_to` used)
    
- Safe file handling with `resolve()` and restricted paths
    

This is In-progress item and being developed.