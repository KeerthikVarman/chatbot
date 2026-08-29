Multi_Source_MCP_RAG_README_AutomatedShelf_Structure.md


Multi-Source MCP & RAG Research Chatbot








A full-stack stateful AI research assistant built with LangGraph, FastAPI, Flask, ChromaDB RAG, and Model Context Protocol (MCP) integration. It enables natural-language querying over local PDF documents, real-time web search, user authentication, database administration, and academic/book discovery through Google Books, Internet Archive, Crossref, and Tavily Search.

🌟 Key Features
1. Agentic LangGraph Workflow
The chatbot uses a stateful LangGraph StateGraph to manage multi-turn conversations.

Multi-turn stateful conversation

User session state persistence using MemorySaver

Tool calling and tool selection

Groq LLM using openai/gpt-oss-120b

Optional local Ollama support using Llama-3.2-3B

2. Retrieval-Augmented Generation (RAG)
The RAG pipeline allows the chatbot to answer questions from uploaded PDF documents.

PDF loading using PyMuPDFLoader

Text extraction using fitz

Text chunking using RecursiveCharacterTextSplitter

Dense embeddings using SentenceTransformer

all-MiniLM-L6-v2 embedding model

Persistent vector storage using ChromaDB

Semantic similarity search

3. Model Context Protocol (MCP) Integration
A custom FastMCP stdio server exposes external research tools.

Google Books API — book descriptions, publication metadata, categories, and authors

Internet Archive API — public texts, historical documents, books, and archives

Crossref API — academic paper metadata, DOIs, and publishers

Tavily Search API — live web search and structured results

4. Real-Time Web Search
The chatbot integrates DuckDuckGoSearchRun for live internet queries.

5. Authentication & Admin Tools
The application provides an SQLite-backed authentication system.

User credential storage

Login validation

Flask authentication interface

CAPTCHA verification

Session tracking

Admin database queries

User account deletion

🏗️ Architecture Overview
Flask Web UI
     │
     ▼
FastAPI Backend
     │
     ▼
LangGraph Agent
     │
 ┌───┼───────────────┐
 ▼   ▼               ▼
RAG Web Search   Database
 │   │               │
 └───┼───────────────┘
     ▼
MCP Server
 │
 ├── Google Books
 ├── Internet Archive
 ├── Crossref
 └── Tavily Search
     │
     ▼
  Final Response
📂 Project Structure
Multi-Source-MCP-RAG-Research-Chatbot/
│
├── Database.py
├── Database.db
├── RAG_pipline.py
├── mainfastapi.py
├── mainflask.py
├── internet_archive_mcp.py
├── insert.py
├── requirement.txt
│
├── data/
│   ├── pdf/
│   └── vector_store/
│
└── templates/
    ├── login.html
    ├── home.html
    └── chat.html
Important Files
File	Description
Database.py	SQLite database schema initialization
Database.db	SQLite database for user credentials
RAG_pipline.py	PDF loading, chunking, embeddings, and ChromaDB RAG logic
mainfastapi.py	FastAPI server, LangGraph agent, tools, and MCP client
mainflask.py	Flask web frontend for authentication and chat
internet_archive_mcp.py	MCP server for Google Books, Internet Archive, Crossref, and Tavily
insert.py	Inserts initial users into the SQLite database
requirement.txt	Python package dependencies
data/pdf/	Input PDF directory
data/vector_store/	ChromaDB persistence directory
templates/login.html	Login and CAPTCHA page
templates/home.html	Main chatbot interface
templates/chat.html	Chat component
🛠️ Prerequisites
Before installing the project, make sure the following are available:

Python 3.10+

Git

Ollama — optional, when using the local Llama-3.2-3B model

Internet connection for external APIs and web-search tools

📦 Installation
Step 1: Clone the Repository
Open a terminal and clone the project:

git clone <YOUR_GITHUB_REPOSITORY_URL>
Move into the project directory:

cd Multi-Source-MCP-RAG-Research-Chatbot
Step 2: Create a Virtual Environment
Create a virtual environment:

python -m venv .venv
Step 3: Activate the Virtual Environment
Windows PowerShell:

.venv\Scripts\Activate.ps1
Windows Command Prompt:

.venv\Scripts\activate
Linux/macOS:

source .venv/bin/activate
After activation, the terminal should show:

(.venv)
Step 4: Install Dependencies
Install all packages from the project's dependency file:

pip install -r requirement.txt
Step 5: Verify Installation
You can verify that the main packages are available:

pip list
🔐 Environment Configuration
Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here
GOOGLE_BOOKS_API_KEY=your_google_books_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
The application uses these credentials for the corresponding external services.

Never upload .env, API keys, or other credentials to GitHub.

Add .env to .gitignore:

.env
🗄️ Database Setup
Initialize the SQLite database:

python Database.py
Then insert the initial users:

python insert.py
The supplied project documentation lists these seed credentials:

admin   / admin123
keerti  / keerti123
aniket  / aniket123
tushar  / tushar123
For a real deployment, replace default credentials with secure credentials.

