import readline from "readline";
import { connectMCP } from "./mcp.js";
import { runAgent } from "./agent.js";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const mcpClient = await connectMCP();

const messages = [
  {
    role: "system",
    content: `
You are a local automation assistant.
You have access to tools.
When a tool is relevant, you MUST call it.
Do not explain the tool call.
When the task is complete, respond briefly.
`.trim()
  }
];

console.log("Local MCP CLI ready.");

rl.on("line", async (line) => {
  await runAgent({
    userInput: line,
    mcpClient,
    messages
  });
});
