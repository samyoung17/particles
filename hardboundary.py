import numpy as np
import linalgutil as la
import shapely.geometry as geom
import matplotlib.pyplot as plt

EPSILON = 0.01

def bounceIfHitsSegment(lineSegments, polygon, x0, v0, x, v):
	if not polygon.contains(geom.Point(x0)):
		raise ValueError('Particle has escaped boundary', x0)
	trajectory = geom.LineString([x0, x])
	xPrime, vPrime = x, v
	for seg in lineSegments:
		intersection = seg.intersection(trajectory)
		if not intersection.is_empty:
			a = np.array([intersection.x, intersection.y])
			c = np.array(seg.coords[1]) - np.array(seg.coords[0])
			n = la.normalVector(c)
			nHat = n / np.linalg.norm(n)
			xPrime = x - 2*np.dot(x-a, nHat)*nHat
			vPrime = v - 2*np.dot(v, nHat)*nHat
			if not polygon.contains(geom.Point(xPrime)):
				# Use recursion in case of multiple bounces
				# Move the intersection point slightly closer to the origin, to ensure that its inside the shape
				xPrime, vPrime = bounceIfHitsSegment(lineSegments, polygon, a * (1-EPSILON), v0, xPrime, vPrime)
	return xPrime,vPrime


class Circle(object):

	def __init__(self, r):
		self.r = float(r)
		self.circle = geom.Point(0,0).buffer(float(r)).boundary

	def bounceIfHits(self, x0, v0, x, v):
		xPrime, vPrime = x,v
		if np.linalg.norm(x) > self.r:
			# Shapely failing to find intersection of line and circle
			theta = la.angleBetweenTwoVectors(x, v)
			s, phi = la.cartToPolar(x)
			psi = np.pi + phi - (2 * theta)
			vPrime = la.polarToCart((np.linalg.norm(v), psi))
			dx = la.polarToCart((np.linalg.norm(x-x0), psi))
			xPrime = la.boundPoint(x0 + dx, self.r - EPSILON)
		return xPrime, vPrime

	def contains(self, x):
		return np.linalg.norm(x) < self.r

	def plot(self, axes):
		circle = plt.Circle((0,0), radius=self.r, color='g', fill=False)
		axes.add_patch(circle)


class CompactPolygon(object):

	def __init__(self, vertices):
		self.lineSegments = [geom.LineString((vertices[i], vertices[(i+1) % len(vertices)])) for i in range(len(vertices))]
		self.polygon = geom.Polygon(vertices)

	def bounceIfHits(self, x0, v0, x, v):
		return bounceIfHitsSegment(self.lineSegments, self.polygon, x0, v0, x, v)

	def testPlot(self, x0, x, xPrime, a, c, nHat):
		w,z = self.polygon.exterior.xy
		plt.plot(w,z)
		w,z = zip(x0, x)
		plt.plot(w,z)
		w,z = zip(a, a+nHat)
		plt.plot(w,z)
		plt.show()

	def contains(self, x):
		return self.polygon.contains(geom.Point(x))

	def plot(self, axes):
		w, z = self.polygon.exterior.xy
		axes.plot(w, z, color='g')
