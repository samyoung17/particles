import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import signal

import particlesim
import runtumble
import langevin
import metropolis
import brownianmotion
import datamodel

ITERATIONS = 20000
N = 200

TIMEOUT = 99999999999999999

def init_worker():
	signal.signal(signal.SIGINT, signal.SIG_IGN)

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

def loadDataFromFile(algorithmProperties):
	data = datamodel.Data(algorithmProperties['filePath'], 'r')
	dataSet = {
		'name': algorithmProperties['name'],
		'data': data
	}
	return dataSet

def runSimulations(algorithmProps):
	data = particlesim.simulate(ITERATIONS, N, algorithmProps['moveFn'], algorithmProps['filePath'])
	dataSet = {
		'name': algorithmProps['name'],
		'data': data
	}
	return dataSet

def calculateCoverage(dataSet):
	covarageDistance = supMinDistanceOverTime(dataSet['data'])
	distanceTravelled = meanDistanceTravelled(dataSet['data'])
	return (dataSet['name'], (distanceTravelled, covarageDistance))

def drawGraph(dataSet, xy):
	plots = []
	for algorithmProperties in dataSet:
		x, y = xy[algorithmProperties['name']]
		plot, = plt.plot(x, y, label=algorithmProperties['name'])
		plots.append(plot)
	plt.legend(handles=plots)
	plt.xlabel('Mean distance travelled')
	plt.ylabel('Coverage distance')
	plt.title('Maximum distance to from target to nearest particle')
	plt.savefig('data/coverage_s=02_rt_langevin_metropolis.png')
	plt.show()

def compareFromFiles(config):
	pool = Pool(len(config), init_worker)
	print('Loading data...')
	dataSets = pool.map_async(loadDataFromFile, config).get(TIMEOUT)
	print('Calculating coverage distances...')
	xy = dict(pool.map_async(calculateCoverage, dataSets).get(TIMEOUT))
	drawGraph(config, xy)

def simulateAndCompare(config):
	pool = Pool(len(config))
	print('Running simulations...')
	dataSets = pool.map_async(runSimulations, config).get(TIMEOUT)
	print('\nCalculating coverage distances...')
	xy = dict(pool.map_async(calculateCoverage, dataSets).get(TIMEOUT))
	drawGraph(config, xy)

def test():
	config = [
		{
			'name': 'Langevin',
			'filePath': 'data/langevin n={} iter={}'.format(N, ITERATIONS),
			'moveFn': langevin.moveParticles
		},
		{
			'name': 'Run and Tumble',
			'filePath': 'data/run tumble n={} iter={}'.format(N, ITERATIONS),
			'moveFn': runtumble.moveParticles
		}
	]
	compareFromFiles(config)

def main():
	config = [
		{
			'name': 'Run and Tumble',
			'filePath': 'data/run tumble n={} iter={}'.format(N, ITERATIONS),
			'moveFn': runtumble.moveParticles
		},
		{
			'name': 'Langevin',
			'filePath': 'data/langevin n={} iter={}'.format(N, ITERATIONS),
			'moveFn': langevin.moveParticles
		},
		{
			'name': 'Metropolis',
			'filePath': 'data/metropolis n={} iter={}'.format(N, ITERATIONS),
			'moveFn': metropolis.moveParticles
		},
		{
			'name': 'Brownian',
			'filePath': 'data/brownian n={} iter={}'.format(N, ITERATIONS),
			'moveFn': brownianmotion.moveParticles
		}
	]
	simulateAndCompare(config)
	# compareFromFiles(dataSets)

if __name__=='__main__':
	main()