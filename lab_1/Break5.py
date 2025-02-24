import subprocess
from datetime import datetime
from pathlib import Path
import hashlib

Q_NUM = 5
Q_DIR = Path(f"Q{Q_NUM}")
LOGIN_SCRIPT = Q_DIR / "Login.pyc"

def get_login_dict():
    with open(Q_DIR / "gang", "r") as f:
        usernames = f.read().split()
    login_dict = {u: set() for u in usernames}

    # Caculate hashed passwords with 2 random nums at the end.
    with open(Q_DIR / "PwnedPWs100k", "r") as f:
        passwords = f.read().split()

    hash_password_dict = {}
    for n, password in enumerate(passwords):
        if( n % 1_000 == 0) or (n == len(passwords) - 1):
            print(f"\rHashed {n+1} / {len(passwords)} passwords. ", end="")

        for i in range(10):
            for j in range(10):
                p = f"{password}{i}{j}"
                h = hashlib.sha256()
                h.update(bytes(p, "utf-8"))
                hash_password_dict[h.hexdigest()] = p
    print("\n")

    # Find all matching hashed passwords.
    with open(Q_DIR / "HashedPWs", "r") as f:
        lines = f.read().split()
    for l in lines:
        u,hp = l.split(",")
        if (u in login_dict) and (hp in hash_password_dict):
            login_dict[u].add(hash_password_dict[hp])

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
