import matplotlib.pyplot as plt
import numpy as np


main_element = np.loadtxt("main_element.dat")
flap = np.loadtxt("flap.dat")
retracted = np.loadtxt("retracted.dat")


def plot_extended_airfoil():
    fig, ax = plt.subplots()

    ax.plot(main_element[:, 0], main_element[:, 1], "r", label="Main element")
    ax.plot(flap[:, 0], flap[:, 1], "r", label="Flap")
    ax.set_title(
        "Main Element and Flap (NACA 64-210)\n($\delta_f=30\degree$, gap=$1.5\%$, overlap=$1\%$)"
    )
    ax.set(xlabel="x/c", ylabel="y/c", xlim=(-0.05, 1.05), ylim=(-0.2, 0.15))
    ax.set_aspect("equal")
    ax.grid()

    plt.show()


def plot_retracted_airfoil():
    fig, ax = plt.subplots()

    ax.plot(retracted[:, 0], retracted[:, 1], "b", label="Flap")
    ax.set_title(
        "Retracted airfoil (NACA 64-210)"
    )
    ax.set(xlabel="x/c", ylabel="y/c", xlim=(-0.05, 1.05), ylim=(-0.15, 0.15))
    ax.set_aspect("equal")
    ax.grid()

    plt.show()

plot_retracted_airfoil()

