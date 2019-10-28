import urllib.request, re, os
from bs4 import BeautifulSoup

#Git youtube downloader comments https://github.com/egbertbouman/youtube-comment-downloader

textToSearch = 'minecraft'
query = urllib.parse.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
    match = re.search(r"youtube\.com/.*v=([^&]*)", 'https://www.youtube.com' + vid['href'])
    if match:
        result = match.group(1)
    try:
        os.system("python3 /Users/andalval/Downloads/hello_docker_flask/youtubeComments.py --youtubeid "+result+" --output probando.json")
    except:
        pass