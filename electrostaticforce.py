import particlesim
import electrostaticboundary
import numpy as np
import linalgutil

K_E  = 1
NU = 0.1
M = 0.1

def forceBetweenTwoPointCharges(q1, q2, r):
	return - K_E * q1 * q2 * r / pow(np.linalg.norm(r),3)

def forceBetweenTwoPointChargesUnitConstants(r, qSquared):
	# This function is called iter * N^2 times, so optimise for speed
	r = linalgutil.boundPointBelow(r, electrostaticboundary.EPSILON)
	return - r * qSquared / pow(r[0] ** 2 + r[1] ** 2, 1.5)

def forceDueToDragUnitConstants(v, m):
	return - NU * v * m

def moveParticles(particles, t, boundary, params):
	q = 1.0 / len(particles)
	for i, particle in enumerate(particles):
		other_particles = particles[:i] + particles[i + 1:]
		displacements = map(lambda p: p.x - particle.x, other_particles)
		forces = map(lambda r: forceBetweenTwoPointChargesUnitConstants(r, q**2), displacements)
		x0, v0 = particle.x, particle.v
		F = sum(forces)
		Fb = boundary.force(x0, q)
		Fd = forceDueToDragUnitConstants(v0, M)
		a = (F + Fb + Fd) / M
		v = a * t + v0
		x = x0 + (v + v0) * t / 2
		# Prevent the particles from jumping across the boundary in between timesteps
		x, v = boundary.bounceIfHits(x0, v0, x, v)
		particle.x, particle.v, particle.F, particle.Fd = x, v, F, Fd

def main():
	n, iterations = 50, 3000
	folder = 'data/electrostatic n={} iter={}'.format(n, iterations)
	boundary = electrostaticboundary.Circle(10.0)
	data = particlesim.simulate(iterations, n, moveParticles, folder, boundary)
	particlesim.motionAnimation(data, 20, boundary)

if __name__ == '__main__':
	main()