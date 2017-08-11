import numpy as np
import particlesim
import hardboundary
import matplotlib.pyplot as plt

M = 1.0
GAMMA = 0.1
S = 0.2
T = 2 * M * pow(S,2) / np.pi


def moveParticles(particles, t):
	var = 2 * GAMMA * T * t
	cov = [[var, 0], [0, var]]
	mean = (0, 0)
	b = np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		dv = - v0 * GAMMA / M * t + (1/M) * b[i]
		v = v0 + dv
		x = x0 + (v + v0)/2 * t
		x,v = hardboundary.bounceIfHitsBoundary(x, v, t, particlesim.R_MAX)
		particle.x, particle.v = x, v

def main():
	iterations = 5000
	n = 200
	data = particlesim.simulate(iterations, n, moveParticles)
	particlesim.writeData(data, 'langevin n={} iter={}.pickle'.format(n, iterations))
	particlesim.motionAnimation(data, 10)

def averageSpeedAndTemp():
	data = particlesim.simulate(5000, 200, moveParticles)
	s = np.linalg.norm(data.v, axis=2)
	sbar = s.mean(axis=1)
	plt.plot(sbar)
	plt.show()
	e = np.apply_along_axis(lambda v: 0.5 * M * pow(np.linalg.norm(v), 2), 2, data.v)
	ebar = e.mean(axis=1)
	plt.plot(ebar)
	plt.show()

if __name__=='__main__':
	main()