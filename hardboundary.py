import numpy as np
import linalgutil as la
import shapely.geometry as geom

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

SQUARE_SEGMENTS = [
	geom.LineString([(-10.0, -10.0), (-10.0, 10.0)]),
	geom.LineString([(-10.0, 10.0), (10.0, 10.0)]),
	geom.LineString([(10.0, 10.0), (10.0, -10.0)]),
	geom.LineString([(10.0, -10.0), (-10.0, -10.0)])
]

def bounceIfHitsBox(x0, v0, x, v):
	trajectory = geom.LineString([x0, x])
	xPrime, vPrime = x, v
	for seg in SQUARE_SEGMENTS:
		intersection = seg.intersection(trajectory)
		if not intersection.is_empty:
			a = np.array([intersection.x, intersection.y])
			c = np.array(seg.coords[1]) - np.array(seg.coords[0])
			n = np.array((c[1], c[0]))
			nHat = n / np.linalg.norm(n)
			xPrime = x - 2*np.dot(x-a, nHat)*nHat
			vPrime = v - 2*np.dot(v, nHat)*nHat
	return xPrime,vPrime