from pytube import YouTube
import os
import pywhatkit
import requests
from moviepy.editor import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import time
from spotipy.oauth2 import SpotifyOAuth
from requests.auth import HTTPBasicAuth
import urllib.parse as parse
import webbrowser
        
class Download():
    def __init__(self, file="songs_name.txt", path = "Songs"):
        self.path = path
        self.vid_ext = "mp4"
        self.aud_ext = "mp3"
        self.command = ('ffmpeg -i "{from_video_path}" '
                        '-f {audio_ext} -ab 192000 '
                        '-vn "{to_audio_path}"')
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.file = file

        isExist = os.path.exists(self.path)
        if not isExist:
            os.mkdir(self.path)
        
    
    def download(self):
        file_object = open(self.file, "r+", encoding="utf-8")
        l = file_object.readlines()
        for x in l:
            y = pywhatkit.playonyt(x, open_video=False)
            url = requests.get(y).url
            yt = YouTube(url)

            video = yt.streams.filter().first()
            out_file = video.download(output_path=self.path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp4'
            os.rename(out_file, new_file)
            os.chdir(self.path)
            files = os.listdir(self.path)
            for f in files:
                if not f.endswith(self.vid_ext):
                    continue

                audio_file_name = '{}.{}'.format(f, self.aud_ext)
                command = self.command.format(
                    from_video_path=f, audio_ext=self.aud_ext, to_audio_path=audio_file_name,
                )
                os.system(command)
            os.remove(new_file)

            print(yt.title + " has been successfully downloaded.")

    def get_songs_from_playlist(self, client_id, client_secret, playlist_link):
        client_cred = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_cred)

        playlist_URI = playlist_link.split("/")[-1].split("?")[0]

        offset = 0
        t_end = time.time() + 3

        while time.time() < t_end:
            for track in sp.playlist_tracks(playlist_URI, offset=offset)["items"]:
                #Track name
                track_name = track["track"]["name"]
                with open(self.file, "a", encoding="utf-8") as f:
                    f.write(track_name + "\n")
                    f.close()
            offset +=100

    def authenticate(self,client_id, client_secret, redirect_uri, scope=None):
        '''Implement OAuth 2 Spotify authentication'''
        # Application: Request authorization to access data
        payload = {'client_id': client_id,
                'response_type': 'code',
                'redirect_uri': redirect_uri,
                'show_dialog': 'true'} # allow second account to login
        if scope:
            payload['scope'] = scope
        auth_url = '{}?{}'.format(self.auth_url, parse.urlencode(payload))
        # Spotify: Displays scopes & prompts user to login (if required)
        # User: Logs in, authorizes access
        webbrowser.open(auth_url)

        response = input('Enter the URL you were redirected to: ')
        code = parse.parse_qs(parse.urlparse(response).query)['code'][0]

        payload = {'redirect_uri': redirect_uri,
                'code': code,
                'grant_type': 'authorization_code'}
        if scope:
            payload['scope'] = scope

        # Application: Request access and refresh tokens
        # Spotify: Returns access and refresh tokens
        auth = HTTPBasicAuth(client_id, client_secret)
        response = requests.post(self.token_url, data=payload, auth=auth)
        if response.status_code != 200:
            response.raise_for_status()
        token_info = response.json()
        token_info['expires_at'] = int(time.time()) + token_info['expires_in']
        token_info['scope'] = scope
        return token_info

    def show_tracks(self, results):
        for item in results['items']:
            track = item['track']
            name = (track['artists'][0]['name'], track['name'])
            with open(self.file,"a", encoding="utf-8") as f:
                f.write(str(name) + "\n")

    def get_songs_from_liked_songs(self, client_id, client_secret, redirect_uri):
        user = Download.authenticate(self,client_id, client_secret, redirect_uri, scope='user-library-read')
        sp = spotipy.Spotify(auth= user['access_token'])
        results = sp.current_user_saved_tracks(limit=1, offset=0)
        while results['next']:
            results = sp.next(results)
            Download.show_tracks(self,results)

    