📚 RAG Document Setup
Create or use the following directory:

data/pdf/
Place the PDF documents that you want the chatbot to search inside data/pdf/.

Then run:

python RAG_pipline.py
The pipeline loads the PDFs, splits the text into chunks, generates embeddings, and stores the vectors in:

data/vector_store/
🚀 Running the Application
The project uses two application servers: FastAPI for the backend and Flask for the web interface.

Step 1: Start FastAPI
Open a terminal with the virtual environment activated:

uvicorn mainfastapi:app --reload --port 8000
The FastAPI server runs at:

http://127.0.0.1:8000
API documentation:

http://127.0.0.1:8000/docs
Step 2: Start Flask
Open a second terminal, activate the same virtual environment, and run:

python mainflask.py
The Flask web interface runs at:

http://127.0.0.1:5000
Open the Flask URL in your browser to use the chatbot.

🔄 Application Workflow
User
 │
 ▼
Flask Login / Chat UI
 │
 ▼
FastAPI
 │
 ▼
LangGraph Agent
 │
 ├── PDF Question ──► ChromaDB RAG
 │
 ├── Web Question ──► DuckDuckGo / Tavily
 │
 ├── Book Search ───► Google Books
 │
 ├── Archive Search ► Internet Archive
 │
 ├── Paper Search ──► Crossref
 │
 └── Admin Request ─► SQLite
 │
 ▼
Response
🧰 Agent Tools Reference
Tool Name	Source Module	Description
document	RAG_pipline.py	Semantic search across uploaded PDF documents
search	DuckDuckGoSearchRun	Live web search
daatabase	mainfastapi.py	Retrieves registered usernames
delete	mainfastapi.py	Removes a specific user
search_books	internet_archive_mcp.py	Searches Google Books
search_internet_archive	internet_archive_mcp.py	Searches Internet Archive
search_crossref	internet_archive_mcp.py	Searches Crossref academic metadata
tavily_search	internet_archive_mcp.py	Performs Tavily live search
🔌 API Endpoints
POST /login
Authenticates a user against the SQLite database.

Request:

{
  "username": "keerti",
  "password": "keerti123"
}
Response:

{
  "username": "keerti"
}
or:

{
  "error": "Invalid Credentials"
}
POST /chatts
Sends a user message to the stateful LangGraph agent.

Request:

{
  "user_name": "keerti",
  "user_in": "Summarize the key points in the uploaded document."
}
Response:

{
  "user_input": "Summarize the key points in the uploaded document.",
  "bot_input": "Based on the uploaded documents..."
}
🖥️ Web Interface
Login Page
Provides:

User authentication

CAPTCHA verification

Session handling

Chat Interface
Allows users to send natural-language questions to the LangGraph research assistant.

Depending on the question, the agent can use:

Uploaded PDF documents

Web search

Google Books

Internet Archive

Crossref

Tavily

Database administration tools

🧪 Testing & Verification
The supplied project README does not define a separate automated test script.

After installation, verify the application by:

Successfully initializing the database.

Running the RAG pipeline with at least one PDF.

Starting FastAPI without errors.

Starting Flask without errors.

Opening the login page.

Logging in with a configured account.

Sending a chatbot query.

Testing an appropriate RAG or external-search query.

🐛 Troubleshooting
Dependency Installation Error
Make sure the virtual environment is activated:

(.venv)
Then reinstall dependencies:

pip install -r requirement.txt
FastAPI Not Starting
Check that the command is run from the project root:

uvicorn mainfastapi:app --reload --port 8000
Flask Not Starting
Run the Flask application in a separate terminal:

python mainflask.py
RAG Returns No Results
Verify:

data/pdf/
data/vector_store/
Then rerun:

python RAG_pipline.py
API Key Error
Check the .env file:

GROQ_API_KEY
GOOGLE_BOOKS_API_KEY
TAVILY_API_KEY
Make sure the variable names match the application configuration.

Ollama Model Issue
Ollama is optional. If using the local Llama-3.2-3B model, make sure Ollama is installed and the required model is available locally.

🌟 Advantages
Stateful multi-turn AI conversations

Retrieval-Augmented Generation over local PDFs

Persistent ChromaDB vector search

Real-time web search

MCP-based external research tools

Google Books integration

Internet Archive integration

Crossref academic search

Tavily search integration

SQLite authentication

CAPTCHA verification

Admin database tools

FastAPI backend

Flask web interface

Optional local Ollama support

🔮 Future Improvements
The supplied project documentation does not define specific future improvements. Potential extensions should be documented separately when they become part of the implementation.

🤝 Contributing
Contributions can be managed through the standard Git workflow:

Fork the repository.

Create a feature branch.

Make your changes.

Test the changes.

Commit the changes.

Push the branch.

Create a Pull Request.

📄 License
This project is open-source and available under the MIT License.

⭐ Support
If you find this project useful, consider giving the repository a ⭐ on GitHub.

<p align="center">

⭐ <strong>Multi-Source MCP & RAG Research Chatbot</strong>
