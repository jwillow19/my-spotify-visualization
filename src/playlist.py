from utils import *
from spotify_class import SpotifyAPI
# Make a playlist class that inherit SpotifyAPI class methods


class Playlist(SpotifyAPI):
    tracks = set()  # store a set of tracks
    # key:val - artist: {tracks: [{albumTitle, albumURL, imageURL, popularity, released_date},...], number of times artists appeared in playlist,}
    artists = dict()
    feature = dict()  # key:value - artist
    temp_list = []

    def __init__(self, api_key, playlist_id, *args, **kwargs):
        super().__init__(api_key, client_id=None, client_secret=None, *args, **kwargs)
        self.playlist_id = playlist_id
        self.api_key = api_key

    def parse_tracks(self):
        temp_list = []
        playlist_id = self.playlist_id
        playlist_items = self.get_playlist(playlist_id)['items']

        if not playlist_items:
            raise Exception('No Playlist, check playlistID')

        for item in playlist_items:
            track_dict = parse_track(item)
            temp_list.append(track_dict)

        self.tracks = temp_list
