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

SQUARE = geom.LinearRing((
		(-10.0, -10.0),
		(-10.0, 10.0),
		(10.0, 10.0),
		(-10.0, 10.0)
	))

SQUARE_SEGMENTS = [
	geom.LineString([(-10.0, -10.0), (-10.0, 10.0)]),
	geom.LineString([(-10.0, 10.0), (10.0, 10.0)]),
	geom.LineString([(10.0, 10.0), (10.0, -10.0)]),
	geom.LineString([(10.0, -10.0), (-10.0, -10.0)])
]

def bounceIfHitsBox(x, v, t):
	xPrime = x + v * t
	trajectory = geom.LineString([x, xPrime])
	for seg in SQUARE_SEGMENTS:
		intersection = seg.intersection(trajectory)
		if not intersection.is_empty:
			a = np.array([intersection.x, intersection.y])
			c = seg.coords.xy
			d = 'lol'
	return x,v