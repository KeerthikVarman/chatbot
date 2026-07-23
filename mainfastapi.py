from fastapi import FastAPI
import sqlite3
import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents.middleware import ModelFallbackMiddleware
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents.middleware import PIIMiddleware
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

'''@tool
def search(query: str) -> str:
    """Search for a query."""
    return f"Searching for {query} on Google"'''


memory=MemorySaver()
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


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.6,
    google_api_key=os.getenv("GEMINI_API_KEY")
)




agent = create_agent(
    model=llm,
    tools=[search,daatabase,delete],
    checkpointer=memory,
    middleware=[
        ModelFallbackMiddleware( 
            "groq:llama-3.1-8b-instant",# Fallback model
        ),
        HumanInTheLoopMiddleware(
            interrupt_on={
                "delete":{
                    "allowed_decision":
                        ["approve", "reject"]
                }
            }
        ),
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True
            )

    ]
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
        response = agent.invoke(
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