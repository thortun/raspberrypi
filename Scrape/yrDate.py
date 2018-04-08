from calendar import isleap  # Import the method for finding leap year

class yrDate():
    """Class to represent yr-date."""
    def __init__(self, (day, month, year), hourInterval = (-1, -1)):
        """Initalizes the yrDate.
        Touple of strings or ints
        """
        self.day = day                   # Store day 
        self.month = month               # Store month 
        self.year = year                 # Store year 
        self.hourInterval = hourInterval # Store the hour interval as a touple of ints

    def __str__(self):
        """Returns the string representation of the date."""
        date = str(self.day) + '.' + str(self.month) + '.' + str(self.year) # Convert to string
        if self.hasHourInterval():
            time = ':' + str(self.hourInterval[0]) + '-' + str(self.hourInterval[1])
        elif self.hourInterval[0] != -1 and self.hourInterval[1] == -1:   # Use -1 as false 
            time = ':' + str(self.hourInterval[0]) 
        else:
            time = str(self.hourInterval[0])        
        return date + time

    def __eq__(self, rhs):
    	"""Checks for equality of dates.""" 
        if self.hasHourInterval() and rhs.hasHourInterval():                 # Check for hour times
        	hourBool = self.hourInterval[0] == rhs.hourInterval[0]   # Determine if the start-points are equal
    	elif self.hasHourInterval() and not rhs.hasHourInterval():           # If lhs has hours but rhs does not
    		hourBool = self.hourInterval[0] == 0 or self.hourInterval[0] == 24
    	elif not self.hasHourInterval() and rhs.hasHourInterval(): 
    		hourBool = rhs.hourInterval[0] == 0 or rhs.hourInterval[0] == 24
    	else:
    		hourBool = True
    	return (self.day == int(rhs.day)) and\
    	       (self.month  == int(rhs.month)) and\
    	       (self.year == int(rhs.year)) and\
    	       hourBool

    def __le__(self, rhs):
    	"""Compares if self <= rhs in time."""
    	if self.year > rhs.year:        # If self.year is > rhs.year
    		return False                # We know for sure self is later rhs
    	elif self.year  < rhs.year:     # If self.year is < than rhs.year
    		return True                 # We know for sure that self is earlier than rhs
    	else:                           # If the year is equal, go to month and do the same
    		if self.month  > rhs.month:      # If self.month is > rhs.month
    			return False                 # We know for sure self is later rhs
    		elif self.month  < rhs.month:    # If self.month is < than rhs.month
    			return True                  # We know for sure that self is earlier than rhs
    		else:                            # Now year AND month are equal, go to day
    			if self.day > rhs.day:       # If self.day is > rhs.day
    				return False                 # We know for sure self is later rhs
    			elif self.day < rhs.day:         # If self.day is < than rhs.day
    				return True                  # We know for sure that self is earlier than rhs
    			else:                            # Now year AND month AND day are equal, check times
    				if self.hasHourInterval() and rhs.hasHourInterval(): # If both has hour time
    					return self.hourInterval[0] <= rhs.hourInterval[0] # Sort on the START of the interval
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
    	day, month, year = self.day, self.month, self.year # Intify
    	for _ in xrange(0, rhsINT): # Add one date at a time
    		if isLastDayOfYear(day, month): # If we are on the last day of the year
    			year += 1                 # Increment the year
    			month = 1                 # Reset month
    			day = 1	                  # Reset day
    		elif isLastDayOfMonth(day, month, year): # If it is the last day of a month but NOT a year
    			month += 1                # Increment month 
    			day = 1                   # Reset day
    		else:                         # If it is just an ordinary day
    			day += 1                  # Increment the day
    	# We have to do some padding work to make sense of this
    	return yrDate((day, month, year), self.hourInterval) # Return a new date

    def hasHourInterval(self):
    	"""Checks if the date has hourTime data."""
    	if self.hourInterval[0] != -1: # Use -1 as invalid hour time
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

def isLastDayOfYear(day, month):
    """Checks if we are on the last day of the year."""
    return int(day) == 31 and int(month) == 12
