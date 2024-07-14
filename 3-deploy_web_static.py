#!/usr/bin/python3
import os
from time import strftime
from dotenv import load_dotenv
from fabric.api import env, local, put, run

load_dotenv()
myweb1 = os.getenv('myweb1')
myweb2 = os.getenv('myweb2')
env.hosts = [myweb1, myweb2]
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    filename = strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(filename)
    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed:
        return None
    return file


def do_deploy(archive_path):
    """Distribute an archive to a web server."""
    if not os.path.isfile(archive_path):
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]
    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed:
        return False
    if run("sudo rm /tmp/{}".format(file)).failed:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False
    if run("sudo rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
