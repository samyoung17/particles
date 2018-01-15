import hardboundary
import numpy as np
import linalgutil as la
import shapely.geometry as geom
import matplotlib.pyplot as plt
import scipy.special


EPSILON = 0.01

def perpendicularDistanceToLine(y1, y2, x):
	a = np.linalg.norm(x - y2)
	b = np.linalg.norm(y2 - y1)
	c = np.linalg.norm(y1 - x)
	gamma = np.arccos((a**2 + b**2 - c**2)/(2*a*b))
	return a*np.sin(gamma), a*np.cos(gamma)

def horizontalForceDueToSegment(a, b, z, rho):
	return rho * (1/np.sqrt(b**2 + z**2) - 1/np.sqrt(a**2 + z**2))

def verticalForceDueToSegment(a, b, z, rho):
	return (rho / z) * (b/np.sqrt(b**2 + z**2) - a/np.sqrt(a**2 + z**2))

def forceDueToSegment(seg, x, rho):
	# See http://physicstasks.eu/659/charged-line-segment
	y1, y2 = np.array(seg.coords[0]), np.array(seg.coords[1])
	z,b = perpendicularDistanceToLine(y1, y2, x)
	a = b - np.linalg.norm(y2 - y1)
	Ex = horizontalForceDueToSegment(a, b, z, rho)
	Ez = verticalForceDueToSegment(a, b, z, rho)
	horizontalUnit = (y2 - y1) / np.linalg.norm(y2 - y1)
	verticalUnit = la.normalVector(horizontalUnit)
	return Ex * horizontalUnit + Ez * verticalUnit

def forceDueToRing(rho, r, s):
	# rho is the charge density on the ring
	# r is the distance from the point to the origin
	# s is the radius of the ring
	return 2 * rho * s/r * np.sign(r-s) * \
			 (scipy.special.ellipe(-4*r*s/(r-s)**2)/(r+s) + scipy.special.ellipk(-4*r*s/(r-s)**2)/(r-s))


class Circle(object):

	def __init__(self, r):
		self.rMax = float(r)
		self.circle = geom.Point(0,0).buffer(float(r)).boundary
		self.hardedge = hardboundary.Circle(r)

	def force(self, x, q):
		r, theta = la.cartToPolar(x)
		xUnit = la.polarToCart((1, theta))
		rho = 1 / (2 * np.pi * self.rMax)
		return xUnit * q * forceDueToRing(rho, r, self.rMax)

	def contains(self, x):
		return np.linalg.norm(x) < self.rMax

	def plot(self, axes):
		circle = plt.Circle((0,0), radius=self.rMax, color='g', fill=False)
		axes.add_patch(circle)

	def bounceIfHits(self, x0, v0, x, v):
		return self.hardedge.bounceIfHits(x0, v0, x, v)


class CompactPolygon(object):

	def __init__(self, vertices):
		self.lineSegments = [geom.LineString((vertices[i], vertices[(i+1) % len(vertices)])) for i in range(len(vertices))]
		self.polygon = geom.Polygon(vertices)
		self.perimeterLength = sum(map(lambda seg: seg.length, self.lineSegments))

	def force(self, x, q):
		forces = map(lambda seg: q * forceDueToSegment(seg, x, seg.length/self.perimeterLength), self.lineSegments)
		return sum(forces)

	def contains(self, x):
		return self.polygon.contains(geom.Point(x))

	def plot(self, axes):
		w, z = self.polygon.exterior.xy
		axes.plot(w, z, color='g')
