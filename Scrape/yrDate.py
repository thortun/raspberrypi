from calendar import isleap  # Import the method for finding leap year

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

	def __add__(self, rhsINT):
		"""Adds an int to the date."""
		day, month, year = int(self.day), int(self.month), int(self.year) # Intify
		for _ in xrange(0, rhsINT): # Add one date at a time
			if isLastDayOfYear(day, month, year): # If we are on the last day of the year
				year += 1                 # Increment the year
				month = 1                 # Reset month
				day = 1	                  # Reset day
			elif isLastDayOfMonth(day, month, year): # If it is the last day of a month but NOT a year
				month += 1                # Increment month 
				day = 1                   # Reset day
			else:                         # If it is just an ordinary day
				day += 1                  # Increment the day
		# We have to do some padding work to make sense of this
		day = str(day)                    # Make into string
		month = str(month)                # Make into string
		year = str(year)                  # Make into string
		if len(day) == 1:                 # If we have made the day-string of length 1
			day = '0' + day               # Do some padding
		if len(month) == 1:               # If the month string is of length 1
			month = '0' + month           # Do some padding
		return yrDate(day + ':' + month + ':' + year) # Return a new date

	def hasHourTime(self):
		"""Checks if the date has hourTime data."""
		if self.hourInterval[0] != '':
			return True
		else:
			return False

def isLastDayOfMonth(day, month, year):
	"""Checks whether a day is the last day 
	of a month given the year.
	"""
	day, month, year = int(day), int(month), int(year) # Intify just in case
	if month in [1, 3, 5, 7, 8, 10, 12]: # Check months with 31 days
		if day == 31:                    # If we are on the last day of the month
			return True                  # This is the last day of the month
	elif month in [4, 6, 9, 11]:         # Check months with 30 days
		if day == 30:                    # If this is the last day
			return True                  # Return True
	elif month == 2:                     # Special case for February
		if isleap(year):                 # On a leap year,
			if day == 29:                # If we are on the last day
				return True              # Return True
		else:                            # If it is not leap, check for last day
			if day == 28:                # If it is the last day
				return True              # Return True
                                         # Now there are no more cases to check
	return False                         # So return False

def isLastDayOfYear(day, month, year):
	"""Checks if we are on the last day of the year."""
	return int(day) == 31 and int(month) == 12
