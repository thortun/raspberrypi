import random as rand
import json

import _globals

def fastExpo(base, exponent):
    """Fast exponentiation of base to the power of exponent."""
    return

def fastExpMod(base, exponent, mod):
    """Fast modular exponentiation,
    base to the power of exponent modulo mod."""
    if exponent < 0:
        return fastExpMod(1/base, -exponent)
    elif exponent == 0:         # Check for trivial exponent 0
        return 1                # Exponent is 0, return 1 (multiplicative identity)
    elif exponent == 1:         # Check for trivial exponent 1
        return base             # Exponent is 1, return the base
    elif exponent % 2 == 0:   # Check if the exponent is even
        return fastExpMod(base*base, exponent/2, mod) % mod          # Recursive step for even
    elif exponent % 2 == 1:
        return base*fastExpMod(base*base, (exponent-1)/2, mod) % mod # Recursive step for odd