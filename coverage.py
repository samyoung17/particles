import particlesim
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool



def distanceToNearestTarget(y, particles):
	return np.min(map(lambda x: np.linalg.norm(x - y), particles))

def supMinDistance(particles, targets):
	distances = map(lambda y: distanceToNearestTarget(y, particles), targets)
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

def meanDistanceTravelled(data):
	s = np.linalg.norm(data.v, axis = 2)
	sbar = np.average(s, axis = 1)
	dx = sbar * particlesim.TIMESTEP
	return np.cumsum(dx)

def calculateDistanceAndCoverage(dataSet):
	print('\nCalculating coverage distance for {}...'.format(dataSet['label']))
	data = particlesim.loadData(dataSet['filePath'])
	covarageDistance = supMinDistanceOverTime(data)
	distanceTravelled = meanDistanceTravelled(data)
	return (dataSet['label'], (distanceTravelled, covarageDistance))

def compareFromFiles(dataSets):
	p = Pool(len(dataSets))
	xy = dict(p.map(calculateDistanceAndCoverage, dataSets))
	plots = []
	for d in dataSets:
		x, y = xy[d['label']]
		plot, = plt.plot(x, y, label = d['label'])
		plots.append(plot)
	plt.legend(handles=plots)
	plt.xlabel('Mean distance travelled')
	plt.ylabel('Coverage distance')
	plt.title('Maximum distance to from target to nearest particle')
	plt.savefig('data/coverage_s=02_rt_langevin_metropolis.png')
	plt.show()

def test():
	dataSets = [
		{
			'label': 'Langevin',
			'filePath': 'data/langevin n=10 iter=1000.pickle'
		},
		{
			'label': 'Run and Tumble',
			'filePath': 'data/run tumble n=10 iter=1000.pickle'
		}
	]
	compareFromFiles(dataSets)

def main():
	dataSets = [
		{
			'label': 'Run and Tumble',
			'filePath': 'data/run tumble n=200 iter=20000.pickle'
		},
		{
			'label': 'Langevin',
			'filePath': 'data/langevin n=200 iter=20000.pickle'
		},
		{
			'label': 'Metropolis',
			'filePath': 'data/metropolis n=200 iter=20000.pickle'
		},
		{
			'label': 'Brownian',
			'filePath': 'data/brownian n=200 iter=20000.pickle'
		}
	]
	compareFromFiles(dataSets)

if __name__=='__main__':
	main()