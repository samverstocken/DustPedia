#!/usr/bin/env python
# -*- coding: utf8 -*-
# **********************************
# **       DUSTPEDIA API          **
# **********************************

# Ensure Python 3 functionality
from __future__ import absolute_import, division, print_function

# Import standard modules
import shutil
import requests
from lxml import html
import os.path
from collections import OrderedDict

# Import astronomical modules
from astropy.io.fits import getheader
from astropy.wcs import WCS
from astropy.units import Unit

# Import other DustPedia modules
from . import network, tables, types
from .utils import lazyproperty

# -----------------------------------------------------------------

# The base link
base_link = "http://dustpedia.astro.noa.gr"

# login: http://dustpedia.astro.noa.gr/Account/Login
login_link = "http://dustpedia.astro.noa.gr/Account/Login"

# data: http://dustpedia.astro.noa.gr/Data
data_link = "http://dustpedia.astro.noa.gr/Data"

# MBB: http://dustpedia.astro.noa.gr/MBB
mbb_link = "http://dustpedia.astro.noa.gr/MBB"

# user
user_link = "http://dustpedia.astro.noa.gr/Account/UserProfile"

# print preview
print_preview_link = "http://dustpedia.astro.noa.gr/Data/GalaxiesPrintView"

# Account page
account_link = "http://dustpedia.astro.noa.gr/Account/UserProfile"

# -----------------------------------------------------------------

# http://dustpedia.astro.noa.gr/Content/tempFiles/mbb/dustpedia_mbb_results.csv

#all_mmb_results_url = "http://dustpedia.astro.noa.gr/Content/tempFiles/mbb/dustpedia_mbb_results.csv"
all_mmb_results_url = "http://dustpedia.astro.noa.gr/Content/tempFiles/mbb/dustpedia_mbb_results_v2.dat"

# emissivity of κλ=8.52 x (250/λ)1.855 cm2/gr adapted to the THEMIS model
# A bootstrap analysis was used to calculate the uncertainties in dust temperatures and masses.

# -----------------------------------------------------------------

all_cigale_results_url = "http://dustpedia.astro.noa.gr/Content/tempFiles/cigale/dustpedia_cigale_results_v4.dat"

# -----------------------------------------------------------------

def create_temp_dir(name):

    """
    This function ...
    :param name:
    :return:
    """

    path = os.path.join(os.getcwd(), name)

    # Check whether the directory does not exist yet
    if not os.path.isdir(path):

        # Create the directory
        os.mkdir(path)

    # Return the path
    return path

# -----------------------------------------------------------------

