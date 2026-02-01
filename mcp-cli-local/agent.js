const OLLAMA_URL = "http://localhost:11434/api/generate";
const MODEL = "qwen2.5:3b-instruct";

export async function runAgent({ userInput, mcpClient }) {
  const systemPrompt = `
You are a local automation assistant.

You operate internally in two modes, but the mode decision is NEVER shown to the user.

MODE RULES (internal only):

CHAT MODE:
- Used for greetings, explanations, or non-actionable questions
- Respond with natural plain text
- NEVER output JSON
- NEVER mention modes, rules, or tools

TOOL MODE:
- Used when the user asks for OR clearly implies a filesystem action
- Respond with ONE valid JSON object only
- Format:
  {
    "tool": "<tool_name>",
    "arguments": { ... }
  }
- Do not include any other text

ABSOLUTE RULES:
- The mode decision is INTERNAL
- NEVER say "CHAT MODE" or "TOOL MODE"
- NEVER output {}
- NEVER guess filenames
- NEVER explain limitations or permissions
- If a relevant tool exists, YOU MUST call it

Internal intent examples (not shown to user):
- "what is current directory" → get_cwd
- "where am I" → get_cwd
- "list files" → list_directory
- "show files here" → list_directory
- "read example.txt" → read_file

Available tools:
${JSON.stringify(mcpClient.tools, null, 2)}
`.trim();




  const prompt = `
SYSTEM:
${systemPrompt}

USER:
${userInput}
`.trim();

  const res = await fetch(OLLAMA_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model: MODEL, prompt })
  });

  const text = await res.text();

  let toolCall = null;
  let normalText = "";

  for (const line of text.split("\n")) {
    if (!line.trim()) continue;

    let obj;
    try {
      obj = JSON.parse(line);
    } catch {
      continue;
    }

    // Tool JSON detected → STOP immediately
    if (obj.tool && obj.arguments) {
      toolCall = obj;
      break;
    }

    // Normal text chunk
    if (obj.response) {
      normalText += obj.response;
    }
  }

  if (toolCall) {
    console.log(`🔧 Calling ${toolCall.tool}...`);
    const result = await mcpClient.callTool(
      toolCall.tool,
      toolCall.arguments
    );
    console.log("✅ Tool result:\n", result);
    return;
  }

  console.log(normalText.trim());
}
