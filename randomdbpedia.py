from SPARQLWrapper import SPARQLWrapper, JSON
from random import randint
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import random

#log the time at which data was generated
#make it a class that can be logged from flask app

# create session dataframe to use for visualization of data
columns = ['type', 'type_priority', 'num_items', 'item_name', 'item_url']
df = pd.DataFrame(columns = columns)


# first way to get random terms from db pedia
# def get_randomterms_dbpedia():
# 	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
# 	sparql.setReturnFormat(JSON)
# 	query = "SELECT ?s WHERE {?s ?p ?o } ORDER BY RAND() LIMIT 10"
# 	sparql.setQuery(query)  # the previous query as a literal string
# 	sparql.query().convert()

# another way to get random articles with random number
def getrandomfromwikidata():
	randomitemnum = randint(1,25348886)
	randitemname = str("https://www.wikidata.org/wiki/Q"+str(randomitemnum))
	print(randitemname)
	r = requests.get(randitemname)
	data = r.text
	soup = BeautifulSoup(r.text)
	termsoup = soup.findAll("span", { "class" : "wikibase-title-label" })
	term = re.findall(r'<span class="wikibase-title-label">(.*)</span>', str(termsoup))
	print(term)
	df.loc[len(df)]=['Knowledge', '0', '', term, randitemname]
	#return list/tuple/etc

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
	df.loc[len(df)]=['Books', '0', '', book, book_url]

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
		df.loc[len(df)]=['Quotes', '0', '', quote, quote_url]



def howmanydatatoget():
	n_data = randint(1,10)
	n_books = randint(1,10)
	n_quotes = randint(1,10)
	print(n_data)
	print(n_books)
	print(n_quotes)
	#Get Data from WikiData
	[getrandomfromwikidata() for _ in range(n_data)]
	#Get Books from Dibipedia
	[getrandomwikibooks() for _ in range(n_books)]
	#Get Random Quotes
	[getrandomquote() for _ in range(n_quotes)]


def generate_random_knowledge():
	#

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"

weighted_choice([('a',1.0),('b',2.0),('c',3.0)])


from numpy.random import choice
draw = choice(list_of_candidates, number_of_items_to_pick, p=probability_distribution)

draw =  choice([a,b,c], 1, p=probability_distribution)

#append to dataframe