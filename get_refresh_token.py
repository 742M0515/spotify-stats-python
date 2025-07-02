import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import sys
import json

def get_refresh_token():
    # Read credentials from environment variables for security
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set as environment variables.")
        sys.exit(1)
    
    REDIRECT_URI = 'http://127.0.0.1:5173/callback/'
    SCOPE = 'user-library-read user-top-read user-read-recently-played user-read-playback-state'

    # Initialize SpotifyOAuth with cache path to store token info
    cache_path = ".spotify_cache"
    try:
        auth_manager = SpotifyOAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    redirect_uri=REDIRECT_URI,
                                    scope=SCOPE,
                                    cache_path=cache_path,
                                    open_browser=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print("Error: Port 5173 is already in use. Please ensure no other server is running on this port.")
            print("You can stop any running server on port 5173 or try a different port by modifying the REDIRECT_URI.")
            sys.exit(1)
        raise
    
    # This will open a browser for authentication
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # Attempt to get current playback to ensure authentication is complete
    sp.current_playback()
    
    # Read the cache file to extract the refresh token
    if os.path.exists(cache_path):
        with open(cache_path, 'r') as f:
            token_info = json.load(f)
            refresh_token = token_info.get('refresh_token')
            if refresh_token:
                print(f"Refresh Token: {refresh_token}")
                print("Copy this token and store it securely as SPOTIFY_REFRESH_TOKEN in your GitHub Secrets.")
            else:
                print("Error: Could not find refresh token in cache.")
                sys.exit(1)
    else:
        print("Error: Cache file not found. Authentication may have failed.")
        sys.exit(1)

if __name__ == "__main__":
    get_refresh_token()
