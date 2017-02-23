import matplotlib.pyplot as plt
import numpy as np
from particles import *

data = loadData("unit model n=100 iter=10000.pickle")
finalPos = data.x[-1,::]
x = filter(lambda xi: np.linalg.norm(xi) <100, finalPos)
r = map(np.linalg.norm, x)
plt.hist(r, bins=10)