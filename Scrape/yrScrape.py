#!/usr/bin/env python
# -*- coding: utf-8 -*-
# "Weather forecast from Yr, delivered by the Norwegian Meteorological Institute and NRK"

import time
from operator import itemgetter # To sort list of touples

import utilities as u # Scraping utilities
import yrDate         # Class to keep track of dates from yr

def isDate(dateString):
	"""Checks whether a string is of the form
	dd.mm.yyyy:t-t
	where t are integers. 
	03.05.1964:16-20
	"""
	try:
		day = int(dateString[0:2])
		month = int(dateString[3:5])
		year = int(dateString[6:10])

		# Now check for correct bounds
		if (day >= 1 and day <= 31) and (month >= 1 and month <= 12):
			return True
		else:
			return False
	except ValueError: # If the things are not dats, a ValueError is raised for sure
		return False

def extractYRHeader(data):
	"""Extract some headers. This gives us the date and where
	temperatures and other data is from.
	"""
	todayData, todayIndex = u.extract_between(data, "<caption>", "</caption>", True)  # Extract the indexes
	newData, newIndex = [], []     # New datas
	for i, data in enumerate(todayData):
		endOfString = data[-10:]
		if isDate(endOfString):
			newData.append(endOfString)
			newIndex.append(todayIndex[i])

	return newData, newIndex

def scrapeYr(url, filename):
	"""Scrapes the temperatures from the given url.
	Writes the data to the filename specified.
	"""
	data = u.generate_HTML_string(url) # Extract the HTML-data

	tempData, tempIndex = u.extract_between(data, "Temperatur: ", "\xc2\xb0.  F", True) # TEMPERATUREdata
	todayData, todayIndex = extractYRHeader(data) # Extract som headers, this is the date (today, tomorrow, day after tomorrow)

	hourData, hourIndex = u.extract_between(data, 'title="klokken">kl</abbr>', '</td>', True) # Extract the hour times
	currentDateIndex = 0  # Start with the date for today
	currentDate = todayData[currentDateIndex] # First data is collected from today

	with open(filename, 'a') as fileID:
		fileID.write('#' + str(time.mktime(time.gmtime())) + '\n')
		for i, hours in enumerate(hourData):
			if tempIndex[i] > todayIndex[currentDateIndex + 1]:
				currentDateIndex += 1 # Update the date
				currentDate = todayData[currentDateIndex]

			hours = hours.replace('\xe2\x80\x93', '-')[1:]
			hours = hours.split('-')
			hours = (hours[0], hours[1])
			fileID.write(str(yrDate.yrDate(currentDate, hours)) + ' ' + str(tempData[i]) + '\n')
	fileID.close()
	return None

url = 'https://www.yr.no/sted/Norge/Trøndelag/Trondheim/Trondheim/'
scrapeYr(url, 'data.txt')

date = yrDate.yrDate('31.05.1977')
print date
print date + 13032

# print time.gmtime()
# print (time.mktime(time.gmtime()))
# print(time.asctime(time.gmtime()))