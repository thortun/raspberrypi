import random
import math
import numpy

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a%b
    return a

def egcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

def modInv(b, n):
	"""Calculates the modular inverse of b modulo n."""
	g, x, _ = egcd(b, n)
	if g == 1: # If the GCD is 1 the inverse exists
		return x % n # Return the value
	return None # If g is not 1 then we return None because it does not exists

def legandre(a, b):
	"""Calculate the legandre symbol of a over b.

	Defined to be:
						1 if exists non-zero b s.t. b^2 = a
	legandre(a, b) =    0 if p|a
						-1 otherwise

	We use some additional properties to construct the algorithm.
	"""
	# Define small helper functions
	def checkMod8(b):
		"""Small helper function for legandre symbol."""
		if b % 8 == 1 or b % 8 == 7: # Check 'denominator' modulo 8
			return 1
		else:
			return -1

	def checkMod4(a, b):
		"""Small helper function for the Legandre symbol.
		Checks the values of a and b modulo 4 and returns
		the correct sign for when we are going to flip.
		"""
		if a % 4 == 3 and b % 4 == 3:
			return -1
		else:
			return 1

	sign = 1        	# Keeping track of the sign
	while a > 2:    	# We can reduce the 'numerator' as much as we need to
		if b == 0:      # It is possibly to get here with b being 0
			return 0    # If this is the case, just return 0
		a = a % b       # Reduce module to 'denominator'
		while a % 2 == 0 and a != 0:        # If a is even, we can pull out a factor 2 and adjust the sign
			sign *= checkMod8(b) # Adjust the sign
			a = a / 2            # Factor out one 2 
		# We are now going to 'flip' the symbol, but need to keep track of the sign when doing so
		sign *= checkMod4(a, b)  # Update the sign
		# Flip the variables
		tempb = b       # Going to swap, store b in a temp variable
		b = a           # Swap
		a = tempb       # Swap
	# Now a is either 1 or 2
	if a == 2:
		return sign*checkMod8(b)
	elif a == 1:
		return sign
	else:
		return 0        # Legandry symbol of 0 is 0

def primalityTestGuess(p, tolerance = -6):
	"""GUESSES whether p is a prime using the
	Legandre symbol.

	tolerance is the log of the probability we want that
	p is prime. That is, stop when we are certain that p
	is prime within 2^tolerance
	"""
	acumulatedProbability = 1      # Starting probability is 1 - acumulatedProbability
	while acumulatedProbability > 2**tolerance: # While we are still uncertain
		k = random.randint(0, p)   # Pick a random number from the group
		legSymbol = legandre(k, p) # Calculate legandre synbol
		powerVal = pow(k, (p - 1)/2, p) # Calculate the power
		# By using 'ordinary' modulo, we are not getting an answer of -1, so fix this
		# powerVal being p - 1 is equivalent to it being -1 in the group
		if powerVal == p - 1: 
			powerVal = powerVal - p		     
		if legSymbol == powerVal:       # For prime p, these values are equal
			# We have probability about 0.5 that this is the case for non-prime aswell
			# so update the accumulated probability by halving it
			acumulatedProbability *= 0.5 
		else:
			return False           # However, if these are not equal we are certain that p is NOT prime
	# If we have not fond evedence (legandre != power),
	# return the GUESS which is that p is prime. 
	# We are certain to within 2^tolerance of this
	return True

def primalityTest(p):
	"""Primality testing algrithm, deterministic.
	Ripped from wikipedia, it is black magic.
	"""
	if p <= 1:
		return False
	elif p <= 3:
		return True
	elif p % 2 == 0 or p % 3 == 0:
		return False
	i = 5
	while i*i <= p:
		if p % i == 0 or p % (i + 2) == 0:
			return False
		i += 6
	return True

def findPrime(lowerBound, upperBound, tolerance = -12):
	"""Finds a prime in the interval [lowerBound, upperBound]."""
	while True: # Test indefinatily
		candidate = random.randint(lowerBound, upperBound + 1)   # Pick a random candidate within bounds
		if primalityTestGuess(candidate, tolerance):             # Make an educated guess whether it is prime
			#if primalityTest(candidate):                         # If it also passes rigorous test:
			return candidate                                 # Return the prime

def posFloatMod(num, mod):
	"""Calculates the modulo of a floating point
	number such that it is positive.
	"""
	num = num % mod
	while num < 0:
		num += mod
	return num

	