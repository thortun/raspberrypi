# Some simple cryptography algorithms.
import random
import cryptoUtilities as cu # Local module of utility functions used here

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
	return (n, e), (n, d), p, q           # Return appropriate keys

def RSAEncrypt(m, ek):
	"""Encrypts the message m by using the touple
	ek = (n, e).
	"""
	return pow(m, ek[1], ek[0]) # Do it

def RSADecrypt(c, dk):
	"""Decrypts the message. Using the touple dk = (n, d)."""
	return pow(c, dk[1], dk[0])