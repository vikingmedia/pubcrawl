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
fh = logging.FileHandler('/var/log/pubcrawl.log')
fh.setLevel(logging.WARNING)
fh.setFormatter(formatter)
logger.addHandler(fh)

# log to StdOut
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


################################################################################
# EMAIL
################################################################################

EMAIL_SENDER = 'immobilien@stadtklan.org'
EMAIL_RECEIVER = 'erik@stadtklan.org'
EMAIL_HOST = 'smtp.gmail.com:587'
EMAIL_USER = 'livingroom@stadtklan.org'
EMAIL_PWD  = 'hail2theclan!'
EMAIL_USE_TLS = True
EMAIL_SUBJECT = 'stadtklan crawler: %(spider)s [%(items)s] new items!'
