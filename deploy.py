from dotenv import load_dotenv
from fabric import Connection
import os
load_dotenv()
web1 = os.getenv("web01")
web2 = os.getenv("web02")

servers = [web1, web2]
def deploy():
    for server in servers:
        print(f"Deploying to {server}")
        with Connection(host=server) as c:
            c.put(remote_path="/tmp/", local_path= "/versions/web_static_20250529211321.tgz")
            # c.run("mkdir -p //data/web_static/releases/")
            # c.run("tar -xzf /tmp/web_static_20250529211321.tgz -C //data/web_static/releases/")