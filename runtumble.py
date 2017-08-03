import numpy as np
import particlesim
import hardboundary

RATE = 0.1
S = 0.2

def randomDirection():
	theta = np.random.uniform(-np.pi, np.pi)
	x = np.sin(theta)
	y = np.cos(theta)
	return np.array((x, y))

def newDirection(angle, rng):
	theta = angle + np.random.uniform(rng[0], rng[1])
	x = np.sin(theta)
	y = np.cos(theta)
	return np.array((x,y))

def moveParticles(particles, t):
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		x = x0 + v0
		if np.random.uniform(0,1) < RATE:
			v = S * newDirection(np.arctan2(v0[0], v0[1]),[-np.pi/2, np.pi/2])
		else:
			v = v0
		x, v = hardboundary.bounceIfHitsBoundary(x, v, t, particlesim.R_MAX)
		particle.x, particle.v = x, v

def main():
	iterations = 5000
	n = 200
	data = particlesim.simulate(iterations, n, moveParticles)
	particlesim.writeData(data, 'run tumble n={} iter={}.pickle'.format(n, iterations))
	particlesim.motionAnimation(data, 10)

if __name__=='__main__':
	main()