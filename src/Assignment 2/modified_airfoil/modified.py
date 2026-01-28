import matplotlib.pyplot as plt
import numpy as np

airfoil = np.loadtxt("NACA_2218_cp.dat", skiprows=3)
modified = np.loadtxt("modified_cp.dat", skiprows=3)

fig, ax = plt.subplots()

ax.set_title("$C_P$ Distribution across Airfoils")
ax.set(ylabel="$C_P$", xlabel="x/c")
ax.invert_yaxis()
ax.plot(airfoil[:,0], airfoil[:,2], c="r", label="original")
ax.plot(modified[:,0], modified[:,2], c="b", label="modified")
ax.grid()
ax.legend()
plt.show()