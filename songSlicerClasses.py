# See https://github.com/jiaaro/pydub/tree/master for pydub docs
# Install with 'pip install pydub'
# Pydub requires ffmpeg or libav to be installed.
# For linux, use 'sudo apt-get install ffmpeg' or similar
# For windows, download the source code: https://ffmpeg.org/download.html
# e.g. get the exe from https://github.com/GyanD/codexffmpeg/releases/tag/2024-08-28-git-b730defd52
# extract the archive
# rename the folder to 'ffmpeg'
# then place the contents in the same folder as this script

import os
import subprocess
from pydub import AudioSegment

# Temporarily add ffmpeg binaries to PATH
# TODO make the searching more flexible
# TODO only run this section if the os is Windows
def initialize_ffmpeg_path():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ffmpeg_path = current_dir+'\\ffmpeg\\bin'
    os.environ['PATH'] += ffmpeg_path
    print(os.environ['PATH'])

class beatParameters:
    def __init__(self, amount, units):
        self.amount = amount
        self.units = units

        if self.units == "bpm":
            # convert to milliseconds
            self.duration =  int(60000/abs(int(self.amount)))
        else:
            # default to milliseconds
            self.duration =  abs(int(self.amount))
        
class songFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.splitext(self.filepath)[0]
        self.extension = os.path.splitext(self.filepath)[1]
        self.filetype = self.extension.replace('.','')
        self.directory = os.path.dirname(self.filepath)

class songSlicer:
    def __init__(self, songFile):
        self.songFile = songFile
        filetype = self.songFile.filetype
        self.sound = AudioSegment.from_file(songFile.filepath, format=filetype)

    def trim(self,direction,duration):
        if duration > len(self.sound):
            print("Trim duration {} ms is longer than soundfile length {} ms".format(duration,len(self.sound)))
            print("Returning empty segment")
            self.sound = AudioSegment.empty()
        if duration > 0:
            if direction == "start":
                self.sound = self.sound[duration:]
            else:
                self.sound = self.sound[:len(self.sound)-duration]
    
    def slice(self, beat):
        print("Slicing into durations of {} ms".format(beat.duration))
        song_chunks = enumerate(self.sound[::beat.duration])
        even_chunks = AudioSegment.empty()
        odd_chunks = AudioSegment.empty()
        for i, chunk in song_chunks:
            if i % 2 == 0:
                even_chunks += chunk
            else:
                odd_chunks += chunk
        self.even_chunks = even_chunks
        self.odd_chunks = odd_chunks

    def export(self,chunk_name):
        output_filename = \
            self.songFile.filename + \
            "_" + \
            chunk_name + \
            "_beats" + \
            self.songFile.extension
        output_filepath = os.path.join(self.songFile.directory,output_filename)
        with open(output_filepath, "wb") as f:
            if chunk_name == "even":
                sliced_sound = self.even_chunks
            elif chunk_name == "odd":
                sliced_sound = self.odd_chunks
            sliced_sound.export(f, format=self.songFile.filetype)
