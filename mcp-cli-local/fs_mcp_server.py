import sys
import json
from pathlib import Path

BASE_DIR = Path.cwd()

def send(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

for line in sys.stdin:
    req = json.loads(line)

    if req["method"] == "initialize":
        send({
            "jsonrpc": "2.0",
            "id": req["id"],
            "result": {
                "tools": [
                    {
                        "name": "read_file",
                        "description": "Read a text file",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": { "type": "string" }
                            },
                            "required": ["path"]
                        }
                    },
                    {
                        "name": "write_file",
                        "description": "Write text to a file",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": { "type": "string" },
                                "content": { "type": "string" }
                            },
                            "required": ["path", "content"]
                        }
                    }
                ]
            }
        })

    elif req["method"] == "tools/call":
        tool = req["params"]["name"]
        args = req["params"]["arguments"]

        try:
            if tool == "read_file":
                content = (BASE_DIR / args["path"]).read_text()
                result = content

            elif tool == "write_file":
                (BASE_DIR / args["path"]).write_text(args["content"])
                result = "File written successfully"

            else:
                raise Exception("Unknown tool")

            send({
                "jsonrpc": "2.0",
                "id": req["id"],
                "result": { "content": result }
            })

        except Exception as e:
            send({
                "jsonrpc": "2.0",
                "id": req["id"],
                "error": { "message": str(e) }
            })
