import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


R_MAX = 1000
R_0 = 1
TIMESTEP = 0.1
MASS = 1

class Particle(object):
	def __init__(self, x, v):
		self.x = x
		self.v = v
		self.F = np.zeros((1,2))

class Data(object):
	def __init__(self, iterations, numpoints):
		self.numpoints = numpoints
		self.iterations = iterations
		self.x = np.zeros((iterations, numpoints, 2))
		self.v = np.zeros((iterations, numpoints, 2))
		self.t = np.zeros((iterations))

def randomDirection():
	theta = np.random.uniform(-np.pi, np.pi)
	x = np.sin(theta)
	y = np.cos(theta)
	return np.array((x, y))

def newDirection(angle, range):
	theta = angle + np.random.uniform(range[0], range[1])
	x = np.sin(theta)
	y = np.cos(theta)
	return np.array((x,y))

def randomPointOnDisc(rMax):
	costheta = np.random.uniform(-1,1)
	u = np.random.uniform(0,1)
	theta = np.arccos(costheta) * np.random.choice((-1,1))
	r = rMax * np.power(u, 1/2.0)
	x = r * np.sin(theta)
	y = r * np.cos(theta)
	return np.array((x,y))

def initParticles(n, r0):
	particles = []
	for i in range(n):
		x = np.array(randomPointOnDisc(r0))
		v = np.array(randomDirection())
		particle = Particle(x, v)
		particles.append(particle)
	return particles

def draw(i, scat, data):
	points = data.x[i]
	scat.set_offsets(points)
	return scat,

def motionAnimation(data, speedMultiplier):
	fig = plt.figure()
	axes = plt.gca()
	padding = 1.5
	axes.set_xlim([-R_MAX * padding, R_MAX * padding])
	axes.set_ylim([-R_MAX * padding, R_MAX * padding])
	scat = axes.scatter(data.x[0,:,0], data.x[0,:,1])
	interval = TIMESTEP * 1000 / speedMultiplier
	ani = animation.FuncAnimation(fig, draw, interval=interval, frames = xrange(data.iterations), fargs=(scat, data), repeat=False)
	plt.show()

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

def recordData(particles, data, i):
	data.x[i] = map(lambda p: p.x, particles)
	data.v[i] = map(lambda p: p.v, particles)
	data.t[i] = i * TIMESTEP

def simulation(iterations, n):
	data = Data(iterations, n)
	particles = initParticles(n, R_0)
	for i in range(1, iterations):
		moveParticles(particles, TIMESTEP)
		recordData(particles, data, i)
	return data

def main():
	data = simulation(10000, 200)
	motionAnimation(data, 100)

if __name__=='__main__':
	main()