from fabric import task, Connection
import os
from dotenv import load_dotenv

# Load environment variables from .env (if using one)
load_dotenv()

# Server IPs (update these or load from env)
web_servers = [os.getenv('WEB_SERVER_1'), os.getenv('WEB_SERVER_2')]


def do_deploy(c, archive_path):
    """Distribute archive to web servers and deploy."""
    if not os.path.exists(archive_path):
        print("Archive path does not exist")
        return False

    try:
        archive_file = archive_path.split("/")[-1]
        archive_folder = archive_file.replace(".tgz", "")
        release_path = f"/data/web_static/releases/{archive_folder}"

        for host in web_servers:
            print(f"Deploying to {host}...")

            conn = Connection(
                host=host,
                user=os.getenv("USER"),  # or hard-code e.g., 'ubuntu'
                connect_kwargs={"key_filename": os.getenv("SSH_KEY")}  # or use password
            )

            # Upload the archive to /tmp/
            conn.put(archive_path, "/tmp/")

            # Create the release folder
            conn.run(f"mkdir -p {release_path}")

            # Extract the archive
            conn.run(f"tar -xzf /tmp/{archive_file} -C {release_path}")

            # Move content out of web_static subfolder
            conn.run(f"mv {release_path}/web_static/* {release_path}/")

            # Remove the now empty subfolder
            conn.run(f"rm -rf {release_path}/web_static")

            # Remove the archive from /tmp/
            conn.run(f"rm /tmp/{archive_file}")

            # Remove old symbolic link
            conn.run("rm -rf /data/web_static/current")

            # Create new symbolic link
            conn.run(f"ln -s {release_path} /data/web_static/current")

            print(f"Deployment to {host} complete.")

        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
