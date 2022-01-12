from urllib.request import urlopen
import prompt_toolkit
import re


def prompt_to_fill(options, prompt_text):
    completer = prompt_toolkit.completion.WordCompleter(options, ignore_case=True, pattern=re.compile(r'\S*'))
    response = prompt_toolkit.prompt(prompt_text, completer=completer)
    return {target for response_slice in response.split(',') for target in response_slice.split(' ')}


def confirm():
    return input("Download (Y/n) ?").lower() in ['y', '']


def download(track):
    mp3_stream_file = urlopen(track.get_stream_url())
    with open(f"{track.title}.mp3", "wb") as mp3_file:
        mp3_file.write(mp3_stream_file.read())
    