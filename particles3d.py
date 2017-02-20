from random import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

N = 100
R_MAX = 10
R_0 = 1

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
		self.x = np.zeros((iterations, numpoints, 3))
		self.v = np.zeros((iterations, numpoints, 3))
		self.F = np.zeros((iterations, numpoints, 3))
		self.Fd = np.zeros((iterations, numpoints, 3))
		self.t = np.zeros((iterations))

class Particle(object):
	def __init__(self, x, v):
		self.x = x
		self.v = v
		self.F = np.zeros((1,3))
		self.Fd = np.zeros((1,3))

def randomPointInSphere(rMax):
    phi = np.random.uniform(0,2 * np.pi)
    costheta = np.random.uniform(-1,1)    
    u = np.random.uniform(0,1)
    theta = np.arccos(costheta)
    r = rMax * np.power(u, 1/3.0)
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.array((x,y,z))

def initParticles(n, r0):
	particles = []
	for i in range(n):
		x = np.array(randomPointInSphere(r0))
		v = np.array((0,0,0))
		particle = Particle(x, v)
		particles.append(particle)
	return particles

def forceBetweenTwoPointCharges(q1, q2, r):
	return - K_E * q1 * q2 * r / pow(np.linalg.norm(r),3)

def forceDueToDrag(v):
	return - 6 * np.pi * VISCOUSITY * PARTICLE_RADIUS * v

def boundingForce(x, q):
    r = np.linalg.norm(x)
    xUnit = x / r
    return  - K_E * N * q * q * xUnit / pow(R_MAX - r, 2)

def moveParticles(particles, t, nu, m):
	for i, particle in enumerate(particles):
		other_particles = particles[:i] + particles[i+1:]
		displacements = map(lambda p: p.x - particle.x, other_particles)
		forces = map(lambda r: forceBetweenTwoPointCharges(Q, Q, r), displacements)
		F = sum(forces) + boundingForce(particle.x, Q)
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

def drawPoints(data): 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data.x[0,:,0], data.x[0,:,1], data.x[0,:,2])
    plt.show()

def draw(i, scat, data):
    xx = np.ma.ravel(data.x[i,:,0])
    xy = np.ma.ravel(data.x[i,:,1])
    xz = np.ma.ravel(data.x[i,:,2])
    scat._offsets3d = (xx, xy, xz)
    return scat,

def motionAnimation(data):
    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')
    pad = 1.1
    axes.set_xlim([-R_MAX * pad, R_MAX * pad])
    axes.set_ylim([-R_MAX * pad, R_MAX * pad])
    axes.set_zlim([-R_MAX * pad, R_MAX * pad])
    scat = axes.scatter(data.x[0,:,0], data.x[0,:,1], data.x[0,:,2])
    ani = animation.FuncAnimation(fig, draw, interval=TIMESTEP * 1000, frames = xrange(ITERATIONS), fargs=(scat, data), repeat=False)
    plt.show()

def main():
    particles = initParticles(N, R_0)
    data = Data(ITERATIONS, N)
    recordData(particles, data, 0)
#    drawPoints(data)
    for i in range(1, ITERATIONS):
        moveParticles(particles, TIMESTEP, VISCOUSITY, MASS)
        recordData(particles, data, i)
    motionAnimation(data)

main()