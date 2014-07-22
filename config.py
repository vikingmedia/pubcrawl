#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jul 22, 2014

@author: zking
'''
import logging

################################################################################
# DB
################################################################################
DB = 'pubcrawl.db'


################################################################################
# LOGGING
################################################################################

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log to File
fh = logging.FileHandler('pubcrawl.log')
fh.setLevel(logging.WARNING)
fh.setFormatter(formatter)
logger.addHandler(fh)

# log to StdOut
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

