import json
import random
# import urllib.parse

import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, url_for, redirect, request, Markup, flash, session, request

app = Flask(__name__)

@app.route("/")
def hello():
	# return "Hello World!"
	return render_template("index.html")

@app.route("/result", methods=['GET', 'POST'])
def result():
	print('we ran the dunction')
	return render_template("result.html")



if __name__ == "__main__":
    app.run(debug =True)
