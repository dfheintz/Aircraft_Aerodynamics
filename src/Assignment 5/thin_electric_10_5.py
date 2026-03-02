import matplotlib.pyplot as plt
import numpy as np

sim = np.loadtxt("prop_data_bem.dat", skiprows=5)
lit = np.loadtxt("prop_data_lit.dat", skiprows=1)

fig_1, ax_1 = plt.subplots()
ax_1.set_title("Thrust Coefficient")
ax_1.plot(sim[:, 0], sim[:, 2], "r", label="javaprop")
ax_1.plot(lit[:, 0], lit[:, 1], "b", label="literature")
ax_1.set(ylabel=r"$C_T$", xlabel=r"J")
ax_1.grid()
ax_1.legend(loc="upper right")

fig_2, ax_2 = plt.subplots()
ax_2.set_title("Power Coefficient")
ax_2.plot(sim[:, 0], sim[:, 3], "r", label="javaprop")
ax_2.plot(lit[:, 0], lit[:, 2], "b", label="literature")
ax_2.set(ylabel=r"$C_P$", xlabel=r"J")
ax_2.grid()
ax_2.legend(loc="upper right")

fig_3, ax_3 = plt.subplots()
ax_3.set_title("Propulsive Efficiency")
ax_3.plot(sim[:, 0], sim[:, 7] / 100, "r", label="javaprop")
ax_3.plot(lit[:, 0], lit[:, 3], "b", label="literature")
ax_3.set(ylabel=r"$\eta$", xlabel=r"J")
ax_3.grid()
ax_3.legend(loc="upper right")


fig_4, ax_4 = plt.subplots()
ax_4.set_title("Torque Coefficient")
ax_4.plot(sim[:, 0], sim[:, 3] / 2 / np.pi, "r", label="javaprop")
ax_4.plot(lit[:, 0], lit[:, 2] / 2 / np.pi, "b", label="literature")
ax_4.set(ylabel=r"$C_Q$", xlabel=r"J")
ax_4.grid()
ax_4.legend(loc="upper right")

plt.show()