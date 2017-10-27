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
parser.add_argument("username", type=str, help="DustPedia archive username")
parser.add_argument("password", type=str, help="DustPedia archive password")
parser.add_argument("galaxy", type=str, help="the name of the galaxy")
arguments = parser.parse_args()

# -----------------------------------------------------------------

# Resolve the name
galaxy_name = resolve_name(arguments.galaxy)

# -----------------------------------------------------------------

# Create the database
database = DustPediaDatabase()

# Login
database.login(arguments.username, arguments.password)

# -----------------------------------------------------------------

# Get parameters
mbb = database.get_dust_black_body_table_parameters(galaxy_name)
cigale = database.get_cigale_parameters(galaxy_name)

# -----------------------------------------------------------------

def union(*sequences):

    """
    This function ...
    :param sequences:
    :return:
    """

    if len(sequences) == 0: return []
    elif len(sequences) == 1: return sequences[0][:]  # make copy of the list

    # OWN IMPLEMENTATION: quadratic complexity!
    else:

        elements = []

        # Just loop over each sequence sequentially
        for sequence in sequences:
            for item in sequence:
                if item not in elements: elements.append(item)

        # Return the list of elements
        return elements

# -----------------------------------------------------------------

# Doesn't retain order
# parameter_names = set(mbb.keys()) | set(cigale.keys())
parameter_names = union(mbb.keys(), cigale.keys())

# -----------------------------------------------------------------

print("")
for name in parameter_names:

    if name in mbb and name in cigale:

        print(" - " + name + ":")
        print("")
        print("    * [MBB]: " + str(mbb[name]))
        print("    * [CIGALE]: " + str(cigale[name]))

        if not name.endswith("_error"):

            diff = abs(mbb[name] - cigale[name])
            reldiff = abs(mbb[name] - cigale[name]) / mbb[name]
            print("")
            print("     => difference: " + str(diff))
            print("     => relative difference: " + str(reldiff * 100) + "%")

        print("")

    elif name in mbb:

        print(" - " + name + " [MBB]: " + str(mbb[name]))

    elif name in cigale:

        print(" - " + name + " [CIGALE]: " + str(cigale[name]))

print("")

# -----------------------------------------------------------------
