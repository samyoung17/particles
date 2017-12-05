import os
import shutil
import numpy as np
import pickle

class Data(object):

	def initShape(self, mode, iterations, numpoints, numTargets):
		if mode == 'w+':
			self.shape[0] = iterations
			self.shape[1] = numpoints
			self.shape[2] = numTargets
		return tuple(self.shape)

	def initBoundary(self, folder, boundary):
		if boundary is None:
			f = open(folder + '/boundary.pickle', 'r')
			self.boundary = pickle.load(f)
			f.close()
		else:
			f = open(folder + '/boundary.pickle', 'w')
			pickle.dump(boundary, f)
			f.close()
			self.boundary = boundary

	def initFolder(self, folder, mode):
		if mode == 'w+':
			if os.path.isdir(folder):
				shutil.rmtree(folder)
			os.mkdir(folder)

	def __init__(self, folder, mode, iterations=0, numpoints=0, numTargets=0, boundary=None):
		self.initFolder(folder, mode)
		self.initBoundary(folder, boundary)
		self.shape = np.memmap(folder + '/shape.dat', dtype='int', mode=mode, shape=(3))
		iterations, numpoints, numTargets = self.initShape(mode, iterations, numpoints, numTargets)
		self.iterations = iterations
		self.x = np.memmap(folder + '/x.dat', dtype='float32', mode=mode, shape=(iterations, numpoints, 2))
		self.v = np.memmap(folder + '/v.dat', dtype='float32', mode=mode, shape=(iterations, numpoints, 2))
		self.F = np.memmap(folder + '/F.dat', dtype='float32', mode=mode, shape=(iterations, numpoints, 2))
		self.Fd = np.memmap(folder + '/Fd.dat', dtype='float32', mode=mode, shape=(iterations, numpoints, 2))
		self.t = np.memmap(folder + '/t.dat', dtype='float32', mode=mode, shape=(iterations))
		self.y = np.memmap(folder + '/y.dat', dtype='float32', mode=mode, shape=(iterations, numTargets, 2))
