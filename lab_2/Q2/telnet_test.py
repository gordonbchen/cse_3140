import telnetlib
import sys

address, username, password = sys.argv[1:]

tn = telnetlib.Telnet(address)
print(tn.read_until(b"login: ").decode(), end="")
tn.write(username.encode("ascii") + b"\n")
print(tn.read_until(b"Password: ").decode(), end="")
tn.write(password.encode("ascii") + b"\n")
print(tn.read_until(b"Welcome", timeout=0.25).decode(), end="")

while True:
    print(tn.read_until(b"$ ").decode(), end="")
    tn.write(input().encode("ascii") + b"\n")

