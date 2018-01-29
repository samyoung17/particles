import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import signal
import pandas as pd
import scipy.special
import datetime
import pprint
import os
import sys

import particlesim
import datamodel
import parameters

EULER_GAMMA = 0.577215664901532

def maxNumberOfCouponsApprox(n):
	return n / np.real(scipy.special.lambertw(n))

def maxNumberOfCoupons(n):
	return (n - 0.5) / np.real(scipy.special.lambertw(np.exp(EULER_GAMMA) * (n - 0.5)))

H = 2 * np.pi / (3 * np.sqrt(3))
LOWER_BOUND = parameters.R_MAX / np.sqrt(parameters.N * H)
INDEPENDENT_LB = parameters.R_MAX / np.sqrt(maxNumberOfCoupons(parameters.N) * H)

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
	params = algorithmProps['params'] if algorithmProps.has_key('params') else {}
	data = particlesim.simulate(parameters.ITERATIONS, parameters.N,
								algorithmProps['moveFn'], algorithmProps['filePath'],
								algorithmProps['boundary'], params)
	dataSet = {
		'name': algorithmProps['name'],
		'data': data
	}
	return dataSet

def calculateCoverage(dataSet):
	covarageDistance = supMinDistanceOverTime(dataSet['data'])
	distanceTravelled = meanDistanceTravelled(dataSet['data'])
	return (dataSet['name'], (distanceTravelled, covarageDistance))

def drawGraph(df, names, filename):
	plots = []
	for name in names:
		plot, = plt.plot(df['time'], df[name + '.coverage'], label=name)
		plots.append(plot)
	plt.axhline(y=LOWER_BOUND, color='k')
	plt.axhline(y=INDEPENDENT_LB, color='k')
	plt.legend()
	plt.xlabel('Time (s)')
	plt.ylabel('Coverage distance (m)')
	plt.gca().set_ylim(bottom=0)
	plt.title('Maximum distance to the nearest agent')
	plt.savefig(filename)
	plt.show()

def drawGraphFromCsv(folder, cfg):
	df = pd.read_csv(folder + '/mean_coverage_distance.csv')
	names = map(lambda i: i['name'], cfg)
	outfilename = folder + '/test.jpg'
	drawGraph(df, names, outfilename)

def createDataFrame(t, distanceAndCoverage):
	df = pd.DataFrame()
	names = distanceAndCoverage.keys()
	df['time'] = t
	for name in names:
		distance, coverage = distanceAndCoverage[name]
		distanceColName = name + '.distance'
		coverageColName = name + '.coverage'
		df[distanceColName] = distance
		df[coverageColName] = coverage
	return df

def saveResults(folder, config, meanDistanceAndCoverage):
	names = map(lambda d: d['name'], config)
	t = np.arange(0, parameters.ITERATIONS * particlesim.TIMESTEP, particlesim.TIMESTEP)
	df = createDataFrame(t, meanDistanceAndCoverage)
	df.to_csv(folder + '/mean_coverage_distance.csv')
	out = open(folder + '/config.txt', 'w')
	out.write('ITERATIONS={} N={}\n'
			  .format(parameters.ITERATIONS, parameters.N))
	out.write(pprint.pformat(config))
	out.close()
	drawGraph(df, names, folder + '/mean_coverage_distance.jpg')

def saveTrialResults(folder, distanceAndCoverage, trialNumber):
	t = np.arange(0, parameters.ITERATIONS * particlesim.TIMESTEP, particlesim.TIMESTEP)
	df = createDataFrame(t, distanceAndCoverage)
	df.to_csv(folder + '/trial' + str(trialNumber+1) + '.csv')

def multipleTrials(config, numberOfTrials):
	names = map(lambda d: d['name'], config)
	pool = Pool(len(config))
	coverageData = np.ndarray((numberOfTrials, len(config), parameters.ITERATIONS))
	distanceData = np.ndarray((numberOfTrials, len(config), parameters.ITERATIONS))
	folder = 'results/coverage_comparison_' + str(datetime.datetime.now())[:19]
	os.mkdir(folder)
	for i in range(numberOfTrials):
		print('Trial ' + str(i + 1) + '/' + str(numberOfTrials))
		print('Running simulations...')
		dataSets = pool.map_async(runSimulations, config).get(TIMEOUT)
		print('\nCalculating coverage distances...')
		distanceAndCoverage = dict(pool.map_async(calculateCoverage, dataSets).get(TIMEOUT))
		saveTrialResults(folder, distanceAndCoverage, i)
		for j, name in enumerate(names):
			distanceData[i,j] = distanceAndCoverage[name][0]
			coverageData[i,j] = distanceAndCoverage[name][1]
		print('\n')
	meanCoverageData = np.mean(coverageData, axis=0)
	meanDistanceData = np.mean(distanceData, axis=0)
	meanDistanceAndCoverage = dict([(name, (meanDistanceData[j], meanCoverageData[j])) for j,name in enumerate(names)])
	saveResults(folder, config, meanDistanceAndCoverage)

if __name__=='__main__':
	if not len(sys.argv) == 3:
		raise ValueError('Arguments should be <config>, <number_of_trials>')
	python, configName, numberOfTrials = sys.argv
	multipleTrials(parameters.CONFIG[configName], int(numberOfTrials))