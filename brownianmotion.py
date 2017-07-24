import numpy as np
import particlesim
import hardboundary

M = 1
GAMMA = 0
IS_BARRIER = True
R_MAX = 1000

def moveParticles(particles, t):
	cov = [[np.sqrt(t), 0], [0, np.sqrt(t)]]
	mean = (0, 0)
	xi = np.random.multivariate_normal(mean, cov, len(particles))
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		a = - GAMMA / M + (1/M) * xi[i]
		v = v0 + a
		x = x0 + (v + v0)/2 * t
		x,v = hardboundary.bounceIfHitsBoundary(x, v, t, R_MAX)
		particle.x, particle.v = x, v

def main():
	data = particlesim.simulate(5000, 200, moveParticles)
	particlesim.motionAnimation(data, 100, R_MAX, ring=True)

if __name__=='__main__':
	main()