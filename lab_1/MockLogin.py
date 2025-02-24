import sys

if __name__ == "__main__":
    username, password = sys.argv[1], sys.argv[2]

    if password == "dragon1":
        print("Login successful.")
    else:
        print("Login failed: incorrect password.")
