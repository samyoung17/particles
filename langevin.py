import numpy as np
import particlesim
import hardboundary
import matplotlib.pyplot as plt
import coverageconfig

M = 1.0
GAMMA = 0.1
S = 0.2
T = 2 * M * pow(S,2) / np.pi

BOUNDARY = hardboundary.CompactPolygon(coverageconfig.WIERD_QUADRILATERAL_VERTICES)

def moveParticles(particles, t, boundary):
	var = 2 * GAMMA * T * t
	cov = [[var, 0], [0, var]]
	mean = (0, 0)
	b = np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		dv = - (GAMMA/M)*v0*t + (1/M)*b[i]
		v = v0 + dv
		x = x0 + v0 * t
		x,v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	n, iterations = 20, 1000
	folder = 'data/langevin n={} iter={}'.format(n, iterations)
	data = particlesim.simulate(iterations, n, moveParticles, folder, BOUNDARY)
	particlesim.motionAnimation(data, 15, BOUNDARY)

def averageTemp(data):
	e = np.apply_along_axis(lambda v: 0.5 * M * pow(np.linalg.norm(v), 2), 2, data.v)
	ebar = e.mean(axis=1)
	plt.plot(ebar)
	plt.show()

if __name__=='__main__':
	main()