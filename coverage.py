import particlesim
import brownianmotion
import forcedistribution
import runtumble
import numpy as np
import matplotlib.pyplot as plt

ITERATIONS = 2000
N = 50

def nearestNeighbour(y, particles):
	return np.min(map(lambda x: np.linalg.norm(x - y), particles))

def avgMinDistance(particles, targets):
	distances = map(lambda y: nearestNeighbour(y, particles), targets)
	return np.mean(distances)

def avgMinDistanceOverTime(data):
	d = np.zeros((data.iterations))
	for i in range(data.iterations):
		d[i] = avgMinDistance(data.x[i], data.y[i])
	return d

def main():
	print('Simulating Brownian Motion')
	bmData = particlesim.simulate(ITERATIONS, N, brownianmotion.moveParticles)
	print('Simulating Force Distribution')
	fdData = particlesim.simulate(ITERATIONS, N, forcedistribution.moveParticles)
	print('Simulating Run and Tumble')
	rtData = particlesim.simulate(ITERATIONS, N, runtumble.moveParticles)
	print('Calculating Avg Min Distances Brownian Motion')
	bmDistances = avgMinDistanceOverTime(bmData)
	print('Calculating Avg Min Distances Force Distribution')
	fdDistances = avgMinDistanceOverTime(fdData)
	print('Calculating Avg Min Distances Run And Tumble')
	rtDistances = avgMinDistanceOverTime(rtData)
	bmPlot, = plt.plot(bmDistances, label = 'BM')
	fdPlot, = plt.plot(fdDistances, label = 'FD')
	rtPlot, = plt.plot(rtDistances, label = 'RT')
	plt.legend(handles=[bmPlot, fdPlot, rtPlot])
	plt.title('Average distance to from target to nearest particle')
	plt.show()

if __name__=='__main__':
	main()