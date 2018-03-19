# Some simple cryptography algorithms.

import cryptoUtilities as cu # Local module of utility functions used here

def RSAKeygen():
	"""Key generatoin algorithm for RSA."""
	lowerBound = 10**12
	p, q = cu.findPrime(lowerBound, lowerBound*10), cu.findPrime(lowerBound, lowerBound*10)
	s = (p - 1)*(q - 1)

	n = p*q                         # Secret key
	e = cu.findPrime(10**2, 10**3)  # Chose a public power
	d = cu.modInv(e, s)                # Chose the modular inverse

	return (n, e), (n, d)           # Return appropriate keys

def RSAEncrypt(m, ek):
	"""Encrypts the message m by using the touple
	ek = (n, e).
	"""
	return pow(m, ek[1], ek[0]) # Do it

def RSADecrypt(c, dk):
	"""Decrypts the message. Using the touple dk = (n, d)."""
	return pow(c, dk[1], dk[0])

ek, dk = RSAKeygen()