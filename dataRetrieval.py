#!/usr/bin
import csv
import requests
import json
import re 
from xlrd import open_workbook
import pandas as pd # to merge the omdb data with the tomato data that we pull from the website using GET requests.

# data to extract from the api call:
# 1. tomatoUserRating
# 2. tomatoRating
# 3. tomatoReviews
# 4. tomatoFresh
# 5. tomatoRotten
# 6. tomatoUserMeter
# 7. tomatoUserReviews
# 8. imdbVotes
# 9. Metascore

# all the genres: set([u'Sci-Fi', u'Crime', u'Romance', u'Animation', u'Music', u'Comedy', u'War', u'genres', u'Horror', u'Film-Noir', u'Adventure', u'News', u'Reality-TV', u'Thriller', u'Western', u'Mystery', u'Short', u'Drama', u'Action', u'Documentary', u'Musical', u'History', u'Family', u'Fantasy', u'Game-Show', u'Sport', u'Biography'])

sep = '!'

def mergeCSV():
	print("starting to merge")
	a = pd.read_csv("movie_data.csv")
	b = pd.read_csv("tomatoData.csv")
	a = a.merge(b, on='movie_title')
	print("both files merged successfully")


def makeAPIcall(movieTitle):
	r = requests.get("http://www.omdbapi.com/?t="+movieTitle+"&tomatoes=true")
	jsonObject = json.loads(r.content)
	return jsonObject

def getData():	
	keyList = []
	keyList.append('tomatoUserRating')
	keyList.append('tomatoRating')
	keyList.append('tomatoReviews')
	keyList.append('tomatoFresh')
	keyList.append('tomatoRotten')
	keyList.append('tomatoUserMeter')
	keyList.append('tomatoUserReviews')
	keyList.append('imdbVotes')
	keyList.append('Metascore')

	data = []

	ofile  = open('tomatoData.csv', "wb")
	writer = csv.writer(ofile, delimiter=',')

	with open('movie_data.csv', 'rb') as file:
		try:
			reader = csv.reader(file)
			for row in reader:
				movieTitle = row[11]
				movieTitle = movieTitle.strip()
				movieTitle = re.sub('[^a-zA-Z0-9 \n\.]', '', movieTitle)
				print("dealing with movie " + movieTitle +"\n")
				jsonResponse = makeAPIcall(movieTitle)
				if(jsonResponse):
					data.append(movieTitle)
					for item in keyList:
						if(item in jsonResponse):
							data.append(jsonResponse[item])
							tomatoUserRating = jsonResponse[item]
							print("The " + item+ " for " + movieTitle + " is " + tomatoUserRating)	
					print("--------------------")
					print(data)
					writer.writerow(data)
					data = []	
		except:
			print("ENCOUNTERED AN EXCEPTION")
			pass
		finally:
			file.close()        
			print("closed the file")

def getGenre(sep):
	genres = set()
	try:
		workbook = open_workbook('movie_data.xls')
		for s in workbook.sheets():
			for row in range(s.nrows):
				value  = (s.cell(row,26).value)
				array = value.split(sep)
				for item in array:
					genres.add(item)
		return genres

	except Exception as e:
		print("exception while splitting the genres", e)
		pass		
def getIndexOfGenre(item, genresList):
	return genresList.index(item)

def splitGenre(sep, genresSet):
	genresList = list(genresSet)
	ofile  = open('genres.csv', "wb")
	writer = csv.writer(ofile, delimiter=',')
	counter = 1
	# writer.writerow(genresList)
	try:
		workbook = 	open_workbook('movie_data.xls')
		for sheet in workbook.sheets():
			for row in range(1,sheet.nrows):
				name = sheet.cell(row,0).value
				genres = sheet.cell(row,26).value
				print(name , "-->",genres)
				convertedList = []
				for i in range(0,len(genresList)):
					convertedList.append(0)
				genreListFromRow = []
				genreListFromRow = genres.split(sep)
				for item in genreListFromRow:
					if item in genresSet:
						index = getIndexOfGenre(item,genresList)
						convertedList[index] = 1 
				convertedList.append(name)		
				print(name, convertedList)
				writer.writerow(convertedList)
				counter = counter + 1
		print("total of " + str(counter) +" rows" + "sheet nrows "+ str(sheet.nrows))

	except Exception as exception:
		print("encountered an exception while splitting the genre" , exception)
		pass			
	
def getCharacter():
	str = "Action|Adventure|Fantasy|Sci-Fi"
	sep = str[6]
	return sep


sep = getCharacter()
# getData()
# mergeCSV()
genres = getGenre(sep)
print(genres)
# print(genres)
splitGenre(sep, genres)