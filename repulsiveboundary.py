import hardboundary
import numpy as np
import linalgutil as la
import shapely.geometry as geom
import matplotlib.pyplot as plt


class Circle(object):

	def __init__(self, r):
		self.rMax = float(r)
		self.circle = geom.Point(0,0).buffer(float(r)).boundary
		self.hardedge = hardboundary.Circle(r)

	def force(self, x, q):
		r, theta = la.cartToPolar(x)
		xUnit = la.polarToCart((q, theta))
		return - xUnit * q

	def contains(self, x):
		return np.linalg.norm(x) < self.rMax

	def plot(self, axes):
		circle = plt.Circle((0,0), radius=self.rMax, color='g', fill=False)
		axes.add_patch(circle)

	def bounceIfHits(self, x0, v0, x, v):
		return self.hardedge.bounceIfHits(x0, v0, x, v)
