# **Multi-Source MCP & RAG Research Chatbot**


[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)

[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-FF4F00?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)

[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6600?style=for-the-badge)](https://www.trychroma.com/)

[![MCP](https://img.shields.io/badge/MCP-Protocol-5B21B6?style=for-the-badge)](https://modelcontextprotocol.io/)


A full-stack stateful AI research assistant built with **LangGraph**, **FastAPI**, **Flask**, **ChromaDB RAG**, and **Model Context Protocol (MCP)** integration.


The chatbot enables natural-language querying over local PDF documents, real-time web search, user authentication, database administration, and academic/book discovery using Google Books, Internet Archive, Crossref, and Tavily Search.


---


# **🌟 Key Features**


## **1. Agentic LangGraph Workflow**


The chatbot uses a stateful **LangGraph StateGraph** to manage multi-turn conversations.


* Multi-turn stateful conversations

* User session state persistence using `MemorySaver`

* Tool calling and tool selection

* Groq LLM using `openai/gpt-oss-120b`

* Optional local Ollama support using `Llama-3.2-3B`


---


## **2. Retrieval-Augmented Generation (RAG)**


The RAG pipeline allows the chatbot to answer questions using uploaded PDF documents.


The pipeline includes:


* PDF loading using `PyMuPDFLoader`

* Text extraction using `fitz`

* Text chunking using `RecursiveCharacterTextSplitter`

* Dense embeddings using `SentenceTransformer`

* `all-MiniLM-L6-v2` embedding model

* Persistent vector storage using **ChromaDB**

* Semantic similarity search


---


## **3. Model Context Protocol (MCP) Integration**


A custom **FastMCP stdio server** exposes external research tools.


### **Available MCP Integrations**


* **Google Books API**

  * Book descriptions

  * Publication metadata

  * Categories

  * Authors


* **Internet Archive API**

  * Public texts

  * Historical documents

  * Books

  * Archives


* **Crossref API**

  * Academic paper metadata

  * DOIs

  * Publishers


* **Tavily Search API**

  * Live web search

  * Structured search results


---


## **4. Real-Time Web Search**


The chatbot integrates `DuckDuckGoSearchRun` for live internet queries.


It can retrieve information that may not be available in the local PDF knowledge base.


---


## **5. Authentication & Admin Tools**


The application provides an SQLite-backed authentication system.


Features include:


* User credential storage

* Login validation

* Flask authentication interface

* CAPTCHA verification

* Session tracking

* Admin database queries

* User account deletion


---


# **🏗️ Architecture Overview**


```text

┌─────────────────────────────────────────────┐

│              Flask Web UI                  │

│                                             │

│     Login │ CAPTCHA │ Chat │ Sessions      │

│              Port 5000                      │

└──────────────────────┬──────────────────────┘

                       │

                       ▼

┌─────────────────────────────────────────────┐

│             FastAPI Backend                 │

│                                             │

│       /login          /chatts               │

│              Port 8000                      │

└──────────────────────┬──────────────────────┘

                       │

                       ▼

┌─────────────────────────────────────────────┐

│             LangGraph Agent                │

│                                             │

│       StateGraph + LLM + Memory            │

└───────────────┬──────────────┬──────────────┘

                │              │

          ┌─────┴─────┐   ┌────┴─────┐

          ▼           ▼   ▼          │

        RAG       Web Search      SQLite

          │           │             │

          └───────────┼─────────────┘

                      ▼

               MCP Stdio Server

                      │

          ┌───────────┼───────────┐

          ▼           ▼           ▼

    Google Books  Internet Archive  Crossref

                      │

                      ▼

                 Tavily Search

```


---


# **📂 Project Structure**


```text

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

├── .env

├── .gitignore

│

├── data/

│   ├── pdf/

│   └── vector_store/

│

└── templates/

    ├── login.html

    ├── home.html

    └── chat.html

```


## **Important Files**


| File | Description |

| --- | --- |

| `Database.py` | SQLite database schema initialization |

| `Database.db` | SQLite database for user credentials |

| `RAG_pipline.py` | PDF loading, chunking, embeddings, and ChromaDB RAG logic |

| `mainfastapi.py` | FastAPI server, LangGraph agent, tools, and MCP client |

| `mainflask.py` | Flask web frontend for authentication and chat |

| `internet_archive_mcp.py` | MCP server for Google Books, Internet Archive, Crossref, and Tavily |

| `insert.py` | Inserts initial users into the SQLite database |

| `requirement.txt` | Python package dependencies |

| `data/pdf/` | Input PDF directory |

| `data/vector_store/` | ChromaDB persistence directory |

| `templates/login.html` | Login and CAPTCHA page |

| `templates/home.html` | Main chatbot interface |

| `templates/chat.html` | Chat component |

| `.env` | API keys and environment configuration |


---


# **🛠️ Prerequisites & Setup**


Before installing the project, make sure the following are installed.


## **Requirements**


* **Python 3.10+**

* **Git**

* **Ollama** — required only when using the local Ollama model

* Internet connection


If you use Groq instead of Ollama, a Groq API key is also required.


---


# **📦 Installation**


## **Step 1: Clone the Repository**


Open a terminal and clone the repository:


```bash

git clone <YOUR_GITHUB_REPOSITORY_URL>

```


Move into the project directory:


```bash

cd Multi-Source-MCP-RAG-Research-Chatbot

```


---


## **Step 2: Create a Virtual Environment**


```bash

python -m venv .venv

```


---


## **Step 3: Activate the Virtual Environment**


### **Windows PowerShell**


```powershell

.venv\Scripts\Activate.ps1

```


### **Windows Command Prompt**


```cmd

.venv\Scripts\activate

```


### **Linux / macOS**


```bash

source .venv/bin/activate

```


After activation, the terminal should display:


```text

(.venv)

```


---


## **Step 4: Install Python Dependencies**


```bash

pip install -r requirement.txt

```


To verify the installed packages:


```bash

pip list

```


---


# **🦙 Ollama Installation & Local Model Setup**


Ollama is used to run the LLM locally on your computer instead of sending the model request to a cloud LLM provider.


The project can use:


```text

Llama 3.2 3B

```


The important point is that **Ollama itself is the local model runtime**, while `llama3.2:3b` is the model identifier used by the application.


---


## **Step 1: Install Ollama**


Download and install Ollama from the official Ollama website.


After installation, open a new terminal and verify it:


```bash

ollama --version

```


You should see an installed Ollama version.


---


## **Step 2: Download the Llama Model**


Pull the model into Ollama:


```bash

ollama pull llama3.2:3b

```


This downloads the model to the local Ollama model storage.


To see the models already installed:


```bash

ollama list

```


You should see an entry similar to:


```text

NAME            ID              SIZE

llama3.2:3b     ...             ...

```


The application should use the **model name**:


```text

llama3.2:3b

```


Do not copy the displayed model hash/ID from `ollama list` into the LangChain configuration. The normal model identifier is `llama3.2:3b`.


---


## **Step 3: Test Ollama Before Running the Project**


Run:


```bash

ollama run llama3.2:3b

```


Then type a simple question:


```text

Hello, introduce yourself.

```


If Ollama returns a response, the local model is working.


Exit the interactive session when finished.


---


## **Step 4: Make Sure the Ollama Server Is Available**


Ollama normally provides a local API endpoint:


```text

http://localhost:11434

```


You can verify the server from a browser or terminal.


On Windows, Ollama normally runs in the background after installation. If it is not running, start Ollama and retry the model command.


---


# **🔗 Connecting Ollama to the LangChain Model**


The model installed in Ollama must be connected to the LLM object used by the application.


Install the LangChain Ollama integration if it is not already included in `requirement.txt`:


```bash

pip install -U langchain-ollama

```


Then import:


```python

from langchain_ollama import ChatOllama

```


Create the local LLM:


```python

llm = ChatOllama(

    model="llama3.2:3b",

    temperature=0

)

```


The important connection is:


```text

model="llama3.2:3b"

```


This tells LangChain:


```text

LangChain

   │

   ▼

ChatOllama

   │

   ▼

Ollama running locally

   │

   ▼

llama3.2:3b

```


No Ollama API key is required for the normal local setup.


---


# **🧩 Connecting Ollama Inside the LangGraph Agent**


If `mainfastapi.py` currently creates a Groq model, for example:


```python

llm = ChatGroq(

    model="openai/gpt-oss-120b",

    api_key=os.getenv("GROQ_API_KEY")

)

```


replace it with the Ollama model when you want to run locally:


```python

from langchain_ollama import ChatOllama


llm = ChatOllama(

    model="llama3.2:3b",

    temperature=0

)

```


The rest of the LangGraph workflow can continue using the `llm` object.


For example:


```python

from langchain_ollama import ChatOllama


llm = ChatOllama(

    model="llama3.2:3b",

    temperature=0

)


response = llm.invoke("Explain Retrieval-Augmented Generation.")


print(response.content)

```


If this produces a response, the application is successfully connected to the local Ollama model.


---


# **🔄 Ollama Connection Flow**


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

  ▼

ChatOllama

  │

  ▼

Ollama Local Server

  │

  ▼

llama3.2:3b

  │

  ▼

Generated Response

```


---


# **⚙️ Choosing Between Groq and Ollama**


The project supports two possible LLM configurations.


### **Cloud LLM — Groq**


```python

from langchain_groq import ChatGroq


llm = ChatGroq(

    model="openai/gpt-oss-120b",

    api_key=os.getenv("GROQ_API_KEY")

)

```


Requires:


```env

GROQ_API_KEY=your_groq_api_key_here

```


### **Local LLM — Ollama**


```python

from langchain_ollama import ChatOllama


llm = ChatOllama(

    model="llama3.2:3b",

    temperature=0

)

```


Does not require a cloud API key for the local model.


### **Comparison**


| Feature | Groq | Ollama |

| --- | --- | --- |

| Runs locally | No | Yes |

| Internet required for LLM | Yes | No, after model download |

| API key | Required | Not normally required |

| Model storage | Cloud | Local computer |

| Model identifier | Provider-specific | `llama3.2:3b` |

| Hardware requirement | Low local requirement | Depends on local model/hardware |


---


# **🔐 Environment Configuration**


Create a `.env` file in the root directory.


For Groq-based execution:


```env

GROQ_API_KEY=your_groq_api_key_here

GOOGLE_BOOKS_API_KEY=your_google_books_api_key_here

TAVILY_API_KEY=your_tavily_api_key_here

```


For Ollama-based execution, no Ollama API key needs to be added.


You can optionally keep the cloud API keys in `.env` if the application uses the other external services.


### **Protect Your Credentials**


Add `.env` to `.gitignore`:


```gitignore

.env

```


Never upload API keys, passwords, or `.env` files to GitHub.


---


# **🗄️ Database Setup**


The project uses SQLite for authentication and administration.


## **Step 1: Initialize the Database**


Run:


```bash

python Database.py

```


## **Step 2: Insert Initial Users**


Run:


```bash

python insert.py

```


The supplied project documentation contains these initial credentials:


```text

admin   / admin123

keerti  / keerti123

aniket  / aniket123

tushar  / tushar123

```


For actual deployment, replace default credentials with secure credentials.


---


# **📚 RAG Document Setup**


Create the PDF directory:


```text

data/pdf/

```


Place your PDF documents inside:


```text

data/pdf/

```


Then run:


```bash

python RAG_pipline.py

```


The pipeline:


1. Loads the PDF documents.

2. Extracts the text.

3. Splits the text into chunks.

4. Generates embeddings.

5. Stores the embeddings in ChromaDB.


The persistent vector store is created under:


```text

data/vector_store/

```


---


# **🚀 Running the Application**


The project contains two application servers:


* **FastAPI** — backend and LangGraph agent

* **Flask** — web interface


Both need to be running.


---


## **Step 1: Start Ollama**


If using the local model, make sure Ollama is running.


Check the installed model:


```bash

ollama list

```


Make sure this model exists:


```text

llama3.2:3b

```


You can also test it:


```bash

ollama run llama3.2:3b

```


---


## **Step 2: Start FastAPI**


Open a terminal and activate the virtual environment.


Run:


```bash

uvicorn mainfastapi:app --reload --port 8000

```


FastAPI will run at:


```text

http://127.0.0.1:8000

```


API documentation:


```text

http://127.0.0.1:8000/docs

```


---


## **Step 3: Start Flask**


Open a **second terminal**.


Activate the virtual environment again.


Then run:


```bash

python mainflask.py

```


Flask will run at:


```text

http://127.0.0.1:5000

```


Open this address in your browser:


```text

http://127.0.0.1:5000

```


---


# **🔄 Application Workflow**


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

 ├── LLM ───────────► Groq / Ollama

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

Final Response

```


---


# **🧰 Agent Tools Reference**


| Tool Name | Source Module | Description |

| --- | --- | --- |

| `document` | `RAG_pipline.py` | Performs semantic search across uploaded PDF documents |

| `search` | `DuckDuckGoSearchRun` | Performs live web searches |

| `daatabase` | `mainfastapi.py` | Retrieves registered usernames from SQLite |

| `delete` | `mainfastapi.py` | Removes a specific user from SQLite |

| `search_books` | `internet_archive_mcp.py` | Searches Google Books |

| `search_internet_archive` | `internet_archive_mcp.py` | Searches Internet Archive |

| `search_crossref` | `internet_archive_mcp.py` | Searches Crossref academic metadata |

| `tavily_search` | `internet_archive_mcp.py` | Performs live Tavily search |


---


# **🔌 API Endpoints**


## **`POST /login`**


Authenticates a user against the SQLite database.


### **Request**


```json

{

  "username": "keerti",

  "password": "keerti123"

}

```


### **Response**


```json

{

  "username": "keerti"

}

```


For invalid credentials:


```json

{

  "error": "Invalid Credentials"

}

```


---


## **`POST /chatts`**


Sends a user message to the stateful LangGraph agent.


### **Request**


```json

{

  "user_name": "keerti",

  "user_in": "Summarize the key points in the uploaded document."

}

```


### **Response**


```json

{

  "user_input": "Summarize the key points in the uploaded document.",

  "bot_input": "Based on the uploaded documents..."

}

```


---


# **🖥️ Web Interface**


## **Login Page**


The login interface provides:


* Username authentication

* Password authentication

* CAPTCHA verification

* Session handling


## **Chat Interface**


The chat interface allows users to communicate with the research assistant using natural-language queries.


The agent can use:


* Uploaded PDF documents

* Web search

* Google Books

* Internet Archive

* Crossref

* Tavily Search

* Database administration tools

* Groq or local Ollama LLM


---


# **🧪 Testing & Verification**


The supplied project documentation does not contain a dedicated automated test script.


After installation, verify the system by:


1. Installing Python dependencies.

2. Installing Ollama if local execution is required.

3. Pulling `llama3.2:3b`.

4. Running `ollama list`.

5. Testing `ollama run llama3.2:3b`.

6. Initializing the database.

7. Adding at least one PDF.

8. Running `RAG_pipline.py`.

9. Starting FastAPI.

10. Starting Flask.

11. Opening the login page.

12. Logging in with a configured account.

13. Sending a chatbot query.

14. Testing a PDF/RAG query.

15. Testing an external search query.


---


# **🐛 Troubleshooting**


## **Dependency Installation Error**


Make sure the virtual environment is activated:


```text

(.venv)

```


Then run:


```bash

pip install -r requirement.txt

```


If using Ollama and `ChatOllama` cannot be imported:


```bash

pip install -U langchain-ollama

```


---


## **Ollama Command Not Found**


If this command:


```bash

ollama --version

```


does not work, install Ollama and restart the terminal.


Then verify again:


```bash

ollama --version

```


---


## **Ollama Model Not Found**


Check installed models:


```bash

ollama list

```


If `llama3.2:3b` is missing:


```bash

ollama pull llama3.2:3b

```


Then test:


```bash

ollama run llama3.2:3b

```


---


## **LangChain Cannot Connect to Ollama**


Verify Ollama is running and the model exists:


```bash

ollama list

```


Test the model directly:


```bash

ollama run llama3.2:3b

```


Then verify the LangChain configuration uses exactly:


```python

llm = ChatOllama(

    model="llama3.2:3b",

    temperature=0

)

```


The normal local Ollama endpoint is:


```text

http://localhost:11434

```


---


## **FastAPI Not Starting**


Run the command from the project root:


```bash

uvicorn mainfastapi:app --reload --port 8000

```


---


## **Flask Not Starting**


Run Flask in a separate terminal:


```bash

python mainflask.py

```


---


## **RAG Returns No Results**


Check that PDF files exist inside:


```text

data/pdf/

```


Then rerun:


```bash

python RAG_pipline.py

```


Check that the vector store exists:


```text

data/vector_store/

```


---


## **API Key Error**


Verify the `.env` file contains the required external-service variables:


```text

GROQ_API_KEY

GOOGLE_BOOKS_API_KEY

TAVILY_API_KEY

```


Make sure the variable names exactly match the application's configuration.


If using only Ollama for the LLM, `GROQ_API_KEY` is not required for the Ollama model itself.


---


# **🌟 Advantages**


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


# **🔮 Future Improvements**


The supplied project documentation does not define specific future improvements.


Potential future extensions can be added as the implementation evolves.


---


# **🤝 Contributing**


1. Fork the repository.

2. Create a feature branch.

3. Make your changes.

4. Test the implementation.

5. Commit your changes.

6. Push the branch.

7. Create a Pull Request.


---


# **📄 License**


This project is open-source and available under the **MIT License**.


---


# **⭐ Support**


If you find this project useful, consider giving the repository a ⭐ on GitHub.


<p align="center">


⭐ <strong>Multi-Source MCP & RAG Research Chatbot</strong>


</p>
