from typing import Optional

from flows import *
import numpy as np
import matplotlib.pyplot as plt
import scipy


class FlowField:
    """
    Defines a flow field class.

    Plots a potential flow field and allows for different canonical flows to be added to it.
    Uses the principle of superposition to calculate the flow properties throughout the flow.
    """

    def __init__(
        self,
        size: tuple[int, int],
        center: tuple[int, int] = (0, 0),
        resolution: Optional[tuple[int, int]] = None,
        arrow_length: float = 1,
        equal_axis: bool = False,
    ) -> None:
        """
        Initializes the flow field.

        :param size: width and height of the flow field.
        :param center: x and y coordinate of the center of the flow field.
        :param resolution: resolution of the flow field in the x and y direction.
        :param arrow_length: length of the arrows displayed for the velocity flow field.
        :param equal_axis: whether the axis of the flow field should be equal or not.
        """
        self.size = size
        self.center = center
        self.arrow_length = arrow_length
        self.equal_axis = equal_axis
        self._has_cylinder = False
        self._cylinder_radius = -1
        self._cylinder_x_0 = 0
        self._cylinder_y_0 = 0

        # if no resolution is passed in the flow field make the resolution equal to the size.
        if resolution is None:
            self.resolution = (size[0] + 1, size[1] + 1)
        else:
            self.resolution = (resolution[0], resolution[1])

        self.flows = []  # list to add the canonical flows to

        self.fig, self.ax = plt.subplots()

        # min and max coordinates of the flow field
        self.x_min = self.center[0] - self.size[0] / 2
        self.x_max = self.center[0] + self.size[0] / 2
        self.y_min = self.center[1] - self.size[1] / 2
        self.y_max = self.center[1] + self.size[1] / 2

    def add(self, flow: BaseFlow) -> None:
        """
        Adds a flow to the flow field.

        :param flow: canonical flow.
        :return: None
        """
        self.flows.append(flow)

    def add_cylinder(
        self,
        radius: float,
        x_0: float = 0,
        y_0: float = 0,
        angular_velocity: Optional[float] = None,
        xtol: float = 1e-3,
    ) -> None:
        """
        Adds a cylinder to the flow at position x_0, y_0 with a given radius. The cylinder will be represented by
        a doublet flow. The strength of the doublet will be calculated by enforcing non-penetration boundary condition
        at the front edge of the cylinder. This is achieved by making the velocity contribution in the x direction of
        the uniform flow and doublet flow equal 0 at the front edge.

        :param radius: radius of the cylinder.
        :param x_0: x position of the center of the cylinder.
        :param y_0: y position of the center of the cylinder.
        :param angular_velocity: angular velocity of the cylinder.
        :param xtol: tolerance for fsolve which solves for the strength of the doublet and vortex.
        :return: None
        """
        # these values are used when plotting to not include areas inside the cylinder
        self._cylinder_radius = radius
        self._has_cylinder = True
        self._cylinder_x_0 = x_0
        self._cylinder_y_0 = y_0

        uniform = self._check_has_uniform_flow()

        doublet = Doublet(x_0, y_0, -1)  # initialize the doublet flow

        # function that calculates the difference between the uniform flow and
        def doublet_strength(x):
            doublet.strength = x

            return doublet.velocity_x(x_0 - radius, y_0) + uniform.velocity_x(
                x_0 - radius, y_0
            )

        strength = scipy.optimize.fsolve(doublet_strength, np.ones(1), xtol=xtol)
        doublet.strength = strength[0]

        self.add(doublet)

        # add vortex to represent a rotating cylinder
        if angular_velocity is not None:
            surface_velocity = 2 * np.pi * angular_velocity * radius

            vortex = Vortex(x_0, y_0, -1)

            def vortex_strength(x):
                vortex.strength = x

                return vortex.velocity_y(x_0 - radius, y_0) - surface_velocity

            strength = scipy.optimize.fsolve(vortex_strength, np.ones(1), xtol=xtol)

            vortex.strength = strength[0]

            self.add(vortex)

    def add_stream_line(
        self,
        x_start: float,
        y_start: float,
        dt: float = 0.1,
        max_iterations: float = 1e6,
    ):
        x_values, y_values = self._stream_line(
            x_start, y_start, dt, round(max_iterations)
        )
        plt.plot(x_values, y_values)

    def plot_stream_function(self) -> None:
        """
        Plots the stream function of the flow field.

        :return: None
        """
        X, Y, Z = self._get_scalar_field("stream_function")

        # plot as a contour
        self.ax.contourf(X, Y, Z)
        self.plot("Stream Function")

    def plot_potential_function(self) -> None:
        """
        Plots the potential function of the flow field.

        :return: None
        """
        X, Y, Z = self._get_scalar_field("potential_function")

        # plot as a contour
        self.ax.contourf(X, Y, Z)
        self.plot("Potential Function")

    def plot_velocity_x(self) -> None:
        """
        Plots the velocity component in the x direction of the flow field.

        :return: None
        """
        X, Y, Z = self._get_scalar_field("velocity_x")

        # plot as a contour
        self.ax.contourf(X, Y, Z)
        self.plot("Velocity X Component")

    def plot_velocity_y(self) -> None:
        """
        Plots the velocity component in the y direction of the flow field.

        :return: None
        """
        X, Y, Z = self._get_scalar_field("velocity_y")

        # plot as a contour
        self.ax.contourf(X, Y, Z)
        self.plot("Velocity Y Component")

    def plot_velocity(self) -> None:
        """
        Plots the velocity of the flow field as arrows.

        :return: None
        """
        # get the coordinates of all the points where the velocity should be evaluated at.
        x_values = np.linspace(self.x_min, self.x_max, self.resolution[0])
        y_values = np.linspace(self.y_min, self.y_max, self.resolution[1])

        # compute the velocity components at each point and sum the contribution of each canonical flow in the flow
        u_values = np.zeros(self.resolution).T
        v_values = np.zeros(self.resolution).T
        z_values = np.zeros(self.resolution).T
        for i, x in enumerate(x_values):
            for j, y in enumerate(y_values):
                if self._is_inside_cylinder(x, y) and self._has_cylinder:
                    u_values[j, i] = 0
                    v_values[j, i] = 0
                else:
                    for flow in self.flows:
                        u, v = flow.velocity(x, y)
                        u_values[j, i] += u
                        v_values[j, i] += v

                # calculate the absolute velocity for the color map
                z_values[j, i] = np.sqrt(u_values[j, i] ** 2 + v_values[j, i] ** 2)

        # get min and max velocities for the color map
        min_velocity = np.min(z_values)
        max_velocity = np.max(z_values)

        # plot an arrow at each evaluated point
        for i, x in enumerate(x_values):
            for j, y in enumerate(y_values):
                angle = np.arctan2(v_values[j, i], u_values[j, i])
                dx = x_values[i] + self.arrow_length * np.cos(angle)
                dy = y_values[j] + self.arrow_length * np.sin(angle)

                if z_values[j, i] == 0:
                    self.ax.annotate(
                        "",
                        (float(x_values[i]), float(y_values[j])),
                        (float(x_values[i]), float(y_values[j])),
                        arrowprops=dict(arrowstyle="->"),
                    )
                else:
                    self.ax.annotate(
                        "",
                        (dx, dy),
                        (float(x_values[i]), float(y_values[j])),
                        arrowprops=dict(
                            arrowstyle="->",
                            color=self._rgb(
                                float(z_values[j, i]), max_velocity, min_velocity
                            ),
                        ),
                    )

        # show the plot
        self.plot("Velocity Field")

    def plot_absolute_velocity(self) -> None:
        """
        Plots the absolute velocity in the flow field.

        :return: None
        """
        X, Y, vel_x = self._get_scalar_field("velocity_x")
        _, _, vel_y = self._get_scalar_field("velocity_y")

        Z = np.sqrt(np.square(vel_x) + np.square(vel_y))

        # plot as a contour
        self.ax.contourf(X, Y, Z)
        self.plot("Absolute velocity")

    def plot_pressure_coefficient(self) -> None:
        freestream = self._check_has_uniform_flow()

        """
        Plots the pressure coefficient in the flow field.

        :return: None
        """
        X, Y, vel_x = self._get_scalar_field("velocity_x")
        _, _, vel_y = self._get_scalar_field("velocity_y")

        Z = 1 - np.square(np.sqrt(np.square(vel_x) + np.square(vel_y)) / freestream)

        # plot as a contour
        self.ax.contourf(X, Y, Z)
        self.plot("Pressure Coefficient")

    def plot_pressure_coefficient_cylinder(self, res: int = 100) -> None:
        """
        Plot the pressure coefficient across the surface of the cylinder.

        :param res: resolution of the plot.
        :return: None
        """
        if not self._has_cylinder:
            Exception("The flow has no cylinder added.")

        uniform = self._check_has_uniform_flow()

        angles = np.linspace(0, 2 * np.pi, res)
        x_values = np.zeros(len(angles))
        y_values = np.zeros(len(angles))

        for i, theta in enumerate(angles):
            x_values[i] = self._cylinder_radius * np.cos(theta) - self._cylinder_x_0
            y_values[i] = self._cylinder_radius * np.sin(theta) - self._cylinder_y_0

        surface = np.zeros(len(x_values))
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            u = v = 0
            for flow in self.flows:
                du, dv = flow.velocity(x, y)
                u += du
                v += dv

            velocity = np.sqrt(u**2 + v**2)
            surface[i] = 1 - (velocity / uniform.freestream_velocity) ** 2

        plt.plot(angles, surface, "r")
        self.ax.yaxis.set_inverted(True)
        plt.show()

    def plot(self, title: Optional[str] = None) -> None:
        """
        Plot the current graph. Used after streamlines are added.

        :param title: title of the plot.
        :return: None
        """
        if title is None:
            title = "Flow Field"

        # show the plot
        self.ax.set(
            xlim=(self.x_min, self.x_max),
            ylim=(self.y_min, self.y_max),
            xlabel="x",
            ylabel="y",
        )
        self.ax.set_title(title)

        if self.equal_axis:
            self.ax.set_aspect("equal")

        plt.show()

    def plot_stream_lines(
        self,
        num: int,
        x_start: Optional[float] = None,
        dt: float = 0.1,
        max_iterations: float = 1e6,
    ) -> None:
        """
        Plot a vertical line of equally spaced streamlines starting at x_start.

        :param num: number of streamlines to plot.
        :param x_start: x coordinate to start streamlines at.
        :param dt: size of the time step when computing the streamlines.
        :param max_iterations: maximum number of iterations of calculating the streamlines.
        :return: None
        """
        if x_start is None:
            x_start = self.x_min

        y_0 = np.linspace(self.y_min, self.y_max, num)

        for y in y_0:
            x_values, y_values = self._stream_line(
                x_start, y, dt, round(max_iterations)
            )
            plt.plot(x_values, y_values)

        # show the plot
        self.plot("Streamlines")

    def _get_scalar_field(self, function) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Private method that evaluates and plots the scalar values of the function in the flow field.

        :param function: function of the canonical flows to be evaluated.
        :return: None
        """
        # get the coordinates of all the points where the function should be evaluated at.
        x_values = np.linspace(self.x_min, self.x_max, self.size[0] * 10)
        y_values = np.linspace(self.y_min, self.y_max, self.size[1] * 10)

        # compute the function at each point and sum the contribution of each canonical flow in the flow field
        z_values = np.zeros((self.size[0] * 10, self.size[1] * 10)).T
        mask = np.zeros((self.size[0] * 10, self.size[1] * 10)).T
        for i, x in enumerate(x_values):
            for j, y in enumerate(y_values):
                if self._is_inside_cylinder(x, y) and self._has_cylinder:
                    mask[j, i] = 1
                else:
                    for flow in self.flows:
                        method = getattr(flow, function)
                        z_values[j, i] += method(x, y)

        return x_values, y_values, np.ma.masked_array(z_values, mask=mask)

    def _stream_line(
        self, x_start: float, y_start: float, dt: float, max_iterations: int
    ) -> tuple[list[float], list[float]]:
        """
        Private method that calculates the path of a streamline starting at x_start, y_start in the flow field.

        :param x_start: x position the streamlines starts at.
        :param y_start: y position the streamlines starts at.
        :param dt: size of the time step when computing the streamlines.
        :param max_iterations: maximum number of iterations of calculating the streamlines.
        :return: x and y values of the streamlines.
        """
        x_values = [x_start]
        y_values = [y_start]

        i = 0
        while (
            self.y_min <= y_values[-1] <= self.y_max
            and self.x_min <= x_values[-1] <= self.x_max
            and i < max_iterations
        ):
            u = v = 0
            for flow in self.flows:
                du, dv = flow.velocity(x_values[-1], y_values[-1])

                u += du
                v += dv

            x_values.append(x_values[-1] + u * dt)
            y_values.append(y_values[-1] + v * dt)

            i += 1

        return x_values, y_values

    def _check_has_uniform_flow(self) -> UniformFlow:
        """
        Checks if the user has added a uniform flow to the flow field.

        :return: The uniform flow field object, if present.
        """
        has_uniform = False
        uniform = 0
        for flow in self.flows:
            if isinstance(flow, UniformFlow):
                has_uniform = True
                uniform = flow
        if not has_uniform:
            raise Exception("Must define a Uniform Flow.")

        return uniform

    def _is_inside_cylinder(self, x, y) -> bool:
        """
        Checks whether a given point is inside the cylinder.

        :param x: x coordinate to evaluate.
        :param y: y coordinate to evaluate.
        :return: True, if inside the cylinder, False otherwise.
        """
        x = x - self._cylinder_x_0
        y = y - self._cylinder_y_0

        r = np.sqrt(x**2 + y**2)

        return True if r < self._cylinder_radius else False

    @staticmethod
    def _rgb(
        value: float, max_value: float, min_value: float = 0
    ) -> tuple[float, float, float]:
        """
        Convert a scalar value to an RGB value.

        :param value: value to be converted.
        :param max_value: maximum of the value.
        :param min_value: minimum of the value.
        :return: rgb color values between 0-1
        """
        # map the input value from min-max to 0-pi
        x = value * np.pi / (max_value - min_value)

        b = (np.cos(x) + 1) / 2
        g = (np.sin(x) + 1) / 2
        r = (-np.cos(x) + 1) / 2

        return r, g, b