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
import time

import particlesim
import datamodel
import coverageconfig
import linalgutil

EULER_GAMMA = 0.577215664901532

def maxNumberOfCouponsApprox(n):
	return n / np.real(scipy.special.lambertw(n))

def maxNumberOfCoupons(n):
	return (n - 0.5) / np.real(scipy.special.lambertw(np.exp(EULER_GAMMA) * (n - 0.5)))

H = np.sqrt(2 * np.pi / (3 * np.sqrt(3)))
LOWER_BOUND = coverageconfig.R_MAX * H / np.sqrt(coverageconfig.N)
INDEPENDENT_LB = coverageconfig.R_MAX * H / np.sqrt(maxNumberOfCoupons(coverageconfig.N))

D_OPTIMAL_AGENTS = LOWER_BOUND * np.sqrt(2)

TIMEOUT = 99999999999999999

def init_worker():
	signal.signal(signal.SIGINT, signal.SIG_IGN)


def supMinDistance(particles, targets):
	distances = linalgutil.distanceMatrix(particles, targets)
	# Take minimum of distance along 0, the particle dimension, then maximum along target dimension
	return np.max(np.min(distances, axis=0))

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
	params = algorithmProps['params'] if 'params' in algorithmProps else {}
	data = particlesim.simulate(coverageconfig.ITERATIONS, coverageconfig.N,
								algorithmProps['moveFn'], algorithmProps['filePath'],
								algorithmProps['boundary'], params)
	dataSet = {
		'name': algorithmProps['name'],
		'data': data
	}
	return dataSet

def calculateRadialDistance(data):
	r = np.linalg.norm(data.x, axis=2)
	rbar = r.mean(axis=1)
	return rbar

def calculateAverageSpeed(data):
	s = np.linalg.norm(data.v, axis=2)
	sbar = s.mean(axis=1)
	return sbar

def calculateSummaryStatistics(dataSet):
	covarageDistance = supMinDistanceOverTime(dataSet['data'])
	speed = calculateAverageSpeed(dataSet['data'])
	distanceTravelled = meanDistanceTravelled(dataSet['data'])
	radialDistance = calculateRadialDistance(dataSet['data'])
	return dataSet['name'], (distanceTravelled, covarageDistance, speed, radialDistance)

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
	outfilename = folder + '/test.png'
	drawGraph(df, names, outfilename)

def createDataFrame(t, summaryStatistics):
	df = pd.DataFrame()
	configuration_names = summaryStatistics.keys()
	df['time'] = t
	for name in configuration_names:
		distance, coverage, speed, radialDistance = summaryStatistics[name]
		df[(name + '.distance')] = distance
		df[(name + '.coverage')] = coverage
		df[(name + '.radialDistance')] = radialDistance
		df[(name + '.speed')] = speed
	return df

def saveResults(folder, config, all_trials_df):
	names = list(map(lambda d: d['name'], config))
	df = all_trials_df.groupby(['time']).mean().reset_index()
	df.to_csv(folder + '/mean_coverage_distance.csv')
	out = open(folder + '/config.txt', 'w')
	out.write('ITERATIONS={} N={}\n'
			  .format(coverageconfig.ITERATIONS, coverageconfig.N))
	out.write(pprint.pformat(config))
	out.close()
	drawGraph(df, names, folder + '/mean_coverage_distance.png')


def multipleTrials(config, numberOfTrials):
	pool = Pool(len(config))
	folder = 'results/coverage_comparison_' + str(datetime.datetime.now())[:19]
	os.mkdir(folder)
	trial_summary_dfs = []
	for i in range(numberOfTrials):
		print('Trial ' + str(i + 1) + '/' + str(numberOfTrials))
		print('Running simulations...')
		sim_start = time.time()
		dataSets = pool.map(runSimulations, config)
		sim_end = time.time()
		print('\nCalculating coverage distances...')
		summaryStatistics = dict(pool.map(calculateSummaryStatistics, dataSets))
		coverage_end = time.time()
		print(f'\nSim_time: {sim_end - sim_start:.2f}s, coverage_calc_time: {coverage_end - sim_end:.2f}s')
		t = np.arange(0, coverageconfig.ITERATIONS * particlesim.TIMESTEP, particlesim.TIMESTEP)
		df = createDataFrame(t, summaryStatistics)
		df['trialNumber'] = i + 1
		trial_summary_dfs.append(df)
		df.to_csv(folder + '/trial' + str(i + 1) + '.csv')
		print('\n')
	all_trials_df = pd.concat(trial_summary_dfs)
	saveResults(folder, config, all_trials_df)

if __name__=='__main__':
	if not len(sys.argv) == 3:
		raise ValueError('Arguments should be <config>, <number_of_trials>')
	python, configName, numberOfTrials = sys.argv
	if not os.path.isdir('results'):
		os.mkdir('results')
	if not os.path.isdir('data'):
		os.mkdir('data')
	multipleTrials(coverageconfig.CONFIG[configName], int(numberOfTrials))