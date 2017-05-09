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

# Import DustPedia API
from core.database import DustPediaDatabase

# -----------------------------------------------------------------

# Parse arguments
parser = argparse.ArgumentParser(description="get image")
parser.add_argument("username", type=str, help="DustPedia archive username")
parser.add_argument("password", type=str, help="DustPedia archive password")
arguments = parser.parse_args()

# -----------------------------------------------------------------

database = DustPediaDatabase()
database.login(arguments.username, arguments.password)

path = os.getcwd()

# Download
database.download_photometry(path)

# -----------------------------------------------------------------
