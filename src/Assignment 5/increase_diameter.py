import numpy as np

a = np.loadtxt("thin_electric_10x5")

a[:,0] = a[:,0] * 2
# a[:,1] = a[:,1] / 4

np.savetxt("longer", a)