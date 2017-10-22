#!/usr/bin/env python
# -*- coding: utf8 -*-
# **********************************
# **       DUSTPEDIA API          **
# **********************************

# -----------------------------------------------------------------

# Ensure Python 3 functionality
from __future__ import absolute_import, division, print_function

# Import standard modules
import os.path
import argparse

# Import DustPedia API
from core.database import DustPediaDatabase
from core.sample import resolve_name

# -----------------------------------------------------------------

instruments = ["GALEX", "SDSS", "DSS", "2MASS", "Spitzer", "WISE", "PACS", "SPIRE", "Planck"]

# -----------------------------------------------------------------

# Parse arguments
parser = argparse.ArgumentParser(description="get image")
parser.add_argument("galaxy", type=str, help="the galaxy name")
parser.add_argument("instrument", type=str, nargs='?', choices=instruments, help="the instrument (optional)")
parser.add_argument("--errors", action="store_true", help="also get error maps")
parser.add_argument("-o", type=str, help="output path")
arguments = parser.parse_args()

# -----------------------------------------------------------------

# Resolve the name
galaxy_name = resolve_name(arguments.galaxy)

# -----------------------------------------------------------------

# Create the database
database = DustPediaDatabase()

# -----------------------------------------------------------------

if arguments.o is not None: path = arguments.o
else: path = os.getcwd()
if not os.path.isdir(path): os.mkdir(path)

# -----------------------------------------------------------------

database.download_images(galaxy_name, path, error_maps=arguments.errors, progress_bar=True, instrument=arguments.instrument)

# -----------------------------------------------------------------
