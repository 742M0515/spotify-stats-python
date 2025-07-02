import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import sys

def get_spotify_stats():
    # Read credentials from environment variables for security
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set as environment variables.")
        sys.exit(1)
    
    REDIRECT_URI = 'http://127.0.0.1:5173/callback/'
    SCOPE = 'user-library-read user-top-read user-read-recently-played user-read-playback-state'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=SCOPE))

    # Prepare data dictionary for JSON output
    stats_data = {}

    # Now Playing
    now_playing = sp.current_playback()
    if now_playing and now_playing['is_playing']:
        track_name = now_playing['item']['name']
        artists = ', '.join([artist['name'] for artist in now_playing['item']['artists']])
        stats_data['now_playing'] = f"{track_name} - {artists}"
    else:
        stats_data['now_playing'] = "Nothing currently playing"

    # Top Artists
    top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
    stats_data['top_artists'] = [artist['name'] for artist in top_artists['items']]

    # Top Songs
    top_tracks = sp.current_user_top_tracks(limit=5, time_range='medium_term')
    stats_data['top_songs'] = [
        {'name': song['name'], 'artists': ', '.join([artist['name'] for artist in song['artists']])}
        for song in top_tracks['items']
    ]

    # Top Albums (corrected from tracks to albums)
    top_albums = sp.current_user_top_tracks(limit=5, time_range='medium_term')
    stats_data['top_albums'] = [
        {'name': album['album']['name'], 'artists': ', '.join([artist['name'] for artist in album['artists']])}
        for album in top_albums['items']
    ]

    # Recently Played
    recently_played = sp.current_user_recently_played(limit=5)
    stats_data['recently_played'] = [
        {'name': track['track']['name'], 'artists': ', '.join([artist['name'] for artist in track['track']['artists']])}
        for track in recently_played['items']
    ]

    return stats_data

if __name__ == "__main__":
    stats = get_spotify_stats()
    # Output to JSON file relative to the current directory
    output_path = "spotify-stats.json"
    with open(output_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"Spotify stats saved to {output_path}")
