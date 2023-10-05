#!/usr/bin/python3

from datetime import datetime
from fabric.api import local, env, run, put
from os.path import isdir, exists


def do_deploy(archive_path):
    if exists(archive_path) is False:
        return False
    
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext)
