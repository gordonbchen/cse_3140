from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import MD5

# Read ciphertext.
q5_files = Path("../Q5files")
with open(q5_files / "Encrypted5", "rb") as f:
    encrypted = f.read()
iv = encrypted[:16]
ciphertext = encrypted[16:]

# Get key (copied from R5.py).
BLOCKSIZE = 2048
h = MD5.new()
count = 0

with open(q5_files/ 'R5.py' , 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        count = count + 1
        h.update(buf)
        buf = afile.read(BLOCKSIZE)
key = h.digest()

# Decrypt cyphertext using key.
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
print(plaintext.decode())
