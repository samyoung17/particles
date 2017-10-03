import particlesim
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import runtumble
import langevin
import metropolis
import brownianmotion

ITERATIONS = 20000
N = 200

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

def calculateCoverageFromFiles(algorithmProperties):
	print('Calculating coverage distance for {}...'.format(algorithmProperties['name']))
	data = particlesim.loadData(algorithmProperties['filePath'])
	covarageDistance = supMinDistanceOverTime(data)
	distanceTravelled = meanDistanceTravelled(data)
	return (algorithmProperties['name'], (distanceTravelled, covarageDistance))

def simulateAndCalculateCoverage(algorithmProperties):
	print('Running simulation for {}...'.format(algorithmProperties['name']))
	data = particlesim.simulate(ITERATIONS, N, algorithmProperties['moveFn'])
	print('Calculating coverage distance for {}...'.format(algorithmProperties['name']))
	covarageDistance = supMinDistanceOverTime(data)
	distanceTravelled = meanDistanceTravelled(data)
	return (algorithmProperties['name'], (distanceTravelled, covarageDistance))

def drawGraph(configs, xy):
	plots = []
	for config in configs:
		x, y = xy[config['name']]
		plot, = plt.plot(x, y, label=config['name'])
		plots.append(plot)
	plt.legend(handles=plots)
	plt.xlabel('Mean distance travelled')
	plt.ylabel('Coverage distance')
	plt.title('Maximum distance to from target to nearest particle')
	plt.savefig('data/coverage_s=02_rt_langevin_metropolis.png')
	plt.show()

def compareFromFiles(config):
	p = Pool(len(config))
	xy = dict(p.map(calculateCoverageFromFiles, config))
	drawGraph(config, xy)

def simulateAndCompare(config):
	p = Pool(len(config))
	xy = dict(p.map(simulateAndCalculateCoverage, config))
	drawGraph(config, xy)

def test():
	dataSets = [
		{
			'name': 'Langevin',
			'filePath': 'data/langevin n=10 iter=1000.pickle',
			'moveFn': langevin.moveParticles
		},
		{
			'name': 'Run and Tumble',
			'filePath': 'data/run tumble n=10 iter=1000.pickle',
			'moveFn': runtumble.moveParticles
		}
	]
	compareFromFiles(dataSets)

def main():
	dataSets = [
		{
			'name': 'Run and Tumble',
			'filePath': 'data/run tumble n=200 iter=20000.pickle',
			'moveFn': runtumble.moveParticles
		},
		{
			'name': 'Langevin',
			'filePath': 'data/langevin n=200 iter=20000.pickle',
			'moveFn': langevin.moveParticles
		},
		{
			'name': 'Metropolis',
			'filePath': 'data/metropolis n=200 iter=20000.pickle',
			'moveFn': metropolis.moveParticles
		},
		{
			'name': 'Brownian',
			'filePath': 'data/brownian n=200 iter=20000.pickle',
			'moveFn': brownianmotion.moveParticles
		}
	]
	simulateAndCompare(dataSets)
	# compareFromFiles(dataSets)

if __name__=='__main__':
	main()