import numpy as np
import linalgutil as la

def projectToBoundary(x, rMax):
	r, phi = la.cartToPolar(x)
	return la.polarToCart((rMax, phi))

def bounce(x, v, t, rMax):
	theta = la.angleBetweenTwoVectors(x, v)
	r, phi = la.cartToPolar(x)
	psi = np.pi + phi - (2 * theta)
	vPrime = la.polarToCart((np.linalg.norm(v,2), psi))
	xPrime = projectToBoundary(x, rMax) + vPrime * t
	return xPrime, vPrime

def bounceIfHitsBoundary(x, v, t, rMax):
	if np.linalg.norm(x, 2) > rMax:
		return bounce(x, v, t, rMax)
	else:
		return x, v
