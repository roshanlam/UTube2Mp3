#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
import re
import subprocess
import settings

def update_youtube_dl():
    """Update Youtube -DL"""
    try:
        print "Checking for youtube-dl updates"
        youtube_dl = os.path.join(settings.BASE, "youtube-dl")
        args = [youtube_dl,
                "-U"
               ]
        subprocess.call(args)
    except Exception as exp:
        print "\n[ERROR] ", exp

def download_playlist(playlist):
    """Download YouTube Playlist into MP3"""
    try:
        youtube_dl = os.path.join(settings.BASE, "youtube-dl")
        if len(settings.FFMPEG) > 0:
            args = [youtube_dl,
                    "--no-post-overwrites",
                    "-x",
                    "--ffmpeg-location",
                    settings.FFMPEG,
                    "--prefer-ffmpeg",
                    "--audio-format",
                    "mp3",
                    "--audio-quality",
                    "0",
                    "https://www.youtube.com/playlist?list="+playlist,
                    "-o",
                    "Music/Playlist/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
                   ]
        else:
            args = [youtube_dl,
                    "--no-post-overwrites",
                    "-x", "--prefer-ffmpeg",
                    "--audio-format", "mp3",
                    "--audio-quality",
                    "0",
                    "https://www.youtube.com/playlist?list="+playlist,
                    "-o",
                    "Music/Playlist/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
                   ]
        subprocess.call(args)
    except Exception as exp:
        print "\n[ERROR] ", exp

def download_mp3(video):
    """Download YouTube Video to MP3"""
    try:
        youtube_dl = os.path.join(settings.BASE, "youtube-dl")
        if len(settings.FFMPEG) > 0:
            args = [youtube_dl,
                    "--no-post-overwrites",
                    "-x",
                    "--ffmpeg-location",
                    settings.FFMPEG,
                    "--prefer-ffmpeg",
                    "--audio-format",
                    "mp3",
                    "--audio-quality",
                    "0",
                    "-o",
                    "Music/%(title)s.%(ext)s",
                    video
                   ]
        else:
            args = [youtube_dl,
                    "--no-post-overwrites",
                    "-x",
                    "--prefer-ffmpeg",
                    "--audio-format",
                    "mp3",
                    "--audio-quality",
                    "0",
                    "-o",
                    "Music/%(title)s.%(ext)s",
                    video
                   ]
        subprocess.call(args)
    except Exception as exp:
        print "\n[ERROR] ", exp

class DownloadPlaylist(tornado.web.RequestHandler):
    """Download Playlist to MP3"""
    def get(self, playlist_id):
        """Download"""
        playlist = playlist_id if playlist_id else ''
        if len(playlist) > 1 and re.match(VIDEO_REGEX, playlist):
            download_playlist(playlist)
            self.write("Playlist Download Completed")
        else:
            self.write("Invalid Request")

class DownloadFile(tornado.web.RequestHandler):
    """Download File to MP3"""
    def get(self, video_id):
        """Download"""
        video = video_id if video_id else ''
        if len(video) > 1 and re.match(VIDEO_REGEX, video):
            download_mp3(video)
            self.write("MP3 Download Complete")
        else:
            self.write("Invalid Request")

if __name__ == "__main__":
    VIDEO_REGEX = r"^([a-zA-Z0-9\_\-]+)$"
    tornado.web.Application([
        (r"/playlist/(?P<playlist_id>[^\/]+)", DownloadPlaylist),
        (r"/video/(?P<video_id>[^\/]+)", DownloadFile),
        ]).listen(8080)
    tornado.ioloop.PeriodicCallback(update_youtube_dl, 300000).start() #15 mins in milliseconds
    tornado.ioloop.IOLoop.instance().start()

    '''
    http://localhost:8080/playlist/url
    http://localhost:8080/video/url
    '''
