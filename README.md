# NexusAI: Agentic RAG & Multi-Source MCP Research Chatbot

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Agentic-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-FF4F00?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6600?style=for-the-badge)](https://www.trychroma.com/)
[![MCP](https://img.shields.io/badge/MCP-Protocol-5B21B6?style=for-the-badge)](https://modelcontextprotocol.io/)

NexusAI is a full-stack, stateful AI research assistant built with **LangGraph**, **FastAPI**, **Flask**, **ChromaDB RAG**, and **Model Context Protocol (MCP)** integration. It enables natural language querying over local PDF documents, real-time web search, user authentication management, and academic/book discovery across Google Books, Internet Archive, and Crossref.

---

## 🌟 Key Features

- **🤖 LangGraph Agentic Workflow**: Multi-turn conversation graph powered by `ChatGroq` (`openai/gpt-oss-120b`) / `ChatOllama` (`Llama-3.2-3B`), equipped with state persistence (`MemorySaver`) for user sessions.
- **📚 Retrieval-Augmented Generation (RAG)**:
  - Custom PDF document loading with `PyMuPDFLoader` (`fitz`).
  - Text chunking using `RecursiveCharacterTextSplitter`.
  - Dense embeddings generated via `SentenceTransformer` (`all-MiniLM-L6-v2`).
  - Vector storage & persistent similarity search via **ChromaDB**.
- **🔌 Model Context Protocol (MCP) Integration**: Custom `FastMCP` stdio server exposing tools to query:
  - **Google Books API**: Find book descriptions, publication metadata, categories, and authors.
  - **Internet Archive API**: Search public texts, historical documents, and archives.
  - **Crossref API**: Retrieve metadata and DOIs for academic research papers.
- **🌐 Real-Time Web Search**: Integrated `DuckDuckGoSearchRun` tool for up-to-date internet queries.
- **🔒 Authentication & Admin Tools**:
  - SQLite authentication database backend (`Database.db`).
  - Interactive web interface built with **Flask**, featuring random **CAPTCHA verification** and session tracking.
  - Admin agent tools allowing database queries (`daatabase`) and user account removal (`delete`).

---

## 🏗️ Architecture Overview

```
 ┌─────────────────────────────────────────────────────────────┐
 │                      Flask Web UI                           │
 │                (http://127.0.0.1:5000)                      │
 │    - CAPTCHA Validation  - Chat Interface  - Sessions       │
 └──────────────────────────────┬──────────────────────────────┘
                                │ HTTP Requests
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                     FastAPI Backend                         │
 │                (http://127.0.0.1:8000)                      │
 │   - /login (Auth)               - /chatts (Stateful Agent)  │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                    LangGraph Agent                          │
 │         StateGraph + Groq LLM + Checkpointer Memory         │
 └──────┬───────────────────────┬───────────────────────┬──────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌────────────────┐
│   RAG Tool    │       │ Web Search    │       │ Database Tools │
│ (ChromaDB +   │       │ (DuckDuckGo)  │       │   (SQLite)     │
│  MiniLM Embed)│       └───────────────┘       └────────────────┘
└───────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────────────┐
│                   MCP Stdio Server Client                      │
│                  (internet_archive_mcp.py)                     │
│  ┌───────────────────┬───────────────────┬──────────────────┐  │
│  │   Google Books    │ Internet Archive  │     Crossref     │  │
│  └───────────────────┴───────────────────┴──────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
├── Database.py               # Database schema initialization script (SQLite)
├── Database.db               # SQLite database file for user credentials
├── RAG_pipline.py            # PDF loader, Chunking, Sentence Transformer & ChromaDB RAG logic
├── mainfastapi.py            # FastAPI server & LangGraph agent setup with tools & MCP client
├── mainflask.py              # Flask web frontend for authentication and chat UI
├── internet_archive_mcp.py   # MCP Server offering Google Books, Internet Archive & Crossref APIs
├── insert.py                 # Seed script to insert initial users into SQLite database
├── requirement.txt           # Python package dependencies list
├── data/
│   ├── pdf/                  # Input PDF directory for vector database ingestion
│   └── vector_store/         # ChromaDB persistence directory
└── templates/
    ├── login.html            # User login & CAPTCHA page
    ├── home.html             # Main chatbot interface
    └── chat.html             # Chat sub-template component
```

---

## 🛠️ Prerequisites & Setup

### 1. Requirements
- **Python 3.10+**
- **Git**
- **Ollama** *(Optional, if using local Llama-3.2 model)*

### 2. Environment Configuration
Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_BOOKS_API_KEY=your_google_books_api_key_here
```

### 3. Installation
Install the dependencies listed in `requirement.txt`:

```bash
# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirement.txt
```

---

## 🚀 Step-by-Step Execution Guide

### Step 1: Initialize Database & Seed Users
Run `Database.py` to create the SQLite table, then `insert.py` to populate initial credentials:

```bash
python Database.py
python insert.py
```

*Default Seed Credentials:*
- `admin` / `admin123`
- `keerti` / `keerti123`
- `aniket` / `aniket123`
- `tushar` / `tushar123`

### Step 2: Index PDF Documents for RAG
Place your PDF files inside the `data/pdf/` folder and execute `RAG_pipline.py` to chunk and store embeddings in ChromaDB:

```bash
python RAG_pipline.py
```

### Step 3: Launch the FastAPI Backend
Start the FastAPI server on port 8000 using `uvicorn`:

```bash
uvicorn mainfastapi:app --reload --port 8000
```
*FastAPI API Documentation will be available at `http://127.0.0.1:8000/docs`.*

### Step 4: Launch the Flask Web UI
In a separate terminal window, launch the Flask frontend app:

```bash
python mainflask.py
```
Open your browser and navigate to **`http://127.0.0.1:5000`**.

---

## 🧰 Agent Tools Reference

| Tool Name | Source Module | Description |
| :--- | :--- | :--- |
| `document` | `RAG_pipline.py` | Performs semantic search across uploaded PDF documents stored in ChromaDB. |
| `search` | `DuckDuckGoSearchRun` | Searches the live web for current events, news, or general search queries. |
| `daatabase` | `mainfastapi.py` | Admin tool to retrieve all registered usernames from SQLite `Database.db`. |
| `delete` | `mainfastapi.py` | Admin tool to remove a specific user from SQLite `Database.db`. |
| `search_books` | `internet_archive_mcp.py` (MCP) | Queries Google Books API for metadata, categories, authors, and summaries. |
| `search_internet_archive` | `internet_archive_mcp.py` (MCP) | Searches the Internet Archive for text documents, books, and archives. |
| `search_crossref` | `internet_archive_mcp.py` (MCP) | Searches Crossref API for scientific paper metadata, publishers, and DOIs. |

---

## 🔌 API Endpoints (FastAPI)

### `POST /login`
Authenticates a user against SQLite database.
- **Request**:
  ```json
  {
    "username": "keerti",
    "password": "keerti123"
  }
  ```
- **Response**: `{"username": "keerti"}` or `{"error": "Invalid Credentials"}`

### `POST /chatts`
Dispatches user messages to the stateful LangGraph agent.
- **Request**:
  ```json
  {
    "user_name": "keerti",
    "user_in": "Summarize the key points in the uploaded document."
  }
  ```
- **Response**:
  ```json
  {
    "user_input": "Summarize the key points in the uploaded document.",
    "bot_input": "Based on the uploaded documents..."
  }
  ```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
