import os
from helpers import *
from spotify import Spotify

if __name__ == '__main__':
	header()
	if os.getenv('SPOTIPY_CLIENT_ID') and os.getenv('SPOTIPY_CLIENT_SECRET'):
		config = load_from_json('config.json')
		os.environ['SPOTIPY_REDIRECT_URI'] = config['redirectURI']
		while True:
			sp = Spotify(config['username'], config['scope'] + ' user-follow-read', config['lookbackDays'])
			print('{}\r'.format(center('[{}] Gathering followed arists...'.format(smart_time()), display=False)), end='')
			followed_artists = sp.get_followed_artists()
			center('[{}] Successfully gathered {:,} followed arists.'.format(smart_time(), len(followed_artists)))
			track_ids = []
			print('{}\r'.format(center('[{}] Gathering recent songs from followed arists...'.format(smart_time()), display=False)), end='')
			for artist in sorted(followed_artists, key=lambda d: d['name']) :
				print('{}\r'.format(center('[{}] Gathering recent songs from {}...'.format(smart_time(), artist['name']), display=False)), end='')
				track_ids.extend(sp.get_artist_track_ids(artist))
			track_ids = list(set(track_ids))
			center('[{}] Successfully gathered {:,} recent songs from {:,} artists.'.format(smart_time(), len(track_ids), len(followed_artists)))
			if track_ids:
				sp.spotify.playlist_replace_items(config['playlistId'], track_ids)
				center('[{}] Successfully updated playlist.'.format(smart_time()))
			smart_sleep(3600)
	else:
		center('[{}] Please set environment variables, SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET, before proceeding.'.format(smart_time()))