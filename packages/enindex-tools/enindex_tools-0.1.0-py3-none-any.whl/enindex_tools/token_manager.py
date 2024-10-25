"""
token_manager.py

Copyright (c) 2024, Enindex Ltd
All rights reserved.

This module provides the Token Manager class which fetches tokens
from the Enindex authentication server for use with the enindex api.

Features:
- Retrieves and stores a token.

Classes:
- TokenManager:  Manages API tokens, including retrieval, storage, and expiration checks.

Usage example:
    import enindex_tools.token_manager as tm
    print(tm.get_token())

Author: PRJ
Date: 2024-09-03
"""

import requests
import json

import enindex_tools.config as config


class TokenManager():

    def __init__(self):
        self._token = None
        self._tokenRoute = 'auth/token'
        self._username = config.config.ENINDEX_USERNAME
        self._client_secret = config.config.ENINDEX_API_KEY
        self._authUrl = config.config.ENINDEX_AUTH_URL + self._tokenRoute
    
    def refresh_token(self):
        """
        Retrieves a new token from the authentication server.

        Returns:
            string | None: Current token.
        """
        res = requests.post(self._authUrl,json = {'username':self._username, 'clientSecret':self._client_secret})
        if res.status_code == 200:
            self._token = json.loads(res.content)['token']
        return self._token
        
    def get_token(self):
        """
        Gets the current stored token. If no token is set, 
        the token will be refreshed.

        Returns:
            string | None: Current token.
        """
        if (self._token is None):
            self.refresh_token()
        return self._token
