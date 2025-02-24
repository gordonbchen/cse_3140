import subprocess
from datetime import datetime
from pathlib import Path
import hashlib

Q_NUM = 6
Q_DIR = Path(f"Q{Q_NUM}")
LOGIN_SCRIPT = Q_DIR / "Login.pyc"

def get_login_dict():
    with open(Q_DIR / "gang", "r") as f:
        usernames = f.read().split()
    login_dict = {u: list() for u in usernames}

    with open(Q_DIR / "PwnedPWs100k", "r") as f:
        passwords = f.read().split()

    # Find matching hashed passwords.
    with open(Q_DIR / "SaltedPWs", "r") as f:
        lines = f.read().split()
    for l in lines:
        username, salt, hashed_pass = l.split(",")
        if username not in login_dict:
            continue

        password = find_password(salt, hashed_pass, passwords)
        if password:
            login_dict[username].append(password)

    return login_dict

def find_password(salt, hashed_pass, passwords):
    for password in passwords:
        for i in range(10):
            p = f"{salt}{password}{i}"
            h = hashlib.sha256()
            h.update(bytes(p, "utf-8"))
            
            if h.hexdigest() == hashed_pass:
                return p[len(salt):]

def try_passwords(username, passwords):
    for i, password in enumerate(passwords):
        output = subprocess.run(["python3", LOGIN_SCRIPT, username, password], capture_output=True, text=True)
        if "Login successful" in output.stdout:
            return password

if __name__ == "__main__":
    print(f"Start time: {datetime.now()}\n")

    login_dict = get_login_dict()
    for username, passwords in login_dict.items():
        print(f"{username:25s}{str(len(passwords)):5s}", end="")

        password = try_passwords(username, passwords)
        if password is None:
            print("FAILED")
        else:
            print(password)

    print(f"\nEnd time: {datetime.now()}")
