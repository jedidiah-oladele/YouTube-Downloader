import pytube
from pytube import Playlist, exceptions


class myvideo:

    def __init__(self, video_url):
        """Create pytube YouTube object from url"""
        self.video_url = video_url

        # Error handling, with meaningful feedbacks
        self.error_message = None
        try:
            self.video = pytube.YouTube(self.video_url)
        except exceptions.RegexMatchError:
            self.error_message = "No video was found"
        except exceptions.AgeRestrictedError:
            self.error_message = "Video is age restricted"
        except exceptions.LiveStreamError:
            self.error_message = "Video is a live stream"
        except exceptions.VideoPrivate:
            self.error_message = "Video is private"
        except:
            self.error_message = "An unexpected error occured \nPlease make a report"
        


    def get_video_details(self):
        """Extracts and returns details about a video"""
        
        video_title = self.video.title
        video_thumbnail = self.video.thumbnail_url
        video_lenght = self.video.length
        # TODO add mp3 format
        streams = self.video.streams.filter(progressive=True)

        # There's probabaly an easier way to parse this html-like stream object
        # Dict key is the unique stream itag, and the value is a list containing stream resolution and filesize
        stream_prop = {}
        for stream in streams:
            s = str(stream).lstrip('<Stream: ').rstrip('>').replace(' ', ', ').replace('=', ':').split(', ')
            s = [var.split(':') for var in s]
            s = dict(s)
            stream_prop[s['itag']] = [s['res'], stream.filesize]


        return {'title':video_title, 'thumbnail':video_thumbnail, 'lenght':video_lenght, 'stream_prop':stream_prop}



    def download_video(self, resolution):
            """Download and return a video file"""

            # TODO choose resolution option
            # TODO filename_prefix
            file = self.video.streams.get_by_resolution(resolution).download()
            return file



    def get_playlist_videos(playlist_link):
        """Return a list of all video urls from a playlist"""
        
        try:
            p = Playlist(playlist_link)
        except:
            return None

        video_urls = [url for url in p.video_urls]
        return video_urls
