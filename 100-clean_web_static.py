import os
from time import strftime
import glob
from dotenv import load_dotenv
from fabric import Connection

# Load environment variables from .env
load_dotenv()

# Retrieve environment variables
web01 = os.getenv('web01')
web02 = os.getenv('web02')
key_path = os.getenv('file_path')
password = os.getenv('password')  # Optional
servers = [web01, web02]

def do_clean(number=0):
    """Delete out-of-date archives.
    Args:
        number (int): The number of archives to keep.
    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
