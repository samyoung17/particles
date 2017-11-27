import numpy as np
import particlesim
import hardboundary
import linalgutil

S = 0.2
R_NEIGHBOUR = 2.0
REPULSION = 0.02
DRAG = 0.02

# BOUNDARY = hardboundary.Square(2 * particlesim.R_MAX)
BOUNDARY = hardboundary.Circle(particlesim.R_MAX)

def newDirection(angle, rng):
	theta = angle + np.random.uniform(rng[0], rng[1])
	x = np.sin(theta)
	y = np.cos(theta)
	return np.array((x,y))

def findNearbyParticles(particles, distances):
	indices = filter(lambda j: distances[j] > 0 and distances[j] < R_NEIGHBOUR, range(len(particles)))
	return map(lambda j: particles[j], indices)

def moveParticles(particles, t, boundary):
	D = linalgutil.distanceMatrix(map(lambda p: p.x, particles))
	for i, particle in enumerate(particles):
		nearbyParticles = findNearbyParticles(particles, D[i,:])
		x0, v0 = particle.x, particle.v
		x = x0 + v0
		accelerationUnitVectors = map(lambda p: (particle.x - p.x)/np.linalg.norm(particle.x - p.x), nearbyParticles)
		a = sum(accelerationUnitVectors) * REPULSION
		v = v0 + a * t - v0 * DRAG
		x, v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	n, iterations = 50, 1000
	folder = 'data/repulsion n={} iter={}'.format(n, iterations)
	data = particlesim.simulate(iterations, n, moveParticles, folder, BOUNDARY)
	particlesim.motionAnimation(data, 15, BOUNDARY)

if __name__=='__main__':
	main()