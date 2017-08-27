import json
import random
import StringIO
import csv

import requests
from bs4 import BeautifulSoup

from flask import Flask
from flask import render_template
from flask import make_response

app = Flask(__name__)

@app.route("/")
def hello():
	# return "Hello World!"
	return render_template("index.html")

@app.route("/results.csv", methods=['GET', 'POST'])
def result():
	si = StringIO.StringIO()
	cw = csv.writer(si)
	
	# TODO: replace csvList with the actual random list
	csvList = [
		'a b c d e f'.split(),
		'1 2 3 4 5 6'.split(),
		'1 2 3 4 5 6'.split(),
		'1 2 3 4 5 6'.split(),
		'1 2 3 4 5 6'.split(),
		'1 2 3 4 5 6'.split()
	]
	# ------------------------
	
	cw.writerows(csvList)
	output = make_response(si.getvalue())
	output.headers["Content-Disposition"] = "attachment; filename=export.csv"
	output.headers["Content-type"] = "text/csv"
	return output

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug =True)
