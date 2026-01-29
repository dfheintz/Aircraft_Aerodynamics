import matplotlib.pyplot as plt
import numpy as np

extended = np.loadtxt("extended_lift_polar.dat", skiprows=5)
retracted = np.loadtxt("retracted_lift_polar.dat", skiprows=5)

fig, ax = plt.subplots()
ax.set_title("Extended vs. Retracted Flap Lift Polars\n($Re=4e6$, $\delta_f$=$30\degree$, gap=$1.5\%$, overlap=$1\%$)")
ax.plot(extended[1:41, 0], extended[1:41, 1], "r", label="flap extended")
ax.plot(retracted[21:55, 0], retracted[21:55, 1], "b", label="flap retracted")
ax.set(ylabel=r"$C_L$", xlabel=r"$\alpha\degree$", xlim=(-20, 15))
ax.grid()
ax.legend(loc="upper right")


plt.show()