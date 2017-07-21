from random import randint
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import random

#clean html garbage
#log the time at which data was generated
#make it a class that can be logged from flask app


columns = ['type', 'item_name', 'item_url']
df = pd.DataFrame(columns = columns)


def getrandomknowledge():
	r = requests.get('https://en.wikipedia.org/wiki/Special:RandomRootpage')
	data = r.text
	soup = BeautifulSoup(r.text)
	knowledgesoup = soup.findAll("h1", { "class" : "firstHeading" })
	knowledge = re.findall(r'>(.*?)<\/', str(knowledgesoup))
	knowledge_url = re.findall(r'<a class="wbc-editpage" href="([^\"]*)', str(soup))
	print(knowledge)
	print(knowledge_url)
	df.loc[len(df)]=['Knowledge', knowledge, knowledge_url]

def getrandomwikibooks():
	global book, book_url, df
	r = requests.get('https://en.wikibooks.org/wiki/Special:RandomRootpage')
	data = r.text
	soup = BeautifulSoup(r.text)
	booksoup = soup.findAll("h1", { "class" : "firstHeading" })
	book = re.findall(r'<h1 class="firstHeading" id="firstHeading" lang="en">(.*)</h1>', str(booksoup))
	book_url = re.findall(r'<a class="wbc-editpage" href="([^\"]*)', str(soup))
	# id="firstHeading" lang="en">(.*)</h1>', str(booksoup))
	print(book)
	print(book_url)
	df.loc[len(df)]=['Books', book, book_url]

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def getrandomquote():
	global quote
	quote = []
	while not quote:
		r = requests.get('https://en.wikiquote.org/wiki/Special:RandomRootpage')
		data = r.text
		soup = BeautifulSoup(r.text)
		mainbody = soup.findAll("div", { "class" : "mw-body-content" })
		quotesoup = re.findall(r'<h2><span class="mw-headline" id="Quotes">Quotes<\/span>(.*?)<\/h2>(.*?)<li>(.*?)(\/li)', str(mainbody))
		quote = re.findall(r'<ul>(.*?)<ul>', str(quotesoup))
		print(quote)
		#stip quote from all html garbage
		quote_url = re.findall(r'Retrieved from "<a dir="ltr" href="([^\"]*)', str(soup))
		print(quote)
		print(quote_url)
		df.loc[len(df)]=['Quotes', quote, quote_url]


def getrandomartist():
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
	print(artist.attrs['title'])
	print(artist.attrs['href'])
	df.loc[len(df)]=['Music', artist.attrs['title'], artist.attrs['href']]



def getrandomdestination():
	r = requests.get('https://earthroulette.com/random-cheap-flights-to-anywhere/')
	data = r.text
	soup = BeautifulSoup(r.text)
	mainbody = soup.findAll("div", { "class" : "caption center-align homepage-padding-top" })
	destination = re.findall(r'<strong>(.*)<\/strong', str(mainbody))[0]
	print(destination)
	destnation_url = str('https://en.wikivoyage.org/wiki/' + destination)
	print(destnation_url)
	df.loc[len(df)]=['Travel', destination, destnation_url]

def howmanydatatoget():
	n_data = randint(1,10)
	n_books = randint(1,10)
	n_quotes = randint(1,10)
	n_songs = randint(1,10)
	n_destinations = randint(1,10)
	#Get Data from WikiData
	[getrandomknowledge() for _ in range(n_data)]
	#Get Books from Dibipedia
	[getrandomwikibooks() for _ in range(n_books)]
	#Get Random Quotes
	[getrandomquote() for _ in range(n_quotes)]
	#Get Random SOng
	[getrandomartist() for _ in range(n_songs)]
	#Get Random Destination
	[getrandomdestination() for _ in range(n_destinations)]



if __name__ == "__main__":
	howmanydatatoget()
	df.to_csv('dataset.csv', index = False)





