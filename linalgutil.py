import numpy as np
import math

def polarToCart(z):
	r, theta = z
	return np.array((r * np.sin(theta), r * np.cos(theta)))

def cartToPolar(y):
	theta = np.arctan2(y[0], y[1])
	r = np.linalg.norm(y,2)
	return np.array((r, theta))

def boundPoint(x, rMax):
	r, theta = cartToPolar(x)
	return polarToCart((np.min([r, rMax]), theta))

def boundPointBelow(x, rMin):
	r, theta = cartToPolar(x)
	return polarToCart((np.max([r, rMin]), theta))

def angleBetweenTwoVectors(a, b):
	return np.arccos(max(min(np.dot(a,b) / (np.linalg.norm(a,2) * np.linalg.norm(b,2)),1),-1))

def distanceMatrix(x, y):
	# Arrays in (x, y, space) dimension order
	x_rep = np.repeat(x[:, :, np.newaxis], len(y), axis=2).transpose(0, 2, 1)
	y_rep = np.repeat(y[:, :, np.newaxis], len(x), axis=2).transpose(2, 0, 1)
	distances = np.linalg.norm(x_rep - y_rep, axis=2)
	return distances

def expectedNormMultivariateGaussian(sigma):
	N = 2.0
	# formula derived in https://arxiv.org/abs/1012.0621
	# https://math.stackexchange.com/questions/827826/average-norm-of-a-n-dimensional-vector-given-by-a-normal-distribution
	return sigma * math.sqrt(2) * math.gamma((N+1)/2) / math.gamma(N/2)

def normalVector(x):
	r, theta = cartToPolar(x)
	return polarToCart((r, theta + np.pi/2))