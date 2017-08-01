import numpy as np
import math
import particlesim
import hardboundary
import matplotlib.pyplot as plt

S = 0.2

def expectedNormMultivariateGaussian(sigma):
	N = 2.0
	# formula derived in https://arxiv.org/abs/1012.0621
	return sigma * math.sqrt(2) * math.gamma((N+1)/2) / math.gamma(N/2)

def moveParticles(particles, t):
	cov = [[1, 0], [0, 1]]
	mean = (0, 0)
	sigma = math.sqrt(t)
	gamma = expectedNormMultivariateGaussian(sigma) / S
	xi = np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0 = particle.x
		# Brownian motion is the limit of strong friction of the Langevin equation
		# 		m*a = -gamma*v + sigma*xi
		# Setting |m*a| << |gamma*x|, we have:
		v = (sigma / gamma) * xi[i]
		x = x0 + (v * t)
		x,v = hardboundary.bounceIfHitsBoundary(x, v, t, particlesim.R_MAX)
		particle.x, particle.v = x, v

def main():
	data = particlesim.simulate(10000, 50, moveParticles)
	particlesim.motionAnimation(data, 200)

def averageSpeed():
	data = particlesim.simulate(50000, 50, moveParticles)
	s = np.linalg.norm(data.v, axis=2)
	sbar = s.mean(axis=1)
	plt.plot(sbar)
	plt.show()

if __name__=='__main__':
	main()