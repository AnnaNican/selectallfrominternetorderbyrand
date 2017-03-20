import json
import random
import urllib.parse

import requests
from bs4 import BeautifulSoup

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"

@app.route("/random")
def stuff():
	r = requests.get("http://en.wikipedia.org/wiki/Special:Random")
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )
	
	soup = BeautifulSoup(r.text, 'html.parser')
	
	content = soup.select_one('#mw-content-text')
	links = content.find_all('a')
	links = filter( lambda x: not 'Template:' in x.attrs['href'], links )
	links = filter( lambda x: not 'Template_talk:' in x.attrs['href'], links )
	links = filter( lambda x: not 'File:' in x.attrs['href'], links )
	links = filter( lambda x: not '?' in x.attrs['href'], links )
	links = filter( lambda x: not '#cite' in x.attrs['href'], links )
	clean_links = []
	for link in links:
		if link.attrs['href'].startswith('/wiki'):
			link.attrs['href'] = 'http://en.wikipedia.org%s' % link.attrs['href']
	return '<br/>'.join(['%s' % l for l in links])

	parts = specs_body.select('.nfo')[0].getText().split(' ')

def get_random_topic_from_wikipedia():
	r = requests.get("http://en.wikipedia.org/wiki/Special:Random")
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )
	
	soup = BeautifulSoup(r.text, 'html.parser')
	
	heading = soup.select_one('#firstHeading')
	return heading.getText()

@app.route("/wikipedia/<int:count>")
def _wikipedia(count):
	return '<br/>'.join(wikipedia(count))

def wikipedia(count):
	return [ get_random_topic_from_wikipedia() for i in range(0,count) ]

@app.route("/nope/<int:count>")
def wikiddg_old(count):
	things = wikipedia(count)
	results = {}
	for t in things:
		results[t] = [ r.as_dict() for r in search_ddg(t,5) ]
	print( len(results[things[0]]) )
	return json.dumps(results)

def clean_ddg_url( url ):
	return urllib.parse.unquote( url.replace('/l/?kh=-1&uddg=','') )

def search_ddg(query,n_results):
	r = requests.get("https://duckduckgo.com/html/?q=%s" % query)
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )

	soup = BeautifulSoup(r.text, 'html.parser')
	results = soup.select('.result__a')
	links = [ Link( r.getText(), clean_ddg_url(r.attrs['href']) ) for r in results ]
	return links

class Link():
	def __init__( self, title, href ):
		self.title = title
		self.href = href
	def as_dict(self):
		return dict( title=self.title, href=self.href )
	def __str__( self ):
		return '<a href="%s">%s</a>' % (self.href,self.title)

def get_urls_for_topics( generate_random_topics, search, n_topics, n_links ):
	topics = generate_random_topics(n_topics)
	results = {}
	for t in topics:
		results[t] = search( t, n_links )
		random.shuffle(results[t])
		results[t] = results[t][0:n_links]
	return results

@app.route("/wikiddg/<int:count>")
def wikiddg(count):
	dicts = {}
	results = get_urls_for_topics( wikipedia, search_ddg, count, 8 )
	for r in results:
		dicts[r] = [ l.as_dict() for l in results[r] ]
	return json.dumps(dicts)

if __name__ == "__main__":
    app.run()
