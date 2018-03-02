import numpy as np
import particlesim
import hardboundary


def newDirection(angle, rng):
	theta = angle + np.random.uniform(rng[0], rng[1])
	x = np.sin(theta)
	y = np.cos(theta)
	return np.array((x,y))

def calculateNoise(m, s, gamma, t, n):
	T = 2 * m * pow(s, 2) / np.pi
	var = 2 * gamma * T * t
	cov = [[var, 0], [0, var]]
	mean = (0, 0)
	return np.random.multivariate_normal(mean, cov, n)

def moveParticles(particles, t, boundary, params):
	rate, s, sNoise, m, gamma = params['rate'], params['s'], params['sNoise'], params['m'], params['gamma']
	tumbleProb = rate * t
	b = calculateNoise(m, sNoise, gamma, t, len(particles))
	for i, particle in enumerate(particles):
		x0, v0 = particle.x, particle.v
		x = x0 + v0 * t
		if np.linalg.norm(v0) == 0 or np.random.uniform(0,1) < tumbleProb:
			v = s * newDirection(np.arctan2(v0[0], v0[1]),[-np.pi, np.pi])
		else:
			v = v0 + -gamma/m *(sNoise/(s + sNoise)) * v0 + (1 / m) * b[i]
		x, v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v = x, v

def main():
	n, iterations = 50, 3000
	params = {'rate': 0.25, 's': 0.5, 'sNoise': 0.5, 'm': 0.1, 'gamma': 0.05}
	folder = 'data/run tumble n={} iter={}'.format(n, iterations)
	boundary = hardboundary.Circle(10.0)
	data = particlesim.simulate(iterations, n, moveParticles, folder, boundary, params)
	particlesim.motionAnimation(data, 20, boundary)

if __name__=='__main__':
	main()