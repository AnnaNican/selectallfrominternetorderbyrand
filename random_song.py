import random

import requests
from bs4 import BeautifulSoup

def get_random_artist():
	# Look at bandcamp https://bandcamp.com/artist_index to get the highest page index
	page_index = 1+int(2283.0 * random.random())
	r = requests.get('https://bandcamp.com/artist_index?page=%s' % page_index)
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )
	
	soup = BeautifulSoup(r.text, 'html.parser')
	
	# get a random artist
	content = soup.select_one('.results')
	artists = content.find_all('a')
	artist = random.choice( artists )

	return dict(
		artist = artist.attrs['title'],
		url = artist.attrs['href']
	)

print get_random_artist()
