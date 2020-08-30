# YouTube Downloader
This project is a tool to download videos from YouTube. The whole program is written with `Python` and the core libraries are [wxPython](https://wxpython.org) and [youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html).  

With these APIs, users can easily download video with the highest quality (such as `1080p`) or the audio with `m4a` format. 

## Requirement
If you want to use this tool, you should first check if the following libraries and the version of Python is suited to use
1. `Python 3.6.5` (or above), the test environment is `3.6.5`
2. `wxPython` to build the GUI interface for users
3. `youtube-dl` download the video from YouTube
4. `FFmpeg` (**optional**) If you need to merge the seperate vidoe file or convert the format of the video

## Run
Install the dependencies and run the program by the following lines:

```shell
$ pip install -r requirements.txt
$ python yt_dl.py
```

## Notice 
The `setting.json` is a **needed** file, which may cause the program crash down if the file does not exist. So when you try to run this tool, you should first check that the `setting.json` is **existed**. 
