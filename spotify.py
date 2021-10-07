import os
from dataclasses import dataclass

import requests


_AUTH_URL = 'https://accounts.spotify.com/api/token'
_SEARCH_URL = 'https://api.spotify.com/v1/search'


@dataclass
class Track:
    """Spotify track"""

    name: str
    artists: list[str]
    album: str
    image_url: str
    open_url: str


def get_auth_token() -> str:
    """
    Get Bearer token from Spotify token API
    using client id and secret from .env file.
    """

    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    req = requests.post(
        _AUTH_URL,
        auth=(client_id, client_secret),
        data={'grant_type': 'client_credentials'},
    )
    token = req.json()['access_token']

    return token


def search_track(name: str, auth_token: str) -> list[Track]:
    """Search for track with exact name using Spotify seach API."""

    # Search for tracks with name.
    params = {'q': name, 'type': 'track', 'limit': 50}
    headers = {'Authorization': f'Bearer {auth_token}'}
    req = requests.get(_SEARCH_URL, headers=headers, params=params)

    # Return first track that exactly matches the name.
    items = req.json()['tracks']['items']
    for item in items:
        if name == item['name'].lower():
            track = Track(
                item['name'],
                artists=[artist['name'] for artist in item['artists']],
                album=item['album']['name'],
                image_url=item['album']['images'][0]['url'],
                open_url=item['external_urls']['spotify'],
            )
            return track

    return None
