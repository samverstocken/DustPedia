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
parser.add_argument("galaxy", type=str, help="the name of the galaxy")
arguments = parser.parse_args()

# -----------------------------------------------------------------

# Resolve the name
galaxy_name = resolve_name(arguments.galaxy)

# -----------------------------------------------------------------

# Create the database
database = DustPediaDatabase()

# -----------------------------------------------------------------

# Get parameters
mbb = database.get_dust_black_body_table_parameters(galaxy_name)
cigale = database.get_cigale_parameters(galaxy_name)

# -----------------------------------------------------------------

parameter_names = set(mbb.keys()) | set(cigale.keys())

# -----------------------------------------------------------------

print("")
for name in parameter_names:

    if name in mbb and name in cigale:

        print(" - " + name + ":")
        print("")
        print("    * [MBB]: " + str(mbb[name]))
        print("    * [CIGALE]: " + str(cigale[name]))
        diff = abs(mbb[name] - cigale[name])
        reldiff = abs(mbb[name] - cigale[name]) / mbb[name]
        print("    * difference: " + str(diff))
        print("    * relative differenfce: " + str(reldiff * 100) + "%")
        print("")

    elif name in mbb:

        print(" - " + name + " [MBB]: " + str(mbb[name]))

    elif name in cigale:

        print(" - " + name + " [CIGALE]: " + str(cigale[name]))

print("")

# -----------------------------------------------------------------
