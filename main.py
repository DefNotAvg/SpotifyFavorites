import os
import pandas
from helpers import *
from spotify import Spotify

if __name__ == '__main__':
	header()
	if os.getenv('SPOTIPY_CLIENT_ID') and os.getenv('SPOTIPY_CLIENT_SECRET'):
		config = load_from_json('config.json')
		os.environ['SPOTIPY_REDIRECT_URI'] = config['redirectURI']
		while True:
			sp = Spotify(config['username'], config['scope'] + ' user-follow-read', config['lookbackDays'], config['explicit'])
			print('{}\r'.format(center('[{}] Gathering playlist tracks...'.format(smart_time()), display=False)), end='')
			playlist_tracks = sp.get_playlist_track_ids(config['playlistId'])
			center('[{}] Successfully gathered {:,} playlist tracks.'.format(smart_time(), len(playlist_tracks)))
			print('{}\r'.format(center('[{}] Gathering followed artists...'.format(smart_time()), display=False)), end='')
			followed_artists = sp.get_followed_artists()
			center('[{}] Successfully gathered {:,} followed artists.'.format(smart_time(), len(followed_artists)))
			tracks = []
			print('{}\r'.format(center('[{}] Gathering recent songs from followed artists...'.format(smart_time()), display=False)), end='')
			for artist in sorted(followed_artists, key=lambda d: d['name']):
				print('{}\r'.format(center('[{}] Gathering recent songs from {}...'.format(smart_time(), artist['name']), display=False)), end='')
				tracks.extend(sp.get_artist_tracks(artist['uri']))
			df = pandas.DataFrame.from_dict(tracks)
			df['rowNum'] = df.sort_values(['explicit', 'albumType'], ascending=[False, True]).groupby(['name', 'artists'], sort=False).cumcount().add(1)
			track_ids = list(set([item['id'] for item in df.to_dict('records') if item['rowNum'] == 1]))
			center('[{}] Successfully gathered {:,} recent songs from {:,} artists.'.format(smart_time(), len(track_ids), len(followed_artists)))
			to_add = [track_id for track_id in track_ids if track_id not in playlist_tracks]
			to_remove = [track_id for track_id in playlist_tracks if track_id not in track_ids]
			if to_add or to_remove:
				if to_remove:
					sp.spotify.playlist_remove_all_occurrences_of_items(config['playlistId'], to_remove)
					center('[{}] Successfully removed {:,} song{} from the playlist.'.format(smart_time(), len(to_remove), 's' if len(to_remove) > 1 else ''))
				if to_add:
					for i in range(0, len(to_add), 100):
						sp.spotify.playlist_add_items(config['playlistId'], to_add[i:i+100])
					center('[{}] Successfully added {:,} song{} to the playlist.'.format(smart_time(), len(to_add), 's' if len(to_add) > 1 else ''))
			else:
				center('[{}] No updates to be made.'.format(smart_time()))
			smart_sleep(3600)
	else:
		center('[{}] Please set environment variables, SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET, before proceeding.'.format(smart_time()))