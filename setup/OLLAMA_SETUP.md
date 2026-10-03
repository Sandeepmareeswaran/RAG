# 🦙 Ollama Setup Guide — Windows
## For RAG Learning Project

---

## What is Ollama?

Ollama lets you run powerful AI language models **completely on your own computer**:
- ✅ No API key required
- ✅ No internet needed (after download)
- ✅ 100% Free, forever
- ✅ Your data stays private on your machine

---

## STEP 1 — Install Ollama

1. Go to: **https://ollama.com/download**
2. Click **"Download for Windows"**
3. Run the installer (`OllamaSetup.exe`)
4. Ollama installs and automatically starts as a background service

**Verify installation:**
```powershell
ollama --version
```
You should see something like: `ollama version 0.3.x`

---

## STEP 2 — Download Required Models

Open PowerShell or Command Prompt and run these commands:

### 2a. Download the LLM (for answering questions)
```powershell
ollama pull llama3.2
```
- Size: ~2 GB
- This is the language model that generates answers
- Wait for download to complete (shows progress bar)

### 2b. Download the Embedding Model (for understanding text meaning)
```powershell
ollama pull nomic-embed-text
```
- Size: ~274 MB
- This converts text into vectors for similarity search
- Much smaller and faster than the LLM

---

## STEP 3 — Verify Everything Works

```powershell
# List all downloaded models
ollama list
```

Expected output:
```
NAME                    ID              SIZE    MODIFIED
llama3.2:latest         a80c4f17acd5   2.0 GB  2 minutes ago
nomic-embed-text:latest 0a109f422b47   274 MB  1 minute ago
```

---

## STEP 4 — Test the Models

### Test the LLM:
```powershell
ollama run llama3.2 "Hello! Tell me about the power of positive thinking in one sentence."
```

### Test embedding (via curl):
```powershell
curl -X POST http://localhost:11434/api/embeddings `
  -H "Content-Type: application/json" `
  -d '{"model": "nomic-embed-text", "prompt": "test text"}'
```

---

## Ollama Commands Reference

| Command | Description |
|---------|-------------|
| `ollama list` | Show downloaded models |
| `ollama pull <model>` | Download a model |
| `ollama run <model>` | Chat with a model in terminal |
| `ollama rm <model>` | Delete a model |
| `ollama ps` | Show running models |
| `ollama stop <model>` | Stop a running model |

---

## Ollama API Reference

Ollama runs a local HTTP server at `http://localhost:11434`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/generate` | POST | Generate text |
| `/api/embeddings` | POST | Get text embeddings |
| `/api/tags` | GET | List models |
| `/api/pull` | POST | Pull a model |

---

## Alternative Models to Try

After completing the tutorial, try these models:

### Better LLMs:
```powershell
ollama pull mistral        # 4.1 GB — Fast and smart
ollama pull llama3.1:8b   # 4.7 GB — More capable
ollama pull gemma2:2b     # 1.6 GB — Tiny but decent
ollama pull phi3:mini     # 2.3 GB — Microsoft's model
```

### Alternative Embedding Models:
```powershell
ollama pull mxbai-embed-large  # Better quality embeddings
```

---

## Troubleshooting

### "Connection refused" error
Ollama isn't running. Start it:
```powershell
ollama serve
```
Or restart the Ollama application from the system tray.

### Model download is slow
Normal — models are 1-4 GB. Wait patiently.

### "Out of memory" error
Try a smaller model: `ollama pull llama3.2:1b` (smaller variant)

### Port already in use
```powershell
# Find what's using port 11434
netstat -ano | findstr :11434
```

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| RAM | 8 GB | 16 GB |
| Disk Space | 10 GB free | 20 GB free |
| OS | Windows 10+ | Windows 11 |
| GPU | Not required | NVIDIA GPU (much faster) |

> **With an NVIDIA GPU:** Ollama automatically uses it for much faster inference.
> **Without GPU:** Runs on CPU, which is slower but works fine for learning.

---

## Next Step

Once Ollama is installed and models are downloaded:
1. Open a terminal and run: `ollama serve` (if not already running)
2. Open the notebook: `notebooks/RAG_Complete_Practical.ipynb`
3. Run cells from top to bottom — enjoy!
