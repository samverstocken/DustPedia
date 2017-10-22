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
parser = argparse.ArgumentParser(description="get photometry")
parser.add_argument("-o", type=str, help="output path")
arguments = parser.parse_args()

# -----------------------------------------------------------------

database = DustPediaDatabase()

# -----------------------------------------------------------------

if arguments.o is not None: path = arguments.o
else: path = os.getcwd()
if not os.path.isdir(path): os.mkdir(path)

# -----------------------------------------------------------------

# Download
database.download_photometry(path)

# -----------------------------------------------------------------
