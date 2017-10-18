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

def angleBetweenTwoVectors(a, b):
	return np.arccos(np.dot(a,b) / (np.linalg.norm(a,2) * np.linalg.norm(b,2)))

def distanceMatrix(x):
	distances = np.zeros((len(x), len(x)))
	for i in range(len(x)):
		for j in range(i + 1):
			d_ij = np.linalg.norm(x[i] - x[j])
			distances[i,j] = d_ij
			distances[j,i] = d_ij
	return distances

def expectedNormMultivariateGaussian(sigma):
	N = 2.0
	# formula derived in https://arxiv.org/abs/1012.0621
	# https://math.stackexchange.com/questions/827826/average-norm-of-a-n-dimensional-vector-given-by-a-normal-distribution
	return sigma * math.sqrt(2) * math.gamma((N+1)/2) / math.gamma(N/2)