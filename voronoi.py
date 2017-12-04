import numpy as np
import particlesim
import scipy.spatial
import matplotlib.pyplot as plt
import linalgutil as la
import voronoiboundary

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

def findRegionVertices(voronoi, p1, ridges, rMax, boundary):
	regionVertexIndices = voronoi.regions[voronoi.point_region[p1]]
	originalVertices = map(lambda i: voronoi.vertices[i], filter(lambda v1: v1>=0, regionVertexIndices))
	boundaryVertices = boundary.findBoundaryVertices(p1, ridges, voronoi)
	vertices = np.array(map(lambda v: la.boundPoint(v, rMax), originalVertices + boundaryVertices))
	return vertices

def printVoronoi(cells, voronoi):
	centroids = np.array(map(lambda cell: cell.centroid, filter(lambda cell: cell.centroid is not None, cells)))
	scipy.spatial.voronoi_plot_2d(voronoi)
	plt.scatter(centroids[:, 0], centroids[:, 1], c='r')
	plt.show()

def createVornoiCells(points, rMax, boundary):
	vrnoi = scipy.spatial.Voronoi(points)
	cells = []
	allRidges = createRidgeDict(vrnoi)
	for p1 in range(len(vrnoi.points)):
		regionVertices = findRegionVertices(vrnoi, p1, allRidges[p1], rMax, boundary)
		centroid = calculateCentroid(regionVertices)
		cells.append(VoronoiCell(vrnoi.points[p1], regionVertices, centroid))
	# printVoronoi(cells, voronoi)
	return cells

def targetVelocity(cell):
	return - K_PROP * (cell.point - cell.centroid)

def moveParticles(particles, t, boundary, params):
	rMax = params['rMax']
	xx = np.array(map(lambda p: p.x, particles))
	cells = createVornoiCells(xx, rMax, boundary)
	velocities = map(targetVelocity, cells)
	for i in range(len(particles)):
		v = velocities[i]
		x = particles[i].x + v * t
		particles[i].v = la.boundPoint(v, S_MAX)
		particles[i].x = la.boundPoint(x, rMax)

def main():
	n, iterations = 50, 1000
	rMax = 10.0
	folder = 'data/voronoi n={} iter={}'.format(n, iterations)
	boundary = voronoiboundary.Circle(rMax)
	data = particlesim.simulate(iterations, n, moveParticles, folder, boundary, {'rMax': rMax})
	particlesim.motionAnimation(data, 15, boundary)

if __name__=='__main__':
	main()