import numpy as np
import particlesim
import hardboundary


def newDirection(angle, rng):
	theta = angle + np.random.uniform(rng[0], rng[1])
	x = np.sin(theta)
	y = np.cos(theta)
	return np.array((x,y))

def moveParticles(particles, t, boundary, params):
	rate, s = params['rate'], params['s']
	tumbleProb = rate * t
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		x = x0 + v0 * t
		if np.linalg.norm(v0) == 0 or np.random.uniform(0,1) < tumbleProb:
			v = s * newDirection(np.arctan2(v0[0], v0[1]),[-np.pi, np.pi])
		else:
			v = v0
		x, v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	n, iterations = 300, 1000
	params = {'rate': 0.01, 's': 0.5}
	folder = 'data/run tumble n={} iter={}'.format(n, iterations)
	boundary = hardboundary.Circle(10.0)
	data = particlesim.simulate(iterations, n, moveParticles, folder, boundary, params)
	particlesim.motionAnimation(data, 100, boundary)

if __name__=='__main__':
	main()