# Ollama Custom Model Setup Guide (Windows / CPU)

This is a step-by-step guide to creating custom Ollama models with hardware constraints, system prompts, and optimal settings for CPU systems.

---

## 1️⃣ Prerequisites

- Ollama installed (GUI + CLI)
- Windows system (tested on 16GB RAM + Ryzen 5 3400G)
- Basic knowledge of PowerShell
- Optional: Git for version control

---

## 2️⃣ Recommended System Settings

1. Limit CPU threads to avoid freezing:

```powershell
# Set permanently (system-wide)
setx OLLAMA_NUM_THREADS 4 /M
Recommended model parameters for CPU efficiency:

Parameter	Suggested Value
num_ctx	2048
num_predict	128–256
temperature	0.6
Notes:

num_ctx limits RAM usage.

num_predict limits token output per request.

temperature controls randomness.

---

## 3️⃣ Create a Modelfile
Create a folder for builds (example):

cd $HOME
mkdir ollama-builds
cd ollama-builds
Create the Modelfile:

notepad Modelfile
Paste the following template:

FROM qwen2.5:3b-instruct

PARAMETER num_ctx 2048
PARAMETER num_predict 256
PARAMETER temperature 0.6

SYSTEM """
You are a concise assistant.
Respond briefly and directly.
Keep answers under 150 words.
"""
⚠️ On Windows, make sure the file is named exactly Modelfile (no .txt extension).

---

## 4️⃣ Build Your Custom Model
ollama create qwen3b-concise -f Modelfile
If successful, your model is added to Ollama’s internal storage.

Check with:

ollama list

---

## 5️⃣ Run Your Model
CLI:
ollama run qwen3b-concise
GUI:
Open Ollama GUI

Select qwen3b-concise from the model list

---

## 6️⃣ Tips for Hardware-Friendly Usage
Avoid running multiple instances of Ollama simultaneously.

For longer chats or RAG tasks, increase num_ctx cautiously.

Reduce num_predict for short answers to save CPU/RAM.

Always check CPU/RAM usage:

# Task Manager → Performance tab

---

## 7️⃣ Optional: Create Multiple Profiles
You can create multiple custom models for different purposes:

qwen3b-fast → short answers, low RAM

qwen3b-coding → optimized for code completion

qwen3b-longchat → longer context for conversations

Simply create separate Modelfiles with different num_ctx / num_predict / SYSTEM prompts.

---

## 8️⃣ Notes
Never edit .ollama\models manually — it’s managed by Ollama.

Modelfile is only needed during ollama create.

Use triple quotes """ for multi-line SYSTEM prompts on Windows.