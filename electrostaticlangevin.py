import numpy as np
import particlesim
import hardboundary
import linalgutil

def findNearbyParticleIndices(particles, distances, rNeighbour):
	return filter(lambda j: distances[j] > 0 and distances[j] < rNeighbour, range(len(particles)))

"""
Parameters:
	m:				The mass (inertia) of the particles
	gamma:		The friction coefficient
	s:				The average speed of the particles (not including electrostatic field)
	rNeighbour:	Distance cut off of the electrostatic field
	qTotal:		Total amount of charge
	alpha:		Exponent of the electrostatic field
						-2 in 3D Coulomb's law
						-1 in 2D Coulomb's law
						 0 for linear repulsion
"""
def moveParticles(particles, t, boundary, params):
	m, gamma, s, rNeighbour, qTotal, alpha \
		= params['m'], params['gamma'], params['s'], params['rNeighbour'], params['qTotal'], params['alpha']
	T = 2 * m * pow(s, 2) / np.pi
	var = 2 * gamma * T * t
	cov = [[var, 0], [0, var]]
	mean = (0, 0)
	b = np.random.multivariate_normal(mean, cov, len(particles))
	D = linalgutil.distanceMatrix(map(lambda p: p.x, particles))
	q = qTotal / len(particles)
	for i, particle in enumerate(particles):
		jj = findNearbyParticleIndices(particles, D[i], rNeighbour)
		F = sum(map(lambda j: q**2 * (particles[i].x - particles[j].x)/D[i,j] * pow(D[i,j], alpha), jj))
		x0, v0 = particle.x, particle.v
		dv = - (gamma / m)*v0*t + (F/m)*t + (1/m)*b[i]
		v = v0 + dv
		x = x0 + v0 * t
		x,v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	n, iterations = 400, 4000
	folder = 'data/electrostatic langevin n={} iter={}'.format(n, iterations)
	boundary = hardboundary.Circle(10.0)
	params = {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 3.0, 'qTotal': 10.0, 'alpha':0}
	data = particlesim.simulate(iterations, n, moveParticles, folder, boundary, params)
	particlesim.motionAnimation(data, 15, boundary)

if __name__=='__main__':
	main()