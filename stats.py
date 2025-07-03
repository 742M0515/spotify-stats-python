import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import sys
import time

def get_spotify_stats():
    # Read credentials from environment variables for security
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set as environment variables.")
        sys.exit(1)
    if not REFRESH_TOKEN:
        print("Error: SPOTIFY_REFRESH_TOKEN must be set as an environment variable for non-interactive authentication.")
        sys.exit(1)

    REDIRECT_URI = 'http://127.0.0.1:5173/callback/'  # Still needed for token refresh context
    SCOPE = 'user-library-read user-top-read user-read-recently-played user-read-playback-state'

    # Updated token_info to fix the KeyError: 'expires_at'
    token_info = {
        'refresh_token': REFRESH_TOKEN,
<<<<<<< HEAD
        'access_token': '',  # Spotipy will fetch a new token using the refresh token
        'expires_in': 0,     # Expires immediately so Spotipy refreshes
        'expires_at': int(time.time()),  # Set to now so Spotipy refreshes immediately
        'scope': SCOPE,
        'token_type': 'Bearer'
    }

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_handler=spotipy.MemoryCacheHandler(token_info=token_info)
    ))
=======
        'token_type': 'Bearer',
        'scope': SCOPE
    }
    try:
        # Custom cache handler to ensure scope is a string
        class CustomCacheHandler(spotipy.cache_handler.CacheHandler):
            def __init__(self, token_info):
                self.token_info = token_info if token_info else {}
                if 'scope' in self.token_info and isinstance(self.token_info['scope'], list):
                    self.token_info['scope'] = ' '.join(self.token_info['scope'])
            
            def get_cached_token(self):
                return self.token_info
            
            def save_token_to_cache(self, token_info):
                self.token_info = token_info if token_info else {}
                if 'scope' in self.token_info and isinstance(self.token_info['scope'], list):
                    self.token_info['scope'] = ' '.join(self.token_info['scope'])
        
        auth_manager = SpotifyOAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    redirect_uri=REDIRECT_URI,
                                    scope=SCOPE,
                                    cache_handler=CustomCacheHandler(token_info))
        sp = spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        print(f"Error during Spotify authentication: {str(e)}")
        sys.exit(1)
>>>>>>> 5401b03 (build)

    # Prepare data dictionary for JSON output
    stats_data = {}

    # Now Playing
    try:
        now_playing = sp.current_playback()
        if now_playing and now_playing['is_playing']:
            track_name = now_playing['item']['name']
            artists = ', '.join([artist['name'] for artist in now_playing['item']['artists']])
            stats_data['now_playing'] = f"{track_name} - {artists}"
        else:
            stats_data['now_playing'] = "Nothing currently playing"
    except Exception as e:
        print(f"Error fetching current playback: {str(e)}")
        stats_data['now_playing'] = "Error fetching data"

    # Top Artists
    try:
        top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
        stats_data['top_artists'] = [artist['name'] for artist in top_artists['items']]
    except Exception as e:
        print(f"Error fetching top artists: {str(e)}")
        stats_data['top_artists'] = ["Error fetching data"]

    # Top Songs
    try:
        top_tracks = sp.current_user_top_tracks(limit=5, time_range='medium_term')
        stats_data['top_songs'] = [
            {'name': song['name'], 'artists': ', '.join([artist['name'] for artist in song['artists']])}
            for song in top_tracks['items']
        ]
    except Exception as e:
        print(f"Error fetching top songs: {str(e)}")
        stats_data['top_songs'] = [{'name': "Error fetching data", 'artists': ""}]

    # Top Albums (corrected from tracks to albums)
    try:
        top_albums = sp.current_user_top_tracks(limit=5, time_range='medium_term')
        stats_data['top_albums'] = [
            {'name': album['album']['name'], 'artists': ', '.join([artist['name'] for artist in album['artists']])}
            for album in top_albums['items']
        ]
    except Exception as e:
        print(f"Error fetching top albums: {str(e)}")
        stats_data['top_albums'] = [{'name': "Error fetching data", 'artists': ""}]

    # Recently Played
    try:
        recently_played = sp.current_user_recently_played(limit=5)
        stats_data['recently_played'] = [
            {'name': track['track']['name'], 'artists': ', '.join([artist['name'] for artist in track['track']['artists']])}
            for track in recently_played['items']
        ]
    except Exception as e:
        print(f"Error fetching recently played: {str(e)}")
        stats_data['recently_played'] = [{'name': "Error fetching data", 'artists': ""}]

    return stats_data

if __name__ == "__main__":
    stats = get_spotify_stats()
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "spotify-stats.json")
with open(output_path, 'w') as f:
    json.dump(stats, f, indent=2)
print(f"Spotify stats saved to {output_path}")
