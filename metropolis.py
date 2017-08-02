import numpy as np
import math
import particlesim
import scipy.special
import linalgutil

LAMBDA = 1
SIGMA = np.diag(0.001 * np.ones(2))

def M(x):
	return np.exp(-LAMBDA * np.linalg.norm(x))

def F(x):
	return np.exp(-np.linalg.norm(x))

def A(y, yPrime):
	return np.sqrt(M(yPrime - y) * F(yPrime) / F(y))

def chi(t):
	return np.sqrt((1 - (t+1) * np.exp(-t)) / math.gamma(2))

def W(z):
	return np.real(scipy.special.lambertw(z, -1))

def chiInverse(s):
	if s == 0:
		return 0
	else:
		return -1 - W((math.gamma(2)*pow(s,2) - 1) /np.exp(1))

def rNtoBall(x):
	(r, theta) = linalgutil.cartToPolar(x)
	return linalgutil.polarToCart((chi(r) * particlesim.R_MAX, theta))

def ballToRn(x):
	(r, theta) = linalgutil.cartToPolar(x)
	return linalgutil.polarToCart((chiInverse(r / particlesim.R_MAX), theta))

def P(y):
	return np.random.multivariate_normal(y, SIGMA)

def moveParticles(particles, t):
	# Metropolis Algorithm for even sampling accross a convex region
	# From Bubley, Dyer and Jerrum 1997
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		y = ballToRn(x0)
		yPrime = P(y)
		while np.random.uniform(0,1) > A(y, yPrime):
			yPrime = P(y)
		x = rNtoBall(yPrime)
		v = x/t
		particle.x, particle.v = x, v

def main():
	data = particlesim.simulate(2000, 50, moveParticles)
	particlesim.motionAnimation(data, 10)

if __name__=='__main__':
	main()