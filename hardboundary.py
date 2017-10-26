import numpy as np
import linalgutil as la
import shapely.geometry as geom
import matplotlib.pyplot as plt

EPSILON = 0.00000000000000001

def bounceIfHitsSegment(lineSegments, x0, v0, x, v):
	trajectory = geom.LineString([x0, x])
	xPrime, vPrime = x, v
	for seg in lineSegments:
		intersection = seg.intersection(trajectory)
		if not intersection.is_empty:
			a = np.array([intersection.x, intersection.y])
			c = np.array(seg.coords[1]) - np.array(seg.coords[0])
			n = np.array((c[1], c[0]))
			nHat = n / np.linalg.norm(n)
			xPrime = x - 2*np.dot(x-a, nHat)*nHat
			vPrime = v - 2*np.dot(v, nHat)*nHat
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


class Square(object):

	def __init__(self, l):
		self.l = l
		self.lineSegments = [
				geom.LineString([(-l/2, -l/2), (-l/2, l/2)]),
				geom.LineString([(-l/2, l/2), (l/2, l/2)]),
				geom.LineString([(l/2, l/2), (l/2, -l/2)]),
				geom.LineString([(l/2, -l/2), (-l/2, -l/2)])
			]
		self.polygon = geom.Polygon([(-l/2, -l/2), (-l/2, l/2), (l/2, l/2), (l/2, -l/2)])

	def bounceIfHits(self, x0, v0, x, v):
		return bounceIfHitsSegment(self.lineSegments, x0, v0, x, v)

	def contains(self, x):
		return self.polygon.contains(geom.Point(x))

	def plot(self, axes):
		rectangle = plt.Rectangle((-self.l/2,-self.l/2), self.l, self.l, color='g', fill=False)
		axes.add_patch(rectangle)


class Rectangle(object):

	def __init__(self, l, h):
		self.l = l
		self.h = h
		self.lineSegments = [
				geom.LineString([(-l/2, -h/2), (-l/2, h/2)]),
				geom.LineString([(-l/2, h/2), (l/2, h/2)]),
				geom.LineString([(l/2, h/2), (l/2, -h/2)]),
				geom.LineString([(l/2, -h/2), (-l/2, -h/2)])
			]
		self.polygon = geom.Polygon([(-l/2, -h/2), (-l/2, h/2), (l/2, h/2), (l/2, -h/2)])

	def bounceIfHits(self, x0, v0, x, v):
		return bounceIfHitsSegment(self.lineSegments, x0, v0, x, v)

	def contains(self, x):
		return self.polygon.contains(geom.Point(x))

	def plot(self, axes):
		rectangle = plt.Rectangle((-self.l/2,-self.h/2), self.l, self.h, color='g', fill=False)
		axes.add_patch(rectangle)


class WierdQuadrilateral(object):

	def __init__(self):
		a = (-10.0,-10.0)
		b = (-2.0, 0.0)
		c = (7.0, 5.0)
		d = (2.0, -3.0)
		self.lineSegments = [
				geom.LineString((a,b)),
				geom.LineString((b,c)),
				geom.LineString((c,d)),
				geom.LineString((d,a))
			]
		self.polygon = geom.Polygon([a,b,c,d])

	def bounceIfHits(self, x0, v0, x, v):
		trajectory = geom.LineString([x0, x])
		xPrime, vPrime = x, v
		for seg in self.lineSegments:
			intersection = seg.intersection(trajectory)
			if not intersection.is_empty:
				a = np.array([intersection.x, intersection.y])
				c = np.array(seg.coords[1]) - np.array(seg.coords[0])
				n = np.array((c[1], c[0]))
				nHat = n / np.linalg.norm(n)
				xPrime = x - 2*np.dot(x-a, nHat)*nHat
				vPrime = v - 2*np.dot(v, nHat)*nHat
			if not self.contains(xPrime):
				self.testPlot(a,n,x,x0, seg)
		return xPrime,vPrime

	def testPlot(self, a, n, x, x0, seg):
		return

	def contains(self, x):
		return self.polygon.contains(geom.Point(x))

	def plot(self, axes):
		return
