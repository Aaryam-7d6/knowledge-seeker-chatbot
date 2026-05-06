# Knowledge Seeker Chatbot

> RAG-based conversational AI for document search and knowledge retrieval.  
> Built during **Infosys Springboard Virtual Internship 6.0**.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit)](https://knowledge-seeker-chatbot-app-live.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)

---

## What This Is

Upload your documents. Ask questions. Get answers grounded in your content.

This project implements a full RAG (Retrieval-Augmented Generation) pipeline —
documents are chunked, embedded, stored in a vector database, and retrieved
at query time to give the LLM relevant context before generating a response.

Built in milestones as part of the internship program, this repo documents
the full development journey from raw indexing to a deployed web app.

---

## Architecture

```
Documents (PDF/TXT/DOCX/MD)
↓
Chunking & Parsing (LlamaIndex)
↓
HuggingFace Embeddings
↓
Qdrant Vector DB (Docker)
↓
Retrieval at Query Time
↓
Gemini LLM → Response
↓
Streamlit Chat Interface

```
---

## Milestone Breakdown

| Milestone | What it does |
|---|---|
| `milestone1` | Document ingestion, chunking, embedding, Qdrant vector storage |
| `milestone2` | milestone1 + LLM integration — terminal-based Q&A |
| `milestone3` | Full Streamlit GUI — memory, follow-up questions, multi-turn chat |
| `milestone4` | Deployment to Streamlit Cloud with Qdrant Cloud |

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python |
| RAG Framework | LlamaIndex |
| Vector DB | Qdrant (Docker — local) |
| Embeddings | HuggingFace (`sentence-transformers`) |
| LLM | Gemini 2.5 Flash / Flash-Lite |
| Frontend | Streamlit |
| Containerization | Docker |
| Environment | Conda / WSL (Ubuntu) |

---

## Supported File Types

`PDF` · `TXT` · `DOCX` · `MD (Markdown)`

---

## Local Setup

### Prerequisites
- Python 3.10+
- Docker
- Conda (recommended)
- Google Gemini API key

### Steps

```bash
# Clone the repo
git clone https://github.com/Aaryam-7d6/knowledge-seeker-chatbot.git
cd knowledge-seeker-chatbot

# Create and activate conda environment
conda create -n knowledge-seeker python=3.10
conda activate knowledge-seeker

# Install dependencies
pip install -r req.txt

# Start Qdrant via Docker
# Linux/Mac:
bash dockerr
# Windows: rename dockerr to dockerr.ps1 and run in PowerShell

# Navigate to milestone3 and run
cd milestone3
streamlit run app.py
```

> **Note:** `dockerr` and `qdrant_storage` must be in the same directory.  
> Windows users: rename `dockerr` to `dockerr.ps1` before running.

---

## Live Version

The production-ready version with additional features is deployed separately:

**→ [Live App](https://knowledge-seeker-chatbot-app-live.streamlit.app/)**  
**→ [Live Repo](https://github.com/Aaryam-7d6/knowledge-seeker-chatbot-streamlit-live)**

Additional features available in the live version:
- Auto-scroll to latest message
- Automatic model switching when rate limit is reached
- User-selectable LLM model
- File hashing to prevent redundant re-indexing

---

## Internship Context

**Program:** Infosys Springboard Virtual Internship 6.0  
**Project Title:** AI-Based Document Search and Knowledge Retrieval with Conversational Interface  
**Artifacts:** Available in `docs/Internship_artifacts/`

---

## License

MIT — see [LICENSE](LICENSE)

---

*Built by [Aarya R. Thakar](https://www.linkedin.com/in/aaryamthakar)*
