import numpy as np
import particlesim
import hardboundary
import matplotlib.pyplot as plt

M = 1
GAMMA = 1E-4
S = 0.01

def moveParticles(particles, t):
	cov = [[np.sqrt(t), 0], [0, np.sqrt(t)]]
	mean = (0, 0)
	xi = S * np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		a = - v0 * GAMMA / M + (1/M) * xi[i]
		v = v0 + a
		x = x0 + (v + v0)/2 * t
		x,v = hardboundary.bounceIfHitsBoundary(x, v, t, particlesim.R_MAX)
		particle.x, particle.v = x, v

def main():
	data = particlesim.simulate(5000, 50, moveParticles)
	particlesim.motionAnimation(data, 100)

def averageSpeed():
	data = particlesim.simulate(100000, 50, moveParticles)
	s = np.linalg.norm(data.v, axis=2)
	sbar = s.mean(axis=1)
	plt.plot(sbar)
	plt.show()

if __name__=='__main__':
	main()