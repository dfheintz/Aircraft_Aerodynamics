from flows import *
from flow_field import FlowField

uniform = UniformFlow(10)

f = FlowField(size=(50, 25), resolution=(35, 25), arrow_length=2, equal_axis=True)

f.add(uniform)
f.add_cylinder(5, angular_velocity=0.35)

# f.plot_velocity()
f.plot_stream_lines(20)
