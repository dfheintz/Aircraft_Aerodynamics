from flows import *
from flow_field import FlowField

vortex = Vortex(-10, 0, 10)

f = FlowField(size=(100, 50), resolution=(50, 25), arrow_length=2)

f.add(vortex)

f.plot_velocity()