"""
config.py

Copyright (c) 2024, Enindex Ltd
All rights reserved.

This module provides the Config class which loads credentials and api details
from a .env file. The user's .env must include ENINDEX_SUBDOMAIN and
ENINDEX_API_KEY which can be found by accessing the platform.
ENINDEX_AUTH_URL defaults to auth.enindex.com and need not be specified in the
.env.

Features:
- loads credentials from .env.

Classes:
- Config: simple class containing API and any other config details.

Usage example:
    import enindex_tools.config as config
    print(config.config.ENINDEX_API_KEY)

Author: PRJ
Date: 2024-09-03
"""

from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

class Config():
    ENINDEX_AUTH_URL = os.getenv('ENINDEX_AUTH_URL','https://auth.enindex.com/')
    ENINDEX_USERNAME = os.getenv('ENINDEX_USERNAME')
    ENINDEX_SUBDOMAIN = os.getenv('ENINDEX_SUBDOMAIN')
    ENINDEX_API_KEY = os.getenv('ENINDEX_API_KEY')

config = Config()