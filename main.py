import utils
from sclib.sync import SoundcloudAPI


def main():
    config = utils.get_config()
    sc_api = SoundcloudAPI()
    playlist_ids = utils.prompt_to_fill(
        config["playlists"].keys(), "Select playlist to download: "
    )

    already_dl_tracks = set(
        open(config["paths"]["DL_PATH"] + "/already_downloaded.txt").read().splitlines()
    )
    tracks_to_dl = set()
    dropped_tracks = set()
    downloaded_tracks = set()

    for playlist_id in playlist_ids:
        playlist_content = sc_api.resolve(config["playlists"][playlist_id])

        for track in playlist_content.tracks:
            if track.id not in already_dl_tracks:
                tracks_to_dl.add(track)

        print(
            f"Found {len(playlist_content)} tracks in {playlist_content.title}, including {len(tracks_to_dl)} new tracks."
        )
        if not utils.confirm():
            continue

        print(f"Downloading tracks...")
        for track in tracks_to_dl:
            try:
                utils.download(track, config["paths"]["DL_PATH"], playlist_id)
                print(f"Downloaded {track.title}")
                downloaded_tracks.add(track.id)
            except Exception as e:
                print(f"Could not download {track.title}")
                print(e)
                dropped_tracks.add(track)

        print(f"Finished downloading {len(downloaded_tracks)} tracks.")
        if len(dropped_tracks) > 0:
            print(f"Could not download {len(dropped_tracks)} tracks.")
        print("Updating history file...")

        with open(config["paths"]["DL_PATH"] + "/already_downloaded.txt", "a") as f:
            for downloaded_track in downloaded_tracks:
                f.write(str(downloaded_track) + "\n")

        print("Done !")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Download interrupted")
