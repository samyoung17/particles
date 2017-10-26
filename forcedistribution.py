import particlesim
import numpy as np

K_E  = 1
NU = 0.1
M = 1

def forceBetweenTwoPointCharges(q1, q2, r):
	return - K_E * q1 * q2 * r / pow(np.linalg.norm(r),3)

def forceBetweenTwoPointChargesUnitConstants(r, qSquared):
	# This function is called iter * N^2 times, so optimise for speed
	return - r * qSquared / pow(r[0] ** 2 + r[1] ** 2, 1.5)

def forceDueToDragUnitConstants(v, m):
	return - NU * v * m

def boundingForce(x, q, n):
	r = np.linalg.norm(x)
	xUnit = x / r
	return  - K_E * n * q * q * xUnit / pow(particlesim.R_MAX - r, 2)

def boundingForceUnitConstants(x, q, n):
	r = np.linalg.norm(x)
	xUnit = x / r
	return  - xUnit * q / pow(particlesim.R_MAX - r, 2)

def moveParticles(particles, t, boundary):
	q = 1.0 / len(particles)
	for i, particle in enumerate(particles):
		other_particles = particles[:i] + particles[i + 1:]
		displacements = map(lambda p: p.x - particle.x, other_particles)
		forces = map(lambda r: forceBetweenTwoPointChargesUnitConstants(r, q**2), displacements)
		F = sum(forces) + boundingForceUnitConstants(particle.x, q, len(particles))
		x0, v0 = particle.x, particle.v
		Fd = forceDueToDragUnitConstants(v0, M)
		a = (F + Fd) / M
		v = a * t + v0
		x = x0 + (v + v0) / 2
		particle.x, particle.v, particle.F, particle.Fd = x, v, F, Fd

def main():
	n, iterations = 100, 1000
	folder = 'data/electrostatic n={} iter={}'.format(n, iterations)
	data = particlesim.simulate(iterations, n, moveParticles, folder)
	particlesim.motionAnimation(data, 15)

if __name__ == '__main__':
	main()