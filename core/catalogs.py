#!/usr/bin/env python
# -*- coding: utf8 -*-
# **********************************
# **       DUSTPEDIA API          **
# **********************************

# Ensure Python 3 compatibility
from __future__ import absolute_import, division, print_function

# Import standard modules
import requests
from lxml import html

# -----------------------------------------------------------------

leda_search_object_url = "http://leda.univ-lyon1.fr/ledacat.cgi?"

# -----------------------------------------------------------------

def get_hyperleda_name(galaxy_name):

    """
    This function ...
    :param galaxy_name:
    :return:
    """

    url = leda_search_object_url + galaxy_name

    page_as_string = requests.get(url).content

    tree = html.fromstring(page_as_string)

    #print(page_as_string)

    tables = [e for e in tree.iter() if e.tag == 'table']

    table = tables[1]
    #table = tables[1]

    #for table in tables: print(table.text_content())

    #print(table.text_content())

    #print(table.text_content())
    objname = table.text_content().split(" (")[0]

    #table_rows = [e for e in table.iter() if e.tag == 'tr']
    #column_headings = [e.text_content() for e in table_rows[0].iter() if e.tag == 'th']

    # return table_rows, column_headings

    #objname = str(table_rows[0].text_content().split("\n")[1]).strip()

    # Return the HYPERLEDA name
    return objname
    
# -----------------------------------------------------------------
