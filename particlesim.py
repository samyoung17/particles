import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import linalgutil as la
import datamodel

R_0 = 1
FURTHEST_TARGET = 10
TARGET_SEPERATION = 0.5
TIMESTEP = 0.25

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

def initTargets(d, rMax, boundary):
	furtherestTarget = rMax * 10.0
	targets = []
	for x1 in np.arange(-furtherestTarget, furtherestTarget, d):
		for x2 in np.arange(-furtherestTarget, furtherestTarget, d):
			x = np.array((x1, x2))
			if boundary.contains(x):
				targets.append(Target(x))
	return targets

def recordData(particles, targets, data, i):
	data.x[i] = tuple(map(lambda p: p.x, particles))
	data.v[i] = tuple(map(lambda p: p.v, particles))
	data.F[i] = tuple(map(lambda p: p.F, particles))
	data.Fd[i] = tuple(map(lambda p: p.Fd, particles))
	data.t[i] = i * TIMESTEP
	data.y[i] = tuple(map(lambda tgt: tgt.y, targets))

def logIteration(i, iterations):
	perc = (i+1) * 100.0 / iterations
	sys.stdout.write("\rCalculating... %.2f%%" % perc)
	sys.stdout.flush()

def simulate(iterations, n, moveFn, folder, boundary, params={}):
	particles = initParticles(n, R_0)
	targets = initTargets(TARGET_SEPERATION, FURTHEST_TARGET, boundary)
	data = datamodel.Data(folder, 'w+', iterations, n, len(targets), boundary)
	recordData(particles, targets, data, 0)
	for i in range(1, iterations):
		moveFn(particles, TIMESTEP, boundary, params)
		recordData(particles, targets, data, i)
		logIteration(i, iterations)
	return data

def draw(i, scat, data):
	points = data.x[i]
	scat.set_offsets(points)
	return scat,

def motionAnimation(data, speedMultiplier, boundary):
	fig = plt.figure()
	axes = plt.gca()
	padding = 1.5
	axes.set_xlim([-FURTHEST_TARGET * padding, FURTHEST_TARGET * padding])
	axes.set_ylim([-FURTHEST_TARGET * padding, FURTHEST_TARGET * padding])
	axes.scatter(data.y[0,:,0], data.y[0,:,1], color='r', s=1)
	boundary.plot(axes)
	scat = axes.scatter(data.x[0,:,0], data.x[0,:,1])
	interval = TIMESTEP * 1000 / speedMultiplier
	ani = animation.FuncAnimation(fig, draw, interval=interval, frames = range(data.iterations), fargs=(scat, data), repeat=False)
	plt.show()

def main(filePath, speedMultiplier):
	data = datamodel.Data(filePath, 'r')
	motionAnimation(data, speedMultiplier, data.boundary)

if __name__ == '__main__':
	if not len(sys.argv) == 3:
		raise ValueError('Arguments should be <data file path>, <speed multiplier>')
	python, fPath, speedMultiplier = sys.argv
	main(fPath, int(speedMultiplier))