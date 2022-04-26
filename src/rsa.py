#Creating an RSA setup

import random
from math import ceil, sqrt, floor
#returns [d, x, y] for a >= b where d = gcd(a,b) = ax + by
def _pulverizer(a,b):
	x1 = 1
	y1 = 0
	x2 = 0
	y2 = 1
	while b != 0:
		q = a//b
		r = a % b
		new_x1 = x2
		new_y1 = y2
		new_x2 = x1 - q*x2
		new_y2 = y1 - q*y2
		a = b
		b = r
		x1 = new_x1
		y1 = new_y1
		x2 = new_x2
		y2 = new_y2
	return [a, x1, y1]

#modular exponentiation for Miller Rabin
def _special_expmod(a,b,m):
	if b == 0:
		return 1
	elif b % 2 == 0:
		y = _special_expmod(a,b//2,m)
		z = pow(y,2,m)
		if z == 1 and y!= 1 and y != -1 and y != (m-1): #since  m-1 = -1 mod p so (m-1)^2 = 1 mod p
			return 0
		else:
			return z
	else:
		y = _special_expmod(a,b-1,m) #if b is prime y will return as 1
		return pow(a*y,1,m)

#Miller-Rabin test
def _isprime(m,iterations):
	while iterations > 0:
		k = random.randrange(1,m)
		if _special_expmod(k,m,m) != k:
			return False
		iterations -= 1
	return True

def gen_keys(bit_length, confidence=None):
	# confidence is the number of iterations for the Miller-Rabin test
	if confidence is None: confidence = 100

	n_lower = pow(2, bit_length-1) #all bits of length (bitlength - 1) turned on
	n_upper = pow(2, bit_length)- 1 #all bits turned on of a given bitlengt
	lower = ceil(sqrt(n_lower))
	upper = floor(sqrt(n_upper))
	while True:
		p = random.randrange(lower,upper)
		if _isprime(p,confidence):
			break
	while True:
		q = random.randrange(lower,upper)
		if _isprime(q,confidence) and q != p:
			break

	print("p = ", p)
	print("q = ", q)

	n = p*q
	phi = (p-1)*(q-1)

	print("n = ",n)
	print("phi = ",phi)

	e = 3
	result = _pulverizer(phi,e)
	while result[0] != 1: #since 3 will not be coprime with every phi, but it will always be odd
		e += 2
		result = _pulverizer(phi,e)
	d = result[2]
	while d < 0:
		d += phi

	print("e = ", e)
	print("d = ", d)

	check = pow(e*d,1,phi)
	if check == 1:
		print("Passed sanity check")
		print(e,"*",d,"=",check)
	else:
		print("Sanity check:you are insane")
		print(e,"*",d,"=",check)
	return {"n": n, "p": p, "q": q, "phi": phi, "e": e, "d": d}

def decrypt(ciphertext,d,n,salt_length):
	salted_m = pow(int(ciphertext),int(d),int(n))
	return salted_m >> salt_length

def encrypt(message,e,n,salt_length):
	lower = pow(2, salt_length-1)
	upper = pow(2, salt_length)- 1
	salt = random.randrange(lower,upper)

	message = message << salt_length
	message += salt

	return pow(int(message),int(e),int(n))


