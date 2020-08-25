import sqlite3
import csv

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
        by                  TEXT, 
        feature             TEXT,
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
        by = row[2]
        feature = row[3]
        album_name = row[4]
        album_image = row[5]
        release_date = row[6]
        album_popularity = row[7]
        duration = row[8]
        year = row[9]

        track_list = [
            track_name,
            by,
            feature,
            album_name,
            album_image,
            release_date,
            album_popularity,
            duration,
        ]
        try:
            cur.execute(
                f"""
            INSERT INTO `{fname}` (track_name, by, feature, album_name, album_image, release_date, album_popularity, duration, year) VALUES (?,?,?,?,?,?,?,?,?)
            """,
                (
                    track_name,
                    by,
                    feature,
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
