#!/usr/bin/env python
# -*- coding: utf-8 -*-
# "Weather forecast from Yr, delivered by the Norwegian Meteorological Institute and NRK"

import time
from operator import itemgetter # To sort list of touples

import utilities as u # Scraping utilities

class yrDate():
	"""Class to represent yr-date."""
	def __init__(self, dateString, hourInterval = ('', '')):
		"""Initalizes the yrDate. 'string'
		should be dd.mm.yyyy
		"""
		self.day = dateString[0:2]       # Store day as str
		self.month = dateString[3:5]     # Store month as str
		self.year = dateString[6:10]      # Store year as str
		self.hourInterval = hourInterval # Store the hour interval as a touple of strings

	def __str__(self):
		"""Returns the string representation of the date."""
		date = self.day + '.' + self.month + '.' + self.year
		if self.hourInterval[0]:
			time = ':' + self.hourInterval[0] + '-' + self.hourInterval[1]
		else:
			time = self.hourInterval[0]
		return date + time

	def __eq__(self, rhs):
		"""Checks for equality of dates."""
		dayInt = int(self.day)      # Cast day to integer
		monthInt = int(self.month)  # Cast month to integer
		yearInt = int(self.year)    # Cast year to integer

		if self.hasHourTime() and rhs.hasHourTime(): # Check for hour times
			hourBool = int(self.hourInterval[0]) == int(rhs.hourInterval[0]) # Determine if the start-points are equal
		elif self.hasHourTime() and not rhs.hasHourTime(): 
			hourBool = int(self.hourInterval[0]) == 0 or int(self.hourInterval[0]) == 24
		elif not self.hasHourTime() and rhs.hasHourTime(): 
			hourBool = int(rhs.hourInterval[0]) == 0 or int(rhs.hourInterval[0]) == 24
		else:
			hourBool = True
		return (dayInt == int(rhs.day)) and\
		       (monthInt == int(rhs.month)) and\
		       (yearInt == int(rhs.year)) and\
		       hourBool

	def __le__(self, rhs):
		"""Compares if self <= rhs in time."""
		dayInt = int(self.day)      # Cast day to integer
		monthInt = int(self.month)  # Cast month to integer
		yearInt = int(self.year)    # Cast year to integer

		if yearInt > int(rhs.year):     # If self.year is > rhs.year
			return False                # We know for sure self is later rhs
		elif yearInt < int(rhs.year):   # If self.year is < than rhs.year
			return True                 # We know for sure that self is earlier than rhs
		else:                           # If the year is equal, go to month and do the same
			if monthInt > int(rhs.month):    # If self.month is > rhs.month
				return False                 # We know for sure self is later rhs
			elif monthInt < int(rhs.month):  # If self.month is < than rhs.month
				return True                  # We know for sure that self is earlier than rhs
			else:                            # Now year AND month are equal, go to day
				if dayInt > int(rhs.day):     # If self.day is > rhs.day
					return False                 # We know for sure self is later rhs
				elif dayInt < int(rhs.day):   # If self.day is < than rhs.day
					return True                  # We know for sure that self is earlier than rhs
				else:                            # Now year AND month AND day are equal, check times
					if self.hasHourTime() and rhs.hasHourTime(): # If both has hour time
						return int(self.hourInterval[0]) <= int(rhs.hourInterval[0]) # Sort on the START of the interval
					else:                        # Here day, month and year are equal and
						return True              # neither has hourTime
						                         
	def __lt__(self, rhs):
		return (self.__le__(rhs) and not self.__eq__(rhs))

	def __ge__(self, rhs):
		return not self.__lt__(rhs)

	def __gt__(self, rhs):
		return (self.__ge__(rhs) and not self.__eq__(rhs))

	def hasHourTime(self):
		"""Checks if the date has hourTime data."""
		if self.hourInterval[0] != '':
			return True
		else:
			return False

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
			fileID.write(str(yrDate(currentDate, hours)) + ' ' + str(tempData[i]) + '\n')
	fileID.close()
	return None

url = 'https://www.yr.no/sted/Norge/Trøndelag/Trondheim/Trondheim/'
scrapeYr(url, 'data.txt')

# print time.gmtime()
# print (time.mktime(time.gmtime()))
# print(time.asctime(time.gmtime()))