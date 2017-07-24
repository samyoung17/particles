import numpy as np

def polarToCart(z):
	r, theta = z
	return np.array((r * np.sin(theta), r * np.cos(theta)))

def cartToPolar(y):
	theta = np.arctan2(y[0], y[1])
	r = np.linalg.norm(y,2)
	return np.array((r, theta))

def angleBetweenTwoVectors(a, b):
	return np.arccos(np.dot(a,b) / (np.linalg.norm(a,2) * np.linalg.norm(b,2)))
