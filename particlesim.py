import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import linalgutil as la
import sPickle

R_0 = 1
R_MAX = 10
TIMESTEP = 0.5

class Data(object):
	def __init__(self, iterations, numpoints, numTargets):
		self.numpoints = numpoints
		self.iterations = iterations
		self.x = np.zeros((iterations, numpoints, 2))
		self.v = np.zeros((iterations, numpoints, 2))
		self.F = np.zeros((iterations, numpoints, 2))
		self.Fd = np.zeros((iterations, numpoints, 2))
		self.t = np.zeros((iterations))
		self.y = np.zeros((iterations, numTargets, 2))

class Particle(object):
	def __init__(self, x, v):
		self.x = x
		self.v = v
		self.F = np.zeros((1,2))
		self.Fd = np.zeros((1,2))
		self.neighbours = 0

class Target(object):
	def __init__(self, y):
		self.y = y

def randomPointOnDisc(r):
	costheta = np.random.uniform(-1,1)    
	u = np.random.uniform(0,1)
	theta = np.arccos(costheta) * np.random.choice((-1,1))
	s = r * np.power(u, 1/2.0)
	return la.polarToCart((s, theta))

def initParticles(n, r0):
	particles = []
	for i in range(n):
		x = np.array(randomPointOnDisc(r0))
		v = np.array((0,0))
		particle = Particle(x, v)
		particles.append(particle)
	return particles

def initTargets(d, rMax):
	targets = []
	for x1 in np.arange(-rMax, rMax, d):
		for x2 in np.arange(-rMax, rMax, d):
			x = np.array((x1, x2))
			r, theta = la.cartToPolar(x)
			if (r < rMax):
				targets.append(Target(x))
	return targets

def recordData(particles, targets, data, i):
	data.x[i] = map(lambda p: p.x, particles)
	data.v[i] = map(lambda p: p.v, particles)
	data.F[i] = map(lambda p: p.F, particles)
	data.Fd[i] = map(lambda p: p.Fd, particles)
	data.t[i] = i * TIMESTEP
	data.y[i] = map(lambda tgt: tgt.y, targets)

def logIteration(i, iterations):
	perc = (i+1) * 100.0 / iterations
	sys.stdout.write("\rCalculating... %.2f%%" % perc)
	sys.stdout.flush()

def loadData(fname):
	f = open(fname, 'r')
	data = sPickle.load(f)
	f.close()
	return data

def writeData(data, fname):
	f = open('data/' + fname, 'w')
	sPickle.dump(data, f)
	f.close()
	print('\nSaved data to file: \'data/' + fname)

def simulate(iterations, n, moveFn):
	particles = initParticles(n, R_0)
	targets = initTargets(float(R_MAX) / 10, R_MAX)
	data = Data(iterations, n, len(targets))
	recordData(particles, targets, data, 0)
	for i in range(1, iterations):
		moveFn(particles, TIMESTEP)
		recordData(particles, targets, data, i)
		logIteration(i, iterations)
	return data

def draw(i, scat, data):
	points = data.x[i]
	scat.set_offsets(points)
	return scat,

def motionAnimation(data, speedMultiplier, ring=True):
	fig = plt.figure()
	axes = plt.gca()
	padding = 1.5
	axes.set_xlim([-R_MAX * padding, R_MAX * padding])
	axes.set_ylim([-R_MAX * padding, R_MAX * padding])
	axes.scatter(data.y[0,:,0], data.y[0,:,1], color='r', s=1)
	if ring:
		circle = plt.Circle((0,0), radius=R_MAX, color='g', fill=False)
		axes.add_patch(circle)
	scat = axes.scatter(data.x[0,:,0], data.x[0,:,1])
	interval = TIMESTEP * 1000 / speedMultiplier
	ani = animation.FuncAnimation(fig, draw, interval=interval, frames = xrange(data.iterations), fargs=(scat, data), repeat=False)
	plt.show()

def averageSpeed(data):
	s = np.linalg.norm(data.v, axis=2)
	sbar = s.mean(axis=1)
	plt.plot(data.t, sbar)
	plt.show()

def averageRadialDisplacement(data):
	r = np.linalg.norm(data.x, axis=2)
	rbar = r.mean(axis=1)
	plt.plot(data.t, rbar)
	plt.show()

def main(filePath, speedMultiplier):
	data = loadData(filePath)
	motionAnimation(data, speedMultiplier)

if __name__ == '__main__':
	if not len(sys.argv) == 3:
		raise ValueError('Arguments should be <data file path>, <speed multiplier>')
	python, fPath, speedMultiplier = sys.argv
	main(fPath, int(speedMultiplier))