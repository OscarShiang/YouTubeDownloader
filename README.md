# YouTube Downloader
This project is a tool for me to download videos from YouTube. The whole program is written with `Python` and the core libraries are [wxPython](https://wxpython.org) and [youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html).  

With these APIs, users can easily download video with the highest quality (such as `1080p`) or simply the audio with `m4a` format. 

### Requirement
If you want to use this tool, you should first check if the following libraries and the version of Python is suited to use
1. `Python 3.6.5` (or above), the test environment is 3.6.5
2. `wxPython`
3. `youtube-dl`

### Notice 
The `setting.json` is a needed file, which may cause the program crash down if the file does not exist. So when you try to run this tool, you should first check that the `setting.json` is existed. 