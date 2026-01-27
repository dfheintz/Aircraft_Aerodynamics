from matplotlib import pyplot as plt

from flows import *
from flow_field import FlowField

uniform = UniformFlow(10)

h_values = np.linspace(0.1, 1, 100)
c_l = np.zeros(len(h_values))
for i, h in enumerate(h_values):
    f = FlowField(size=(20, 10), plot=False)

    f.add(uniform)
    f.add_wing_ground_effect(10, 0, h)

    c_l[i] = f.get_lift_coefficient(1)

c_l_infinity = 2 * np.pi * np.sin(10 * np.pi / 180)


fig, ax = plt.subplots()
ax.set_title(r"Airfoil in Ground Effect (AOA = $10\degree$)")
ax.set(xlim=(0, 1), ylim=(0, 13), xlabel="$h/c$", ylabel=r"$C_L$")
ax.plot([0, 1], [c_l_infinity, c_l_infinity], "k--", label=r"$C_{L\infty}$")
ax.plot(h_values, c_l, "r", label=r"$C_L$")
ax.legend()
plt.show()

