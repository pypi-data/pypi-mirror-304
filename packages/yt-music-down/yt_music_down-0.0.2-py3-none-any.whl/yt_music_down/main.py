from rich import print
from os import makedirs
import tkinter as tk
from tkinter import filedialog
from pytubefix import Playlist
from pytubefix.exceptions import VideoUnavailable
from pytubefix.cli import on_progress

# def download_video(url: str, save_dir: str) -> None:
#     ...

def download_music_playlist(playlist_url: str, save_dir: str | None = None) -> None:
    playlist = Playlist(playlist_url)

    print("[blue]====================================================================[/blue]")
    print(f"[blue]Downloading all music in {playlist.title}[/blue]")
    print("[blue]====================================================================[/blue]")

    for video in playlist.videos:
        try:
            print(f"Downloading video: {video.title} ...", end=" ")
            ys = video.streams.get_audio_only()
            ys.download(output_path=save_dir, mp3=True)
            print("[green]:white_heavy_check_mark:[/green]")
        except VideoUnavailable as e:
            print(f"[red]{e} :cross_mark:[/red]")
            continue


def open_dialog_box() -> str | None:
    save_directory = filedialog.askdirectory()
    if save_directory:
        print(f"Selected: {save_directory}")
        makedirs(save_directory, exist_ok=True)
        return save_directory
    else:
        print("Videos will be downloaded in current directory")
        return None

def main():
    root = tk.Tk()
    root.withdraw()

    url = input(" URL: ")
    save_dir = open_dialog_box()
    download_music_playlist(url, save_dir)


if __name__ == "__main__":
    main()
