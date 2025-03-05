import sys
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

with open(sys.argv[1], "rb") as f:
    aes_key = f.read()

for file in os.listdir():
    if not file.endswith(".txt.encrypted"): continue

    with open(file, "rb") as f:
        encrypted_text = f.read()
    iv = encrypted_text[:16]
    ciphertext = encrypted_text[16:]

    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    decrypted_text = unpad(aes_cipher.decrypt(ciphertext), AES.block_size)
    with open(file[:-len(".encrypted")], "wb") as f:
        f.write(decrypted_text)
    
    os.remove(file)
