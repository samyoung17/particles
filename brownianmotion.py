import numpy as np
import particlesim

M = 1
GAMMA = 0

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
		particle.x = x
		particle.v = v

def main():
	data = particlesim.simulate(5000, 200, moveParticles)
	particlesim.motionAnimation(data, 100, 1000)

if __name__=='__main__':
	main()