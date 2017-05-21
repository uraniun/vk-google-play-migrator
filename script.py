import json

from gmusicapi import Mobileclient
from termcolor import colored

def milisecondsToTime(miliseconds):
    miliseconds = int(miliseconds)
    seconds = (miliseconds / 1000) % 60
    seconds = int(seconds)
    minutes = (miliseconds / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (miliseconds / (1000 * 60 * 60)) % 24
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

def findSongInLibrary(songFullName):
    result = api.search(songFullName, 5)
    first_match = result['song_hits'][0] if result['song_hits'] else None
    if(first_match):
        song_lenght = milisecondsToTime(first_match['track']['durationMillis'])
        song_size = "%.2f MB" % (float(first_match['track']['estimatedSize']) / 1000000.0)
        song = {
            "album": first_match['track']['album'],
            "artist": first_match['track']['artist'],
            "title": first_match['track']['title'],
            "year": first_match['track']['year'],
            "duration": song_lenght,
            "size": song_size,
            "storeID": first_match['track']['storeId'],
        }
        return song
    else:
        print(colored("Song mismatch %s"%songFullName,'red'))
        return None

def addSongToOwnLibrary(songStoreID):
    return api.add_store_tracks([songStoreID])

def checkPlaylistExists(playlistName):
    playlists = api.get_all_user_playlist_contents()
    for playlist in playlists:
        if(playlist['name'] == playlistName): return playlist['id']
    return None


# --------------------------------------------------------------------------
api = Mobileclient()
addToPlaylist = True
playlistName = "Music from VK"
logged_in = api.login('login here', 'pass here', Mobileclient.FROM_MAC_ADDRESS)

if(logged_in):
    input_file = open('json.txt', 'r') # json with song from vk
    file_dict = json.loads(input_file.read())
    for item in file_dict['response']['audios']['items']:
        songFullName = item['artist'] + ' - ' + item['title']
        song = findSongInLibrary(songFullName)
        if(song):
            print(
                "Original name: %s\n" % songFullName,
                "Album: %s"%song['album'],
                "Artist: %s" % song['artist'],
                "Title: %s" % song['title'],
                "Year: %s" % song['year'],
                "Duration: %s" % song['duration'],
                "Size: %s" % song['size'],
                "Store ID: %s" % song['storeID'],
                "-----------------------------------------------",
                sep='\n'
            )
            songID = addSongToOwnLibrary(song['storeID'])
            if(addToPlaylist):
                playlistID = checkPlaylistExists(playlistName)
                if(not playlistID):
                    playlistID = api.create_playlist(playlistName)
                api.add_songs_to_playlist(playlistID, songID)
else:
    print('Error')
