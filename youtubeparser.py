#Extracting YouTube links using BeautifulSoup
import requests
import json
from bs4 import BeautifulSoup

url = "https://www.youtube.com/watch?v=xoWxv2yZXLQ"
# url = "https://www.youtube.com/watch?v=WW1BpABbzHs"

def getYouTubeLinks(url):
	response = requests.get(url)
	data = response.content.decode("utf-8")
	soup = BeautifulSoup(data, 'html.parser')
	page = soup.prettify()

	X = [i.split("\n") for i in page[page.find(
			".googlevideo.com/videoplayback?"):].split(",") if '"url":' in i]

	filename = ''.join(soup.find("title", text=True))
	links, thumbs, videos, audios = [], [], [], []

	for x in X:
		try:
			links.append(json.loads(str(x[0])+'}'))
		except:
			try:
				links.append(json.loads('{'+str(x[0])+'}'))
			except:
				continue

	for m in links:
		try:
			if "maxresdefault.jpg" in m["url"]:
				thumbs.append(m["url"])
			if "mime=video%2" in m["url"]:
				videos.append(m["url"])
			if "mime=audio%2" in m["url"]:
				audios.append(m["url"])
		except:
			continue
	return filename, links, thumbs, videos, audios

filename,links, thumbs, videos, audios = getYouTubeLinks(url)

print(filename)
print(len(links), links)
print(len(thumbs), thumbs)
print(len(videos), videos)
print(len(audios), audios)

#Downloading files from links
def downloadLink(link, filename):
	r = requests.get(link, stream=True, allow_redirects=True)
	ext = r.headers.get('content-type').split("/")[-1]
	x = filename.replace("/", "_").replace("\\","_")+"."+ext
	with open(x, "wb") as file:
		i = 0
		total_length = int(r.headers.get('content-length'))
		print(f"[DOWNLOAD STARTED]: {filename} of {total_length / 1000000:.2} MB" )
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				file.write(chunk)
			else:
				break
		print("[DOWNLOAD FINISHED]")

downloadLink(audios[0], filename)
