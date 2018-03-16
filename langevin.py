import numpy as np
import particlesim
import hardboundary
import matplotlib.pyplot as plt


"""
Parameters:
	m:			The mass (inertia) of the particles
	gamma:	The friction coefficient
	s:			The average speed of the particles (not including electrostatic field)
"""
def moveParticles(particles, t, boundary, params):
	m, gamma, s = params['m'], params['gamma'], params['s']
	T = 2 * m * pow(s,2) / np.pi
	var = 2 * gamma * T * t
	cov = [[var, 0], [0, var]]
	mean = (0, 0)
	b = np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		dv = - (gamma/m)*v0*t + (1/m)*b[i]
		v = v0 + dv
		x = x0 + v0 * t
		x,v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	params = {
		'm': 0.1,
		'gamma': 0.02,
		's': 0.35
	}
	n, iterations = 300, 1000
	folder = 'data/langevin n={} iter={}'.format(n, iterations)
	boundary = hardboundary.Circle(10.0)
	data = particlesim.simulate(iterations, n, moveParticles, folder, boundary, params)
	# averageSpeed(data)
	particlesim.motionAnimation(data, 100, boundary)

def averageTemp(data, m):
	e = np.apply_along_axis(lambda v: 0.5 * m * pow(np.linalg.norm(v), 2), 2, data.v)
	ebar = e.mean(axis=1)
	plt.plot(ebar)
	plt.show()

def averageSpeed(data):
	e = np.apply_along_axis(np.linalg.norm, 2, data.v)
	ebar = e.mean(axis=1)
	plt.plot(ebar)
	plt.show()

if __name__=='__main__':
	main()