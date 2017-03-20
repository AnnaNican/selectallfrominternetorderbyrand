from SPARQLWrapper import SPARQLWrapper, JSON
from random import randint
import requests
from bs4 import BeautifulSoup
import re


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
	#return list/tuple/etc

def gerrandomwikibooks():
	r = requests.get('https://en.wikibooks.org/wiki/Special:RandomRootpage')
	data = r.text
	soup = BeautifulSoup(r.text)
	booksoup = soup.findAll("h1", { "class" : "firstHeading" })
	book = re.findall(r'<h1 class="firstHeading" id="firstHeading" lang="en">(.*)</h1>', str(booksoup))
	print(book)

def howmanydatatoget():
	n_data = randint(1,10)
	n_books = randint(1,10)
	print(n_data)
	print(n_books)
	#Get Data from WikiData
	[getrandomfromwikidata() for _ in range(n_data)]
	#Get Books from Dibipedia
	[gerrandomwikibooks() for _ in range(n_books)]