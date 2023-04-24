import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

class Spotify:
	def __init__(self, username, scope, lookback_days, explicit):
		'''Initialize Spotify class with some attributes.

		Attributes:
			spotify: Authorized Spotipy instance.
			lookback_days: Number of days within release all songs must be.
			explicit: True if explicit songs should be included and preferred to their clean counterpart, False to avoid explicit tracks altogether.
		'''
		token = spotipy.util.prompt_for_user_token(username, scope)
		self.spotify = spotipy.Spotify(auth=token)
		self.lookback_days = lookback_days
		self.explicit = explicit

	def days_since_release(self, album):
		'''Given Spotify API album info, obtain the number of days it's been since the specified Spotify album was released.

		Args:
			album: Spotify API album info.

		Returns:
			Number of days it's been since the specified Spotify album was released.
		'''
		date_format = '%Y-%m-%d' if album['release_date_precision'] == 'day' else '%Y'
		release_date = datetime.strptime(album['release_date'], date_format)
		return (datetime.utcnow() - release_date).days

	def get_playlist_track_ids(self, playlist_id, limit=50, offset=0):
		'''Obtain track IDs from the specified playlist.

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

	def get_artist_tracks(self, artist_uri):
		'''Obtain various track info from the specified artist.

		Args:
			artist_uri: Spotify artist URI.

		Returns:
			List of dictionaries containing various track info.
		'''
		results = []
		for album in self.get_artist_albums(artist_uri):
			results.extend(self.get_album_tracks(album['uri'], album['type'], artist_uri))
		return results

	def track_info(self, track, album_type):
		'''Obtain various track info given full Spotify API track info and album type.

		Args:
			track: Spotify API track info.
			album_type: Album type the track is a part of.

		Returns:
			Dictionary containing various track info.
		'''
		return {
			'albumType': album_type,
			'artists': ', '.join(sorted([artist['name'] for artist in track['artists']])),
			'explicit': track['explicit'],
			'id': track['id'],
			'name': track['name']
		}

	def get_album_tracks(self, album_id, album_type, artist_uri, limit=50, offset=0):
		'''Obtain various track info for all of the tracks from the specified album in which the specified artist is a part of.

		Args:
			album_id: Spotify album ID.
			album_type: Album type.
			artist_uri: Spotify artist URI.
			limit: Number of tracks to return within a single API call.
			offset: The total number of tracks scanned thus far.

		Returns:
			List of dictionaries containing various track info.
		'''
		results = self.spotify.album_tracks(album_id, limit=limit, offset=offset)['items']
		if not results or len(results) < limit:
			return [self.track_info(item, album_type) for item in results if (self.explicit or not item['explicit']) and any(artist['uri'] == artist_uri for artist in item['artists'])]
		else:
			return [self.track_info(item, album_type) for item in results if (self.explicit or not item['explicit']) and any(artist['uri'] == artist_uri for artist in item['artists'])] + self.get_album_tracks(album_id, album_type, artist_uri, limit=limit, offset=offset + limit)

	def get_artist_albums(self, artist_uri, limit=50, offset=0):
		'''Obtain album IDs from the specified artist released in the last self.lookback_days days.

		Args:
			artist_uri: Spotify artist URI.
			limit: Number of albums to return within a single API call.
			offset: The total number of albums scanned thus far.

		Returns:
			List of dictionaries containing an album's URI and type.
		'''
		results = self.spotify.artist_albums(artist_uri, limit=limit, offset=offset)['items']
		if not results or len(results) < limit:
			return [{'uri': item['uri'], 'type': item['album_type']} for item in results if item['album_type'] != 'compilation' and self.days_since_release(item) <= self.lookback_days]
		else:
			return [{'uri': item['uri'], 'type': item['album_type']} for item in results if item['album_type'] != 'compilation' and self.days_since_release(item) <= self.lookback_days] + self.get_artist_albums(artist_uri, limit=limit, offset=offset + limit)

	def get_followed_artists(self, limit=50, after=None):
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