import matplotlib.pyplot as plt
import numpy as np

blade_2 = np.loadtxt("default.dat", skiprows=5)
blade_3= np.loadtxt("3_blade.dat", skiprows=5)
blade_4= np.loadtxt("4_blade.dat", skiprows=5)

fig, ax = plt.subplots()
ax.set_title("Propulsive Efficiency (T = 2.5N)")
ax.plot(blade_2[:, 0], blade_2[:, 7] / 100, "r", label="2 blades")
ax.plot(blade_3[:, 0], blade_3[:, 7] / 100, "b", label="3 blades")
ax.plot(blade_4[:, 0], blade_4[:, 7] / 100, "g", label="4 blades")
ax.set(ylabel=r"$\eta$", xlabel=r"J")
ax.grid()
ax.legend(loc="upper right")

plt.show()