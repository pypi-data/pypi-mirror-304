"""
api_client.py

Copyright (c) 2024, Enindex Ltd
All rights reserved.

This module provides the ApiClient class which retreives data
from the enindex api.

Features:
- Makes requests to the enindex api
- Implements rate limiting

Classes:
- ApiClient: Rate-limited get requests

Usage example:
    import enindex_tools.api_client as api_client
    client.get()
    

Author: PRJ
Date: 2024-09-03
"""
import requests
from ratelimit import limits, sleep_and_retry

import enindex_tools.config as config
import enindex_tools.token_manager as tm

MAX_CALLS = 1
PERIOD_SECONDS = 1

class ApiClient:
    def __init__(self, token_manager=None):
        """
        Initialize the API client.

        Parameters:
        - token_manager: An instance of TokenManager to handle authentication.
        """
        self._base_url = f'https://{config.config.ENINDEX_SUBDOMAIN}.enindex.com/api/'
        self._token_manager = (tm.TokenManager() if token_manager is None else token_manager) 
   
    @sleep_and_retry
    @limits(calls=MAX_CALLS, period=PERIOD_SECONDS)
    def _make_request(self,method,endpoint,**kwargs):
        """
        Send rate limited request to enindex api and return result.

        Parameters:
        - token_manager: An instance of TokenManager to handle authentication.
        
        Returns:
        - response object.
        """
        url = f"{self._base_url}{endpoint}"
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f"Bearer {self._token_manager.get_token()}"
        response = requests.request(method, url, headers=headers, **kwargs)
        print(response.url)
        response.raise_for_status()
        return response

    def get(self, endpoint, params=None):
        """
        Perform a GET request.

        Parameters:
        - endpoint: The API endpoint to call.
        - params: A dictionary or object containing query parameters.

        Returns:
        - The response object from the GET request.
        """
        if not isinstance(params, dict):
            raise ValueError("The 'params' argument must be a dictionary.")
        return self._make_request('GET', endpoint, params=params)


