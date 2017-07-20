import numpy as np
import particlesim

def moveParticles(particles, t):
	cov = [[np.sqrt(t), 0], [0, np.sqrt(t)]]
	mean = (0, 0)
	dx = np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0 = particle.x
		x = x0 + dx[i]
		v = dx[i] / t
		particle.x = x
		particle.v = v

def main():
	data = particlesim.simulate(1000, 200, moveParticles)
	particlesim.motionAnimation(data, 100, 100)

if __name__=='__main__':
	main()