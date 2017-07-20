import matplotlib.pyplot as plt
import numpy as np
import particlesim

data = particlesim.loadData("n=400 iter=10000 unit forces and constants.pickle")
finalPos = data.x[-1,::]
x = filter(lambda xi: np.linalg.norm(xi) <100, finalPos)
r = map(np.linalg.norm, x)
plt.hist(r, bins=20)