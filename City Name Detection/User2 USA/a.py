

list = []
#url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=5...1b&per_page=250&accuracy=1&has_geo=1&extras=geo,tags,views,description"
#url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=c814b1149b2b2b254c1d89948ffc404f&format=rest&auth_token=72157674075506661-2ceaa6f59f74c04a&api_sig=de6798a242fce56bfee3c62cc364a208"
soup = BeautifulSoup(urlopen(url)) #soup it up
for data in soup.find_all('photo'):
    dict = {
        "id": data.get('id'),
        "title": data.get('title'),?
        "tags": data.get('tags'),
        "latitude": data.get('latitude'),
        "longitude": data.get('longitude'),
    }
print (dict)

list.append(dict)