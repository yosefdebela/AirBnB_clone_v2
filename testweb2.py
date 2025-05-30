#!/usr/bin/env python3
from dotenv import load_dotenv
import os
from fabric import Connection
from sys import argv

# Load environment variables
load_dotenv()
web01 = os.getenv('web01')
web02 = os.getenv('web02')
key_path = os.getenv('file_path')
password = os.getenv('password')

def list():
    """List contents of /etc on web01"""
    c = Connection(
        host=web01,
        user='ubuntu',
        connect_kwargs={"key_filename": key_path, "password": password}
    )
    result = c.run('ls -l /etc', hide=True)
    print(result.stdout.strip())

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python3 your_script.py <function_name>")
        exit(1)

    func_name = argv[1]

    if func_name in globals() and callable(globals()[func_name]):
        globals()[func_name]()  # Call the function
    else:
        print(f"Function '{func_name}' not found.")
