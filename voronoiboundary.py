import linalgutil as la
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry as geom

BIG_R = 100.0

def testPlot(v, x1, x2, endpoint, rMax):
	axes = plt.gca()
	padding = 1.5
	axes.set_xlim([-rMax * padding, rMax * padding])
	axes.set_ylim([-rMax * padding, rMax * padding])
	circle = plt.Circle((0, 0), radius=rMax, color='g', fill=False)
	axes.add_patch(circle)
	axes.scatter([endpoint[0]], [endpoint[1]], c='g')
	axes.scatter([v[0]], [v[1]], c = 'b')
	axes.scatter([x1[0], x2[0]], [x1[1], x2[1]], c='r')
	plt.show()

def findRidgeUnit(v, midpoint):
	ridgeUnit = (midpoint - v) / np.linalg.norm(midpoint - v)
	if np.dot(midpoint, ridgeUnit) < 0:
		ridgeUnit = -ridgeUnit
	return ridgeUnit

def findIntersectionWithCircle(v, midpoint, rMax):
	'''
	We use the geometry of a triangle with points (origin, midpoint, new boundary vertex)
	to find the vector to the new boundary vertex in the voronoi diagram.
	create a unit vector pointing from the vertex to the nearest boundary through the midpoint of x1 and x2
		alpha is the angle between the midpoint vector and the vector from the midpoint to the new boundary vertex
		beta is the angle between the midpoint/boundary vertex vector and the boundary vertex vector
		gamma is the angle between the boundary vertex vector and the midpoint vector
	'''
	ridgeUnit = findRidgeUnit(v, midpoint)
	r, theta = la.cartToPolar(v)
	s, phi = la.cartToPolar(ridgeUnit)
	alpha = np.pi - theta + phi
	b = np.linalg.norm(midpoint)
	a = rMax
	# Apply the sine rule once to find beta
	beta = np.arcsin(b * np.sin(alpha) / a)
	gamma = np.pi - alpha - beta
	# Apply the sine rule a second time to find the length of the midpoint/boundary vertex vector
	c = np.sin(gamma) / np.sin(beta) * b
	# Add the midpiont/boundary vertex vector to the midpoint vector to yield the new vertex vector
	intersectingPoint = la.polarToCart((c, phi)) + midpoint
	return intersectingPoint

def findIntersectionWithPolygon(v, midpoint, rMax, segments):
	ridgeUnit = findRidgeUnit(v, midpoint)
	endpoint = v + rMax * ridgeUnit
	trajectory = geom.LineString([v, endpoint])
	for seg in segments:
		intersection = seg.intersection(trajectory)
		if not intersection.is_empty:
			return np.array([intersection.x, intersection.y])
	raise ValueError('No intersection found')

def identifyCornerPoints(points, corners):
	Dxy = la.distanceMatrix(points, corners)
	ii = np.argmin(Dxy, axis=0)
	return dict(zip(ii, corners))

class Circle(object):

	def __init__(self, rMax):
		self.rMax = float(rMax)
		self.circle = geom.Point(0,0).buffer(float(rMax)).boundary

	def findBoundaryVertices(self, p1, ridges, voronoi):
		semiInfiniteRidges = filter(lambda (p2, v1, v2): v1 == -1 or v2 == -1, ridges)
		boundaryVertices = []
		for ridge in semiInfiniteRidges:
			p2, v1, v2 = ridge
			vertex = la.boundPoint(voronoi.vertices[v1 if v1 >= 0 else v2], self.rMax)
			midpoint = (voronoi.points[p1] + voronoi.points[p2]) / 2
			endpoint = findIntersectionWithCircle(vertex, midpoint, self.rMax)
			# testPlot(vertex, voronoi.points[p1], voronoi.points[p2], endpoint, self.rMax)
			boundaryVertices.append(endpoint)
		return boundaryVertices

	def contains(self, x):
		return np.linalg.norm(x) < self.rMax

	def boundPoint(self, x):
		return la.boundPoint(x, self.rMax)

	def plot(self, axes):
		circle = plt.Circle((0,0), radius=self.rMax, color='g', fill=False)
		axes.add_patch(circle)


class CompactPolygon(object):

	def __init__(self, corners):
		self.lineSegments = [geom.LineString((corners[i], corners[(i + 1) % len(corners)])) for i in range(len(corners))]
		self.polygon = geom.Polygon(corners)
		self.corners = corners

	def findBoundaryVertices(self, p1, ridges, voronoi):
		semiInfiniteRidges = filter(lambda (p2, v1, v2): v1 == -1 or v2 == -1, ridges)
		boundaryVertices = []
		cornerPoints = identifyCornerPoints(voronoi.points, self.corners)
		if len(semiInfiniteRidges) == 2:
			edgeVertex1 = self.findBoundaryVertex(p1, semiInfiniteRidges[0], voronoi)
			boundaryVertices.append(edgeVertex1)
			if cornerPoints.has_key(p1):
				boundaryVertices.append(cornerPoints[p1])
			edgeVertex2 = self.findBoundaryVertex(p1, semiInfiniteRidges[1], voronoi)
			boundaryVertices.append(edgeVertex2)
		return boundaryVertices

	def findBoundaryVertex(self, p1, ridge, voronoi):
		p2, v1, v2 = ridge
		vertex = self.boundPoint(voronoi.vertices[v1 if v1 >= 0 else v2])
		midpoint = (voronoi.points[p1] + voronoi.points[p2]) / 2
		endpoint = findIntersectionWithPolygon(vertex, midpoint, BIG_R, self.lineSegments)
		return endpoint

	def contains(self, x):
		return self.polygon.contains(geom.Point(x))

	def boundPoint(self, x):
		if not self.contains(x):
			return findIntersectionWithPolygon(np.array([0,0]), x, BIG_R, self.lineSegments) * 0.95
		else:
			return x

	def plot(self, axes):
		w, z = self.polygon.exterior.xy
		axes.plot(w, z, color='g')
