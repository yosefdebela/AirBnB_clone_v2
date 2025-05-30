#!/usr/bin/python3
from fabric import task
from time import strftime
from fabric import Connection

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

# @task
# def do_pack(c):
#     """
#     Generates a .tgz archive from the contents of the web_static folder.
#     Archive will be stored in the versions/ directory with a timestamp.
#     """
#     timestamp = strftime("%Y%m%d%H%M%S")
#     archive_path = f"versions/web_static_{timestamp}.tgz"
#
#     try:
#         # Create versions folder if it doesn't exist
#         c.local("mkdir -p versions")
#
#         # Create the archive
#         c.local(f"tar -czvf {archive_path} web_static/")
#
#         print(f"web_static packed: {archive_path}")
#         return archive_path
#
#     except Exception as e:
#         print(f"Packing failed: {e}")
#         return None
