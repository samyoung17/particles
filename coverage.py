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

def supMinDistance(particles, targets):
	distances = map(lambda y: nearestNeighbour(y, particles), targets)
	return np.max(distances)

def supMinDistanceOverTime(data):
	d = np.zeros((data.iterations))
	for i in range(data.iterations):
		d[i] = supMinDistance(data.x[i], data.y[i])
	return d

def main():
	print('Simulating Brownian Motion')
	bmData = particlesim.simulate(ITERATIONS, N, brownianmotion.moveParticles)
	print('Simulating Force Distribution')
	fdData = particlesim.simulate(ITERATIONS, N, forcedistribution.moveParticles)
	print('Simulating Run and Tumble')
	rtData = particlesim.simulate(ITERATIONS, N, runtumble.moveParticles)
	print('Calculating Sup Min Distances Brownian Motion')
	bmDistances = supMinDistanceOverTime(bmData)
	print('Calculating Sup Min Distances Force Distribution')
	fdDistances = supMinDistanceOverTime(fdData)
	print('Calculating Sup Min Distances Run And Tumble')
	rtDistances = supMinDistanceOverTime(rtData)
	bmPlot, = plt.plot(bmDistances, label = 'BM')
	fdPlot, = plt.plot(fdDistances, label = 'FD')
	rtPlot, = plt.plot(rtDistances, label = 'RT')
	plt.legend(handles=[bmPlot, fdPlot, rtPlot])
	plt.title('Maximum distance to from target to nearest particle')
	plt.show()

if __name__=='__main__':
	main()