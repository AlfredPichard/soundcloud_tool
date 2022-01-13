import utils
from sclib import SoundcloudAPI

def main(): 
    config = utils.get_config()
    sc_api = SoundcloudAPI()
    playlist_ids = utils.prompt_to_fill(config['playlists'].keys(), 'Select playlist to download: ')

    already_dl_tracks = set()
    tracks_to_dl = set()
    dropped_tracks = set()

    for playlist_id in playlist_ids:
        playlist_content = sc_api.resolve(config['playlists'][playlist_id])
        
        for track in playlist_content.tracks:
            if track.id not in already_dl_tracks:
                tracks_to_dl.add(track)
                already_dl_tracks.add(track.id)

        print(f"Found {len(playlist_content)} tracks in {playlist_content.title}, including {len(tracks_to_dl)} new tracks.")
        if not utils.confirm():
            continue

        print(f"Downloading tracks...")
        for track in tracks_to_dl:
            try:
                utils.download(track)
                print(f"Downloaded {track.title}")
            except Exception as e:
                print(f"Could not download {track.title}")
                dropped_tracks.add(track)

        print(f"Finished downloading {len(tracks_to_dl) - len(dropped_tracks)} tracks.")
        print(f"Could not download {len(dropped_tracks)} tracks.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Download interrupted")
