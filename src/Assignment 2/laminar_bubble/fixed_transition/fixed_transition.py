import os
import subprocess
import numpy as np
from matplotlib import pyplot as plt

xfoil_path = "C:\\Users\\dfhei\\Desktop\\School\\Aircraft_Aerodynamics\\Aircraft_Aerodynamics_exercises\\src\\xfoil.exe"
airfoil_name = 2218
c_l = 0.8
reynolds_number = 3e5
transition_points = np.linspace(0, 1, 50)

def run_xfoil(path, airfoil, re, points):
    # set-up
    input_file = open("fixed_transition_input_file.in", 'w')
    input_file.write(f"NACA {airfoil}\n")
    input_file.write("OPER\n")
    input_file.write(f"Visc {re}\n")
    input_file.write("ITER 100000\n")
    input_file.write(f"vpar\n")
    input_file.write(f"n\n")
    input_file.write(f"12\n\n")

    for i, point in enumerate(points):
        if os.path.exists(f"fixed_transition_{i}.dat"):
            os.remove(f"fixed_transition_{i}.dat")

        input_file.write("vpar\n")
        input_file.write("xtr\n")
        input_file.write(f"{point}\n\n\n")
        input_file.write("pacc\n")
        input_file.write(f"fixed_transition_{i}.dat\n\n")
        input_file.write(f"cl {c_l}\n")
        input_file.write("pacc\n")
        input_file.write("pdel\n")
        input_file.write("0\n")

    input_file.write("\nquit\n")
    input_file.close()

    subprocess.call(f"{path} < fixed_transition_input_file.in", shell=True)


def process_data(points):
    c_d = np.zeros(len(points))
    c_d_p = np.zeros(len(points))
    c_d_f = np.zeros(len(points))

    for i, point in enumerate(points):
        data = np.loadtxt(f"fixed_transition_{i}.dat", skiprows=12)
        c_d[i] = data[2]
        c_d_p[i] = data[3]
        c_d_f[i] = data[2] - data[3]


    return c_d, c_d_p, c_d_f

# run_xfoil(xfoil_path, airfoil_name, reynolds_number, transition_points)
c_d, c_d_p, c_d_f = process_data(transition_points)

fig, ax = plt.subplots()
ax.set_title("NACA 2218 Drag Coefficient for different Transition Points\n($C_L = 0.8, Re = 3e5, M=0$)")
ax.set(ylabel=r"$C_D$", xlabel=r"x/c", ylim=(0, 0.019))
ax.grid()
ax.plot(transition_points, c_d, "r", label="$C_D$")
ax.plot(transition_points, c_d_p, "b", label="$C_{D_p}$")
ax.plot(transition_points, c_d_f, "g", label="$C_{D_f}$")
ax.plot([0.3061, 0.3061], [0, 0.019], "k--", alpha=0.4, label="$xtr=0.31$")
ax.legend(loc="lower right")

plt.show()

