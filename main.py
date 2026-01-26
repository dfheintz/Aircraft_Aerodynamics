from flows import *
from flow_field import FlowField

uniform = UniformFlow(10)

f = FlowField(size=(5, 5), resolution=(5, 5), arrow_length=2, equal_axis=True)

f.add(uniform)
f.add_wing(10)

f.plot_stream_lines(20, dt=0.001)
print(f.get_lift_coefficient(1))