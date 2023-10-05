#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
from os.path import isdir


def do_pack():
