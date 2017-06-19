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

# Parse arguments
parser = argparse.ArgumentParser(description="get cutouts")
parser.add_argument("username", type=str, help="DustPedia archive username")
parser.add_argument("password", type=str, help="DustPedia archive password")
parser.add_argument("galaxies", type=str, help="the galaxy names")
arguments = parser.parse_args()

# -----------------------------------------------------------------

# Create the database
database = DustPediaDatabase()

# Login
database.login(arguments.username, arguments.password)

# -----------------------------------------------------------------

path = os.getcwd()

# -----------------------------------------------------------------

# Resolve the names
galaxy_names = [resolve_name(name.strip()) for name in arguments.galaxies.split(",")]
print("galaxies: ", galaxy_names)

# -----------------------------------------------------------------

# Loop over the galaxies, download the cutouts png
for galaxy_name in galaxy_names:

        # Download
        filepath = database.download_photometry_cutouts(galaxy_name, path)

        # Change name
        new_path = "thumbnails_" + galaxy_name + ".png"
        os.rename(filepath, new_path)

# -----------------------------------------------------------------
