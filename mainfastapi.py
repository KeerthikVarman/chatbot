from fastapi import FastAPI
from contextlib import asynccontextmanager
import sqlite3
import os
import sys
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import AnyMessage, SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langchain_mcp_adapters.client import MultiServerMCPClient
from RAG_pipline import RAGRetriever, Embedding, VectorStore

load_dotenv()

embedding_model = Embedding()
vector_store = VectorStore()
retriever = RAGRetriever(vector_store, embedding_model)

class Login(BaseModel):
    username: str
    password: str

class Chart(BaseModel):
    user_name: str = Field(description="The name of the user")
    user_in: str = Field(description="The input from the user")
    bot_in: str = Field(default="", description="The output from the bot")

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

ollama = ChatOllama(
    model="hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:latest",
    temperature=0
)

memory = MemorySaver()
lllm = None
langgraph = None

@tool
def document(query: str) -> str:
    """
    Retrieve information from the user's documents.
    Use this tool when the user asks about information contained in uploaded documents.
    """
    results = retriever.retrieve(query)
    if not results:
        return "No relevant information was found in the documents."
    response = ""
    for doc in results:
        response += (
            f"Source: {doc['metadata'].get('source_file')}\n"
            f"Page: {doc['metadata'].get('page')}\n"
            f"Content: {doc['document']}\n\n"
        )
    return response

@tool
def search(query: str) -> str:
    """
    Search the internet using DuckDuckGo.
    Use this only when current, online, or web information is required.
    Do not use this tool for greetings or simple casual conversation.
    """
    duck = DuckDuckGoSearchRun()
    return duck.invoke(query)

@tool
def daatabase() -> str:
    """
    Retrieve all usernames from the authentication database.
    """
    conn = sqlite3.connect("Database.db")
    con = conn.cursor()
    con.execute("SELECT USERNAME FROM AUTHENTICATION")
    data = con.fetchall()
    con.close()
    conn.close()
    return str(data)

@tool
def delete(username: str) -> str:
    """
    Delete a username from the authentication database.
    """
    conn = sqlite3.connect("Database.db")
    con = conn.cursor()
    con.execute(
        "DELETE FROM AUTHENTICATION WHERE USERNAME=?",
        (username,)
    )
    deleted = con.rowcount
    conn.commit()
    con.close()
    conn.close()
    if deleted > 0:
        return f"Deleted {username}"
    return f"No {username} found"

client = MultiServerMCPClient({
    "internet_archive": {
        "transport": "stdio",
        "command": sys.executable,
        "args": ["internet_archive_mcp.py"]
    }
})

async def chat(state: State) -> State:
    global lllm
    system_message = SystemMessage(
        content="""
You are a helpful AI assistant.

Follow these rules:
1. For greetings and casual conversation, answer directly.
2. Do not use the web search tool for greetings or casual messages.
3. Use the document tool when the user asks about information in the uploaded documents.
4. Use the web search tool only when current or online information is required.
5. Use database tools only when the user asks about database information.
6. Use delete only when the user explicitly asks to delete a username.
7. Use Internet Archive tools when the user asks to search for books or Internet Archive content.
8. If no tool is required, answer directly.
"""
    )
    messages = [system_message] + state["messages"]
    response = await lllm.ainvoke(messages)
    return {"messages": [response]}

@asynccontextmanager
async def lifespan(app: FastAPI):
    global lllm, langgraph

    print("Starting MCP client...")

    mcp_tools = await client.get_tools()

    print("\nMCP tools loaded:")
    for t in mcp_tools:
        print("   ", t.name)

    tools = [
        search,
        daatabase,
        delete,
        document
    ] + mcp_tools

    print("\nAll tools:")
    for t in tools:
        print("   ", t.name)

    lllm = llm.bind_tools(tools)

    graph = StateGraph(State)

    graph.add_node("chat", chat)
    graph.add_node("tools", ToolNode(tools))

    graph.add_edge(START, "chat")

    graph.add_conditional_edges(
        "chat",
        tools_condition
    )

    graph.add_edge("tools", "chat")

    langgraph = graph.compile(
        checkpointer=memory
    )

    print("\nLangGraph + RAG + MCP + Groq ready!")

    yield

    print("\nApplication shutting down...")

app = FastAPI(lifespan=lifespan)

@app.post("/login")
def check_user(user: Login):
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM AUTHENTICATION
        WHERE USERNAME=? AND PASSWORD=?
        """,
        (user.username, user.password)
    )

    data = cur.fetchone()
    conn.close()

    if data:
        return {"username": user.username}

    return {"error": "Invalid Credentials"}

@app.post("/chatts")
async def chatt(cha: Chart):
    try:
        response = await langgraph.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": cha.user_in
                    }
                ]
            },
            {
                "configurable": {
                    "thread_id": cha.user_name
                }
            }
        )

        print(response)

        bot_reply = response["messages"][-1].content

        if isinstance(bot_reply, list):
            if bot_reply and isinstance(bot_reply[0], dict):
                bot_reply = bot_reply[0].get("text", str(bot_reply))
            else:
                bot_reply = str(bot_reply)

        return {
            "user_input": cha.user_in,
            "bot_input": bot_reply
        }

    except Exception as e:
        print("ERROR:", e)
        return {
            "error": str(e)
        }