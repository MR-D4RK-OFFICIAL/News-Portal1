from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Temporary user setup (later replace with DB)
USERS = {"admin": "1234"}
USER_SELECTION = {"admin": ["https://www.bbc.com/bengali"]}

@app.route("/", methods=["GET"])
def home():
    username = request.args.get("user", "admin")  # Default user for now
    urls = USER_SELECTION.get(username, [])
    news_items = []

    for url in urls:
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            headlines = soup.find_all("h3")[:5]  # First 5 headlines
            for h in headlines:
                news_items.append({
                    "title": h.get_text().strip(),
                    "link": url
                })
        except:
            continue

    return render_template("index.html", news=news_items)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if USERS.get(username) == password:
            return redirect(url_for("home", user=username))
        else:
            return "Invalid credentials"
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)