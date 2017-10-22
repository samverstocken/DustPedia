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
#parser.add_argument("username", type=str, help="DustPedia archive username")
#parser.add_argument("password", type=str, help="DustPedia archive password")
parser.add_argument("galaxy", type=str, help="the name of the galaxy")
arguments = parser.parse_args()

# -----------------------------------------------------------------

# Resolve the name
galaxy_name = resolve_name(arguments.galaxy)

# -----------------------------------------------------------------

# Create the database
database = DustPediaDatabase()

# Login
#database.login(arguments.username, arguments.password)

# -----------------------------------------------------------------

parameters = database.get_dust_black_body_table_parameters(galaxy_name)

print("")
for name in parameters: print(" - " + name + ": " + str(parameters[name]))
print("")

# -----------------------------------------------------------------
