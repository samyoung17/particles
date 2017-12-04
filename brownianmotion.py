import numpy as np
import math
import particlesim
import hardboundary

S = 0.2

def expectedNormMultivariateGaussian(sigma):
	N = 2.0
	# formula derived in https://arxiv.org/abs/1012.0621
	return sigma * math.sqrt(2) * math.gamma((N+1)/2) / math.gamma(N/2)

def moveParticles(particles, t, boundary, params):
	cov = [[1, 0], [0, 1]]
	mean = (0, 0)
	sigma = math.sqrt(t)
	gamma = expectedNormMultivariateGaussian(sigma) / S
	xi = np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0 = particle.x, v0 = particle.v
		# Brownian motion is the limit of strong friction of the Langevin equation
		# 		m*a = -gamma*v + sigma*xi
		# Setting |m*a| << |gamma*x|, we have:
		v = (sigma / gamma) * xi[i]
		x = x0 + (v * t)
		x,v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	iterations, n = 20000, 200
	folder = 'data/brownian n={} iter={}'.format(n, iterations)
	boundary = hardboundary.Circle(10)
	data = particlesim.simulate(iterations, n, moveParticles, folder, boundary)
	particlesim.motionAnimation(data, 200, boundary)

if __name__=='__main__':
	main()