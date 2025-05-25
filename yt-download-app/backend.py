from pytube import Playlist, YouTube
from moviepy.editor import AudioFileClip  # FIXED IMPORT
import yt_dlp
import os

class Youtubedownloader:
    
    def download_single_video(self, url, save_path):
        try:
            url = url.strip()
            print(f"Processing URL: {url}")
            
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            print(f"Download complete! Video saved in {save_path}")
            return True
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
    
    def download_playlist(self, url, save_path):
        try:
            p = Playlist(url)
            for video_url in p.video_urls:  # Fixed: video_urls (plural)
                print(f"Downloading video: {video_url}")
                self.download_single_video(video_url, save_path)
                
            print("All videos have been downloaded in .mp4 format")
        except Exception as e:
            print(f"An error has occurred: {e}")
    
    def download_video_as_audio(self, url, save_path):
        try:
            url = url.strip()
            print(f"Processing URL: {url}")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            print(f"Audio download complete! File saved in {save_path}")
            return True
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False