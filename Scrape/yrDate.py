

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