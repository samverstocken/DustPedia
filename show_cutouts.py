#!/usr/bin/env python
# -*- coding: utf8 -*-
# **********************************
# **       DUSTPEDIA API          **
# **********************************

# -----------------------------------------------------------------

# Ensure Python 3 functionality
from __future__ import absolute_import, division, print_function

# Import standard modules
import os
import argparse
import platform
import subprocess

# Import DustPedia API
from core.database import DustPediaDatabase
from core.sample import resolve_name

# -----------------------------------------------------------------

def open_file(path, wait=False):

    """
    This function ...
    :param path:
    :param wait:
    :return:
    """

    # Check if existing
    if not os.path.isfile(path): raise ValueError("The file '" + path + "' does not exist")

    # Determine command
    if platform.system() == "Darwin": command = ["open", path]
    else: command = ["xdg-open", path]

    # Call the command
    if wait:
        subprocess.call(command, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
        time.wait(10)
    else: subprocess.Popen(command)
    
# -----------------------------------------------------------------

# Parse arguments
parser = argparse.ArgumentParser(description="get image")
parser.add_argument("username", type=str, help="DustPedia archive username")
parser.add_argument("password", type=str, help="DustPedia archive password")
parser.add_argument("galaxy", type=str, help="the galaxy name")
arguments = parser.parse_args()

# -----------------------------------------------------------------

# Create the database
database = DustPediaDatabase()

# Login
database.login(arguments.username, arguments.password)

# -----------------------------------------------------------------

path = os.getcwd()

# -----------------------------------------------------------------

# Resolve the name
galaxy_name = resolve_name(arguments.galaxy)

# -----------------------------------------------------------------

# Download
filepath = database.download_photometry_cutouts(galaxy_name, path)

# Change name
new_path = "thumbnails_" + galaxy_name + ".png"
os.rename(filepath, new_path)

# Open
open_file(new_path)

# -----------------------------------------------------------------
