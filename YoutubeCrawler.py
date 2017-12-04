'''IMPORTANT if you are running this on windows
Download the ffmpeg package from http://ffmpeg.zeranoe.com/builds/, unzip it,
copy ALL the contents of the Bin directory to the directory where youtube-dl.exe
is located. If you are on linux installing ffmpeg with apt-get should work'''

from __future__ import unicode_literals
import youtube_dl
#import urllib.parse
import urllib2
import json
from apiclient.discovery import build
import random, string
import webbrowser


DEVELOPER_KEY = "AIzaSyAt7Cfjmv0qRyTf2ipGbL3DpsKffkeLnpQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


#creates random string
def randomword(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


#searches the youtube api using a random string and music category
def youtube_search():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
              developerKey = DEVELOPER_KEY)

    #this searches for 5 youtube vids with a random string of the music
    #category and places the result in search_response we're only using
    # a three letter string this length could be experimented with to find what
    #will give you better or more "random" results
    search_response = youtube.search().list(
        q=randomword(3),
        part="id, snippet",
        type="video",
        videoCategoryId='10',
        maxResults= 5,
        videoEmbeddable = 'true',
        order = 'date'
        ).execute()

    videos = []
    channelIds = []
    userVids = []
    userUploads = []

    #Parses the data in the string response into a an array containg the
    #title videoId ChannelId and publish date
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":

            videos.append("Title: %s\nvideoId: (%s)\nChannelId: (%s)\npublishedAt: (%s)\n" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"],
                                 search_result["snippet"]["channelId"],
                                 search_result["snippet"]["publishedAt"]))

            channelIds.append(search_result["snippet"]["channelId"])

    #searches for the channelIds the youtube videos
    channel_response = []
    for i in range(0, len(channelIds)):
        channel_response.append(youtube.channels().list(
            part = "contentDetails",
            id = channelIds[i]
        ).execute())

    #parse the data in the channel_response[]
    #and find the upload playlists and put them in uservids[]
    for i in range(0, len(channel_response)):
        for channel_result in channel_response[i].get("items", []):
            userUploads.append(channel_result["contentDetails"]["relatedPlaylists"]["uploads"])

    #get the channels upload playlist
    playlist_response = []

    for i in range(0, len(userUploads)):
        playlist_response.append(youtube.playlistItems().list(
            part='id, snippet',
            maxResults = 25,
            playlistId = userUploads[i],
        ).execute())



    #parse the playlist data regard the first video and then place a shuffled list of uploads in uservids[]
    for i in range(0, len(playlist_response)):
        tempUserVids = []
        for playlist_result in playlist_response[i].get("items", []):
            if playlist_result["kind"] == "youtube#playlistItem" and playlist_result["snippet"]["position"] > 0:
                tempUserVids.append(playlist_result["snippet"]["resourceId"]["videoId"])
        userVids.append(random.sample(tempUserVids, len(tempUserVids)))

    #flatten the user vids list
    flatUserVids = []
    for sublist in userVids:
        for item in sublist:
            flatUserVids.append(item)

    #getting the
    videoStat = []
    for vid in flatUserVids:
        videoStat.append(youtube.videos().list(
            part = 'status, snippet',
            id = vid
        ).execute())


    for i in range(0, len(videoStat)):
        for stat in videoStat[i].get("items", []):
            if stat["status"]["privacyStatus"] == "public" and stat["snippet"]["categoryId"] == "10":
                return stat["id"]

    #debug printing
    print "Videos:\n", "\n".join(videos), "\n"
    print "Channel Id's:\n", "\n".join(channelIds), "\n"
    print "User Upload Playlists: \n", "\n".join(userUploads), "\n"
    print "User's Uploaded Video's:\n", "\n".join(flatUserVids), "\n"

#function that grabs a random youtubevideo id is using randomyoutube api
#This is the api that the above algorithm is based upon
def getRandomId():
    url = 'https://randomyoutube.net/api/getvid?api_token=TktN4bc321ZUZvidMKRVyKHcacVXnwlHCUkm8qb3c22YelU2hiR7FIQgBM6t'
    response = urllib2.urlopen(url)
    jsonResponse = response.read()
    stringResponse = json.loads(jsonResponse)
    return stringResponse['vid']


#uses youtube_dl to download only the audio portions of youtube link
def download_song(url):
    #outtmpl option determines where your file will be output
    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'wav',
            'preferredquality' : '192',
        }],
        'outtmpl' : './Machine-Learning/test_songs/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    youtubeURL = 'https://www.youtube.com/watch'
    vidID = youtube_search()
    url = '?v='.join([youtubeURL, vidID])
    webbrowser.open(url)
    download_song(url)




#random youtube api key
#TktN4bc321ZUZvidMKRVyKHcacVXnwlHCUkm8qb3c22YelU2hiR7FIQgBM6t

#youtube api key
#AIzaSyAt7Cfjmv0qRyTf2ipGbL3DpsKffkeLnpQ
