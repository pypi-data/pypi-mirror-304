"""
api.py

Copyright (c) 2024, Enindex Ltd
All rights reserved.

This module provides the Api class which is the interface
of the Endindex API. Users of Enindex tools should make
requests using this class.

Features:
- Makes requests to the enindex api
- Returns data as json or dataframe
- Chunks requests

Classes:
- Api: Interface for using the API

Usage example:
    import enindex_tools.api as api
    import datetime as dt
    api = api.Api()
    timeFrom = dt.datetime(2024,9,3,12,0,0)
    timeTo = dt.datetime(2024,9,3,13,0,0)
    net_ccl_df = api.get_index('NET_CCL_ND',timeFrom,timeTo,type='pandas')
    

Author: PRJ
Date: 2024-09-03
"""

import enindex_tools.api_client as api_client
import datetime as dt
import pandas as pd
import json

class Api():
    def __init__(self,client=None):
        self._client = (api_client.ApiClient() if client == None else client)
        self._supported_formats = set(['json','pandas'])

    def get_index(self, dataset, time_from, time_to,format='json'):
        """
        Request an index dataset and return the result.

        Paramaters: 
        - dataset: string containing the id of the index e.g. "NET_CCL_ND"
        - timeFrom: datetime.datetime (with tzInfo). If not on a minute boundary
                    this will be rounded to the prior minute boundary
        - timeTo: datetime.datetime (with txInfo). If not on a minute boundary
                  this will be rounded to the prior minute boundary
        - format: 'json' returns the response.json(). 
                  'pandas' returns a pandas dataframe. 

        Returns:
        - list of IndexSegment. Index segments contain:
            IndexSegment {
                dataset: string,
                timeFrom: string,
                levelFrom: number,
                timeTo: string,
                levelTo: number
            }
        """
        self._check_format(format)
        chunk_list = self._create_req_chunks(time_from,time_to)
        responses = self._make_chunked_requests(f'index/{dataset}',chunk_list)
        
        if (format == 'pandas'):
            return pd.DataFrame.from_records(responses)
        else:
            return responses
    
    def get_stack_at(self,time,format='json'):
        """
        Request the full system stack for a specific time.

        Paramaters: 
        - time: datetime.datetime (with tzInfo). If not on a minute boundary
                    this will be rounded to the prior minute boundary

        Returns:
        - list of StackElements. Stack elements come in one of two types
          BmStackElements and Disbsad Stack Elements:
          

          {
            'timeType': 'FROM',
            'bmUnit': 'T_COSO-1',
            'elementId': 1,
            'time': '2024-09-03T12:00:00.000Z',
            'elementType': 'BM',
            'commitmentTime': 360,
            'direction': 'OFFER',
            'eFlaggedAccepted': 0,
            'eFlaggedNet': 0,
            'eFlaggedReversed': 0,
            'mainPrice': 175,
            'memberOf': ['UP_REG_ENERGY', 'VOLTS_INERTIA_SYNC'],
            'noticeTime': 60,
            'pairId': 1,
            'quantity': 470,
            'quantityAccepted': 0,
            'quantityAvailable': 470,
            'revenueRate': 0,
            'reversePrice': 50.099998474121094,
            'sFlaggedAccepted': 0,
            'sFlaggedNet': 0,
            'sFlaggedReversed': 0,
            'side': 'EXPORT',
            'zeroToSel': True,
            'zeroToSil': False},
        }

        Note that this end point will return stack elements with timeType FROM only
        corresponding to the instant immediately after the request time.
        """
        self._check_format(format)
        response = self._client.get('stack/at',{'time':time.isoformat()})
        response_json = response.json()
        if (format == 'pandas'):
            return pd.DataFrame.from_records(response_json)
        else:
            return response_json


    def get_bmu_stack(self, bm_unit, time_from, time_to,format='json'):
        """
        Request stack elements for a specifc BMU in a given time range.

        Paramaters: 
        - bm_unit: The bmu id of the unit being requested (e.g. T_COSO-1)
        - time_from: datetime.datetime (with tzInfo). If not on a minute boundary
                    this will be rounded to the prior minute boundary
        - time_to: datetime.datetime (with tzInfo). If not on a minute boundary
                  this will be rounded to the prior minute boundary

        Returns:
        - list of StackElements. Stack elements come in one of two types
          BmStackElements and Disbsad Stack Elements:
          This endpoint will always return BmStackElements, an example of
          which is given below.

          {
            'timeType': 'FROM',
            'bmUnit': 'T_COSO-1',
            'elementId': 1,
            'time': '2024-09-03T12:00:00.000Z',
            'elementType': 'BM',
            'commitmentTime': 360,
            'direction': 'OFFER',
            'eFlaggedAccepted': 0,
            'eFlaggedNet': 0,
            'eFlaggedReversed': 0,
            'mainPrice': 175,
            'memberOf': ['UP_REG_ENERGY', 'VOLTS_INERTIA_SYNC'],
            'noticeTime': 60,
            'pairId': 1,
            'quantity': 470,
            'quantityAccepted': 0,
            'quantityAvailable': 470,
            'revenueRate': 0,
            'reversePrice': 50.099998474121094,
            'sFlaggedAccepted': 0,
            'sFlaggedNet': 0,
            'sFlaggedReversed': 0,
            'side': 'EXPORT',
            'zeroToSel': True,
            'zeroToSil': False},
        }

        Note that this end point will return stack elements with timeType FROM and TO,
        corresponding to the instant before and after time.
        """
        self._check_format(format)
        chunk_list = self._create_req_chunks(time_from,time_to,max_req_duraton_hrs=1)
        responses = self._make_chunked_requests(f'stack/{bm_unit}',chunk_list)
        
        if (format == 'pandas'):
            return pd.DataFrame.from_records(responses)
        else:
            return responses
        
    """
    Private functions which should not be called directly by a user of the Api object 
    """
    
    def _create_req_chunks(self, time_from, time_to, max_req_duraton_hrs = 48):
        """
        Creates a list of from and to times each no linger than self._max_req_duration
        starting the minute boundary on or before time_from and ending on or after
        time_to.

        Paramaters: 
        - time_from: datetime.datetime for request start
        - time_to: datetiem.datetime for request end
        
        Returns:
        - list of tuples: [(time_from,time_to),(time_from,time_to)...]
        """
        max_req_duration = dt.timedelta(hours=max_req_duraton_hrs)
        rounded_time_from = time_from.replace(second=0, microsecond=0)
        #subtract 1 microsecond from min added to time_to to avoid rounding minute boundary up
        rounded_time_to = (time_to + dt.timedelta(seconds=60) - dt.timedelta(microseconds=1)).replace(second=0, microsecond=0)

        t0 = rounded_time_from
        t1 = t0

        chunk_list = []

        while (t1<rounded_time_to):
            t0 = t1
            t1 = min(t0 + max_req_duration, rounded_time_to)
            chunk_list.append((t0,t1))

        return chunk_list
    
    def _make_chunked_requests(self,endpoint,chunk_list):
        """
        Makes requests of the endpoint for each chunk.

        Paramaters: 
        - endpoint: string path to the data e.g. "index/NET_CCL_MW 
        - chunk list: list of tuples with from and to times for each chunk: [(time_from,time_to),(time_from,time_to)...]
        
        Returns:
        - list of json response objects for each chunk.
        """
        responses = []
        for chunk in chunk_list:
            response = self._client.get(endpoint,{'timeFrom':chunk[0].isoformat(),'timeTo':chunk[1].isoformat()})
            response_json = response.json()
            responses.extend(response_json)
        return responses
    
    def _check_format(self,format):
        if not format in self._supported_formats:
            raise ValueError(f'Format must be one of {[format in self._supported_formats]}')
    
        