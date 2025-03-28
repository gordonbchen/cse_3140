import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

rsa_private_key = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""
rsa_key = RSA.import_key(rsa_private_key)
rsa_cipher = PKCS1_OAEP.new(rsa_key)

with open(sys.argv[1], "rb") as f:
    decrypted_text = rsa_cipher.decrypt(f.read())

with open("DecryptedSharedKey", "wb") as f:
    f.write(decrypted_text)
