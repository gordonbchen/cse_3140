from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

q4_files = Path("../Q4files")
with open(q4_files / ".key.txt", "rb") as f:
    key = f.read()

with open(q4_files / "Encrypted4", "rb") as f:
    encrypted = f.read()
iv = encrypted[:16]
ciphertext = encrypted[16:]

cipher = AES.new(key, AES.MODE_CBC, iv=iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
print(plaintext.decode())
