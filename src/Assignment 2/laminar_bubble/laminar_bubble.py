import matplotlib.pyplot as plt
import numpy as np

viscous = np.loadtxt('viscous_cp.dat', skiprows=3)
potential = np.loadtxt('potential_cp.dat', skiprows=3)

fig, ax = plt.subplots()

ax.set_title("NACA 2218 Viscous vs. Potential Flow Pressure Distribution\n($C_L = 0.4, Re=3e5, M=0$)")
ax.set(xlabel = "$x/c$", ylabel = "$C_P$")
ax.plot(viscous[:,0], viscous[:,2], c='r', label='Viscous Flow')
ax.plot(potential[:,0], potential[:,2], c='b', label='Potential Flow')
ax.legend()
ax.invert_yaxis()

plt.show()