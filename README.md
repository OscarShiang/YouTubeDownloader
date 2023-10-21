# YouTube Downloader
This project is a tool to download videos from YouTube. The whole program is written with `Python` and the core libraries [youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html).

With these APIs, users can easily download video with the highest quality (such as `1080p`) or the audio with `m4a` format. 

## Requirements
If you want to use this tool, you should first check if the following libraries are suitable to use
1. `PyQt6` to build the UI layout
2. `youtube-dl` download the video from YouTube
3. `FFmpeg` merge the seperate vidoe file or convert the format of the video

## Run
Install the dependencies and run the program by the following lines:

```shell
$ pip install pyqt6
$ pip install git+https://github.com/ytdl-org/youtube-dl.git@master

$ python main.py
```
