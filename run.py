import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "bissamsekele123"
messages = []


def add_messages(username, message):
    """ Add messages to the `messages` list"""
    now = datetime.now().strftime("%B %d, %H:%M:%S")
    messages_dict = {"timestamp": now, "from": username, "message": message}
    messages.append(messages_dict)


@app.route("/", methods=["GET", "POST"])
def index():
    """ Main page with instruction """
    if request.method == "POST":
        session["username"] = request.form["username"]
    if "username" in session:
        return redirect("/"+session["username"])
    return render_template("index.html")


@app.route("/<username>", methods=["GET", "POST"])
def user(username):
    """Display chat messages"""
    if request.method == "POST":
        message = request.form["message"]
        add_messages(username, message)
        return redirect("/"+username)
    return render_template("chat.html",
                           username=username, chat_messages=messages)


@app.route("/<username>/<message>")
def send_message(username, message):
    """Create a new message and redirect back to chat page"""
    add_messages(username, message)
    return redirect("/" + username)


@app.route("/clear")
def clear():
    """clear all messages """
    messages.clear()
    return redirect("/"+session["username"])


@app.route("/logout")
def logout():
    """log out from session """
    session.clear()
    return redirect("/")


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", "5000")),
    debug=False)
