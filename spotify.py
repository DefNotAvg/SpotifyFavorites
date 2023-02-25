import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

class Spotify:
	def __init__(self, username, scope, lookback_days):
		'''Initialize Spotify class with some attributes.

		Attributes:
			spotify: Authorized Spotipy instance.
		'''
		token = spotipy.util.prompt_for_user_token(username, scope)
		self.spotify = spotipy.Spotify(auth=token)
		self.lookback_days = lookback_days

	def days_since_release(self, track):
		'''Given Spotify API track info, return the number of days it's been since the specified Spotify track was released.

		Args:
			track: Spotify API track info.

		Returns:
			Number of days it's been since the specified list of dictionaries containing an artist's name and their Spotify ID.
		'''
		date_format = '%Y-%m-%d' if track['album']['release_date_precision'] == 'day' else '%Y'
		release_date = datetime.strptime(track['album']['release_date'], date_format)
		return (datetime.utcnow() - release_date).days

	def get_artist_track_ids(self, artist, limit=10, offset=0):
		'''Return track IDs from the specified artist released in the last self.lookback_days days.

		Args:
			artist: Dictionary containing a Spotify arist's name and URI.
			limit: Number of tracks to return within a single API call.
			offset: The total number of tracks scanned thus far.

		Returns:
			List of track IDs.
		'''
		results = self.spotify.search(artist['name'], limit=limit, offset=offset, type='track', market=None)['tracks']['items']
		if not results or any(self.days_since_release(item) > self.lookback_days for item in results):
			return [self.uri_to_id(item['uri']) for item in results if self.days_since_release(item) <= self.lookback_days and any(search_artist['uri'] == artist['uri'] for search_artist in item['artists'])]
		else:
			return [self.uri_to_id(item['uri']) for item in results if self.days_since_release(item) <= self.lookback_days and any(search_artist['uri'] == artist['uri'] for search_artist in item['artists'])] + self.get_artist_track_ids(artist_uri, limit, offset + limit)

	def get_followed_artists(self, limit=20, after=None):
		'''Obtain all artists the authenticated user follows.

		Args:
			limit: Number of artists to return within a single API call.
			after: The last artist ID retrieved from the previous API call.

		Returns:
			A list of dictionaries containing an artist's name and their Spotify URI.
		'''
		results = self.spotify.current_user_followed_artists(limit=limit, after=after)['artists']['items']
		artists = [{'name': item['name'], 'uri': item['uri']} for item in results]
		if len(artists) < limit:
			return artists
		else:
			return artists + self.get_followed_artists(limit, self.uri_to_id(artists[-1]['uri']))

	def uri_to_id(self, uri):
		'''Parse ID from Spotify URI.

		Args:
			uri: Spotify URI.

		Returns:
			Spotify ID string.
		'''
		return uri.split(':')[-1]