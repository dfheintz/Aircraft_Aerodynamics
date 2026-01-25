from typing import Optional

from flows import *
import numpy as np
import matplotlib.pyplot as plt


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

    def plot_stream_function(self) -> None:
        """
        Plots the stream function of the flow field.

        :return: None
        """
        self._plot_scalar("stream_function", "Stream Function")

    def plot_potential_function(self) -> None:
        """
        Plots the potential function of the flow field.

        :return: None
        """
        self._plot_scalar("potential_function", "Potential Function")

    def plot_absolute_velocity(self) -> None:
        """
        Plots the absolute velocity of the flow field.

        :return: None
        """
        self._plot_scalar("absolute_velocity", "Absolute Velocity")

    def _plot_scalar(self, function, title) -> None:
        """
        Private method that evaluates and plots the scalar values of the function in the flow field.

        :param function: function of the canonical flows to be evaluated.
        :param title: title of the plot.
        :return: None
        """
        # get the coordinates of all the points where the function should be evaluated at.
        x_values = np.linspace(self.x_min, self.x_max, self.resolution[0])
        y_values = np.linspace(self.y_min, self.y_max, self.resolution[1])

        # compute the function at each point and sum the contribution of each canonical flow in the flow field
        z_values = np.zeros(self.resolution).T
        for i, x in enumerate(x_values):
            for j, y in enumerate(y_values):
                for flow in self.flows:
                    method = getattr(flow, function)
                    z_values[j, i] += method(x, y)

        # plot as a contour
        self.ax.contour(x_values, y_values, z_values)
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
                for flow in self.flows:
                    u, v = flow.velocity(x, y)
                    u_values[j, i] += u
                    v_values[j, i] += v

                    # calculate the absolute velocity for the color map
                    z_values[j, i] += flow.absolute_velocity(x, y)

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
                            color=self._rgb(float(z_values[j, i]), max_velocity, min_velocity),
                        ),
                    )

        # show the plot
        self.ax.set(
            xlim=(self.x_min, self.x_max),
            ylim=(self.y_min, self.y_max),
            xlabel="x",
            ylabel="y",
        )
        self.ax.set_title("Velocity Field")

        if self.equal_axis:
            self.ax.set_aspect("equal")

        plt.show()

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