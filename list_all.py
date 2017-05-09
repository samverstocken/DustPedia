#!/usr/bin/env python
# -*- coding: utf8 -*-
# **********************************
# **       DUSTPEDIA API          **
# **********************************

# -----------------------------------------------------------------

# Ensure Python 3 functionality
from __future__ import absolute_import, division, print_function

# Import DustPedia API
from core.sample import DustPediaSample

# -----------------------------------------------------------------

sample = DustPediaSample()
names = sample.get_names()
for name in names: print(name)

# -----------------------------------------------------------------
