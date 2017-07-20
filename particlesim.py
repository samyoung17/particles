import numpy as np
import sys
import pickle
import matplotlib.pyplot as plt
import matplotlib.animation as animation

R_MAX = 10
R_0 = 1
TIMESTEP = 0.1
MASS = 1

class Data(object):
	def __init__(self, iterations, numpoints):
		self.numpoints = numpoints
		self.iterations = iterations
		self.x = np.zeros((iterations, numpoints, 2))
		self.v = np.zeros((iterations, numpoints, 2))
		self.F = np.zeros((iterations, numpoints, 2))
		self.Fd = np.zeros((iterations, numpoints, 2))
		self.t = np.zeros((iterations))

class Particle(object):
	def __init__(self, x, v):
		self.x = x
		self.v = v
		self.F = np.zeros((1,2))
		self.Fd = np.zeros((1,2))

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
		v = np.array((0,0))
		particle = Particle(x, v)
		particles.append(particle)
	return particles

def recordData(particles, data, i):
	data.x[i] = map(lambda p: p.x, particles)
	data.v[i] = map(lambda p: p.v, particles)
	data.F[i] = map(lambda p: p.F, particles)
	data.Fd[i] = map(lambda p: p.Fd, particles)
	data.t[i] = i * TIMESTEP

def logIteration(i, iterations):
	perc = (i+1) * 100.0 / iterations
	sys.stdout.write("\rSimulating... %.2f%%" % perc)
	sys.stdout.flush()

def loadData(fname):
	f = open('data/' + fname, 'r')
	data = pickle.load(f)
	f.close()
	return data

def writeData(data, fname):
	f = open('data/' + fname, 'w')
	pickle.dump(data, f)
	f.close()
	print('\nSaved data to file: \'data/' + fname)

def simulate(iterations, n, moveFn):
	particles = initParticles(n, R_0)
	data = Data(iterations, n)
	recordData(particles, data, 0)
	for i in range(1, iterations):
		moveFn(particles, TIMESTEP, MASS)
		recordData(particles, data, i)
		logIteration(i, iterations)
	return data

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
	circle = plt.Circle((0,0), radius=R_MAX, color='g', fill=False)
	axes.add_patch(circle)
	scat = axes.scatter(data.x[0,:,0], data.x[0,:,1])
	interval = TIMESTEP * 1000 / speedMultiplier
	ani = animation.FuncAnimation(fig, draw, interval=interval, frames = xrange(data.iterations), fargs=(scat, data), repeat=False)
	plt.show()