import matplotlib.pyplot as plt
import matplotlib.animation as animation
from particles import *

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

def draw(i, scat, data):
	points = data.x[i]
	scat.set_offsets(points)
	return scat,

def motionAnimation(data, speedMultiplier):
	R_MAX = 10
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

if __name__ == '__main__':
	speedMultiplier = 1
	if len(sys.argv) == 3:
		fname = sys.argv[1]
		speedMultiplier = int(sys.argv[2])
	elif len(sys.argv) == 2:
		fname = sys.argv[1]
	else:
		raise ValueError('Arguments should be: infile, [speedmultiplier]')
	data = loadData(fname)
	motionAnimation(data, speedMultiplier)