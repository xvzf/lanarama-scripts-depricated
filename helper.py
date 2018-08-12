import json
from fabric import Connection


def get_server(name: str):
    with open("server.json") as f:
        config = json.loads(f.read())
        host = config[name]
        # Check if available
        if not host:
            return None

        return Connection(host["ip"],
                          user=host["user"])

def psuccess(toprint):
    print(f"[+]", toprint)

def pwarning(toprint):
    print(f"[!]", toprint)

def perror(toprint):
    print(f"[-]", toprint)
