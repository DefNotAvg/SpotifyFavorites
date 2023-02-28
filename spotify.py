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

	def days_since_release(self, album):
		'''Given Spotify API album info, return the number of days it's been since the specified Spotify album was released.

		Args:
			album: Spotify API album info.

		Returns:
			Number of days it's been since the specified list of dictionaries containing an artist's name and their Spotify ID.
		'''
		date_format = '%Y-%m-%d' if album['release_date_precision'] == 'day' else '%Y'
		release_date = datetime.strptime(album['release_date'], date_format)
		return (datetime.utcnow() - release_date).days

	def get_playlist_track_ids(self, playlist_id, limit=50, offset=0):
		'''Return track IDs from the specified playlist.

		Args:
			playlist_id: Spotify playlist ID.
			limit: Number of tracks to return within a single API call.
			offset: The total number of tracks scanned thus far.

		Returns:
			List of track IDs.
		'''
		results = self.spotify.playlist_tracks(playlist_id, limit=limit, offset=offset)['items']
		if not results or len(results) < limit:
			return [item['track']['id'] for item in results]
		else:
			return [item['track']['id'] for item in results] + self.get_playlist_track_ids(playlist_id, limit=limit, offset=offset + limit)

	def get_artist_track_ids(self, artist_uri):
		'''Return track IDs from the specified artist released in the last self.lookback_days days.

		Args:
			artist_uri: Spotify artist URI.

		Returns:
			List of track IDs.
		'''
		results = []
		for album_id in self.get_artist_album_ids(artist_uri):
			results.extend(self.get_album_track_ids(album_id, artist_uri))
		return results

	def get_album_track_ids(self, album_id, artist_uri, limit=50, offset=0):
		'''Return track IDs from the specified album in which the specified artist is a part of.

		Args:
			album_id: Spotify album ID.
			artist_uri: Spotify artist URI.
			limit: Number of tracks to return within a single API call.
			offset: The total number of tracks scanned thus far.

		Returns:
			List of track IDs.
		'''
		results = self.spotify.album_tracks(album_id, limit=limit, offset=offset)['items']
		if not results or len(results) < limit:
			return [item['id'] for item in results if any(artist['uri'] == artist_uri for artist in item['artists'])]
		else:
			return [item['id'] for item in results if any(artist['uri'] == artist_uri for artist in item['artists'])] + self.get_album_track_ids(album_id, artist_uri, limit=limit, offset=offset + limit)

	def get_artist_album_ids(self, artist_uri, limit=50, offset=0):
		'''Return album IDs from the specified artist released in the last self.lookback_days days.

		Args:
			artist_uri: Spotify artist URI.
			limit: Number of albums to return within a single API call.
			offset: The total number of albums scanned thus far.

		Returns:
			List of album IDs.
		'''
		results = self.spotify.artist_albums(artist_uri, limit=limit, offset=offset)['items']
		if not results or len(results) < limit:
			return [item['uri'] for item in results if item['album_type'] != 'compilation' and self.days_since_release(item) <= self.lookback_days]
		else:
			return [item['uri'] for item in results if item['album_type'] != 'compilation' and self.days_since_release(item) <= self.lookback_days] + self.get_artist_album_ids(artist_uri, limit=limit, offset=offset + limit)

	def get_followed_artists(self, limit=20, after=None):
		'''Obtain all artists the authenticated user follows.

		Args:
			limit: Number of artists to return within a single API call.
			after: The last artist ID retrieved from the previous API call.

		Returns:
			A list of dictionaries containing an artist's name, their Spotify ID, and their Spotify URI.
		'''
		results = self.spotify.current_user_followed_artists(limit=limit, after=after)['artists']['items']
		artists = [{'name': item['name'], 'id': item['id'], 'uri': item['uri']} for item in results]
		if len(artists) < limit:
			return artists
		else:
			return artists + self.get_followed_artists(limit=limit, after=artists[-1]['id'])