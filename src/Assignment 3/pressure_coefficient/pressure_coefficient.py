import matplotlib.pyplot as plt
import numpy as np

main_element = np.loadtxt("main_element_cp.dat", skiprows=12)
flap = np.loadtxt("flap_cp.dat", skiprows=12)
retracted = np.loadtxt("retracted_cp.dat", skiprows=12)
main_element_5_deg = np.loadtxt("main_element_cp_5_deg.dat", skiprows=12)
flap_5_deg = np.loadtxt("flap_cp_5_deg.dat", skiprows=12)
main_element_gap = np.loadtxt("main_element_cp_gap.dat", skiprows=12)
flap_gap = np.loadtxt("flap_cp_gap.dat", skiprows=12)
main_element_overlap = np.loadtxt("main_element_cp_overlap.dat", skiprows=12)
flap_overlap = np.loadtxt("flap_cp_overlap.dat", skiprows=12)


def plot_extended_cp():
    fig, ax = plt.subplots()

    ax.set_title("$C_P$ Distribution Extended Airfoil\n($\delta_f=30\degree$, $overlap=1\%$ Re=4e6)")
    ax.set(ylabel="$C_P$", xlabel="x/c", ylim=(-20, 1.5))
    ax.invert_yaxis()
    ax.plot(main_element[:,0], main_element[:,2], "k--", alpha=0.5)
    ax.plot(main_element_gap[:, 0], main_element_gap[:, 2], "r", alpha=0.7)
    ax.plot(flap[:, 0], flap[:, 2], "k--", alpha=0.5)
    ax.plot(flap_gap[:, 0], flap_gap[:, 2], "r", alpha=0.7)
    ax.legend(["gap=$1.5\%$, $C_L=0.500$", "gap=$3.5\%$, $C_L=0.283$"], loc="upper left")
    ax.grid()
    plt.show()

def plot_retracted_cp():
    fig, ax = plt.subplots()

    ax.set_title("$C_P$ Distribution Retracted Airfoil\n($C_L=0.5,Re=4e6, M=0$)")
    ax.set(ylabel="$C_P$", xlabel="x/c")
    ax.invert_yaxis()
    ax.plot(retracted[:,0], retracted[:,2], c="b", label="original")
    ax.grid()
    plt.show()

plot_extended_cp()