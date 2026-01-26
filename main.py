from flows import *
from flow_field import FlowField

uniform = UniformFlow(10)

f = FlowField(size=(50, 40), resolution=(500, 400), arrow_length=2, equal_axis=True)

f.add(uniform)
f.add_cylinder(10, angular_velocity=0.05)

f.plot_absolute_velocity()