class DustPediaDatabase(object):

    """
    This class ...
    """

    def __init__(self):

        """
        The constructor ...
        :return:
        """

        # Determine the path to a temporary directory
        self.temp_path = create_temp_dir("_tmp_database")

        # Create the session
        self.session = requests.session()

        # A flag that states whether we are connected
        self.connected = False

    # -----------------------------------------------------------------

    def login(self, username, password):

        """
        This function ...
        :param username:
        :param password:
        :return:
        """

        # Inform the user
        print("Logging in to the DustPedia database ...")

        r = self.session.get(user_link)
        p = self.session.post(login_link, {'UserName': username, 'password': password})

        # Check login
        r = self.session.get(user_link)

        # Check whether the login was successful
        self.connected = username in r.content

        # If the login failed, raise an error
        if not self.connected: raise RuntimeError("Login failed")
        else: print("Succesfully connected to the DustPedia database")

    # -----------------------------------------------------------------

    @property
    def full_user_name(self):

        """
        This function ...
        :return:
        """

        if not self.connected: raise ValueError("Must be logged in")

        # Get account page text
        r = self.session.get(account_link)
        page_as_string = r.content

        # Get the name
        full_name = page_as_string.split("    Welcome ")[1].split(",")[0]

        # Return the name
        return full_name

    # -----------------------------------------------------------------

    def reset(self, username, password):

        """
        This function ...
        :return:
        """

        # Logout
        self.logout()

        # Create new session
        self.session = requests.session()

        # Login
        self.login(username, password)

    # -----------------------------------------------------------------

    def logout(self):

        """
        This function ...
        :return:
        """

        # Inform the user
        print("Logging out from the DustPedia database ...")

        # Disconnect
        if self.connected: self.session.close()

    # -----------------------------------------------------------------

    def __del__(self):

        """
        The destructor ...
        :return:
        """

        # Remove the temporary directory
        if os.path.isdir(self.temp_path): shutil.rmtree(self.temp_path)

        # Log out from the database
        self.logout()

    # -----------------------------------------------------------------

    def get_galaxy_names(self, parameters):

        """
        This function ...
        :param parameters:
        :return:
        """

        # Inform the user
        print("Getting the galaxy names ...")

        link = page_link_from_parameters(parameters)

        r = self.session.get(link)
        r = self.session.get(print_preview_link)

        page_as_string = r.content

        tree = html.fromstring(page_as_string)

        tables = [e for e in tree.iter() if e.tag == 'table']
        table = tables[-1]

        table_rows = [e for e in table.iter() if e.tag == 'tr']
        column_headings = [e.text_content() for e in table_rows[0].iter() if e.tag == 'th']

        galaxy_names = []

        for row in table_rows[1:]:

            column_index = 0

            for e in row.iter():

                if e.tag != "td": continue

                galaxy_info = e.text_content()

                galaxy_name = galaxy_info.split("Name: ")[1].split(" \r\n")[0]
                galaxy_names.append(galaxy_name)
                break

        return galaxy_names

    # -----------------------------------------------------------------

    def get_galaxies(self, parameters):

        """
        This function ...
        :param parameters:
        :return:
        """

        name_column = []
        ra_column = []
        dec_column = []
        stage_column = []
        type_column = []
        v_column = []
        d25_column = []
        i_column = []

        link = page_link_from_parameters(parameters)

        r = self.session.get(link)
        r = self.session.get(print_preview_link)

        page_as_string = r.content

        tree = html.fromstring(page_as_string)

        page_tables = [e for e in tree.iter() if e.tag == 'table']
        table = page_tables[-1]

        table_rows = [e for e in table.iter() if e.tag == 'tr']
        column_headings = [e.text_content() for e in table_rows[0].iter() if e.tag == 'th']

        info_boxes = []

        for row in table_rows[1:]:

            column_index = 0

            for e in row.iter():

                if e.tag != "td": continue

                galaxy_info = e.text_content()

                #galaxy_name = galaxy_info.split("Name: ")[1].split(" \r\n")[0]
                #galaxy_names.append(galaxy_name)
                info_boxes.append(galaxy_info)
                break

        for box in info_boxes:

            lines = box.split("\r\n")

            name = None
            ra = None
            dec = None
            stage = None
            type = None
            v = None
            d25 = None
            i = None

            for line in lines:

                if "Name" in line: name = line.split(": ")[1].strip()
                elif "RA(2000)" in line: ra = float(line.split(": ")[1])
                elif "DEC(2000)" in line: dec = float(line.split(": ")[1])
                elif "Hubble Stage(T)" in line: stage = float(line.split(": ")[1])
                elif "Hubble Type: Sab" in line: type = line.split(": ")[1].strip()
                elif "V (km/s)" in line: v = float(line.split(": ")[1])
                elif "D25 (arcmin)" in line: d25 = float(line.split(": ")[1])
                elif "Inclination (deg.)" in line: i = float(line.split(": ")[1])

            if add_hubble_type(type, parameters):

                name_column.append(name)
                ra_column.append(ra)
                dec_column.append(dec)
                stage_column.append(stage)
                type_column.append(type)
                v_column.append(v)
                d25_column.append(d25)
                i_column.append(i)

        # Create the table
        names = ["Name", "RA", "DEC", "Hubble stage", "Hubble type", "V", "D25", "Inclination"]
        data = [name_column, ra_column, dec_column, stage_column, type_column, v_column, d25_column, i_column]
        table = tables.new(data, names)

        return table

    # -----------------------------------------------------------------

    def get_image_urls(self, galaxy_name, error_maps=True):

        """
        This function ...
        :param galaxy_name:
        :param error_maps:
        :return:
        """

        # Inform the user
        print("Getting the URLs of the available images for galaxy '" + galaxy_name + "' ...")

        # Go to the page
        r = self.session.get(data_link + "?GalaxyName="+galaxy_name+"&tLow=&tHigh=&vLow=&vHigh=&inclLow=&inclHigh=&d25Low=&d25High=&SearchButton=Search")

        page_as_string = r.content

        tree = html.fromstring(page_as_string)

        tables = [ e for e in tree.iter() if e.tag == 'table']
        table = tables[-1]

        table_rows = [ e for e in table.iter() if e.tag == 'tr']
        column_headings = [ e.text_content() for e in table_rows[0].iter() if e.tag == 'th']

        galaxy_info = None
        image_links = []

        for row in table_rows[1:]:

            column_index = 0

            #row_content = []

            for e in row.iter():

                if e.tag != "td": continue

                if column_index == 0:

                    galaxy_info = e.text_content()

                else:

                    #print("CHILDREN")
                    #for ee in e.iterchildren(): print(ee)
                    #print()
                    #print("DESCENDANTS")
                    #for ee in e.iterdescendants(): print(ee)
                    #print()
                    #print("LINKS")
                    for ee in e.iterlinks():

                        link = base_link + ee[2]

                        name = os.path.basename(link)
                        if "_Error" in name and not error_maps: continue

                        image_links.append(link)

                    #print()
                    #print("SIBLINGS")
                    #for ee in e.itersiblings(): print(ee)

                column_index += 1

        # Request other page
        #r = self.session.get(user_link)

        #self.session.prepare_request()

        #print(image_links)

        return image_links

    # -----------------------------------------------------------------

    def get_image_names(self, galaxy_name, error_maps=True):

        """
        This function ...
        :param galaxy_name:
        :param error_maps:
        :return:
        """

        # Inform the user
        print("Getting the names of the images that are available for galaxy '" + galaxy_name + "' ...")

        # Example link: http://dustpedia.astro.noa.gr/Data/GetImage?imageName=NGC3031_Planck_10600.fits&instrument=Planck

        names = []

        for url in self.get_image_urls(galaxy_name):

            name = url.split("imageName=")[1].split("&instrument")[0]
            if "_Error" in name and not error_maps: continue
            names.append(name)

        return names

    # -----------------------------------------------------------------

    def get_image_names_and_urls(self, galaxy_name, error_maps=True):

        """
        This function ...
        :param galaxy_name:
        :param error_maps:
        :return:
        """

        # Initialize a dictionary for the urls
        urls = dict()

        # Loop over all the urls
        for url in self.get_image_urls(galaxy_name):

            name = url.split("imageName=")[1].split("&instrument")[0]
            if "_Error" in name and not error_maps: continue
            urls[name] = url

        # Return the dictionary of urls
        return urls

    # -----------------------------------------------------------------

    def get_header(self, galaxy_name, image_name, path):

        """
        This function ...
        :param galaxy_name:
        :param image_name:
        :param path
        :return:
        """

        # Inform the user
        print("Getting the header for the '" + image_name + "' for galaxy '" + galaxy_name + "' ...")

        # Determine a temporary path for the image file
        local_path = os.path.join(path, image_name)

        # Download the image to the temporary directory
        self.download_image(galaxy_name, image_name, local_path)

        # Load the header
        header = getheader(local_path)

        # Remove again
        os.remove(local_path)

        # Return the header
        return header

    # -----------------------------------------------------------------

    def get_wcs(self, galaxy_name, image_name, path):

        """
        This function ...
        :param galaxy_name:
        :param image_name:
        :param path:
        :return:
        """

        # Inform the user
        print("Getting the coordinate system for the '" + image_name + "' for galaxy '" + galaxy_name + "' ...")

        # Get the header
        header = self.get_header(galaxy_name, image_name, path)

        # Create and return the coordinate system
        return WCS(header=header)

    # -----------------------------------------------------------------

    def get_coordinate_system(self, galaxy_name, image_name, path):

        """
        This function ...
        :param galaxy_name: 
        :param image_name: 
        :param path:
        :return: 
        """

        return self.get_wcs(galaxy_name, image_name, path)

    # -----------------------------------------------------------------

    def download_image(self, galaxy_name, image_name, path, progress_bar=True):

        """
        This function ...
        :param galaxy_name:
        :param image_name:
        :param path:
        :param progress_bar:
        :return:
        """

        # Inform the user
        print("Downloading the image '" + image_name + "' for galaxy '" + galaxy_name + "' to '" + path + " ...")

        get_link = None

        for url in self.get_image_urls(galaxy_name):

            #print(url)
            link_name = url.split("imageName=")[1].split("&instrument")[0]

            if link_name == image_name:
                get_link = url
                break

        #print(get_link)

        if os.path.isdir(path): filepath = os.path.join(path, image_name)
        else: filepath = path

        # Download
        network.download_file(get_link, filepath, progress_bar=progress_bar, stream=True, session=self.session)

    # -----------------------------------------------------------------

    def download_image_from_url(self, url, path):

        """
        This function ...
        :param url:
        :param path:
        :return:
        """

        # Download
        network.download_file(url, path, progress_bar=True, stream=True, session=self.session)

    # -----------------------------------------------------------------

    def download_images(self, galaxy_name, path, error_maps=True, progress_bar=True, instrument=None):

        """
        This function ...
        :param galaxy_name:
        :param path: directory
        :param error_maps:
        :param progress_bar:
        :param instrument:
        :return:
        """

        # Inform the user
        print("Downloading all images for galaxy '" + galaxy_name + "' to '" + path + " ...")

        # Loop over the image URLS found for this galaxy
        for url in self.get_image_urls(galaxy_name, error_maps=error_maps):

            # Determine instrument
            instr = url.split("instrument=")[1]
            if instrument is not None and instr != instrument: continue

            # Determine path
            image_name = url.split("imageName=")[1].split("&instrument")[0]
            image_path = os.path.join(path, image_name)

            print("Downloading '" + image_name + "' ...")

            # Download this image
            network.download_file(url, image_path, progress_bar=progress_bar, stream=True, session=self.session)

    # -----------------------------------------------------------------

    def get_galaxy_info(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        # Inform the user
        print("Getting general information about galaxy '" + galaxy_name + "' ...")

        # Set the names of the table columns
        names = ["Name", "RA", "DEC", "Hubble Stage", "Hubble Type", "V", "D25", "Inclination"]

        r = self.session.get(data_link + "?GalaxyName="+galaxy_name+"&tLow=&tHigh=&vLow=&vHigh=&inclLow=&inclHigh=&d25Low=&d25High=&SearchButton=Search")

        page_as_string = r.content

        tree = html.fromstring(page_as_string)

        table_list = [ e for e in tree.iter() if e.tag == 'table']
        table = table_list[-1]

        table_rows = [ e for e in table.iter() if e.tag == 'tr']

        galaxy_info = None

        for row in table_rows[1:]:

            column_index = 0

            for e in row.iter():

                if e.tag != "td": continue

                if column_index == 0:

                    #for ee in e.iterchildren(): print(ee.text_content())
                    #for ee in e.iterdescendants(): print(ee.text_content())
                    #for ee in e.itersiblings(): print(ee.text_content())

                    galaxy_info = e.text_content()

                    #print(galaxy_info)

                column_index += 1

        splitted = galaxy_info.split("\r\n")

        lines = [split.strip() for split in splitted if split.strip()]

        name = None
        ra = None
        dec = None
        stage = None
        type = None
        v = None
        d25 = None
        i = None

        for line in lines:

            if "Name" in line: name = line.split(": ")[1]
            elif "RA(2000)" in line: ra = float(line.split(": ")[1])
            elif "DEC(2000)" in line: dec = float(line.split(": ")[1])
            elif "Hubble Stage(T)" in line: stage = float(line.split(": ")[1])
            elif "Hubble Type: Sab" in line: type = line.split(": ")[1]
            elif "V (km/s)" in line: v = float(line.split(": ")[1])
            elif "D25 (arcmin)" in line: d25 = float(line.split(": ")[1])
            elif "Inclination (deg.)" in line: i = float(line.split(": ")[1])

        data = [[name], [ra], [dec], [stage], [type], [v], [d25], [i]]

        table = tables.new(data, names)

        return table

    # -----------------------------------------------------------------

    def get_dust_black_body_parameters(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        # Inform the user
        print("Getting general information about galaxy '" + galaxy_name + "' ...")

        # http://dustpedia.astro.noa.gr/MBB?GalaxyName=NGC3031&tLow=&tHigh=&vLow=&vHigh=&inclLow=&inclHigh=&d25Low=&d25High=&SearchButton=Search

        r = self.session.get(mbb_link + "?GalaxyName=" + galaxy_name + "&tLow=&tHigh=&vLow=&vHigh=&inclLow=&inclHigh=&d25Low=&d25High=&SearchButton=Search")

        page_as_string = r.content

        tree = html.fromstring(page_as_string)

        table_list = [e for e in tree.iter() if e.tag == 'table']
        table = table_list[-1]

        table_rows = [e for e in table.iter() if e.tag == 'tr']

        galaxy_info = None

        for row in table_rows[1:]:

            column_index = 0

            for e in row.iter():

                if e.tag != "td": continue

                if column_index == 0:

                    # for ee in e.iterchildren(): print(ee.text_content())
                    # for ee in e.iterdescendants(): print(ee.text_content())
                    # for ee in e.itersiblings(): print(ee.text_content())

                    galaxy_info = e.text_content()

                    # print(galaxy_info)

                column_index += 1

        splitted = galaxy_info.split("\r\n")

        lines = [split.strip() for split in splitted if split.strip()]

        #return lines

        # Dust Temperature (K): 22.6±0.7
        # Dust Mass (M_sun): 4900000±1000000
        # Dust Luminosity (L_sun): 2.10E+09

        temperature = None
        temperature_error = None
        mass = None
        mass_error = None
        luminosity = None
        luminosity_error = None

        #for index in range(len(lines)):
        index = 0
        while index < len(lines):

            line = lines[index]

            if "Dust Temperature" in line:

                next_line = lines[index+1]
                valuestr, errorstr = next_line.split("&plusmn")
                value = float(valuestr)
                error = float(errorstr)

                temperature = value * Unit("K")
                temperature_error = error * Unit("K")

                index += 1

            elif "Dust Mass" in line:

                next_line = lines[index+1]
                valuestr, errorstr = next_line.split("&plusmn")
                value = float(valuestr)
                error = float(errorstr)

                mass = value * Unit("Msun")
                mass_error = error * Unit("Msun")

                index += 1

            elif "Dust Luminosity" in line:

                next_line = lines[index+1]

                valuestr, errorstr = next_line.split("&plusmn")
                value = float(valuestr)
                error = float(errorstr)

                #value = float(next_line)
                #error = None

                luminosity = value * Unit("Lsun")
                luminosity_error = error * Unit("Lsun")
                #luminosity_error = None

            index += 1

        # Return the parameters
        return mass, mass_error, temperature, temperature_error, luminosity, luminosity_error

    # -----------------------------------------------------------------

    def download_dust_black_body_plot(self, galaxy_name, path):

        """
        This function ...
        :param galaxy_name:
        :param path:
        :return:
        """

        # http://dustpedia.astro.noa.gr/Content/Dustpedia_SEDs_THEMIS/NGC3031.png

        url = "http://dustpedia.astro.noa.gr/Content/Dustpedia_SEDs_THEMIS/" + galaxy_name + ".png"

        # Download
        filepath = network.download_file(url, path, session=self.session, progress_bar=True)

        # Return the filepath
        return filepath

    # -----------------------------------------------------------------

    def download_dust_black_body_table(self, path):

        """
        This function ...
        :param path:
        :return:
        """

        filepath = network.download_file(all_mmb_results_url, path, session=self.session, progress_bar=True)
        return filepath

    # -----------------------------------------------------------------

    def get_dust_black_body_table(self):

        """
        This function ...
        :return:
        """

        filepath = self.download_dust_black_body_table(self.temp_path)
        return tables.from_file(filepath, format="ascii")

    # -----------------------------------------------------------------

    @lazyproperty
    def dust_black_body_table(self):

        """
        This function ...
        :return:
        """

        return self.get_dust_black_body_table()

    # -----------------------------------------------------------------

    def get_black_body_galaxy_index(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = tables.find_index(self.dust_black_body_table, galaxy_name, "Name")
        return index

    # -----------------------------------------------------------------

    def get_dust_mass_black_body(self, galaxy_name):

        """
        This function ....
        :param galaxy_name:
        :return:
        """

        index = self.get_black_body_galaxy_index(galaxy_name)
        value = self.dust_black_body_table["Mdust__Mo"][index] * Unit("Msun")
        return value

    # -----------------------------------------------------------------

    def get_dust_mass_error_black_body(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_black_body_galaxy_index(galaxy_name)
        value = self.dust_black_body_table["Mdust_err"][index] * Unit("Msun")
        return value

    # -----------------------------------------------------------------

    def get_dust_temperature_black_body(self, galaxy_name):

        """
        This function ....
        :param galaxy_name:
        :return:
        """

        index = self.get_black_body_galaxy_index(galaxy_name)
        value = self.dust_black_body_table["Tdust__K"][index] * Unit("K")
        return value

    # -----------------------------------------------------------------

    def get_dust_temperature_error_black_body(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_black_body_galaxy_index(galaxy_name)
        value = self.dust_black_body_table["Tdust_err"][index] * Unit("K")
        return value

    # -----------------------------------------------------------------

    def get_dust_luminosity_black_body(self, galaxy_name):

        """
        This fucntion ...
        :param galaxy_name:
        :return:
        """

        index = self.get_black_body_galaxy_index(galaxy_name)
        value = self.dust_black_body_table["Ldust__Lo"][index] * Unit("Lsun")
        return value

    # -----------------------------------------------------------------

    def get_dust_luminosity_error_black_body(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_black_body_galaxy_index(galaxy_name)
        value = self.dust_black_body_table["Ldust_err"][index] * Unit("Lsun")
        return value

    # -----------------------------------------------------------------

    def get_chi_squared_black_body(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_black_body_galaxy_index(galaxy_name)
        value = self.dust_black_body_table["nchi2"][index]
        return value

    # -----------------------------------------------------------------

    def get_dust_black_body_table_parameters(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        # Get the index of the galaxy in the black body table
        index = self.get_black_body_galaxy_index(galaxy_name)

        # Get the values
        dust_temperature = self.dust_black_body_table["Tdust__K"][index] * Unit("K")
        dust_temperature_error = self.dust_black_body_table["Tdust_err"][index] * Unit("K")
        dust_luminosity = self.dust_black_body_table["Ldust__Lo"][index] * Unit("Lsun")
        dust_luminosity_error = self.dust_black_body_table["Ldust_err"][index] * Unit("Lsun")
        dust_mass = self.dust_black_body_table["Mdust__Mo"][index] * Unit("Msun")
        dust_mass_error = self.dust_black_body_table["Mdust_err"][index] * Unit("Msun")
        chi_squared = self.dust_black_body_table["nchi2"][index]

        # Create the parameters dictionary
        parameters = OrderedDict()
        parameters["dust_temperature"] = dust_temperature
        parameters["dust_temperature_error"] = dust_temperature_error
        parameters["dust_luminosity"] = dust_luminosity
        parameters["dust_luminosity_error"] = dust_luminosity_error
        parameters["dust_mass"] = dust_mass
        parameters["dust_mass_error"] = dust_mass_error
        parameters["chi_squared"] = chi_squared

        # Return the parameters dictionary
        return parameters

    # -----------------------------------------------------------------

    def download_cigale_table(self, path):

        """
        This function ....
        :param path:
        :return:
        """

        filepath = network.download_file(all_cigale_results_url, path, session=self.session, progress_bar=True)
        return filepath

    # -----------------------------------------------------------------

    def get_cigale_table(self):

        """
        This function ...
        :return:
        """

        filepath = self.download_cigale_table(self.temp_path)
        return tables.from_file(filepath, format="ascii")

    # -----------------------------------------------------------------

    @lazyproperty
    def cigale_table(self):

        """
        This function ...
        :return:
        """

        return self.get_cigale_table()

    # -----------------------------------------------------------------

    def get_cigale_galaxy_index(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        # Get the galaxy index
        index = tables.find_index(self.cigale_table, galaxy_name, "Name")
        return index

    # -----------------------------------------------------------------

    def get_dust_mass_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["Mdust__Mo"][index] * Unit("Msun")
        return value

    # -----------------------------------------------------------------

    def get_dust_mass_error_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["Mdust_err"][index] * Unit("Msun")
        return value

    # -----------------------------------------------------------------

    def get_sfr_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["SFR__Mo_per_yr"][index] * Unit("Msun/yr")
        return value

    # -----------------------------------------------------------------

    def get_sfr_error_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["SFR_err"][index] * Unit("Msun/yr")
        return value

    # -----------------------------------------------------------------

    def get_stellar_mass_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["Mstar__Mo"][index] * Unit("Msun")
        return value

    # -----------------------------------------------------------------

    def get_stellar_mass_error_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["Mstar_err"][index] * Unit("Msun")
        return value

    # -----------------------------------------------------------------

    def get_stellar_luminosity_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["Lstar__W"][index] * Unit("W")
        return value

    # -----------------------------------------------------------------

    def get_stellar_luminosity_error_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["Lstar_err"][index] * Unit("W")
        return value

    # -----------------------------------------------------------------

    def get_dust_luminosity_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["Ldust__W"][index] * Unit("W")
        return value

    # -----------------------------------------------------------------

    def get_dust_luminosity_error_cigale(self, galaxy_name):

        """
        THis function ....
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["Ldust_err"][index] * Unit("W")
        return value

    # -----------------------------------------------------------------

    def get_fuv_attenuation_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["FUV_att"][index]
        return value

    # -----------------------------------------------------------------

    def get_fuv_attenuation_error_cigale(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        index = self.get_cigale_galaxy_index(galaxy_name)
        value = self.cigale_table["FUV_att_err"][index]
        return value

    # -----------------------------------------------------------------

    def get_cigale_parameters(self, galaxy_name):

        """
        This function ...
        :param galaxy_name:
        :return:
        """

        # Get the index of the galaxy in the Cigale results table
        index = self.get_cigale_galaxy_index(galaxy_name)

        # Get the parameters
        dust_mass = self.cigale_table["Mdust__Mo"][index] * Unit("Msun")
        dust_mass_error = self.cigale_table["Mdust_err"][index] * Unit("Msun")
        stellar_mass = self.cigale_table["Mstar__Mo"][index] * Unit("Msun")
        stellar_mass_error = self.cigale_table["Mstar_err"][index] * Unit("Msun")
        sfr = self.cigale_table["SFR__Mo_per_yr"][index] * Unit("Msun/yr")
        sfr_error = self.cigale_table["SFR_err"][index] * Unit("Msun/yr")
        stellar_luminosity = self.cigale_table["Lstar__W"][index] * Unit("W")
        stellar_luminosity_error = self.cigale_table["Lstar_err"][index] * Unit("W")
        dust_luminosity = self.cigale_table["Ldust__W"][index] * Unit("W")
        dust_luminosity_error = self.cigale_table["Ldust_err"][index] * Unit("W")
        fuv_attenuation = self.cigale_table["FUV_att"][index]
        fuv_attenuation_error = self.cigale_table["FUV_att_err"][index]

        # Create the parameters dictionary
        parameters = OrderedDict()
        parameters["sfr"] = sfr
        parameters["sfr_error"] = sfr_error
        parameters["stellar_mass"] = stellar_mass
        parameters["stellar_mass_error"] = stellar_mass_error
        parameters["dust_mass"] = dust_mass
        parameters["dust_mass_error"] = dust_mass_error
        parameters["stellar_luminosity"] = stellar_luminosity
        parameters["stellar_luminosity_error"] = stellar_luminosity_error
        parameters["dust_luminosity"] = dust_luminosity
        parameters["dust_luminosity_error"] = dust_luminosity_error
        parameters["fuv_attenuation"] = fuv_attenuation
        parameters["fuv_attenuation_error"] = fuv_attenuation_error

        # Return the parameters dictionary
        return parameters

    # -----------------------------------------------------------------

    def get_photometry_cutouts_url(self, galaxy_name):

        """
        This fucntion ...
        :param galaxy_name:
        :return:
        """

        # http://dustpedia.astro.noa.gr/Data/GetImage?imageName=ESO097-013_Thumbnail_Grid.png&mode=photometry
        url = "http://dustpedia.astro.noa.gr/Data/GetImage?imageName=" + galaxy_name + "_Thumbnail_Grid.png&mode=photometry"
        return url

    # -----------------------------------------------------------------

    def download_photometry_cutouts(self, galaxy_name, dir_path, progress_bar=True):

        """
        This function ...
        :param galaxy_name:
        :param dir_path:
        :param progress_bar:
        :return:
        """

        # Inform the user
        print("Downloading the photometry cutouts for galaxy '" + galaxy_name + "' ...")

        url = self.get_photometry_cutouts_url(galaxy_name)
        return network.download_file(url, dir_path, session=self.session, progress_bar=progress_bar)

    # -----------------------------------------------------------------

    def download_photometry(self, dir_path):

        """
        This function ...
        :param dir_path:
        :return:
        """

        # Inform the user
        print("Downloading all of the photometry ...")

        # main photometry: http://dustpedia.astro.noa.gr/Content/tempFiles/DustPedia_Aperture_Photometry.csv
        # IRAS: http://dustpedia.astro.noa.gr/Content/tempFiles/DustPedia_IRAS_SCANPI.csv
        # Planck: http://dustpedia.astro.noa.gr/Content/tempFiles/DustPedia_Planck_CCS2.csv
        # Release notes: http://dustpedia.astro.noa.gr/Content/tempFiles/Photometry_Notes.pdf

        urls = ["http://dustpedia.astro.noa.gr/Content/tempFiles/DustPedia_Aperture_Photometry.csv",
                "http://dustpedia.astro.noa.gr/Content/tempFiles/DustPedia_IRAS_SCANPI.csv",
                "http://dustpedia.astro.noa.gr/Content/tempFiles/DustPedia_Planck_CCS2.csv"]

        # Download the photometry files
        network.download_files(urls, dir_path)

# -----------------------------------------------------------------

def page_link_from_parameters(parameters):

    """
    This function ...
    :param parameters:
    :return:
    """

    if "T" in parameters:
        tlow = str(parameters["T"][0]) if parameters["T"][0] is not None else ""
        thigh = str(parameters["T"][1]) if parameters["T"][1] is not None else ""
    else:
        tlow = thigh = ""

    if "V" in parameters:
        vlow = str(parameters["V"][0]) if parameters["V"][0] is not None else ""
        vhigh = str(parameters["V"][1]) if parameters["V"][1] is not None else ""
    else:
        vlow = vhigh = ""

    if "inclination" in parameters:
        incllow = str(parameters["inclination"][0]) if parameters["inclination"][0] is not None else ""
        inclhigh = str(parameters["inclination"][1]) if parameters["inclination"][1] is not None else ""
    else:
        incllow = inclhigh = ""

    if "D25" in parameters:
        d25low = str(parameters["D25"][0]) if parameters["D25"][0] is not None else ""
        d25high = str(parameters["D25"][1]) if parameters["D25"][1] is not None else ""
    else:
        d25low = d25high = ""

    return data_link + "?GalaxyName=&tLow=" + tlow + "&tHigh=" + thigh + "&vLow=" + vlow + \
            "&vHigh=" + vhigh + "&inclLow=" + incllow + "&inclHigh=" + inclhigh + "&d25Low=" + d25low + \
            "&d25High=" + d25high + "&SearchButton=Search"

# -----------------------------------------------------------------

def add_hubble_type(hubble_type, parameters):

    """
    This function ...
    :param hubble_type:
    :param parameters:
    :return:
    """

    if "Hubble type" in parameters:

        if types.is_string_type(parameters["Hubble type"]): return hubble_type == parameters["Hubble type"]
        else: return hubble_type in parameters["Hubble type"]

    else: return True

# -----------------------------------------------------------------
