from fastapi import FastAPI
import sqlite3
import os
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

app = FastAPI()


class Login(BaseModel):
    username: str
    password: str


class Chart(BaseModel):
    user_in: str
    bot_in: str

'''@tool
def search(query: str) -> str:
    """Search for a query."""
    return f"Searching for {query} on Google"'''

search=DuckDuckGoSearchRun()


@tool
def daatabase()->str:
    "retrive all the username from database"
    conn=sqlite3.connect("Database.db")
    con=conn.cursor()
    con.execute("SELECT USERNAME FROM AUTHENTICATION")
    a=con.fetchall()
    con.close()
    return str(a)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.6,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

agent = create_react_agent(
    model=llm,
    tools=[search,daatabase]
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