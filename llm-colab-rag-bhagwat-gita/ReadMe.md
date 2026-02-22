
This project implements RAG based intelligent Agentic assistant who answer user questions from Bhagwat Gita.


# 🧠 Overall Flow

User Question  
     ↓  
Embedding (MiniLM - Free)  
     ↓  
FAISS Vector Search  
     ↓  
Top Relevant Verses Retrieved  
     ↓  
FLAN-T5 Generates Final Answer

Runs fully inside **Colab free tier**.