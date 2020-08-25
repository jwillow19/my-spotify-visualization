import sqlite3
import csv


"""
Python script to load data in CSV file (created from playlits2csv.py) to sqlite Database
"""


fname = "top_spotify_tracks"

conn = sqlite3.connect("../db/spotify.sqlite")
cur = conn.cursor()

try:
    conn.execute(f"DROP TABLE IF EXISTS `{fname}` ")
    print("Table dropped")
except Exception as e:
    raise (e)

try:
    conn.execute(
        f"""
    CREATE TABLE `{fname}` (
        track_name          TEXT,
        track_id            TEXT,
        by                  TEXT, 
        feature             TEXT,
        album_id            TEXT,
        album_name          TEXT,
        album_image         TEXT,
        release_date        DATE,
        album_popularity    INT,
        duration            INT,
        year                INT);
    """
    )
    print("Table created successfully")
except Exception as e:
    print(str(e))
    print("Table Creation Failed!")


with open(f"../data/{fname}.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        track_name = row[1]
        track_id = row[2]
        by = row[3]
        feature = row[4]
        album_id = row[5]
        album_name = row[6]
        album_image = row[7]
        release_date = row[8]
        album_popularity = row[9]
        duration = row[10]
        year = row[11]

        track_list = [
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
            year,
        ]
        try:
            cur.execute(
                f"""
            INSERT INTO `{fname}` (track_name, track_id, by, feature, album_id, album_name, album_image, release_date, album_popularity, duration, year) VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """,
                (
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
                    year,
                ),
            )
            conn.commit()
            print("Data Inserted Successfully")

        except Exception as e:
            print(str(e))
            print("Data Insertion Failed")

    conn.close()
