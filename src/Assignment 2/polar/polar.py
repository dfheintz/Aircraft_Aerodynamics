import matplotlib.pyplot as plt
import numpy as np

NACA_2218 = np.loadtxt("NACA_2218_polar.dat", skiprows=12)
modified = np.loadtxt("modified_polar.dat", skiprows=12)


def plot_xtr():
    fig, ax = plt.subplots()
    ax.set_title("NACA 2218 vs. Modified Airfoil Transition Point Location\n($Re=8e5, M=0$)")
    ax.plot(NACA_2218[:, 0], NACA_2218[:, 5], "k", label="upper surface")
    ax.plot(modified[:, 0], modified[:, 5], "k--", label="lower surface")
    ax.plot(NACA_2218[:, 0], NACA_2218[:, 5], "r", label="NACA 2218")
    ax.plot(NACA_2218[:, 0], NACA_2218[:, 6], "r--", label=None)
    ax.plot(modified[:, 0], modified[:, 5], "b", label="modified")
    ax.plot(modified[:, 0], modified[:, 6], "b--", label=None)
    ax.set(xlabel=r"$\alpha$ [$\degree$]", ylabel=r"x/c", ylim=(0.1, 1.2))
    ax.grid()
    ax.legend(loc="upper left")

    plt.show()


def plot_cd():
    fig, ax = plt.subplots()
    ax.set_title("NACA 2218 Drag Polar\n($Re=8e5, M=0$)")
    ax.plot(NACA_2218[:, 0], NACA_2218[:, 3])
    ax.set(xlabel=r"$\alpha$ [$\degree$]", ylabel=r"$C_D$")
    ax.grid()

    plt.show()


plot_xtr()