#!/usr/bin/python3
"""Compress web static package
"""
# import dotenv
from dotenv import load_dotenv
import os
from os.path import exists
from fabric.api import *
# from datetime import datetime
from os import path
from fabric.api import env

load_dotenv()

myweb1 = os.getenv('myweb1')
myweb2 = os.getenv('myweb2')
env.hosts = [myweb1, myweb2]
# env.hosts = ['127.17.0.2']

env.user = 'ubuntu'
# env.users = 'root'

env.key_filename = '~/.ssh/school'


# def do_deploy(archive_path):
#     """Deploy web files to server using Fabric
#     , this one will deploy our web_static files to the server"""
#     try:
#         if not (path.exists(archive_path)):
#             return False
#
#         # upload archive
#         put(archive_path, '/tmp/')
#
#         # create target dir
#
#         timestamp = archive_path[-18:-4]
#         run('sudo mkdir -p /data/web_static/\
# releases/web_static_{}/'.format(timestamp))
#
#         # uncompress archive and delete .tgz
#         run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
# /data/web_static/releases/web_static_{}/'
#             .format(timestamp, timestamp))
#
#         # remove archive
#         run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))
#
#         # move contents into host web_static
#         run('sudo mv  /data/web_static/releases/web_static_{}/web_static/* \
# /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))
#
#         # remove extraneous web_static dir
#         run('sudo rm -rf /data/web_static/releases/\
# web_static_{}/web_static'
#             .format(timestamp))
#
#         # delete pre-existing sym link
#         run('sudo rm -rf /data/web_static/current')
#
#         # re-establish symbolic link
#         run('sudo ln -s /data/web_static/releases/\
# web_static_{}/ /data/web_static/current'.format(timestamp))
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return False
#
#     # return True on success
#     return True
def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False