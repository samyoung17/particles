import numpy as np
import particlesim
import hardboundary
import linalgutil

S = 0.2
R = 2.0

MAX_RATE = 0.25
MIN_RATE = 0.05
C = 0.15
M = 0.3

def newDirection(angle, rng):
	theta = angle + np.random.uniform(rng[0], rng[1])
	x = np.sin(theta)
	y = np.cos(theta)
	return np.array((x,y))

def numberOfNearbyParticles(i, D):
	r = 2
	nearbyDistances = filter(lambda d: d < r, D[i,:])
	# Subtract one, because D[i] includeds d_ii the distance from i to itself
	return len(nearbyDistances) - 1

def densityMultiplier(n):
	return (1.0 / n) / (pow(R,2) / pow(particlesim.R_MAX,2))

def rate(concentrationGradient):
	unboundedRate = M * concentrationGradient + C
	return max(min(unboundedRate, MAX_RATE), MIN_RATE)

def moveParticles(particles, t):
	D = linalgutil.distanceMatrix(map(lambda p: p.x, particles))
	m = densityMultiplier(len(particles))
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		x = x0 + v0
		neighbours = numberOfNearbyParticles(i, D)
		densityGradient = m * (neighbours - particle.neighbours)
		if np.random.uniform(0,1) < rate(densityGradient):
			v = S * newDirection(np.arctan2(v0[0], v0[1]),[-np.pi, np.pi])
		else:
			v = v0
		x, v = hardboundary.bounceIfHitsBoundary(x, v, t, particlesim.R_MAX)
		particle.x, particle.v, particle.neighbours = x, v, neighbours

def main():
	iterations = 5000
	n = 200
	data = particlesim.simulate(iterations, n, moveParticles)
	particlesim.writeData(data, 'run tumble gradient n={} iter={}.pickle'.format(n, iterations))
	particlesim.motionAnimation(data, 10)

if __name__=='__main__':
	main()