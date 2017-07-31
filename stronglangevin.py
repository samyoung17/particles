import numpy as np
import particlesim
import hardboundary
import matplotlib.pyplot as plt

M = 1
GAMMA = 1
SIGMA = 1

def moveParticles(particles, t):
	cov = [[np.sqrt(t), 0], [0, np.sqrt(t)]]
	mean = (0, 0)
	xi = np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0 = particle.x
		# Taking the limit of strong friction, |M*a| << |GAMMA*x|
		v = (SIGMA / GAMMA) * xi[i]
		x = x0 + v
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