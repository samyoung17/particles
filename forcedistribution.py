import particlesim
import numpy as np
import sys

K_E  = 8.99E9
Q = 3E-8
VISCOUSITY = 1E-2
PARTICLE_RADIUS = 1E-3
NU = 0.2
M = 1
R_MAX = 10

def forceBetweenTwoPointCharges(q1, q2, r):
	return - K_E * q1 * q2 * r / pow(np.linalg.norm(r),3)

def forceBetweenTwoPointChargesUnitConstants(r, qSquared):
	# This function is called iter * N^2 times, so optimise for speed
	return - r * qSquared / pow(r[0] ** 2 + r[1] ** 2, 1.5)

def forceDueToDrag(v):
	return - 6 * np.pi * VISCOUSITY * PARTICLE_RADIUS * v

def forceDueToDragUnitConstants(v, m):
	return - NU * v * m

def boundingForce(x, q, n):
	r = np.linalg.norm(x)
	xUnit = x / r
	return  - K_E * n * q * q * xUnit / pow(R_MAX - r, 2)

def boundingForceUnitConstants(x, q, n):
	r = np.linalg.norm(x)
	xUnit = x / r
	return  - xUnit * q / pow(R_MAX - r, 2)

def moveParticles(particles, t):
	q = 1.0 / len(particles)
	for i, particle in enumerate(particles):
		other_particles = particles[:i] + particles[i + 1:]
		displacements = map(lambda p: p.x - particle.x, other_particles)
		forces = map(lambda r: forceBetweenTwoPointChargesUnitConstants(r, q**2), displacements)
		F = sum(forces) + boundingForceUnitConstants(particle.x, q, len(particles))
		v0 = particle.v
		x0 = particle.x
		Fd = forceDueToDragUnitConstants(v0, M)
		a = (F + Fd) / M
		v = a * t + v0
		x = x0 + (v + v0) / 2
		particle.x = x
		particle.v = v
		particle.F = F
		particle.Fd = Fd

if __name__ == '__main__':
	if len(sys.argv) != 4:
		raise ValueError('Arguments should be: n, iter, outfile')
	script, n, iterations, fname = sys.argv
	data = particlesim.simulate(int(iterations), int(n), moveParticles)
	particlesim.writeData(data, fname)
	speedMultiplier = 10
	particlesim.motionAnimation(data, speedMultiplier, R_MAX, True)