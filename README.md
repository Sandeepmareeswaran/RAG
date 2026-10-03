# 🤖 RAG Learning Project
### Learn Retrieval-Augmented Generation — Practically, from Scratch

> Build a complete AI chatbot that answers questions from a real book,
> running 100% locally on your machine — no API keys, no cloud, no cost.

---

## 📦 What's Inside

```
RAG_Learning/
├── 📓 notebooks/
│   └── RAG_Complete_Practical.ipynb   ← Main Jupyter notebook (START HERE)
├── 📊 data/
│   ├── as_a_man_thinketh.pdf          ← Complete 32-page book in PDF format
│   ├── as_a_man_thinketh.txt          ← Plain text format (Project Gutenberg)
│   └── chroma_db/                     ← Created automatically (vector database)
├── 📚 guides/
│   ├── RAG_Complete_Beginner_Guide.pdf ← 20-page complete PDF learning manual & guide
│   └── RAG_Complete_Beginner_Guide.md  ← Markdown version
├── 🛠️ scripts/
│   ├── generate_book_pdf.py           ← Generates the book PDF
│   └── generate_guide_pdf.py          ← Generates the 20-page guide PDF
├── ⚙️ setup/
│   └── OLLAMA_SETUP.md                ← How to install Ollama
└── requirements.txt                   ← Python packages needed
```

---

## 🚀 Quick Start (3 Steps)

### Step 1 — Install Ollama
Read `setup/OLLAMA_SETUP.md` OR run these commands:

```powershell
# Download Ollama from: https://ollama.com/download
# After installing:
ollama pull llama3.2          # The LLM (~2 GB)
ollama pull nomic-embed-text  # The embedding model (~274 MB)
```

### Step 2 — Install Python Packages

```powershell
cd "d:\OutliersUnited(rework)\RAG_Learning"
pip install -r requirements.txt
```

### Step 3 — Open & Run the Notebook

```powershell
jupyter notebook notebooks/RAG_Complete_Practical.ipynb
```

Run each cell from top to bottom. The notebook will:
1. ✅ Install all Python packages
2. ✅ Download the book automatically
3. ✅ Chunk, embed, and store it in ChromaDB
4. ✅ Start an interactive chat loop

---

## 📖 The Book

We use **"As a Man Thinketh"** by James Allen (1903).

- **100% Free** — published in 1903, in the public domain worldwide
- **Downloaded from Project Gutenberg** — the world's largest free ebook library
- **Covers:** mindset, thought power, discipline, character, success — great themes for self-improvement
- **Why not the 5 AM Club?** — Robin Sharma's book is under copyright. Using it would be illegal.
  James Allen's book covers the same core themes: discipline, mindset, and personal transformation.

---

## 🧠 What You Learn

| Concept | Where |
|---------|-------|
| What is RAG and why it exists | Notebook Cell 1 intro + Guide Ch.1 |
| Document Loading | Notebook Cell 3 |
| Chunking (why, how, parameters) | Notebook Cell 4 + Guide Ch.4 |
| Embeddings (vectors, similarity) | Notebook Cell 5 + Guide Ch.5 |
| Vector Stores (ChromaDB) | Notebook Cell 6 + Guide Ch.6 |
| Retrieval (k, MMR, scores) | Notebook Cell 7 + Guide Ch.7 |
| Ollama LLM setup | Notebook Cell 8 + Guide Ch.12 |
| Prompt Templates | Notebook Cell 9 + Guide Ch.9 |
| Full RAG Chain (LCEL) | Notebook Cell 9-10 + Guide Ch.10 |
| Interactive Chat with Memory | Notebook Cell 11 |
| Reloading from disk | Notebook Cell 12 |
| Similarity score visualization | Notebook Cell 13 |

---

## 🛠️ Tech Stack

| Technology | Role |
|-----------|------|
| **Python 3.10+** | Core language |
| **Jupyter Notebook** | Interactive learning environment |
| **LangChain** | RAG orchestration framework |
| **Ollama** | Local LLM runtime |
| **llama3.2** | The language model (generates answers) |
| **nomic-embed-text** | Embedding model (text → vectors) |
| **ChromaDB** | Vector database (stores embeddings) |
| **pypdf** | PDF reader (for future PDF experiments) |

---

## 💬 Sample Questions to Ask the Chatbot

Once the chat loop is running, try these:

```
❓ "What does the book say about the power of thought?"
❓ "How does the mind affect our health?"
❓ "What is the relationship between thought and character?"
❓ "How can a person change their life circumstances?"
❓ "What does James Allen say about purpose?"
❓ "How do our thoughts shape our destiny?"
```

---

## 📚 Full Learning Manual & Architecture Guide
The complete beginner guide is provided in both **PDF** and **Markdown** formats:
- 📄 **PDF Manual:** [`guides/RAG_Complete_Beginner_Guide.pdf`](guides/RAG_Complete_Beginner_Guide.pdf) — 20-page beautifully formatted document ready for offline reading and printing.
- 📝 **Markdown Guide:** [`guides/RAG_Complete_Beginner_Guide.md`](guides/RAG_Complete_Beginner_Guide.md)

**Topics Covered in Depth:**
- What RAG is, why it was invented, and how it solves hallucination
- Stage-by-stage visual architecture diagrams
- What is Chunking, why overlap matters, and splitting strategies
- Embeddings: mathematical vectors, semantic similarity, high-dimensional spaces
- Vector Stores: ChromaDB internals and indexing algorithms (HNSW)
- Semantic Retrieval: Top-K similarity, MMR, and score thresholds
- LLM Integration & Prompt Engineering for grounded answers
- Step-by-step LangChain LCEL pipeline assembly
- Complete glossary of all AI/RAG terms
- Common beginner mistakes and troubleshooting playbook
- RAG tuning checklist and advanced production roadmap

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|---------|
| `Connection refused on port 11434` | Ollama isn't running. Run: `ollama serve` |
| `Model not found` | Run: `ollama pull llama3.2` |
| Slow embedding | Normal on first run. It embeds ~50-80 chunks sequentially. |
| `ModuleNotFoundError` | Run Cell 1 (installs packages) |
| Out of memory | Use smaller model: `ollama pull llama3.2:1b` |
