# UTube2Mp3

# Requirements
* Ubuntu (that's what I used)
* Install libav
`sudo apt-get install -y libav-tools`

# Download One Video

If you want to download just one video instead of a playlist then just install pytube and run the code below:

`pip install pytube`

The Code:

`from pytube import YouTube
yt = YouTube("") # Video Url
yt = yt.get('mp4', '720p') #settings
yt.download('') # path to download directory`
