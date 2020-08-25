import os
import numpy as np
from playlist import Playlist

"""
Python script to create Playlist objects using SpotifyAPI, extract information and transform it into a pd.DataFrame object, save to csv
"""

top_2019_id = "37i9dQZF1EtsKZinWyvvzX"
top_2018_id = "37i9dQZF1EjefPCsndl34q"
top_2017_id = "37i9dQZF1E9PDuAPTNqRWN"
top_2016_id = "37i9dQZF1Cz1NXVJwDDfcU"

# Instantiate Playlist Class using: api_key and playlistID
api_key = input("Enter Spotify Auth Token: ")
top2019 = Playlist(api_key, top_2019_id)
top2018 = Playlist(api_key, top_2018_id)
top2017 = Playlist(api_key, top_2017_id)
top2016 = Playlist(api_key, top_2016_id)

print("Creating DataFrames for Playlists...")
df2019 = top2019.construct_dataframe()
df2018 = top2018.construct_dataframe()
df2017 = top2017.construct_dataframe()
df2016 = top2016.construct_dataframe()

# Append year to each DF - np.full(dim_shape, fill_value)
df2019["playlist"] = np.full((df2019.shape[0], 1), 2019)
df2018["playlist"] = np.full((df2018.shape[0], 1), 2018)
df2017["playlist"] = np.full((df2017.shape[0], 1), 2017)
df2016["playlist"] = np.full((df2016.shape[0], 1), 2016)


main_df = df2019.append([df2018, df2017, df2016], ignore_index=True)

# Save to csv
print("Saving DataFrames to CSVs...")

df2019.to_csv("../data/top_2019.csv", sep=",")
df2018.to_csv("../data/top_2018.csv", sep=",")
df2017.to_csv("../data/top_2017.csv", sep=",")
df2016.to_csv("../data/top_2016.csv", sep=",")
main_df.to_csv("../data/top_spotify_tracks.csv", sep=",")

print("Done!")
