#!/usr/bin/env python3
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


def get_latest_archive():
    """Find the latest .tgz archive in the versions/ directory"""
    matching_files = glob.glob("versions/web_static_*.tgz")
    if matching_files:
        latest = max(matching_files, key=os.path.getmtime)
        print(f"Latest archive: {latest}"
        return latest
    else:
        print("No archives found.")
        return None


def do_deploy():
    """Deploy the latest archive to all web servers"""
    archive_path = get_latest_archive()
    if not archive_path or not os.path.exists(archive_path):
        print("❌ No archive found to deploy.")
        return

    archive_file = os.path.basename(archive_path)  # e.g., web_static_20250530.tgz
    archive_name = archive_file.replace(".tgz", "")  # e.g., web_static_20250530
    release_path = f"/data/web_static/releases/{archive_name}/"

    for server in servers:
        if not server:
            continue  # Skip if server is None

        print(f"\n🚀 Deploying to {server}...")

        c = Connection(
            host=server,
            user='ubuntu',
            connect_kwargs={"key_filename": key_path, "password": password}
        )

        try:
            # Upload archive
            c.put(archive_path, "/tmp/")

            # Create release directory
            c.run(f"mkdir -p {release_path}")

            # Extract archive
            c.run(f"tar -xzf /tmp/{archive_file} -C {release_path}")

            # Move content from web_static to release path root
            c.run(f"mv {release_path}web_static/* {release_path}")
            c.run(f"rm -rf {release_path}web_static")

            # Remove the archive
            c.run(f"rm /tmp/{archive_file}")

            # Update symbolic link
            c.run("rm -rf /data/web_static/current")
            c.run(f"ln -s {release_path} /data/web_static/current")

            print(f"✅ Deployment to {server} completed successfully.")

        except Exception as e:
            print(f"❌ Deployment to {server} failed: {e}")


def deploy_all():
    """Pack and deploy web_static to all servers"""
    archive_path = do_pack()
    if archive_path:
        do_deploy()

if __name__ == "__main__":
    deploy_all()































