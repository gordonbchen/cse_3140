import os
from Crypto.Hash import SHA256

if __name__ == "__main__":
    with open("../Q2hash.txt", "r") as f:
        target_hash = f.read()
    print(f"Target: {target_hash}")

    files = os.listdir("../Q2files")
    for filename in files:
        with open(f"../Q2files/{filename}", "rb") as f:
            contents = f.read()
        hash_obj = SHA256.new(data=contents)
        h = hash_obj.hexdigest()
        if h == target_hash:
            print(f"Matching file: {filename}")
            break
