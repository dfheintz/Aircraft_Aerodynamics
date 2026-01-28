import matplotlib.pyplot as plt
import numpy as np
import csv


naca_2218 = np.loadtxt("NACA_2218.dat")
modified = np.loadtxt("modified.dat")

fig, ax = plt.subplots()

ax.plot(naca_2218[:, 0], naca_2218[:, 1], "r", label="original")
ax.plot(modified[:, 0], modified[:, 1], "b--", label="modified", alpha=0.5)
ax.set_title("NACA 2218 vs. Modified Airfoil")
ax.set(xlabel='x/c', ylabel='y/c', xlim=(-.05, 1.05), ylim=(-.1, .2))
ax.set_aspect("equal")
ax.legend(loc="upper right")
ax.grid()

plt.show()
