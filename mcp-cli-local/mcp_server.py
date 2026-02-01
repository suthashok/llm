import sys
import json

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
                        "name": "echo",
                        "description": "Echo input",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "text": { "type": "string" }
                            },
                            "required": ["text"]
                        }
                    }
                ]
            }
        })

    elif req["method"] == "tools/call":
        send({
            "jsonrpc": "2.0",
            "id": req["id"],
            "result": {
                "content": req["params"]["arguments"]["text"]
            }
        })
