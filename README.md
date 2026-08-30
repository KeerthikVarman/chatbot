# Multi-Source MCP & RAG Research Chatbot

<p align="center">

A full-stack stateful AI research assistant built with **LangGraph, FastAPI, Flask, ChromaDB RAG, and Model Context Protocol (MCP)**.

</p>

##  Key Features

### 1. Agentic LangGraph Workflow

* Multi-turn stateful conversations
* User session state persistence using `MemorySaver`
* Tool calling and tool selection
* Groq LLM using `openai/gpt-oss-120b`
* Optional local Ollama support using `Llama-3.2-3B`

### 2. Retrieval-Augmented Generation

The RAG pipeline allows the chatbot to answer questions using uploaded PDF documents.

The pipeline includes:

* PDF loading using `PyMuPDFLoader`
* Text extraction using `fitz`
* Text chunking using `RecursiveCharacterTextSplitter`
* Dense embeddings using `SentenceTransformer`
* `all-MiniLM-L6-v2` embedding model
* Persistent vector storage using ChromaDB
* Semantic similarity search

### 3. Model Context Protocol

A custom FastMCP stdio server exposes external research tools.

Supported integrations:

* Google Books API
* Internet Archive API
* Crossref API
* Tavily Search API

### 4. Real-Time Web Search

The chatbot integrates `DuckDuckGoSearchRun` for live internet queries.

### 5. Authentication & Administration

* SQLite authentication
* Login validation
* Flask authentication interface
* CAPTCHA verification
* Session tracking
* Admin database queries
* User account deletion

---

# Architecture

The application follows this architecture:

```text
                    ┌─────────────────────────────┐
                    │        Flask Web UI         │
                    │                             │
                    │   Login │ CAPTCHA │ Chat    │
                    │          Port 5000           │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       FastAPI Backend       │
                    │                             │
                    │       /login   /chatts      │
                    │          Port 8000           │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │      LangGraph Agent        │
                    │                             │
                    │    StateGraph + LLM         │
                    │        + Memory              │
                    └──────────────┬──────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
                ▼                  ▼                  ▼
             RAG             Web Search            SQLite
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       MCP Stdio Server      │
                    └──────────────┬──────────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
       Google Books         Internet Archive          Crossref
             │
             ▼
       Tavily Search
```

---

#  Project Structure

```text
Multi-Source-MCP-RAG-Research-Chatbot/
│
├── assets/
│   ├── login.png
│   ├── chat.png
│   └── architecture.png
│
├── data/
│   ├── pdf/
│   └── vector_store/
│
├── templates/
│   ├── login.html
│   ├── home.html
│   └── chat.html
│
├── Database.py
├── Database.db
├── RAG_pipline.py
├── mainfastapi.py
├── mainflask.py
├── internet_archive_mcp.py
├── insert.py
├── requirement.txt
├── .env
├── .gitignore
└── README.md
```

## Important Files

| File                      | Description                                                         |
| ------------------------- | ------------------------------------------------------------------- |
| `Database.py`             | SQLite database schema initialization                               |
| `Database.db`             | SQLite database for user credentials                                |
| `RAG_pipline.py`          | PDF loading, chunking, embeddings, and ChromaDB RAG logic           |
| `mainfastapi.py`          | FastAPI server, LangGraph agent, tools, and MCP client              |
| `mainflask.py`            | Flask web frontend for authentication and chat                      |
| `internet_archive_mcp.py` | MCP server for Google Books, Internet Archive, Crossref, and Tavily |
| `insert.py`               | Inserts initial users into the SQLite database                      |
| `requirement.txt`         | Python package dependencies                                         |
| `data/pdf/`               | Input PDF directory                                                 |
| `data/vector_store/`      | ChromaDB persistence directory                                      |
| `templates/login.html`    | Login and CAPTCHA page                                              |
| `templates/home.html`     | Main chatbot interface                                              |
| `templates/chat.html`     | Chat component                                                      |
| `.env`                    | API keys and environment configuration                              |

---

#  Prerequisites

Before installing the project, make sure the following are installed:

