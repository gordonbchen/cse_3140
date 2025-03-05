from Crypto.PublicKey import RSA

rsa_key = RSA.generate(3072)

with open("e.key", "wb") as f:
    f.write(rsa_key.public_key().export_key())

with open("d.key", "wb") as f:
    f.write(rsa_key.export_key())

