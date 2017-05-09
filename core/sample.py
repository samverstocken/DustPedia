#!/usr/bin/env python
# -*- coding: utf8 -*-
# **********************************
# **       DUSTPEDIA API          **
# **********************************

# Ensure Python 3 compatibility
from __future__ import absolute_import, division, print_function

# Import standard modules
import os.path
import inspect

# Import astronomical modules
from astropy.table import Table

# Import DustPedia modules
from . import catalogs

# -----------------------------------------------------------------

this_path = inspect.getfile(inspect.currentframe())
base_path = this_path.split("/core/sample")[0]
data_path = os.path.join(base_path, "data")
ledawise_table_path = os.path.join(data_path, "DustPedia_LEDAWISE_Herschel.csv")

# -----------------------------------------------------------------

filter_names = {"GALEX FUV": "GALEX_FUV",
                "GALEX NUV": "GALEX_NUV",
                "SDSS u": "SDSS_u",
                "SDSS g": "SDSS_g",
                "SDSS r": "SDSS_r",
                "SDSS i": "SDSS_i",
                "SDSS z": "SDSS_z",
                "2MASS J": "2MASS_J",
                "2MASS H": "2MASS_H",
                "2MASS Ks": "2MASS_Ks",
                "IRAC I1": "Spitzer_3.6",
                "IRAC I2": "Spitzer_4.5",
                "IRAC I3": "Spitzer_5.8",
                "IRAC I4": "Spitzer_8.0",
                "MIPS 24mu": "Spitzer_24",
                "MIPS 70mu": "Spitzer_70",
                "MIPS 160mu": "Spitzer_160",
                "WISE W1": "WISE_3.4",
                "WISE W2": "WISE_4.6",
                "WISE W3": "WISE_12",
                "WISE W4": "WISE_22",
                "Pacs blue": "PACS_70",
                "Pacs green": "PACS_100",
                "Pacs red": "PACS_160",
                "SPIRE PSW": "SPIRE_250",
                "SPIRE PMW": "SPIRE_350",
                "SPIRE PLW": "SPIRE_500",
                "HFI 857": "Planck_350",
                "HFI 545": "Planck_550",
                "HFI 353": "Planck_850",
                "HFI 217": "Planck_1380",
                "HFI 143": "Planck_2100",
                "HFI_100": "Planck_3000",
                "LFI 070": "Planck_4260",
                "LFI 044": "Planck_6810",
                "LFI 030": "Planck_10600"}

# -----------------------------------------------------------------

# naming convention: [galaxy] [telescope] [band].fits.

# -----------------------------------------------------------------

def resolve_name(galaxy_name):

    """
    This function ...
    :param galaxy_name: 
    :return: 
    """

    sample = DustPediaSample()
    name = sample.get_name(galaxy_name)
    return name

# -----------------------------------------------------------------

class DustPediaSample(object):

    """
    This class ...
    """

    def __init__(self):

        """
        The constructor ...
        """

        # Load the table
        leda_wise_herschel = Table.read(ledawise_table_path) # 877 galaxies

        # Get the object names
        names = list(leda_wise_herschel["objname"])
        self.primary_sample = names

    # -----------------------------------------------------------------

    def get_names(self):

        """
        This function ...
        :return: 
        """

        return self.primary_sample

    # -----------------------------------------------------------------

    def get_name(self, galaxy_name): # gets name = HYPERLEDA name, and checks whether in DustPedia sample

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        # Get the HYPERLEDA name
        objname = catalogs.get_hyperleda_name(galaxy_name)

        #print(objname)

        # CHECK WHETHER IN DUSTPEDIA SAMPLE
        if objname not in self.primary_sample: raise ValueError("This galaxy is not in the DustPedia primary sample")

        # Return the name of the galaxy
        return objname

    # -----------------------------------------------------------------

    def get_filter_name(self, fltr):

        """
        This function ...
        :param fltr:
        :return:
        """

        fltr_string = str(fltr)

        if fltr_string not in filter_names: raise ValueError("Filter not recognized")

        return filter_names[fltr_string]

# -----------------------------------------------------------------
