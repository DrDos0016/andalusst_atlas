# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import os
"""
This file contains additional settings to be used in settings.py, split by developer environment.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!! It is important to not leave this uploaded anywhere it can be publicly accessed !!!
!!! as it contains the site's key as well as MySQL credentials                      !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

ADMINS = (
    ('','')
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# DeviantArt API
CLIENT_ID = ""
CLIENT_SECRET = ""

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'pmdu',                      # Or path to database file if using sqlite3.
            'USER': 'pmdu',                      # Not used with sqlite3.
            'PASSWORD': 'p0ryg0n-Z',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
   

if os.path.isfile("/path/to/project/contributor.user"): # Contributor's dev environment
    OWNER           = ""
    DEBUG           = True
    TEMPLATE_DEBUG  = DEBUG
    ENV             = "DEV"
    ALLOWED_HOSTS   = [".pmdunity.org"]
    SITE_ROOT       = "/path/to/project"
    TEMPLATE_DIRS   = (
        "/path/to/project/templates",
        "/path/to/project/templates/error",
    )
    LOGIN_REDIRECT  = "http://django.pi:8000/login"
else:
    print "ERROR NO USER FILE FOUND"
