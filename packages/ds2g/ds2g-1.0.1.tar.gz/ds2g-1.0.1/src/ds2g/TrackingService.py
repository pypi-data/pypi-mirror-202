import asyncio
import httpx
from datetime import datetime

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json

class TrackingService:
    """TrackingService class"""
    def __init__(self, key):
        if key is None:
            raise Exception('Track-Anything: Key has to be set!')
        self.trackingURL = 'https://tracking.ds2g.io:443/' + key

    def __prepData(self, params):
        track_type = ''
        track_application = ''
        track_value = ''
        track_date = ''

        if 'type' in params:
            track_type = str(params['type'])
        
        if 'applicationKey' in params:
            track_application = str(params['applicationKey'])
        
        if 'value' in params:
            track_value = str(params['value'])
        
        if 'date' in params:
            track_date = str(params['date'])
        else:
            track_date = str(datetime.now().isoformat())
            
        return {
            'type': track_type,
            'application':track_application,
            'value': track_value,
            'trackDate': track_date
        }

    async def __async_send_track(self, client, post_fields):
        try:
            await client.post(self.trackingURL, json=post_fields)
        except httpx.HTTPError as error:
            if error.code == 503:
                try:
                    await client.get(self.trackingURL, params=post_fields)
                except httpx.HTTPError as error_retry:
                    print(error_retry)
            else:
                print(error)
    
    async def __async_send_many_tracks(self, post_fields_list):
        async with httpx.AsyncClient() as client:
            requests = []
            for post_fields in post_fields_list:
                requests.append(asyncio.ensure_future(self.__async_send_track(client, post_fields)))
            await asyncio.gather(*requests)

    def send_track(self, params):
        post_fields = self.__prepData(params)

        try:
            httpx.post(self.trackingURL, json=post_fields)
        except httpx.HTTPError as error:
            if error.code == 503:
                try:
                    httpx.get(self.trackingURL, params=post_fields)
                except httpx.HTTPError as error_retry:
                    print(error_retry)
            else:
                print(error)

    def send_many_tracks(self, tracks):
        post_fields_list = list(map(self.__prepData, tracks))
        asyncio.run(self.__async_send_many_tracks(post_fields_list))