from fastapi import FastAPI
import sqlite3
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents.middleware import PIIMiddleware
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from RAG_pipline import RAGRetriever , Embedding , VectorStore
embedding_model = Embedding()
vector_store = VectorStore()
retriever = RAGRetriever(vector_store, embedding_model)
#from langchain.memory import ConversationBufferMemory

load_dotenv()

app = FastAPI()




class Login(BaseModel):
    username: str
    password: str




class Chart(BaseModel):
    user_name:str=Field(description="The name of the user")
    user_in: str=Field(description="The input from the user")
    bot_in: str=Field(description="The output from the bot")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.6,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

class State(TypedDict):
    messages:Annotated[list,add_messages]

graph=StateGraph(State)

def chat(state: State) -> State:
    return ({"messages":[lllm.invoke(state["messages"])]})



'''@tool
def search(query: str) -> str:
    """Search for a query."""
    return f"Searching for {query} on Google"'''


memory=MemorySaver()

@tool
def document(query: str) -> str:
    """Retrieve information from the documents."""

    results = retriever.retrieve(query)

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
    """Search the web using DuckDuckGo for current information."""
    duck = DuckDuckGoSearchRun()
    return duck.invoke(query)



@tool
def daatabase()->str:
    "retrive all the username from database"
    conn=sqlite3.connect("Database.db")
    con=conn.cursor()
    con.execute("SELECT USERNAME FROM AUTHENTICATION")
    a=con.fetchall()
    con.close()
    return str(a)

@tool
def delete(username:str)->str:
    "delete the username from the database"
    conn=sqlite3.connect("Database.db")
    con=conn.cursor()
    con.execute("DELETE FROM AUTHENTICATION WHERE USERNAME=?", (username,))
    delete=con.rowcount
    conn.commit()
    con.close()
    if delete>0:
        return f"Deleted {username}"
    else:
        return f"No {username} found"


tools=[search,daatabase,delete,document]

lllm=llm.bind_tools(tools)

###graph

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


@app.post("/login")
def check_user(user:Login):
    conn=sqlite3.connect("Database.db")
    cur=conn.cursor()
    cur.execute(
        "SELECT * FROM AUTHENTICATION WHERE USERNAME=? AND PASSWORD=?",
        (user.username, user.password)
    )
    data=cur.fetchone()
    conn.close()

    if data:
        return {"username": user.username}
    return {"error": "Invalid Credentials"}


@app.post("/chatts")
def chatt(cha:Chart):
    try:
        response = langgraph.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": cha.user_in
                    }
                ]
            },{
            "configurable":{
                    "thread_id":cha.user_name
                }
            }
        )
        print(response)
        bot_reply = response["messages"][-1].content
        if isinstance(bot_reply, list):
            bot_reply = bot_reply[0]["text"]
        return {
            "user_input": cha.user_in,
            "bot_input": bot_reply
        }
    except Exception as e:
        print(e)
        return {"error": str(e)}