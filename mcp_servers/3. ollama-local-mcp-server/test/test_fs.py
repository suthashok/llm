import sys
from pathlib import Path

# Add MCP root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools import fs_tools

# -------------------------
# Paths for sandbox testing
# -------------------------
test_dir = Path(r"C:\Users\Ashok Suthar\Documents\GitHub\MCP_Servers\3. ollama-local-mcp-server\test\temp").resolve()
allowed_file = test_dir / "test.txt"
illegal_file = Path(r"C:\Windows\system32\config.txt")

# -------------------------
# Ensure sandbox exists
# -------------------------
test_dir.mkdir(parents=True, exist_ok=True)

# -------------------------
# Test writing
# -------------------------
print("Testing write to allowed path...")
fs_tools.safe_write(allowed_file, "Hello MCP! Testing fs_tools in sandbox.")
print("Write successful ✅")

# -------------------------
# Test reading
# -------------------------
print("Testing read from allowed path...")
content = fs_tools.safe_read(allowed_file)
print("Read content:", content)

# -------------------------
# Test listing
# -------------------------
print("Testing list on allowed directory...")
files = fs_tools.safe_list(test_dir)
print("Files in folder:", files)

# -------------------------
# Test illegal path
# -------------------------
print("Testing read on illegal path...")
try:
    fs_tools.safe_read(illegal_file)
except PermissionError as e:
    print("Caught expected exception ✅", e)
