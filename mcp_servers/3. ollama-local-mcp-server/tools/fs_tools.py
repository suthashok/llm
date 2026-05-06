import os
from pathlib import Path


#---------------------------------------------
#Define which folders the MCP agent can access
#---------------------------------------------


ALLOWED_PATHS=[
                Path(r"C:\Users\Ashok Suthar\Documents\GitHub\MCP_Servers\3. ollama-local-mcp-server\test\temp").resolve()
            ]

#------------------------------------------------
# Check for Allowed Path
#-----------------------------------------------

def _is_allowed(path_to_check: str) -> bool:
    """This function checks whether the path tool is trying to access is allowed or not."""

    try:
        target=Path(path_to_check).resolve()

        for allowed_path in ALLOWED_PATHS:
            if target.is_relative_to(allowed_path):
                return True
    except (ValueError, RuntimeError):
        pass
    return False

#------------------------------------------------
# File System Operations
#-----------------------------------------------

def safe_read(file_path: str) -> str:
    """Read a file only if within allowed directories."""
    if not _is_allowed(file_path):
        raise PermissionError(f"Access denied: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def safe_write(file_path: str, content: str) -> None:
    """Write a file only if within allowed directories."""
    if not _is_allowed(file_path):
        raise PermissionError(f"Access denied: {file_path}")
    os.makedirs(Path(file_path).parent, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def safe_list(dir_path: str) -> list:
    """List files/folders in allowed directory."""
    if not _is_allowed(dir_path):
        raise PermissionError(f"Access denied: {dir_path}")
    return os.listdir(dir_path)