* Python 3.10+
* Git
* Internet connection
* Ollama — only required when using the local Ollama model

If using Groq instead of Ollama, a Groq API key is also required.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Multi-Source-MCP-RAG-Research-Chatbot.git
cd Multi-Source-MCP-RAG-Research-Chatbot
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

## 3. Activate the Virtual Environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirement.txt
```

---

# Ollama Setup

The project can optionally use a local Ollama model instead of a cloud LLM.

The configured model is:

```text
llama3.2:3b
```

## Install Ollama

Install Ollama from its official website and verify the installation:

```bash
ollama --version
```

## Download the Model

```bash
ollama pull llama3.2:3b
```

Check installed models:

```bash
ollama list
```

Test the model:

```bash
ollama run llama3.2:3b
```

Then enter:

```text
Hello, introduce yourself.
```

If Ollama responds successfully, the local model is working.

---

#  Connect Ollama with LangChain

Install the integration:

```bash
pip install -U langchain-ollama
```

Import the model:

```python
from langchain_ollama import ChatOllama
```

Create the LLM:

```python
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)
```

The connection is:

```text
LangChain
    │
    ▼
ChatOllama
    │
    ▼
Ollama Local Server
    │
    ▼
llama3.2:3b
```

---

#  LLM Configuration

The project supports Groq and Ollama.

| Feature                   | Groq                  | Ollama                          |
| ------------------------- | --------------------- | ------------------------------- |
| Runs locally              | No                    | Yes                             |
| Internet required for LLM | Yes                   | No, after model download        |
| API key                   | Required              | Not normally required           |
| Model storage             | Cloud                 | Local computer                  |
| Model identifier          | Provider-specific     | `llama3.2:3b`                   |
| Hardware requirement      | Low local requirement | Depends on local model/hardware |

### Groq

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)
```

### Ollama

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)
```

---

# Environment Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_BOOKS_API_KEY=your_google_books_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

If using Ollama as the LLM, `GROQ_API_KEY` is not required for Ollama itself.

### Important

Never upload API keys or `.env` files to GitHub.

Your `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
data/vector_store/
```

---

#  Database Setup

Initialize the SQLite database:

```bash
python Database.py
```

Insert the initial users:

```bash
python insert.py
```

> For a public GitHub repository, do **not** publish real passwords or production credentials. Use environment variables or create users during deployment.

---

#  RAG Document Setup

Create the PDF directory:

```text
data/pdf/
```

Place your PDF documents inside this directory.

Then run:

```bash
python RAG_pipline.py
```

The RAG pipeline:

```text
PDF Documents
      │
      ▼
Text Extraction
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
      │
      ▼
ChromaDB Vector Store
      │
      ▼
Semantic Search
```

The persistent vector store is created under:

```text
data/vector_store/
```

---

#  Running the Application

The project uses two application servers:

* FastAPI — backend and LangGraph agent
* Flask — web interface

Both servers need to be running.

## Terminal 1 — Start Ollama

If using Ollama:

```bash
ollama run llama3.2:3b
```

## Terminal 2 — Start FastAPI

```bash
uvicorn mainfastapi:app --reload --port 8000
```

FastAPI:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Terminal 3 — Start Flask

```bash
python mainflask.py
```

Flask:

```text
http://127.0.0.1:5000
```

Open the Flask address in your browser.

---

# Application Workflow

```text
User
 │
 ▼
Flask Web Interface
 │
 ▼
FastAPI Backend
 │
 ▼
LangGraph Agent
 │
 ├── LLM ─────────────► Groq / Ollama
 │
 ├── PDF Question ────► ChromaDB RAG
 │
 ├── Web Question ────► DuckDuckGo / Tavily
 │
 ├── Book Search ─────► Google Books
 │
 ├── Archive Search ──► Internet Archive
 │
 ├── Paper Search ────► Crossref
 │
 └── Admin Request ───► SQLite
 │
 ▼
