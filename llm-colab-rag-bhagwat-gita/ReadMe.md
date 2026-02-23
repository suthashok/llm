# 🧘 Bhagavad Gita AI: Your Spiritual Guide

Imagine having a conversation with the Bhagavad Gita. This project uses a smart AI technique called **RAG** (Retrieval-Augmented Generation) to let you ask questions and get answers directly from the sacred text.

Instead of the AI guessing or "hallucinating" an answer, it first "reads" the relevant verses from the Gita and then explains them to you.

---

## ✨ What makes this special?

- **No Guessing:** The AI doesn't just make up spiritual advice; it looks at the actual text of the Bhagavad Gita first.
    
- **Fast & Free:** It’s designed to run entirely for free on **Google Colab**, using a "lightweight" version of Meta’s powerful **Llama-3** brain.
    
- **Simple Setup:** You don't need a supercomputer. If you have a Google account, you can run this.
    

---

## 🛠️ How it works (The Simple Version)

1. **The Library:** We give the AI a digital copy of the Bhagavad Gita.
    
2. **The Searcher:** When you ask a question (like _"How do I find peace?"_), the system quickly searches through all the chapters to find the most relevant verses.
    
3. **The Teacher:** The AI (Llama-3) reads those specific verses and writes a helpful response for you.
    

---

## 🚀 How to try it yourself

You don't need to install anything on your computer!

1. **Open the Notebook:** Click the **"Open in Colab"** button at the top of the file.
    
2. **Get a Key:** You'll need a "Hugging Face" token (it's like a free password to use the AI). You can get one at [huggingface.co](https://huggingface.co/).
    
3. **Press Play:** Run the code cells one by one.
    
4. **Ask Away:** Look for the box at the bottom where you can type your questions!
    

---

## 🏗️ What’s "Under the Hood"?

For those who want to know the tools we used:

- **Brain (LLM):** Llama-3 (A very smart AI from Meta).
    
- **Memory (Vector DB):** ChromaDB (A tool that helps the AI find the right verses quickly).
    
- **Framework:** LangChain (The "glue" that connects the text to the AI).
    
- **Speed Booster:** Unsloth (A tool that makes the AI run much faster and use less memory).
    

---

## 🤝 Want to help?

If you have ideas on how to make the AI's answers even better, or if you want to add more books (like the Upanishads), feel free to fork this project and share your changes!