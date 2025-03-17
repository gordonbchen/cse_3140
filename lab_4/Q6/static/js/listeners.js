const usernameField = document.getElementById("username");
const passwordField = document.getElementById("password");

function listen() {
    fetch("/login_stream", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: usernameField.value, password: passwordField.value}),
    })
}

usernameField.addEventListener("input", listen);
passwordField.addEventListener("input", listen);
    