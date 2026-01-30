import os
import subprocess
import numpy as np
from matplotlib import pyplot as plt

xfoil_path = "C:\\Users\\dfhei\\Desktop\\School\\Aircraft_Aerodynamics\\Aircraft_Aerodynamics_exercises\\src\\xfoil.exe"
airfoil_name = 2218
reynolds_number = 8e5
transition_points = np.linspace(0, 1, 100)

def run_xfoil(path, airfoil, re, points):
    # set-up
    input_file = open("fixed_transition_input_file.in", 'w')
    input_file.write(f"NACA {airfoil}\n")
    input_file.write("OPER\n")
    input_file.write(f"Visc {re}\n")
    input_file.write("ITER 500\n")

    for i, point in enumerate(points):
        if os.path.exists(f"fixed_transition_{i}.dat"):
            os.remove(f"fixed_transition_{i}.dat")

        input_file.write("vpar\n")
        input_file.write("xtr\n")
        input_file.write(f"{point}\n\n\n")
        input_file.write("pacc\n")
        input_file.write(f"fixed_transition_{i}.dat\n\n")
        input_file.write("cl 0.4\n")
        input_file.write("pacc\n")
        input_file.write("pdel\n")
        input_file.write("0\n")

    input_file.write("\nquit\n")
    input_file.close()

    subprocess.call(f"{path} < fixed_transition_input_file.in", shell=True)


def process_data(points):
    c_d = np.zeros(len(points))

    for i, point in enumerate(points):
        data = np.loadtxt(f"fixed_transition_{i}.dat", skiprows=12)

        c_d[i] = data[2]

    return c_d

# run_xfoil(xfoil_path, airfoil_name, reynolds_number, transition_points)
c_d = process_data(transition_points)

fig, ax = plt.subplots()
ax.set_title("NACA 2218 Drag Coefficient for different Transition Points\n($C_L = 0.4, Re=8e5, M=0$)")
ax.set(ylabel=r"$C_D$", xlabel=r"x/c", ylim=(0.0081, 0.0114))
ax.grid()
ax.plot([0.37777, 0.37777], [0.0, 1], "k--", alpha=0.5)

ax.plot(transition_points, c_d)
ax.legend(["Non-forced transition point"])
plt.show()

