import numpy as np
import particlesim
import scipy.spatial
import matplotlib.pyplot as plt
import linalgutil as la

K_PROP = 1
S_MAX = 0.3

class VoronoiCell:
	def __init__(self, point, vertices=None, centroid=None):
		self.point = point
		self.vertices = vertices
		self.centroid = centroid

def calculateCentroid(polygonVertices):
	x = polygonVertices[:,0]
	y = polygonVertices[:,1]
	n = len(polygonVertices)
	Aterms = [x[i] * y[i+1] - x[i+1] * y[i] for i in range(n - 1)]
	Aterms.append(x[n-1] * y[0] - x[0] * y[n-1])
	A = 0.5 * np.sum(Aterms)
	Cxterms = [(x[i] + x[i+1]) * (x[i] * y[i+1] - x[i+1] * y[i]) for i in range(n - 1)]
	Cxterms.append((x[n-1] + x[0]) * (x[n-1] * y[0] - x[0] * y[n-1]))
	Cx = 1 / (6 * A) * np.sum(Cxterms)
	Cyterms = [(y[i] + y[i+1]) * (x[i] * y[i+1] - x[i+1] * y[i]) for i in range(n - 1)]
	Cyterms.append((y[n-1] + y[0]) * (x[n-1] * y[0] - x[0] * y[n-1]))
	Cy = 1 / (6 * A) * np.sum(Cyterms)
	return (Cx, Cy)

def createRidgeDict(voronoi):
	all_ridges = {}
	for (p1, p2), (v1, v2) in zip(voronoi.ridge_points, voronoi.ridge_vertices):
		all_ridges.setdefault(p1, []).append((p2, v1, v2))
		all_ridges.setdefault(p2, []).append((p1, v1, v2))
	return  all_ridges

def findIntersectionWithCircle(v, midpoint):
	'''
	We use the geometry of a triangle with points (origin, midpoint, new boundary vertex)
	to find the vector to the new boundary vertex in the voronoi diagram.
	create a unit vector pointing from the vertex to the nearest boundary through the midpoint of x1 and x2
		alpha is the angle between the midpoint vector and the vector from the midpoint to the new boundary vertex
		beta is the angle between the midpoint/boundary vertex vector and the boundary vertex vector
		gamma is the angle between the boundary vertex vector and the midpoint vector
	'''
	ridgeUnit = (midpoint - v) / np.linalg.norm(midpoint - v)
	if np.dot(midpoint, ridgeUnit) < 0:
		ridgeUnit = -ridgeUnit
	r, theta = la.cartToPolar(v)
	s, phi = la.cartToPolar(ridgeUnit)
	alpha = np.pi - theta + phi
	b = np.linalg.norm(midpoint)
	a = particlesim.R_MAX
	# Apply the sine rule once to find beta
	beta = np.arcsin(b * np.sin(alpha) / a)
	gamma = np.pi - alpha - beta
	# Apply the sine rule a second time to find the length of the midpoint/boundary vertex vector
	c = np.sin(gamma) / np.sin(beta) * b
	# Add the midpiont/boundary vertex vector to the midpoint vector to yield the new vertex vector
	intersectingPoint = la.polarToCart((c, phi)) + midpoint
	return intersectingPoint

def findRegionVertices(voronoi, p1, ridges):
	regionVertexIndices = voronoi.regions[voronoi.point_region[p1]]
	originalVertices = map(lambda i: voronoi.vertices[i], filter(lambda v1: v1>=0, regionVertexIndices))
	boundaryVertices = findBoundaryVertices(p1, ridges, voronoi)
	vertices = np.array(map(lambda v: la.boundPoint(v, particlesim.R_MAX), originalVertices + boundaryVertices))
	return vertices

def findBoundaryVertices(p1, ridges, voronoi):
	semiInfiniteRidges = filter(lambda (p2, v1, v2): v1 == -1 or v2 == -1, ridges)
	boundaryVertices = []
	for ridge in semiInfiniteRidges:
		p2, v1, v2 = ridge
		vertex = la.boundPoint(voronoi.vertices[v1 if v1 >= 0 else v2], particlesim.R_MAX)
		midpoint = (voronoi.points[p1] + voronoi.points[p2]) / 2
		endpoint = findIntersectionWithCircle(vertex, midpoint)
		# testPlot(vertex, voronoi.points[p1], voronoi.points[p2], endpoint)
		boundaryVertices.append(endpoint)
	return boundaryVertices

def testPlot(v, x1, x2, endpoint):
	axes = plt.gca()
	padding = 1.5
	axes.set_xlim([-particlesim.R_MAX * padding, particlesim.R_MAX * padding])
	axes.set_ylim([-particlesim.R_MAX * padding, particlesim.R_MAX * padding])
	circle = plt.Circle((0, 0), radius=particlesim.R_MAX, color='g', fill=False)
	axes.add_patch(circle)
	axes.scatter([endpoint[0]], [endpoint[1]], c='g')
	axes.scatter([v[0]], [v[1]], c = 'b')
	axes.scatter([x1[0], x2[0]], [x1[1], x2[1]], c='r')
	plt.show()

def printVoronoi(cells, voronoi):
	centroids = np.array(map(lambda cell: cell.centroid, filter(lambda cell: cell.centroid is not None, cells)))
	scipy.spatial.voronoi_plot_2d(voronoi)
	plt.scatter(centroids[:, 0], centroids[:, 1], c='r')
	plt.show()

def createVornoiCells(points):
	voronoi = scipy.spatial.Voronoi(points)
	cells = []
	allRidges = createRidgeDict(voronoi)
	for p1 in range(len(voronoi.points)):
		regionVertices = findRegionVertices(voronoi, p1, allRidges[p1])
		centroid = calculateCentroid(regionVertices)
		cells.append(VoronoiCell(voronoi.points[p1], regionVertices, centroid))
	# printVoronoi(cells, voronoi)
	return cells

def targetVelocity(cell):
	return - K_PROP * (cell.point - cell.centroid)

def moveParticles(particles, t, boundary):
	xx = np.array(map(lambda p: p.x, particles))
	cells = createVornoiCells(xx)
	velocities = map(targetVelocity, cells)
	for i in range(len(particles)):
		v = velocities[i]
		x = particles[i].x + v * t
		particles[i].v = la.boundPoint(v, S_MAX)
		particles[i].x = la.boundPoint(x, particlesim.R_MAX)

def main():
	n, iterations = 50, 1000
	folder = 'data/voronoi n={} iter={}'.format(n, iterations)
	data = particlesim.simulate(iterations, n, moveParticles, folder)
	particlesim.motionAnimation(data, 15)

if __name__=='__main__':
	main()