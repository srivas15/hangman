from flask import Flask, render_template, request

app = Flask(__name__)

import requests
import urllib2
from bs4 import BeautifulSoup
import random

chances = 0;
firstTime = True
mainList = [];
alphabetList = ['a', 'e', 'i', 'o', 'u', ' ', '0', '1', '2','3','4','5','6','7','8','9']
main = "";

@app.route('/')
@app.route('/index')
def index():
    	return render_template('index.html')

@app.route('/setup.html')
def setup():
	global firstTime
	global mainList
	global main

	firstTime = True
	url = 'http://www.imdb.com/chart/top'
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html, "html.parser")

	allMovies = []
	movies = soup.find_all("td", {"class":"titleColumn"})
	for movie in movies:
		movieName = movie.find("a");
		movieName = movieName.getText()
	        allMovies.append(movieName)

	main = random.choice(allMovies)
	main = main.lower()
	mainList = list(main)

	return render_template('setup.html')

@app.route('/play.html', methods=['POST'])
def play():
	global firstTime
	global mainList
	global alphabetList
	global chances
	global main

	if firstTime:
		chances = request.form['chances']
		chances = int(chances)
		firstTime = False
	else:
		gameWon = True
		newAlpha = request.form['newAlpha']
		if newAlpha in mainList:
			alphabetList.append(newAlpha)
		else:
			gameWon = False
			chances = chances-1
	movie = ""
	for alphabet in mainList:
		if alphabet in alphabetList:
			if(alphabet == ' '):
				movie = movie + '   '
			else:
				movie = movie+alphabet
		else:
			movie = movie+'*'
			gameWon = False
	if gameWon:
		return render_template('won.html', chances=chances, movie=movie)
	if chances == 0:
		return render_template('lost.html', chances=chances, movie=main)
	return render_template('play.html', chances=chances, movie=movie)

if __name__ == '__main__':
    app.run(debug=True)

