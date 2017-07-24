import numpy as np

def polarToCart(z):
	r, theta = z
	return np.array((r * np.sin(theta), r * np.cos(theta)))

def cartToPolar(y):
	theta = np.arctan2(y[0], y[1])
	r = np.linalg.norm(y,2)
	return np.array((r, theta))

def projectToBoundary(x, rMax):
	r, phi = cartToPolar(x)
	return polarToCart((rMax, phi))

def angleBetweenTwoVectors(a, b):
	return np.arccos(np.dot(a,b) / (np.linalg.norm(a,2) * np.linalg.norm(b,2)))

def bounce(x, v, t, rMax):
	theta = angleBetweenTwoVectors(x, v)
	r, phi = cartToPolar(x)
	psi = np.pi + phi - (2 * theta)
	vPrime = polarToCart((np.linalg.norm(v,2), psi))
	xPrime = projectToBoundary(x, rMax) + vPrime * t
	return xPrime, vPrime

def bounceIfHitsBoundary(x, v, t, rMax):
	if np.linalg.norm(x, 2) > rMax:
		return bounce(x, v, t, rMax)
	else:
		return x, v
