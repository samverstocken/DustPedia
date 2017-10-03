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
from core.sample import resolve_name

# -----------------------------------------------------------------

# Parse arguments
parser = argparse.ArgumentParser(description="get image")
parser.add_argument("galaxy", type=str, help="galaxy name")
arguments = parser.parse_args()

# -----------------------------------------------------------------

# Resolve the name
try:
    galaxy_name = resolve_name(arguments.galaxy)
    print("YES: " + galaxy_name)
except ValueError: print("NO")

# -----------------------------------------------------------------
