def convert_ms(millis):
    '''
    convert milliseconds into seconds
    '''
    millis = int(millis)
    seconds = (millis/1000) % 60
    seconds = int(seconds)
    minutes = (millis/(1000*60)) % 60
    minutes = int(minutes)
#     hours=(millis/(1000*60*60))%24
    min2sec = minutes * 60

    return min2sec + seconds


def parse_track(item):
    '''
    Parses one item from the playlist and return artist dictionary
    '''
    track = item['track']

    track_name = item['track']['name']
    track_artists = [artist['name'] for artist in track['artists']]
    lead, feature = track_artists[0], track_artists[1:]

    if not feature:
        feature = None

    album_name, album_image = track['album']['name'], track['album']['images'][0]['url']
    release_date = track['album']['release_date']
    album_popularity = track['popularity']
    duration = convert_ms(track['duration_ms'])

    return {track_name: {
        'album': album_name,
        'album_image': album_image,
        'release_date': release_date,
        'popularity': album_popularity,
        'duration': duration},
        'by': lead,
        'features': feature}

    #  {lead: {'track': track_name,
    #                'album': album_name,
    #                'albumImage': album_image,
    #                'release_date': release_date,
    #                'popularity': album_popularity,
    #                'duration': duration},
    #         'features': feature}
