from flask import Flask, render_template, request, redirect, url_for, session
import requests
import string
import random

app = Flask(__name__)
app.secret_key = "hello"


@app.route("/")
def login():
    captcha = "".join(random.choices(string.ascii_letters, k=5))
    session["token"] = captcha
    return render_template("login.html", captch=captcha)

@app.route("/login_accesss", methods=["POST", "GET"])
def login_access():
    if request.method=="POST":
        user=request.form["nm"]
        password=request.form["pass"]
        captcha=request.form["cap"]
        response=requests.post("http://127.0.0.1:8000/login",json={"username": user,"password": password})
        data=response.json()
        if captcha==session["token"]:
            if "username" in data:
                session["user"]=data["username"]
                return redirect(url_for("chat"))
            else:
                captcha = "".join(random.choices(string.ascii_letters, k=5))
                session["token"] = captcha
                return render_template("login.html",error="Invalid Credentials",captch=captcha)
        else:
            captcha = "".join(random.choices(string.ascii_letters, k=5))
            session["token"] = captcha
            return render_template("login.html",error="Invalid Captcha",captch=captcha)
    return render_template("login.html")
@app.route("/chat", methods=["POST", "GET"])
def chat():
    if "messages" not in session:
        session["messages"]=[]
    if request.method=="POST":
        user=request.form["chat_in"]
        response=requests.post("http://127.0.0.1:8000/chatts",
        json={"user_in": user,"bot_in":""})
        print(response.status_code)
        print(response.text)
        data = response.json()
        messages = session["messages"]
        messages.append(
            {
                "side": "right",
                "text": user
            }
        )
        if "bot_input" in data:
            messages.append(
                {
                    "side": "left",
                    "text": data["bot_input"]
                }
            )
        else:
            messages.append(
                {
                    "side": "left",
                    "text": data["error"]
                }
            )
        session["messages"] = messages
    return render_template("home.html",messages=session["messages"],user=session.get("user"))


if __name__ == "__main__":
    app.run(debug=True)