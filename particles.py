from random import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


N = 30
LENGTH = 100
WIDTH = 100
START_LENGTH = 1
START_WIDTH = 1
TIMESTEP = 0.01
K_E  = 8.99E9
Q = 3E-8
VISCOUSITY = 1E-2
PARTICLE_RADIUS = 1E-3
MASS = 1E-4
ITERATIONS = 200

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

def initParticles(n, length, width, startLength, startWidth):
	particles = []
	for i in range(n):
		xx = (random() * startWidth) + (width / 2)
		xy = (random() * startLength) + (length / 2)
		x = np.array((xx, xy))
		v = np.array((0,0))
		particle = Particle(x, v)
		particles.append(particle)
	return particles

def forceBetweenTwoPointCharges(q1, q2, r):
	return - K_E * q1 * q2 * r / pow(np.linalg.norm(r),3)

def forceDueToDrag(v):
	return - 6 * np.pi * VISCOUSITY * PARTICLE_RADIUS * v

def moveParticles(particles, t, nu, m):
	for i, particle in enumerate(particles):
		other_particles = particles[:i] + particles[i+1:]
		displacements = map(lambda p: p.x - particle.x, other_particles)
		forces = map(lambda r: forceBetweenTwoPointCharges(Q, Q, r), displacements)
		F = sum(forces)
		v0 = particle.v
		x0 = particle.x
		Fd = forceDueToDrag(v0)
		a = (F + Fd) / m
		v = a * t + v0
		x = x0 + (v + v0) / 2
		particle.x = x
		particle.v = v
		particle.F = F
		particle.Fd = Fd


def recordData(particles, data, i):
	data.x[i] = map(lambda p: p.x, particles)
	data.v[i] = map(lambda p: p.v, particles)
	data.F[i] = map(lambda p: p.F, particles)
	data.Fd[i] = map(lambda p: p.Fd, particles)
	data.t[i] = i * TIMESTEP

def draw(i, scat, data):
	points = data.x[i]
	scat.set_offsets(points)
	return scat,

def motionAnimation(data):
	fig = plt.figure()
	axes = plt.gca()
	axes.set_xlim([0,WIDTH])
	axes.set_ylim([0,LENGTH])
	scat = plt.scatter(data.x[0,:,0], data.x[0,:,1])
	ani = animation.FuncAnimation(fig, draw, interval=TIMESTEP * 1000, 
		frames = xrange(ITERATIONS), fargs=(scat, data), repeat=False)
	plt.show()

def kineticEnergy(v):
	vnorm = np.linalg.norm(v, axis=2)
	return np.multiply(vnorm, vnorm) * MASS * 0.5

def distancesFromParticleI(x, i):
	xi = x[:,i,:]
	r = np.zeros((ITERATIONS, N, 2))
	for j in range(N):
		xj = x[:,j,:]
		r[:,j,:] = xj - xi
	r = np.delete(r, (i), axis = 1)
	return np.linalg.norm(r, axis=2)

def potentialEnergy(x):
	Ep = np.zeros((ITERATIONS, N))
	for i in range(N):
		r = distancesFromParticleI(x, i)
		Ep[:,i] = 0.5 * K_E * (Q ** 2) / np.sum(r, axis = 1)
	return Ep
	
def energyPlot(data):
	Ek = kineticEnergy(data.v)
	Ep = potentialEnergy(data.x)
	E = Ek + Ep
	# for i in range(N):
	# 	plt.plot(data.t[1:], E[1:,i])
	# plt.show()

	totalEk = np.sum(Ek, axis=1)
	totalEp = np.sum(Ep, axis=1)
	totalE = totalEk + totalEp
	
	# plt.plot(data.t[1:], totalE[1:])
	# plt.show()
	plt.plot(data.t, totalEk, 'b')
	plt.show()
	plt.plot(data.t, totalEp, 'r')
	plt.show()

def main():
	particles = initParticles(N, LENGTH, WIDTH, START_LENGTH, START_WIDTH)
	data = Data(ITERATIONS, N)
	recordData(particles, data, 0)
	for i in range(1, ITERATIONS):
		moveParticles(particles, TIMESTEP, VISCOUSITY, MASS)
		recordData(particles, data, i)
	# motionAnimation(data)
	energyPlot(data)

main()