Final Response
```

---

#  Agent Tools

| Tool Name                 | Source Module             | Description                                            |
| ------------------------- | ------------------------- | ------------------------------------------------------ |
| `document`                | `RAG_pipline.py`          | Performs semantic search across uploaded PDF documents |
| `search`                  | `DuckDuckGoSearchRun`     | Performs live web searches                             |
| `daatabase`               | `mainfastapi.py`          | Retrieves registered usernames from SQLite             |
| `delete`                  | `mainfastapi.py`          | Removes a specific user from SQLite                    |
| `search_books`            | `internet_archive_mcp.py` | Searches Google Books                                  |
| `search_internet_archive` | `internet_archive_mcp.py` | Searches Internet Archive                              |
| `search_crossref`         | `internet_archive_mcp.py` | Searches Crossref academic metadata                    |
| `tavily_search`           | `internet_archive_mcp.py` | Performs live Tavily search                            |

---

#  API Endpoints

## `POST /login`

Authenticates a user against the SQLite database.

### Request

```json
{
  "username": "username",
  "password": "password"
}
```

### Response

```json
{
  "username": "username"
}
```

---

## `POST /chatts`

Sends a user message to the stateful LangGraph agent.

### Request

```json
{
  "user_name": "username",
  "user_in": "Summarize the key points in the uploaded document."
}
```

### Response

```json
{
  "user_input": "Summarize the key points in the uploaded document.",
  "bot_input": "Based on the uploaded documents..."
}
```

---

# Web Interface

## Login Page

The login interface provides:

* Username authentication
* Password authentication
* CAPTCHA verification
* Session handling

## Chat Interface

The chatbot can work with:

* Uploaded PDF documents
* Web search
* Google Books
* Internet Archive
* Crossref
* Tavily Search
* Database administration tools
* Groq or local Ollama LLM

---

# Testing & Verification

After installation, verify the system in this order:

1. Install Python dependencies.
2. Install Ollama if local execution is required.
3. Pull `llama3.2:3b`.
4. Run `ollama list`.
5. Test `ollama run llama3.2:3b`.
6. Initialize the database.
7. Add at least one PDF.
8. Run `RAG_pipline.py`.
9. Start FastAPI.
10. Start Flask.
11. Open the login page.
12. Log in with a configured account.
13. Send a chatbot query.
14. Test a PDF/RAG query.
15. Test an external search query.

---

#  Troubleshooting

## Dependency Installation Error

Make sure the virtual environment is activated:

```text
(.venv)
```

Then run:

```bash
pip install -r requirement.txt
```

If `ChatOllama` cannot be imported:

```bash
pip install -U langchain-ollama
```

## Ollama Command Not Found

Run:

```bash
ollama --version
```

If the command does not work, install Ollama and restart your terminal.

## Ollama Model Not Found

Check:

```bash
ollama list
```

If `llama3.2:3b` is missing:

```bash
ollama pull llama3.2:3b
```

Test:

```bash
ollama run llama3.2:3b
```

## FastAPI Not Starting

Run from the project root:

```bash
uvicorn mainfastapi:app --reload --port 8000
```

## Flask Not Starting

Run:

```bash
python mainflask.py
```

## RAG Returns No Results

Make sure PDFs exist inside:

```text
data/pdf/
```

Then run:

```bash
python RAG_pipline.py
```

Verify that:

```text
data/vector_store/
```

exists.

## API Key Error

Verify the required environment variables:

```text
GROQ_API_KEY
GOOGLE_BOOKS_API_KEY
TAVILY_API_KEY
```

---

# Advantages

* Stateful multi-turn AI conversations
* Retrieval-Augmented Generation over local PDFs
* Persistent ChromaDB vector search
* Real-time web search
* MCP-based external research tools
* Google Books integration
* Internet Archive integration
* Crossref academic search
* Tavily Search integration
* SQLite authentication
* CAPTCHA verification
* Admin database tools
* FastAPI backend
* Flask web interface
* Optional local Ollama support
* Local Llama 3.2 3B execution without a cloud LLM API key

---

# Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the implementation.
5. Commit your changes.
6. Push the branch.
7. Create a Pull Request.

---

# Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

<p align="center">

<strong>Multi-Source MCP & RAG Research Chatbot</strong>

</p>
