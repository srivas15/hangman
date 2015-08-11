import requests
import urllib2
from bs4 import BeautifulSoup
import random

url = 'http://www.imdb.com/chart/top'

print '\nGet ready to play hangman\n\n'
print 'Your game is loading, please be patient ... \n\n'

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
chances = input('Please enter the number of chances you want (default = 5): ')

alphabetList = ['a', 'e', 'i', 'o', 'u', ' ', '0', '1', '2','3','4','5','6','7','8','9']

mainList = list(main)

while(chances > 0):
	gameWon = True
	for alphabet in mainList:
		if alphabet in alphabetList:
			print alphabet,
		else:
			print '_',
			gameWon = False
	
	print '\nChances remaining: ', chances
	if gameWon:
		break
	newAlpha = raw_input('Please enter the next alphabet: ')
	
	while(newAlpha in alphabetList):
		newAlpha = raw_input('Please enter a different alphabet: ')
	print '\n'
	if newAlpha in mainList:
		alphabetList.append(newAlpha)
	else:
		chances = chances-1

if gameWon:
	print 'congratulations!!!'
else:
	print 'Chances remaining: ', chances
	print 'Sorry, please try again'
