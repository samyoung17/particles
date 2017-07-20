import numpy as np
import particlesim


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
	rate = 0.1
	for i, particle in enumerate(particles):
		v0 = particle.v
		x0 = particle.x
		x = x0 + v0
		if np.random.uniform(0,1) < rate:
			v = newDirection(np.arctan2(v0[0], v0[1]),[-np.pi/2, np.pi/2])
		else:
			v = v0
		particle.x = x
		particle.v = v

def main():
	data = particlesim.simulate(10000, 200, moveParticles)
	particlesim.motionAnimation(data, 100, 1000)

if __name__=='__main__':
	main()