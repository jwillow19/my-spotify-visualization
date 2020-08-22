#!/usr/bin/env python
# coding: utf-8

# In[1]:


import base64
import requests
# urlencode - wrap this around a data dictionary to create a URL ready string
from urllib.parse import urlencode

import datetime
from secrets import client_id, client_secret


class SpotifyAPI():
    # Placeholder for attributes
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_endpoint = 'https://accounts.spotify.com/api/token'
    user_id = '12185809439'
    playlist_endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'

    def __init__(self, api_key, client_id=None, client_secret=None, *args, **kwargs):
        # super init - allows it to call any class that its inheriting from
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key

    def get_client_credentials(self):
        '''
        Returns a base64 encoded string
        '''
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("Must set client_id and client_secret")
        client_cred = f"{client_id}:{client_secret}"
        client_cred_b64 = base64.b64encode(client_cred.encode())
        return client_cred_b64.decode()

    def get_token_headers(self):
        client_cred_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_cred_b64}"
        }

    def get_bearer_headers(self):
        api_key = self.api_key
        return {
            "Authorization": f"Bearer {api_key}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def auth(self):
        token_endpoint = self.token_endpoint
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()

        r = requests.post(token_endpoint, data=token_data,
                          headers=token_headers)

        if r.status_code not in range(200, 299):
            return False

        print(f"Status Code: {r.status_code}")
        now = datetime.datetime.now()
        token_response = r.json()
        access_token = token_response['access_token']
        expires_in = token_response['expires_in']  # in seconds
        # use datetime to calculate the time of expiration
        expires = now + datetime.timedelta(seconds=expires_in)

        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        self.token_res = token_response
        return True

    def get_my_playlists(self, limit, offset):
        user_id = '12185809439'
        playlist_endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        headers = self.get_bearer_headers()
        data = urlencode({"limit": limit, 'offset': offset})
        # A URL ready string to get user playlists
        lookup_url = f"{playlist_endpoint}?{data}"

        res = requests.get(lookup_url, headers=headers)

        if res.status_code not in range(200, 299):
            raise Exception(res.json())

        playlists_name = [playlist['name'] for playlist in res.json()['items']]
        self.my_playlists = playlists_name

    def get_playlist(self, playlist_id):
        '''
        Takes a playlistID and return the playlist
        '''
        headers = self.get_bearer_headers()
        playlist_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        res = requests.get(playlist_endpoint, headers=headers)

        if res.status_code not in range(200, 299):
            raise Exception(res.json())
        return res.json()
