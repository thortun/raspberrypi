# Some simple cryptography algorithms.
import time
import cryptoUtilities as cu # Local module of utility functions used here
import numpy as np

def DHProtocol(server):
    """The vanilla DH protocol between us and the server."""
    a = rand.randint(0, _globals.PRIME)    # Select a random number in the group
    x = pow(_globals.GENERATOR, a, _globals.PRIME) # Calculate the message
    payload = json.dumps({"DHMsg": x})     # Take the DH_MSG into a JSON-format
    server.send(payload)                   # Send the payload
    # Now we recieve the clients DH_MSG to share a secret
    DHRecv = server.recv(1024)             # Receive the payload, it is in JSON format
    DHRecv = json.loads(DHRecv)["DHMsg"]   # Unpack the JSON
    DHSecret = (x*DHRecv) % _globals.PRIME # Calculate the shared secret
    return DHSecret                        # Return the shared secret

def RSAKeygen(bitSize = 64):
	"""Key generatoin algorithm for RSA."""
	# LowerBOund should be about half the bitsize of the key to
	# get a key of correct size
	lowerBound = 2**(bitSize//2)
	p, q = cu.findPrime(lowerBound, lowerBound*2), cu.findPrime(lowerBound, lowerBound*2)
	s = (p - 1)*(q - 1)

	n = p*q                         # Secret key
	e = cu.findPrime(10**2, 10**3)  # Chose a public power
	d = cu.modInv(e, s)             # Chose the modular inverse
	return (n, e), (n, d)           # Return appropriate keys

def RSAEncrypt(m, ek):
	"""Encrypts the message m by using the touple
	ek = (n, e).
	"""
	return pow(m, ek[1], ek[0]) # Do it

def RSADecrypt(c, dk):
	"""Decrypts the message. Using the touple dk = (n, d)."""
	return pow(c, dk[1], dk[0])

def timeRSAKeygen(bitsize):
	print "Finding", bitsize, "bit key"
	startTime = time.clock()
	key = RSAKeygen(524)[0][0]
	endTime = time.clock()
	print "Found", bitsize, "bit key in", "{0:.3}".format(str(endTime - startTime)), "seconds"
	print key

def LWEKeygen(bitSize, q, alpha):
	"""Generates a LWE-key."""
	n = 2**bitSize         # Security parameter, number of rows in A
	k = 2**bitSize         # More parameters, number of columns in A (how many equations)

	s = np.zeros(n, dtype = np.uint32) # Preallocate space for secret key

	# Generate secret key
	for i in xrange(0, np.size(s)):
		s[i] = np.random.randint(0, q)  # Populate the secret vector

	# Generate public key
	# First generate A
	A = np.zeros((n, k), dtype = np.uint32)
	for i in xrange(n):
		for j in xrange(k):
			A[i][j] = np.random.randint(0, q)

	e = np.random.normal(0.0, alpha*q, k)    # Generate error-vector
	b = np.dot(s, A) + e                     # Calculate b-vector
	for i, _ in enumerate(b):                
		b[i] = b[i] % q                      # Reduce each element modulo q

	return (s, (A, b)) # (private, public)   # Return the decryption key and the encryption key

def LWEEncrypt(bitSize, q, m, ek, dk):
	"""Encryption using basic LWE.
	This algorithm only encrypts bits, m = 0 or 1
	"""
	n = 2**bitSize
	k = 2**bitSize  # For readability
	s = dk
	A = ek[0]       # For readability
 	b = ek[1]       # For readability

 	A = A.T         # Transpose the matrix to get the equations as rows

	kSubset = np.random.randint(0, 2, k)     # Choose a random subset of 1,..., k
	# We are now choosing the columns of A corresponding to the subset S
	colSum = np.zeros(n, dtype = np.uint32)  # Preallocate sum of subset of columns of A
	for i, s in enumerate(kSubset):  # Iterate over kSubset
		if s == 1:                   # If we are including the row,
			colSum += A[i]           # include it
			colSum = colSum % q      # Reduce it

	# Now sum the coordinates of b which are in the ciphertext
	bSum = np.sum(np.dot(s, b)) % q # Sum the elements we are interestd in

	if m == 0:
		return [colSum, bSum]
	elif m == 1:
		return [colSum, (bSum + q//2) % q]
	else:
		# Return encryption error
		pass

def LWEDecrypt(bitSize, q, c, dk):
	"""Decrypts a LWE-message.
	c = (\sum a_i, \sum b_i)

	"""
	s = dk        # Beautify
	a = c[0]      # Beautify
	b = c[1]      # Beautify

	d = b - np.dot(a, s) % q    # Value of this
	# Now check distance to q//2
	d = cu.posFloatMod(d - q//2, q)
	print b - np.dot(a, s) % q, d
	if d < q//4:
		return 0
	elif d >= q//4 and d <= 3*q//4:
		return 1