#!/usr/bin/env python3
import os
from fabric import Connection
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve environment variables
web01 = os.getenv('web01')
web02 = os.getenv('web02')
key_path = os.getenv('file_path')
password = os.getenv('password')  # Optional
servers = [web01, web02]

def do_clean(number=0):
    """Delete out-of-date archives locally and on remote servers."""
    number = int(number)
    number = 1 if number <= 1 else number

    # === Clean local ===
    archives = sorted(os.listdir("versions"))
    to_delete = archives[:-number]
    for archive in to_delete:
        local_path = os.path.join("versions", archive)
        if os.path.isfile(local_path):
            os.remove(local_path)
            print(f"Deleted local archive: {archive}")

    # === Clean remote ===
    for host in servers:
        if host:
            print(f"\nConnecting to {host}...")
            c = Connection(
                host=host,
                user='ubuntu',
                connect_kwargs={"key_filename": key_path, "password": password}
            )
            with c.cd("/data/web_static/releases"):
                result = c.run("ls -tr", hide=True)
                archives = result.stdout.strip().split()
                archives = [a for a in archives if a.startswith("web_static_")]
                to_delete = archives[:-number]
                for archive in to_delete:
                    c.run(f"rm -rf {archive}")
                    print(f"Deleted remote archive: {archive} on {host}")


if __name__ == '__main__':
    do_clean()
