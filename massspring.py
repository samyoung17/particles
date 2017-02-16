from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def MassSpring(state,t):
  x = state[0]
  xd = x
  return [xd]

state0 = [1.0]
t = np.arange(0.0, 10.0, 0.1)

state = odeint(MassSpring, state0, t)

plt.plot(t, state)
plt.xlabel('TIME (sec)')
plt.ylabel('STATES')
plt.title('Mass-Spring System')
plt.legend(('$x$ (m)', '$\dot{x}$ (m/sec)'))

plt.show()
