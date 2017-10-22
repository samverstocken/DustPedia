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
import subprocess

# -----------------------------------------------------------------

# Parse arguments
parser = argparse.ArgumentParser(description="examples")
#parser.add_argument("username", type=str, help="DustPedia archive username", nargs='?')
#parser.add_argument("password", type=str, help="DustPedia archive password", nargs='?')
arguments = parser.parse_args()

# -----------------------------------------------------------------

#if arguments.username is None: print("Username is not provided: some commands will be unavailable")
#elif arguments.password is None: raise ValueError("Username is provided but not the password")

# -----------------------------------------------------------------

print("")
print("-----------------------------------------------------------------")
print("")

# # -----------------------------------------------------------------

first = "python in_sample.py M77"

print("1.")
print("Executing: '" + first + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(first, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

second = "python in_sample.py M31"

print("2.")
print("Executing: '" + second + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(second, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

third = "python get_urls.py M81"

print("3.")
print("Executing: '" + third + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(third, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

fourth = "python get_info.py M51"

print("4.")
print("Executing: '" + fourth + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(fourth, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

fifth = "python get_image.py NGC3031_Planck_10600"

print("5.")
print("Executing: '" + fifth + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(fifth, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

sixth = "python get_images.py NGC1068 Planck -o images"

print("6.")
print("Executing: '" + sixth + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(sixth, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

seventh = "python list_all.py"

print("7.")
print("Executing: '" + seventh + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(seventh, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

eight = "python get_photometry.py -o photometry"

print("8.")
print("Executing: '" + eight + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(eight, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

nineth = "python show_header.py NGC3031_Planck_10600"

print("9.")
print("Executing: '" + nineth + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(nineth, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

tenth = "python show_wcs.py NGC3031_Planck_10600"

print("10.")
print("Executing: '" + tenth + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(tenth, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

eleventh = "python show_cutouts.py M77"

print("11.")
print("Executing: '" + eleventh + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(eleventh, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

twelfth = "python get_cigale_parameters.py M81"

print("12.")
print("Executing: '" + twelfth + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(twelfth, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

thirteenth = "python get_mbb_parameters.py M81"

print("13.")
print("Executing: '" + thirteenth + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(thirteenth, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------

fourteenth = "python get_parameters.py M81"

print("14.")
print("Executing: '" + fourteenth + "'")
print("")
print("gives:")
print("")

output = subprocess.check_output(fourteenth, shell=True)
for line in output.split("\n"): print("    " + line)

print("")
print("-----------------------------------------------------------------")
print("")

# -----------------------------------------------------------------
