#!/usr/bin/env python3
from fabric import task
from time import strftime
from fabric import Connection
from sys import argv




def do_pack():
    timestamp = strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"

    try:
        # Create versions folder if it doesn't exist
        c = Connection(host='NB02', user='yosef')
        print("Creating versions directory...")
        c.local("mkdir -p versions")

        # Create the archive
        c.local(f"tar -czvf {archive_path} web_static/")

        print(f"web_static packed: {archive_path}")
        return archive_path

    except Exception as e:
        print(f"Packing failed: {e}")
        return None
do_pack()

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python3 your_script.py <function_name>")
        exit(1)

    func_name = argv[1]

    if func_name in globals() and callable(globals()[func_name]):
        globals()[func_name]()  # Call the function
    else:
        print(f"Function '{func_name}' not found.")
