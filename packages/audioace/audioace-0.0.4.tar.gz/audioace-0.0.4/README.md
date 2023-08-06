
# AudioAce

#### A simple module for downloading your favourite songs


# Documentation
 
#### coming soon....



## Installation

Install audioace with pip

```bash
pip install audioace
```
    
or upgrade

```bash
pip install audioace --upgrade
```


## Quick Start

To get started, install audioace and install ffmpeg from the link [here](https://ffmpeg.org/) or watch a tutorial on how to download ffmpeg from [here](https://www.youtube.com/watch?v=5xgegeBL0kw)



### To Download Songs from a text file
First create a ```songs.txt``` file in your working directory and then type the songs you wanna add eg: Butter by BTS, etc..

```python
import audioace
download_file = "songs.txt"
test = audioace.Download(file=download_file)
test.download()
```

### To Download Songs from a Spotify Playlist
If you wanna download your songs from spotify you first have to create an app on https://developers.spotify.com/ then access your client id and client secret and redirect uri
```python
client_id = #your client id
client_secret = #your client secret
redirect_uri = #redirect uri
playlist_link = #the link of playlist you wanna download from

test = audioace.Download()
test.get_songs_from_playlist(client_id=client_id, client_secret=client_secret, playlist_link=playlist_link)
test.download()
```

### To Download Songs from Your Liked Songs
```python
client_id = #your client id
client_secret = #your client secret
redirect_uri = #redirect uri
test = audioace.Download()
test.get_songs_from_liked_songs(client_id=client_id,client_secret=client_secret, redirect_uri=redirect_uri)

"""
    This will open your default web browser asking for your permission,
    grant it and then it will redirect you to your redirect page,
    copy the link and paste it in your terminal
"""
test.download()
```


## Reporting Issues

If you have any suggestions or found any errors or bugs, please feel free to mention them [here](https://github.com/VikranthMaster/AudioAce/issues)

or you can send me a mail on vikrantht32@gmail.com