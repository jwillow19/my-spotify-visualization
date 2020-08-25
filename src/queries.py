import sqlite3

conn = sqlite3.connect("../db/spotify.sqlite")
cur = conn.cursor()

table_name = "top-spotify-tracks"


def get_all_tracks():
    """
    Select the entire table
    """
    for row in cur.execute(f"select * from `{table_name}`"):
        print(row)
    # return cur.fetchall()


def most_frequent_artist():
    """
    Query: find the top 10 most frequent artist from favourite playlist
    """
    cur.execute(
        f"""SELECT by, count(*) FROM `{table_name}` GROUP BY by ORDER BY count(*) DESC LIMIT 10"""
    )
    return cur.fetchall()


artist_list = most_frequent_artist()
print(artist_list)
