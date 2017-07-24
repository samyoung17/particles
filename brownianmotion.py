import numpy as np
import particlesim

M = 1
GAMMA = 0
IS_BARRIER = True
R_MAX = 1000

def outOfRange(x):
	return np.linalg.norm(x, 2) > R_MAX

def projectToBoundary(x):
	phi = np.arctan2(x[0], x[1])
	return np.array((R_MAX * np.sin(phi), R_MAX * np.cos(phi)))

def bounce(x0, v0, x, v, t):
	theta = np.arccos(np.dot(x,v) / (np.linalg.norm(x,2) * np.linalg.norm(v,2)))
	phi = np.arctan2(x[0], x[1])
	s = np.linalg.norm(v,2)
	psi = np.pi + phi - (2 * theta)
	vPrime = np.array((s * np.sin(psi), s * np.cos(psi)))
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