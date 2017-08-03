import particlesim
import numpy as np
import matplotlib.pyplot as plt

ITERATIONS = 10000
N = 50

def nearestNeighbour(y, particles):
	return np.min(map(lambda x: np.linalg.norm(x - y), particles))

def supMinDistance(particles, targets):
	distances = map(lambda y: nearestNeighbour(y, particles), targets)
	return np.max(distances)

def supMinDistanceOverTime(data):
	d = np.zeros((data.iterations))
	for i in range(data.iterations):
		particlesim.logIteration(i, data.iterations)
		d[i] = supMinDistance(data.x[i], data.y[i])
	return d

def lowerBound(iterations, n, rMax):
	bound = rMax / np.sqrt(n)
	return bound * np.ones((iterations))

def compareFromFiles(dataSets):
	plots = []
	for d in dataSets:
		print('Calculating Distances for {}...'.format(d['label']))
		data = particlesim.loadData(d['filePath'])
		distances = supMinDistanceOverTime(data)
		plot, = plt.plot(distances, label = d['label'])
		plots.append(plot)
	plt.legend(handles=plots)
	plt.title('Maximum distance to from target to nearest particle')
	plt.show()

if __name__=='__main__':
	dataSets = [
		{
			'label': 'RT Fixed',
			'filePath': 'data/run tumble n=200 iter=5000.pickle'
		},
		{
			'label': 'RT Avoident',
			'filePath': 'data/run tumble variable n=200 iter=5000.pickle'
		},
		{
			'label': 'Metropolis',
			'filePath': 'data/metropolis n=200 iter=5000.pickle'
		}
	]
	compareFromFiles(dataSets)