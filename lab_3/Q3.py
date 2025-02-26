from pathlib import Path
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

if __name__ == "__main__":
    with open("../Q3pk.pem", "r") as f:
        public_key = f.read()
    key = RSA.import_key(public_key)
    
    q3_dir = Path("../Q3files/")
    for file in q3_dir.glob("*.exe"):
        with open(file, "rb") as f:
            contents = f.read()
        h = SHA256.new(contents)
        
        with open(f"{file}.sign", "rb") as f:
            signature = f.read()

        try:
            pkcs1_15.new(key).verify(h, signature)
        except Exception as e:
            print(e)
            continue

        print(file.name)

