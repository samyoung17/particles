import numpy as np
import particlesim
import hardboundary

RATE = 0.1
S = 0.2

BOUNDARY = hardboundary.Square(2 * particlesim.R_MAX)
# BOUNDARY = hardboundary.Circle(particlesim.R_MAX)

def newDirection(angle, rng):
	theta = angle + np.random.uniform(rng[0], rng[1])
	x = np.sin(theta)
	y = np.cos(theta)
	return np.array((x,y))

def moveParticles(particles, t, boundary):
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		x = x0 + v0
		if np.random.uniform(0,1) < RATE:
			v = S * newDirection(np.arctan2(v0[0], v0[1]),[-np.pi, np.pi])
		else:
			v = v0
		x, v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	n, iterations = 10, 1000
	folder = 'data/run tumble n={} iter={}'.format(n, iterations)
	data = particlesim.simulate(iterations, n, moveParticles, folder, BOUNDARY)
	particlesim.motionAnimation(data, 15, BOUNDARY)

if __name__=='__main__':
	main()