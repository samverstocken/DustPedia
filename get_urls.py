#!/usr/bin/env python
# -*- coding: utf8 -*-
# **********************************
# **       DUSTPEDIA API          **
# **********************************

# -----------------------------------------------------------------

# Ensure Python 3 functionality
from __future__ import absolute_import, division, print_function

# Import standard modules
import argparse

# Import DustPedia API
from core.database import DustPediaDatabase
from core.sample import resolve_name

# -----------------------------------------------------------------

# Parse arguments
parser = argparse.ArgumentParser(description="get image")
parser.add_argument("galaxy", type=str, help="galaxy name")
arguments = parser.parse_args()

# -----------------------------------------------------------------

# Resolve the name
galaxy_name = resolve_name(arguments.galaxy)

# -----------------------------------------------------------------

# Create the database
database = DustPediaDatabase()

# -----------------------------------------------------------------

urls = database.get_image_urls(galaxy_name)
for url in urls: print(url)

# -----------------------------------------------------------------
