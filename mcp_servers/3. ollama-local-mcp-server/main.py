import shlex
from tools import fs_tools
import ollama
from pathlib import Path
import re


# -------------------------
# Tool router (robust version)
# -------------------------
def tool_router(command: str):
    try:
        tokens = shlex.split(command)
    except ValueError as e:
        return f"Error parsing command: {e}"

    if not tokens:
        return "No command provided."

    action = tokens[0].lower()
    if len(tokens) < 2:
        return "Incomplete command."

    # READ FILE
    if action == "read" and tokens[1].lower() == "file":
        if len(tokens) != 3:
            return "Usage: read file \"<path>\""
        return fs_tools.safe_read(tokens[2])

    # WRITE FILE
    elif action == "write" and tokens[1].lower() == "file":
        if len(tokens) < 4:
            return "Usage: write file \"<path>\" \"<content>\""
        path = tokens[2]
        content = " ".join(tokens[3:])
        fs_tools.safe_write(path, content)
        return f"Wrote to {path}"

    # LIST FOLDER
    elif action == "list" and tokens[1].lower() == "folder":
        if len(tokens) != 3:
            return "Usage: list folder \"<path>\""
        return fs_tools.safe_list(tokens[2])

    else:
        return "Unknown command."

# -------------------------
# LLM integration
# -------------------------
def run_llm(prompt: str) -> str:
    """
    Sends a prompt to the local Ollama model (llama3-safe)
    and returns the generated text response in a robust way
    for SDK v0.6.1.
    """
    response = ollama.chat(model="llama3-safe",messages=[{"role": "user", "content": prompt}])

    # SDK v0.6.1 returns a ChatResponse object
    # which has a .results list with assistant messages

    try:
        return response.message.content.strip()
    except AttributeError:
        # fallback
        return str(response)


# -------------------------
# Extract clean command from LLM output
# -------------------------
def extract_command(llm_output: str) -> str:
    """
    Extract the first line that starts with write/read/list,
    removes backticks and extra text.
    """
    llm_output = llm_output.replace("`", "")
    for line in llm_output.splitlines():
        line = line.strip()
        if line.lower().startswith(("write file", "read file", "list folder")):
            return line
    return llm_output.strip()



# -------------------------
# Sandbox paths
# -------------------------
sandbox_folder = Path(r"C:\Users\Ashok Suthar\Documents\GitHub\MCP_Servers\3. ollama-local-mcp-server\test\temp")
sandbox_folder.mkdir(parents=True, exist_ok=True)



# -------------------------
# Example multi-step session
# -------------------------
if __name__ == "__main__":
    # Step 1: Write file
    prompt_write = f"""
Important: Do not remove or change any spaces or characters in folder/file names.
Generate a command to write "Hello from LLM in sandbox" to the file 
\"{sandbox_folder / 'LLM File.txt'}\".
Use format: write file "<full path>" "<content>"
"""
    llm_write_raw = run_llm(prompt_write)
    llm_write_command = extract_command(llm_write_raw)
    print("LLM extracted write command:", llm_write_command)
    result_write = tool_router(llm_write_command)
    print("Execution result:", result_write)

    # Step 2: Read file
    prompt_read = f"""
Important: Do not remove or change any spaces or characters in folder/file names.
Generate a command to read the file \"{sandbox_folder / 'LLM File.txt'}\".
Use format: read file "<full path>"
"""
    llm_read_raw = run_llm(prompt_read)
    llm_read_command = extract_command(llm_read_raw)
    print("LLM extracted read command:", llm_read_command)
    result_read = tool_router(llm_read_command)
    print("Read result:", result_read)

    # Step 3: List folder
    prompt_list = f"""
Important: Do not remove or change any spaces or characters in folder/file names.
Generate a command to list all files in \"{sandbox_folder}\".
Use format: list folder "<full path>"
"""
    llm_list_raw = run_llm(prompt_list)
    llm_list_command = extract_command(llm_list_raw)
    print("LLM extracted list command:", llm_list_command)
    result_list = tool_router(llm_list_command)
    print("List result:", result_list)
