import matplotlib.pyplot as plt
import numpy as np

default = np.loadtxt("default.dat", skiprows=5)
double = np.loadtxt("double_length.dat", skiprows=5)
quad = np.loadtxt("quad_length.dat", skiprows=5)

fig, ax = plt.subplots()
ax.set_title("Propulsive Efficiency (T = 2.5N)")
ax.plot(default[:, 0], default[:, 7] / 100, "r", label="⌀ = 10\"")
ax.plot(double[:, 0], double[:, 7] / 100, "b", label="⌀ = 20\"")
ax.plot(quad[:, 0], quad[:, 7] / 100, "g", label="⌀ = 40\"")
ax.set(ylabel=r"$\eta$", xlabel=r"J")
ax.grid()
ax.legend(loc="upper right")

plt.show()