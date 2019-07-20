import youtube_dl

opts = {
	'format': 'm4a',
	'outtmpl': '~/Desktop/new/%(title)s.%(ext)s',
	'merge_output_format': 'mp3'
}

url = 'https://www.youtube.com/watch?v=pRfmrE0ToTo'

with youtube_dl.YoutubeDL(opts) as ydl:
	result = ydl.extract_info(url, download=True)
