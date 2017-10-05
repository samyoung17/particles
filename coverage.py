import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import signal
import os
import pandas as pd

import particlesim
import runtumble
import langevin
import metropolis
import brownianmotion
import datamodel

ITERATIONS = 20000
N = 200

C = np.sqrt(8 * np.pi/ (3 * np.sqrt(3)))
LOWER_BOUND = particlesim.R_MAX / np.sqrt(N)
UPPER_BOUND = C * particlesim.R_MAX / np.sqrt(N / np.log(N))

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

def drawGraph(df, algoNames):
	plots = []
	for name in algoNames:
		plot, = plt.plot(df[name + '.distance'], df[name + '.coverage'], label=name)
		plots.append(plot)
	plt.axhline(y=LOWER_BOUND, color='k')
	plt.axhline(y=UPPER_BOUND, color='k')
	plt.legend(handles=plots)
	plt.xlabel('Mean distance travelled')
	plt.ylabel('Coverage distance')
	plt.title('Maximum distance to from target to nearest particle')
	plt.savefig('data/coverage graph N={} ITER={}.png'.format(N, ITERATIONS))
	plt.show()

def createDataFrame(dataSets, distanceAndCoverage):
	df = pd.DataFrame()
	df['time'] = dataSets[0]['data'].t
	for dataSet in dataSets:
		distance, coverage = distanceAndCoverage[dataSet['name']]
		distanceColName = dataSet['name'] + '.distance'
		coverageColName = dataSet['name'] + '.coverage'
		df[distanceColName] = distance
		df[coverageColName] = coverage
	return df

def coverageComparison(dataSets, pool):
	distanceAndCoverage = dict(pool.map_async(calculateCoverage, dataSets).get(TIMEOUT))
	df = createDataFrame(dataSets, distanceAndCoverage)
	df.to_csv('data/coverage N={} ITER={}.csv'.format(N, ITERATIONS))
	names = map(lambda d: d['name'], dataSets)
	drawGraph(df, names)

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
	pool = Pool(len(config))
	if all(map(lambda c: os.path.isdir(c['filePath']), config)):
		print('Loading data...')
		dataSets = pool.map_async(loadDataFromFile, config).get(TIMEOUT)
	else:
		print('Running simulations...')
		dataSets = pool.map_async(runSimulations, config).get(TIMEOUT)
	print('\nCalculating coverage distances...')
	coverageComparison(dataSets, pool)

if __name__=='__main__':
	main()