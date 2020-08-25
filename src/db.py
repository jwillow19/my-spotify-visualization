import sqlite3
import os

"""
Database Class for establishing connection to sqlite DB and making queries
"""


class Database(object):
    def __init__(self, dbFileName, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._dbFile = dbFileName

        fileExist = self.exists()
        if fileExist:
            self.conn = sqlite3.connect(dbFileName)
            self.cur = self.conn.cursor()

    @property
    def dbFile(self):
        return self._dbFile

    @property
    def tables(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cur.fetchall()

    def exists(self):
        dbFileName = self._dbFile
        return os.path.exists(dbFileName)

    def fetch_all(self):
        try:
            table = self.table
            self.cur.execute(f"select * from `{table}`")
            return self.cur.fetchall()[1:]

        except AttributeError as e:
            print("No table selected. Select a table from DB first.")
            raise

    #             raise Exception('Select a table first')

    def select_table(self, table):
        self.table = table

    def top_artists(self, limit=10):
        """
        Using format string to declare table name and Parameter markers only for expressions, i.e., values
        """
        table = self.table
        self.cur.execute(
            f"SELECT by, count(*) FROM `{table}` GROUP BY by ORDER BY count(*) DESC LIMIT ?",
            (limit,),
        )
        return self.cur.fetchall()

    def top_tracks(self, limit=5):
        """
        Using format string to declare table name and Parameter markers only for expressions, i.e., values
        """
        table = self.table

        self.cur.execute(
            f"""SELECT track_name, by, count(track_name) AS track_occurance
                FROM `{table}`
                GROUP BY track_name, by
                ORDER BY track_occurance desc
                LIMIT ?""",
            (10,),
        )
        return self.cur.fetchall()

    def top_albums(self, limit=5):
        """
        PROBLEM: query DOES NOT count for repeating tracks - If song X appears in table twice it will count the album twice 
        """
        table = self.table

        self.cur.execute(
            f"""
        SELECT album_name, by, count(album_name) as occurance
        FROM `{table}`
        GROUP BY album_name
        ORDER BY occurance DESC
        LIMIT ?
        """,
            (limit,),
        )
        return self.cur.fetchall()

    def hipster_rating(self, year):
        """
        Finds the average popularity score of songs from a specific year
        """
        self.cur.execute(
            f"""
        SELECT AVG(album_popularity) 
        FROM `{table}`
        WHERE year=?
        """,
            (year,),
        )
        return self.cur.fetchone()[0]

    def average_duration(self, year):
        """
        Finds the average song duration from specific year
        """
        self.cur.execute(
            f"""
        SELECT AVG(duration) 
        FROM `{table}`
        WHERE year=?
        """,
            (year,),
        )
        duration_seconds = self.cur.fetchone()[0]
        minutes = round(duration_seconds) // 60
        seconds = round(duration_seconds) % 60
        print(f"{minutes}:{seconds}")

    ## Python destructor..
    #     For the database,  when the reference to object to the object is deleted,  the connection should be closed
    def __del__(self):
        self.conn.close()
