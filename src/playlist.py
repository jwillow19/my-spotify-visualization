from utils import *
import pandas as pd
import numpy as np
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
        """
        Parse all tracks and save list of dicts of tracks to self.track 
        """
        temp_list = []
        rows = []
        playlist_id = self.playlist_id
        playlist_items = self.get_playlist(playlist_id)["items"]

        if not playlist_items:
            raise Exception("No Playlist, check playlistID")

        for item in playlist_items:
            track_dict = parse_track(item)
            temp_list.append(track_dict)
            rows.append(item_to_row(item))

        self.tracks = temp_list

    def construct_dataframe(self):
        rows = []
        playlist_id = self.playlist_id
        playlist_items = self.get_playlist(playlist_id)["items"]
        for item in playlist_items:
            rows.append(item_to_row(item))

        rows = np.array(rows, dtype=object)
        df = pd.DataFrame(
            data=rows,
            columns=[
                "track_name",
                "track_id",
                "by",
                "feature",
                "album_id",
                "album_name",
                "album_image",
                "release_date",
                "album_popularity",
                "duration",
            ],
        )
        return df

    def get_artists(self):
        """
        Returns a set of unique artists from the Playlist
        """
        tracks = self.tracks

        artists = [track["by"] for track in tracks]
        unique_artists = set(artists)

        self.artists = unique_artists
        return unique_artists

    def count_by_artist(self):
        """
        Count the number of tracks from artist in this playlist
        """
        artist_dict = {}
        tracks = self.tracks
        artists = [track["by"] for track in tracks]

        #     Logic - loop through the list of artists, check if artist is in dict
        # if false: add to dict
        # if true: increment value by 1
        for artist in artists:
            if artist not in artist_dict:
                artist_dict[artist] = 1
            else:
                num_occurance = artist_dict[artist]
                to_update = {artist: num_occurance + 1}
                artist_dict.update(to_update)

        # sort by value in desccending order then convert to dict
        sorted_artists = dict(
            sorted(artist_dict.items(), key=lambda kv: kv[1], reverse=True)
        )

        return sorted_artists
