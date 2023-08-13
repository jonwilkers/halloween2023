from pytube import YouTube
import pydub
import os
import subprocess
import csv

SONG_LIST = 'songs.csv'
YT_FORMAT = 'mp4'

class process_file:
    dest_filename: str = ""
    dest_format: str = ""
    dest_path: str = ""
    url: str = ""

    def __init__(self, d: dict):
        for k,v in d.items():
            setattr(self, k.strip(), v.strip())

if __name__ == '__main__':
    process_files = []

    with open(SONG_LIST, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            process_files.append(process_file(row))

    for i in range(len(process_files)):
        f: process_file = process_files[i]

        yt = YouTube(f.url)
        audio = yt.streams.filter(only_audio=True).first()
        out_file = audio.download(output_path=f.dest_path)

        base, ext = os.path.splitext(out_file)
        new_file = os.path.join(f.dest_path, f.dest_filename + ext)
        os.rename(out_file, new_file)

        mp4 = os.path.join(f.dest_path, f"{f.dest_filename}.{YT_FORMAT}")
        new_format = os.path.join(f.dest_path, f"{f.dest_filename}.{f.dest_format}")

        sound = pydub.AudioSegment.from_file(mp4, format=YT_FORMAT)
        sound.export(new_format, format=f.dest_format)

        os.unlink(mp4)

        print('hello world')