from urllib.request import urlopen
import prompt_toolkit
import re
import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config


def prompt_to_fill(options, prompt_text):
    completer = prompt_toolkit.completion.WordCompleter(
        options, ignore_case=True, pattern=re.compile(r"\S*")
    )
    response = prompt_toolkit.prompt(prompt_text, completer=completer)
    return {
        target
        for response_slice in response.split(",")
        for target in response_slice.split(" ")
    }


def confirm():
    return input("Download (Y/n) ?").lower() in ["y", ""]


def de_emoji(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)  # no emoji


def download(track, dl_path, playlist):
    mp3_stream_file = urlopen(track.get_stream_url())
    with open(
        dl_path
        + "/"
        + playlist
        + f"/{de_emoji(track.artist)} - {de_emoji(track.title)}.mp3",
        "wb",
    ) as mp3_file:
        mp3_file.write(mp3_stream_file.read())
