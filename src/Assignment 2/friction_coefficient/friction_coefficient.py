import matplotlib.pyplot as plt
import numpy as np

alpha_0 = np.loadtxt("alpha_0.dat", skiprows=1)
alpha_4 = np.loadtxt("alpha_4.dat", skiprows=1)

fig, ax = plt.subplots()

ax.set_title("NACA 2218 Friction Coefficient along Upper Surface\n($Re=8e5, M=0$)")
ax.plot(alpha_0[0:82, 1], alpha_0[0:82, 6], "r", label=r"$\alpha=0\degree$")
ax.plot(alpha_4[0:82, 1], alpha_4[0:82, 6], "b", label=r"$\alpha=4\degree$")
ax.set(ylabel=r"$C_f$", xlabel=r"x/c")
ax.grid()
ax.legend()


plt.show()
