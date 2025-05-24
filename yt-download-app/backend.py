from pytube import Playlist, Youtube

from moviepy.editor import *

import os

class Youtubedownloader:
    
    def download_single_video(self, url, save_path):
        try:
            yt = Youtube(url)
            stream = yt.stream.filter(file_extension="mp4").get_highest_resolution()
            print("video ttitle:", yt.title)
            filename= yt.title.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_').replace('&', '_').replace('%', '_').replace('#', '_').replace('{', '_').replace('}', '_').replace('[', '_').replace(']', '_').replace('=', '_').replace('+', '_').replace('-', '_').replace('--', '_').replace(';', '_').replace('!', '_').replace('@', '_').replace('$', '_').replace('^', '_').replace('`', '_').replace('~', '_').replace(',', '_').replace('.', '_').replace(' ', '_')
            
            
            
            
        except Exception as e:
            print(f"an error has occurred: {e}")
    
    def donwload_playlist(self, url, save_path):
        try:
            pass
        except Exception as e:
            print(f"an error has occurred: {e}")
    
    def donwload_video_as_audio(self, url, save_path):
        try:
            pass
        except Exception as e:
            print(f"an error has occurred: {e}")
    
    def download_playlist_as_mp3(self, url, save_path):
        try:
            pass
        except Exception as e:
            print(f"an error has occurred: {e}")