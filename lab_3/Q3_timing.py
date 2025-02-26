import time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

def time_rsa(key_length):
    print(f"\nKey length: {key_length} bits")

    t0 = time.time()
    key = RSA.generate(key_length)
    t1 = time.time()
    print(f"Keygen time: {t1 - t0} sec")

    message = b"This is a message to be signed"
    h = SHA256.new(message)

    rsa_sig = pkcs1_15.new(key)
    t0 = time.time()
    signature = rsa_sig.sign(h)
    t1 = time.time()
    print(f"Signature time: {t1 - t0} sec")

    t0 = time.time()
    rsa_sig.verify(h, signature)
    t1 = time.time()
    print(f"Verify time: {t1 - t0} sec")

if __name__ == "__main__":
    for key_length in (1024, 2048):
        time_rsa(key_length)
