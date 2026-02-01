import { spawn } from "child_process";

export async function connectMCP() {
  const proc = spawn("python", ["fs_mcp_server.py"], {
    stdio: ["pipe", "pipe", "inherit"]
  });

  let buffer = "";

  proc.stdout.on("data", (chunk) => {
    buffer += chunk.toString();
  });

  function send(message) {
    proc.stdin.write(JSON.stringify(message) + "\n");
  }

  async function receive() {
    while (!buffer.includes("\n")) {
      await new Promise(r => setTimeout(r, 5));
    }
    const idx = buffer.indexOf("\n");
    const line = buffer.slice(0, idx);
    buffer = buffer.slice(idx + 1);
    return JSON.parse(line);
  }

  await send({
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {}
  });

  const init = await receive();

  return {
    tools: init.result.tools,
    callTool: async (name, arguments_) => {
      await send({
        jsonrpc: "2.0",
        id: Date.now(),
        method: "tools/call",
        params: { name, arguments: arguments_ }
      });
      const res = await receive();
      return res.result.content;
    }
  };
}
