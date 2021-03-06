import numpy as np
import particlesim
import electrostaticboundary
import repulsiveboundary
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
	m, gamma, d, rNeighbour, q, qRing, alpha \
		= params['m'], params['gamma'], params['d'], params['rNeighbour'], \
		  params['q'], params['qRing'], params['alpha']
	var = 2 * d * t
	cov = [[var, 0], [0, var]]
	mean = (0, 0)
	b = np.random.multivariate_normal(mean, cov, len(particles))
	xx = np.array(list(map(lambda p: p.x, particles)))
	D = linalgutil.distanceMatrix(xx, xx)
	for i, particle in enumerate(particles):
		jj = findNearbyParticleIndices(particles, D[i], rNeighbour)
		F = sum(map(lambda j: (particles[i].x - particles[j].x)/D[i,j] * electrostaticForce(D[i,j], q, alpha), jj))
		x0, v0 = particle.x, particle.v
		if (boundary.rMax - np.linalg.norm(x0)) < rNeighbour/2.0:
			Fb = boundary.force(x0, q) * qRing
		else:
			Fb = 0.0
		dv = - (gamma / m)*v0*t + (Fb + F)/m*t + (1/m)*b[i]
		v = v0 + dv
		x = x0 + v0 * t
		x,v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	n, iterations = 100, 1000
	folder = 'data/electrostatic langevin n={} iter={}'.format(n, iterations)
	boundary = repulsiveboundary.Circle(10.0)
	h = np.sqrt(2 * np.pi / (3 * np.sqrt(3)))
	params = {'m': 1, 'gamma': 0.5, 's': 0.5, 'rNeighbour': 0,#h * np.sqrt(3) * 10 / np.sqrt(n),
			  'q': 0.0 / (3 * pow(h, 2)),
			  'qRing': 3.0, 'alpha': 0}
	data = particlesim.simulate(iterations, n, moveParticles, folder, boundary, params)
	particlesim.motionAnimation(data, 10, boundary)

if __name__=='__main__':
	main()