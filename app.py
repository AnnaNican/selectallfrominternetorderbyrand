import json
import random
import StringIO
import csv

import requests
from bs4 import BeautifulSoup

from flask import Flask
from flask import render_template
from flask import make_response

from lib.getrandom import howmanydatatoget

app = Flask(__name__)

@app.route("/")
def hello():
	# return "Hello World!"
	return render_template("index.html")

@app.route("/results.csv", methods=['GET', 'POST'])
def result():
	si = StringIO.StringIO()
	dataframe = howmanydatatoget()
	dataframe.to_csv(si, index=False)
	output = make_response(si.getvalue())
	#output.headers["Content-Disposition"] = "attachment; filename=export.csv"
	output.headers["Content-type"] = "text/csv"
	return output

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug =True)
