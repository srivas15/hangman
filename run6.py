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
	print 'index'
	global alphabetList
	global main
	main = ""
	alphabetList = ['-', 'a', 'e', 'i', 'o', 'u', ' ', '0', '1', '2','3','4','5','6','7','8','9']
	#print data.chances
	#print data.main
	#print data.mainList
    	return render_template('index.html')

@app.route('/play.html', methods=['POST', 'GET'])
def play():
	'''
	global firstTime
	global mainList
	global alphabetList
	global chances
	global main
	
	if firstTime:
		chances = request.form['chances']
		chances = int(chances)
		firstTime = False
	'''
	#global mainList
	#global chances
	global alphabetList
	print type(alphabetList)
	chances = request.form.get('chances', 5)
	print chances
	chances = int(chances)
	mainList = request.form.get('mainList', [])
	#print 'mainList is ', mainList, type(mainList)
	if (mainList == []):
		print 'do nothing'
	else:
		print 'do something'
		mainList = list(mainList)
	'''
		mainList = mainList.strip('[]')
		#mainList = mainList.split(',')
		mainList = mainList.replace("u'", "")
		mainList = mainList.replace("'", "")
		mainList = " "+mainList
		print 'mainlist IS ', mainList
		mainList = mainList.split(',')
		mainList = [m.replace(' ', '', 1) for m in mainList]
		print mainList, type(mainList)
	'''	
	#movie = ""
	if(request.method == 'GET'):
		print 'get'
		#print chances
		url = 'http://www.imdb.com/chart/top'
        	html = urllib2.urlopen(url).read()
        	#print 'urlib done'
		soup = BeautifulSoup(html, "html.parser")
		#print 'bs4 done'
        	allMovies = []
        	movies = soup.find_all("td", {"class":"titleColumn"})
        	for movie1 in movies:
        	        movieName = movie1.find("a");
        	        movieName = movieName.getText()
        	        allMovies.append(movieName)
		#print 'found movie'
        	main = random.choice(allMovies)
        	main = main.lower()
		print 'movie when i found it ', main
        	mainList = list(main)
		print 'creating mainList ', mainList
		#chances = 5
		gameWon = False
		#return render_template('play.html', chances=chances)
	elif(request.method == 'POST'):
		#chances
		print 'post'
		print chances
		#print 'newalpha is ', newAlpha
		#print 'post and chances are ', chances
		#test = test+test
		gameWon = True
		newAlpha = request.form['newAlpha']
		print 'newAlpha is ', newAlpha
		if newAlpha in mainList:
			alphabetList.append(newAlpha)
		else:
			gameWon = False
			chances = chances-1
		#movie2 = request.form.get('movie', '')
		#print 'movie2 is ', movie2
	#print 'out'
	#movie = request.form.get('movie', '')
	#print 'movie is ', movie
	movie = ""
	#print 'movie before entering loop is ', movie
	#print 'mainList before entering loop is ', mainList
	#print 'alphabetList before entering loop is ', alphabetList
	for alphabet in mainList:
		#print 'alphabaet in mainlist :', alphabet
		if alphabet in alphabetList:
		#	print 'in alphabetList'
			if(alphabet == ' '):
		#		print 'isspace'
				movie = movie + '   '
			else:
		#		print 'is not space'
				movie = movie+alphabet
		else:
		#	print 'not in alphabetList'
			movie = movie+'*'
			gameWon = False
		#print 'movie is ', movie
	#print 'everything done lets see ', movie
	if gameWon:
		return render_template('won.html', chances=chances, movie=movie)
	if chances == 0:
		return render_template('lost.html', chances=chances, movie=main)
	str1 = ''.join(mainList)
	return render_template('play.html', chances=chances, movie=movie, mainList=str1)

if __name__ == '__main__':
    app.run(debug=True)

