from flows import *
from flow_field import FlowField

uniform = UniformFlow(5)

f = FlowField(size=(50, 40), resolution=(50, 40), equal_axis=True)

f.add(uniform)
f.add_cylinder(10, angular_velocity=0.05)

f.plot_pressure_coefficient_cylinder()
