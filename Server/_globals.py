"""Global variables used by many of the other modules."""

import cryptoUtilities as cu

HOST = '192.168.1.10'
PORT = 9099

# _____ DIFFIE HELLMAN GLOBALS _____ #
PRIME = cu.findPrime(2**127, 2**128) # A large prime number
GENERATOR = 3      # Generator for the ring Z_P with PRIME elements