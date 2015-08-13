from flask import Flask, render_template, request

app = Flask(__name__)

import requests
import urllib2
from bs4 import BeautifulSoup
import random

alphabetList = ['-', 'a', 'e', 'i', 'o', 'u', ' ', '0', '1', '2','3','4','5','6','7','8','9']
main = ""
mainList = []

@app.route('/')
def index():
	global alphabetList
	global main
	main = ""
	alphabetList = ['-', 'a', 'e', 'i', 'o', 'u', ' ', '0', '1', '2','3','4','5','6','7','8','9']
    	return render_template('index.html')

@app.route('/play.html', methods=['POST', 'GET'])
def play():
	chances = request.form.get('chances', 5)
	print chances
	chances = int(chances)
	
	alphabetList = request.form.get('alphabetList', ['-', 'a', 'e', 'i', 'o', 'u', ' ', '0', '1', '2','3','4','5','6','7','8','9'])
	if (type(alphabetList) == "<type 'list'>"):
		print 'do nothing'
	else:
		print 'do something'
		alphabetList = list(alphabetList)
	
	mainList = request.form.get('mainList', [])
	if (mainList == []):
		print 'do nothing'
	else:
		print 'do something'
		mainList = list(mainList)
	
	main = request.form.get('main', '')
	
	if(request.method == 'GET'):
		print 'get'
		url = 'http://www.imdb.com/chart/top'
        	html = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")
        	allMovies = []
        	movies = soup.find_all("td", {"class":"titleColumn"})
        	for movie1 in movies:
        	        movieName = movie1.find("a");
        	        movieName = movieName.getText()
        	        allMovies.append(movieName)
        	main = random.choice(allMovies)
        	main = main.lower()
        	mainList = list(main)
		gameWon = False
	elif(request.method == 'POST'):
		gameWon = True
		newAlpha = request.form['newAlpha']
		newAlpha = newAlpha.lower()
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
	str1 = ''.join(mainList)
	str2 = ''.join(alphabetList)
	return render_template('play.html', chances=chances, main=main, movie=movie, mainList=str1, alphabetList=str2)

if __name__ == '__main__':
    app.run(debug=True)

