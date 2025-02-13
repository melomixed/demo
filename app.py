from flask import Flask, render_template, request, redirect, session
from db import create_user, get_user, get_user_by_username, create_thread, get_threads, like_thread, add_comment
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")

# Define your routes
@app.route("/")
def home():
    threads = get_threads()
    return render_template("index.html", threads=threads, session=session)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = get_user(email)
        if user and user["password"] == password:
            session["username"] = user["username"]
            return redirect("/")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        create_user(username, email, password)
        return redirect("/login")
    return render_template("signup.html")

@app.route("/post", methods=["POST"])
def post_thread():
    if "username" in session:
        content = request.form["content"]
        create_thread(session["username"], content)
    return redirect("/")

@app.route("/like/<thread_id>")
def like(thread_id):
    if "username" in session:
        like_thread(thread_id, session["username"])
    return redirect("/")

@app.route("/comment/<thread_id>", methods=["POST"])
def comment(thread_id):
    if "username" in session:
        comment = request.form["comment"]
        add_comment(thread_id, session["username"], comment)
    return redirect("/")

@app.route("/user/<username>")
def user_profile(username):
    user = get_user_by_username(username)
    if user:
        threads = db.threads.find({"username": username})
        return render_template("profile.html", user=user, threads=threads)
    return "User not found", 404
