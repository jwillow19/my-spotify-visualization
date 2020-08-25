def convert_ms(millis):
    """
    convert milliseconds into seconds
    """
    millis = int(millis)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    #     hours=(millis/(1000*60*60))%24
    min2sec = minutes * 60

    return min2sec + seconds


def parse_track(item):
    """
    Parses one item from the playlist and return artist dictionary
    """
    track = item["track"]

    track_id = track["id"]
    track_name = track["name"]
    track_artists = [artist["name"] for artist in track["artists"]]
    lead, feature = track_artists[0], track_artists[1:]

    if not feature:
        feature = None

    album_name, album_image = track["album"]["name"], track["album"]["images"][0]["url"]
    release_date = track["album"]["release_date"]
    album_popularity = track["popularity"]
    duration = convert_ms(track["duration_ms"])

    return {
        track_name: {
            "album": album_name,
            "album_image": album_image,
            "track_id": track_id,
            "release_date": release_date,
            "popularity": album_popularity,
            "duration": duration,
        },
        "by": lead,
        "features": feature,
    }

    #  {lead: {'track': track_name,
    #                'album': album_name,
    #                'albumImage': album_image,
    #                'release_date': release_date,
    #                'popularity': album_popularity,
    #                'duration': duration},
    #         'features': feature}


def item_to_row(item):
    """
    Parses a Spotify Playlist Item, extract and transform into row format 
    For converting to DataFrame
    """
    track = item["track"]

    track_id = track["id"]
    track_name = track["name"]
    track_artists = [artist["name"] for artist in track["artists"]]
    by, feature = track_artists[0], track_artists[1:]

    if not feature:
        feature = None

    album_id = track["album"]["id"]
    album_name, album_image = track["album"]["name"], track["album"]["images"][0]["url"]
    release_date = track["album"]["release_date"]
    album_popularity = track["popularity"]
    duration = convert_ms(track["duration_ms"])

    return [
        track_name,
        track_id,
        by,
        feature,
        album_id,
        album_name,
        album_image,
        release_date,
        album_popularity,
        duration,
    ]
