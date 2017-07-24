import numpy as np
import particlesim

M = 1
GAMMA = 0
IS_BARRIER = True
R_MAX = 1000

def polarToCart(z):
	r, theta = z
	return np.array((r * np.sin(theta), r * np.cos(theta)))

def cartToPolar(y):
	theta = np.arctan2(y[0], y[1])
	r = np.linalg.norm(y,2)
	return np.array((r, theta))

def outOfRange(x):
	return np.linalg.norm(x, 2) > R_MAX

def projectToBoundary(x):
	r, phi = cartToPolar(x)
	return polarToCart((R_MAX, phi))

def angleBetweenTwoVectors(a, b):
	return np.arccos(np.dot(a,b) / (np.linalg.norm(a,2) * np.linalg.norm(b,2)))

def bounce(x0, v0, x, v, t):
	theta = angleBetweenTwoVectors(x, v)
	r, phi = cartToPolar(x)
	psi = np.pi + phi - (2 * theta)
	vPrime = polarToCart((np.linalg.norm(v,2), psi))
	xPrime = projectToBoundary(x0) + vPrime * t
	return xPrime, vPrime

def moveParticles(particles, t):
	cov = [[np.sqrt(t), 0], [0, np.sqrt(t)]]
	mean = (0, 0)
	xi = np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0 = particle.x
		v0 = particle.v
		a = - GAMMA / M + (1/M) * xi[i]
		v = v0 + a
		x = x0 + (v + v0)/2 * t
		if IS_BARRIER and outOfRange(x):
			x, v = bounce(x0, v0, x, v, t)
		particle.x = x
		particle.v = v

def main():
	data = particlesim.simulate(5000, 200, moveParticles)
	particlesim.motionAnimation(data, 100, R_MAX, ring=True)

if __name__=='__main__':
	main()