import numpy as np
import particlesim
import electrostaticboundary
import linalgutil


def findNearbyParticleIndices(particles, distances, rNeighbour):
	return filter(lambda j: distances[j] > 0 and distances[j] < rNeighbour, range(len(particles)))

def electrostaticForce(r, q, alpha):
	# Bound the distance between two particles below by EPSILON to bodge distretisation errors
	r = max(r, electrostaticboundary.EPSILON)
	return q**2 * pow(r, alpha)

"""
Parameters:
	m:			The mass (inertia) of the particles
	gamma:		The friction coefficient
	s:			The average speed of the particles (not including electrostatic field)
	rNeighbour:	Distance cut off of the electrostatic field
	qTotal:		Total amount of charge
	alpha:		Exponent of the electrostatic field
						-2 in 3D Coulomb's law
						-1 in 2D Coulomb's law
						 0 for linear repulsion
"""
def moveParticles(particles, t, boundary, params):
	m, gamma, s, rNeighbour, qTotal, qRing, alpha \
		= params['m'], params['gamma'], params['s'], params['rNeighbour'], \
		  params['qTotal'], params['qRing'], params['alpha']
	T = 2 * m * pow(s, 2) / np.pi
	var = 2 * gamma * T * t
	cov = [[var, 0], [0, var]]
	mean = (0, 0)
	b = np.random.multivariate_normal(mean, cov, len(particles))
	xx = map(lambda p: p.x, particles)
	D = linalgutil.distanceMatrix(xx, xx)
	q = qTotal / len(particles)
	for i, particle in enumerate(particles):
		jj = findNearbyParticleIndices(particles, D[i], rNeighbour)
		F = sum(map(lambda j: (particles[i].x - particles[j].x)/D[i,j] * electrostaticForce(D[i,j], q, alpha), jj))
		x0, v0 = particle.x, particle.v
		if (boundary.rMax - np.linalg.norm(x0)) < rNeighbour:
			Fb = boundary.force(x0, q) * qRing
		else:
			Fb = 0.0
		dv = - (gamma / m)*v0*t + (Fb + F)/m*t + (1/m)*b[i]
		v = v0 + dv
		x = x0 + v0 * t
		x,v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	n, iterations = 150, 6000
	folder = 'data/electrostatic langevin n={} iter={}'.format(n, iterations)
	boundary = electrostaticboundary.Circle(10.0)
	params = {'m': 0.1, 'gamma': 0.1, 's': 0.1, 'rNeighbour': 0.375, 'qTotal': 20.0, 'qRing': 3.0, 'alpha': 0}
	data = particlesim.simulate(iterations, n, moveParticles, folder, boundary, params)
	particlesim.motionAnimation(data, 20, boundary)

if __name__=='__main__':
	main()