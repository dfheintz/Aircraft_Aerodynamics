from abc import ABC, abstractmethod
import numpy as np


class BaseFlow(ABC):
    """
    Abstract base class for all canonical potential flows.

    Defines helper methods to convert between radians and angles and cartesian to polar coordinates.
    Defines a helper to transform the given coordinate to the flows local coordinate system.
    To be defined by subclasses: the stream function expression, potential function expression, and the
     function for each of the canonical flows.
    """

    def __init__(self, x_0: int, y_0: int) -> None:
        """
        Base initialize method. Sets the origin of the flow type.

        :param x_0: x position of the center
        :param y_0: y position of the center
        """
        self.x_0 = x_0
        self.y_0 = y_0

    @abstractmethod
    def stream_function(self, x: int, y: int) -> float:
        """
        Defines the stream function of the flow type given an x, y position.

        :param x: x position to evaluate the stream function at.
        :param y: y position to evaluate the stream function at.
        :return: stream function evaluated at the x, y position.
        """
        pass

    @abstractmethod
    def potential_function(self, x: int, y: int) -> float:
        """
        Defines the potential function of the flow type given an x, y position.

        :param x: x position to evaluate the potential function at.
        :param y: y position to evaluate the potential function at.
        :return: potential function evaluated at the x, y position.
        """
        pass

    @abstractmethod
    def velocity(self, x: int, y: int) -> tuple[float, float]:
        """
        Defines the velocity component in the x and y direction of the flow type given an x, y position.

        :param x: x position to evaluate the velocity at.
        :param y: y position to evaluate the velocity at.
        :return: velocity in the x direction and y direction evaluated at the x, y position.
        """
        pass

    def absolute_velocity(self, x: int, y: int) -> float:
        """
        Defines the absolute velocity of the flow type given an x, y position.

        :param x: x position to evaluate the absolute velocity at.
        :param y: y position to evaluate the absolute velocity at.
        :return: absolute velocity evaluated at the x, y position.
        """
        u, v = self.velocity(x, y)

        return np.sqrt(u**2 + v**2)

    def _transform(self,
                   x: int,
                   y: int) -> tuple[int, int]:
        """
        Transform the given global coordinates to the flow's local coordinate system.

        :param x: global x position
        :param y: global y position
        :return: local x position, local y position
        """
        return x - self.x_0, y - self.y_0

    @staticmethod
    def _to_polar_coordinates(x: int,
                              y: int) -> tuple[float, float]:
        """
        Transform cartesian to polar coordinates.

        :param x: cartesian x position.
        :param y: cartesian y position.
        :return: radius and angle that define the given coordinate.
        """
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan2(y, x)

        return r, theta

    @staticmethod
    def _to_cartesian_velocity(u_r: float,
                               u_theta: float,
                               r: float,
                               theta: float) -> tuple[float, float]:
        """
        Transform polar velocity components to cartesian velocity components.

        :param u_r: polar velocity component in the radius direction.
        :param u_theta: polar velocity component in the theta direction.
        :param r: radius of polar coordinate.
        :param theta: angle of polar coordinate.
        :return: velocity component in the x direction, velocity component in the y direction.
        """
        u = u_r * np.cos(theta) - u_theta * np.sin(theta)
        v = u_r * np.sin(theta) + u_theta * np.cos(theta)

        return u, v

    @staticmethod
    def _to_radians(angle_deg: float) -> float:
        """
        Convert degrees to radians.

        :param angle_deg: angle in degrees.
        :return: angle in radians.
        """
        return angle_deg * np.pi / 180

    @staticmethod
    def _to_degrees(angle_rad: float) -> float:
        """
        Convert radians to degrees.

        :param angle_rad: angle in radians.
        :return: angle in degrees.
        """
        return angle_rad * 180 / np.pi

    def _is_center(self,
                   x: int,
                   y: int) -> bool:
        """
        Determines if the given coordinate is at the center of the flow.
        Most of the canonical flows are not defined at their center.

        :param x: x position.
        :param y: y position.
        :return: whether the given coordinate is at the center of the flow.
        """
        if x == self.x_0 and y == self.y_0:
            return True
        else:
            return False


class UniformFlow(BaseFlow):
    """
    Uniform flow class.

    Defines the potential flow functions for a uniform flow.
    """
    def __init__(
        self,
        freestream_velocity: float,
        angle: float = 0,
        angle_units: str = "deg",
    ) -> None:
        """
        Initialize the uniform flow class.

        :param freestream_velocity: freestream velocity in m/s.
        :param angle: angle of the flow.
        :param angle_units: units of the given angle.
        """
        self.freestream_velocity = freestream_velocity

        # if the angle is given in degrees, convert to radians
        if angle_units == "rad":
            self.angle = angle
        elif angle_units == "deg":
            self.angle = self._to_radians(angle)
        else:
            Exception(
                'Invalid angle units. Either "rad" for radians or "deg" for degrees.'
            )

        # As a uniform flow is the same everywhere, the center is not important.
        super().__init__(0, 0)

    def stream_function(self, x: int, y: int) -> float:
        return self.freestream_velocity * (
            (self.y_0 + y) * np.cos(self.angle) - (self.x_0 + x) * np.sin(self.angle)
        )

    def potential_function(self, x: int, y: int) -> float:
        return self.freestream_velocity * (
            (self.x_0 + x) * np.cos(self.angle) + (self.y_0 + y) * np.sin(self.angle)
        )

    def velocity(self, x: int, y: int) -> tuple[float, float]:
        u = self.freestream_velocity * np.cos(self.angle)
        v = self.freestream_velocity * np.sin(self.angle)

        return u, v


class Vortex(BaseFlow):
    """
    Vortex flow class.

    Defines the potential flow functions for a vortex flow.
    """
    def __init__(self, x_0: int, y_0: int, strength: float) -> None:
        """
        Initialize the vortex flow class.

        :param x_0: x position of the center of the vortex.
        :param y_0: y position of the center of the vortex.
        :param strength: strength of the vortex.
        """
        self.strength = strength

        super().__init__(x_0, y_0)

    def stream_function(self, x: int, y: int) -> float:
        # check if the given coordinate is at the center of the vortex
        if self._is_center(x, y):
            return 0

        # transform to the local coordinate system
        x, y = self._transform(x, y)

        r, theta = self._to_polar_coordinates(x, y)

        return -self.strength * np.log(r) / 2 / np.pi

    def potential_function(self, x: int, y: int) -> float:
        # check if the given coordinate is at the center of the vortex
        if self._is_center(x, y):
            return 0

        # transform to the local coordinate system
        x, y = self._transform(x, y)

        r, theta = self._to_polar_coordinates(x, y)

        return self.strength * theta / 2 / np.pi

    def velocity(self, x: int, y: int) -> tuple[float, float]:
        # check if the given coordinate is at the center of the vortex
        if self._is_center(x, y):
            return 0, 0

        # transform to the local coordinate system
        x, y = self._transform(x, y)

        r, theta = self._to_polar_coordinates(x, y)

        u_r = 0
        u_theta = self.strength / 2 / np.pi / r

        return self._to_cartesian_velocity(u_r, u_theta, r, theta)


class SourceSink(BaseFlow):
    """
    Source sink flow class.

    Defines the potential flow functions for a source or sink flow.
    """
    def __init__(self, x_0: int, y_0: int, strength: float) -> None:
        """
        Initialize the source sink flow class.

        :param x_0: x position of the center of the source.
        :param y_0: y position of the center of the source.
        :param strength: strength of the source or sink. +ive defines a source, -ive defines a sink.
        """
        self.strength = strength

        super().__init__(x_0, y_0)

    def stream_function(self, x: int, y: int) -> float:
        # check if the given coordinate is at the center of the source/sink
        if self._is_center(x, y):
            return 0

        # transform to the local coordinate system
        x, y = self._transform(x, y)

        r, theta = self._to_polar_coordinates(x, y)

        return self.strength * theta / 2 / np.pi

    def potential_function(self, x: int, y: int) -> float:
        # check if the given coordinate is at the center of the source/sink
        if self._is_center(x, y):
            return 0

        # transform to the local coordinate system
        x, y = self._transform(x, y)

        r, theta = self._to_polar_coordinates(x, y)

        return self.strength * np.log(r) / 2 / np.pi

    def velocity(self, x: int, y: int) -> tuple[float, float]:
        # check if the given coordinate is at the center of the source/sink
        if self._is_center(x, y):
            return 0, 0

        # transform to the local coordinate system
        x, y = self._transform(x, y)

        r, theta = self._to_polar_coordinates(x, y)

        if r == 0:
            print(x, y)

        u_r = self.strength / 2 / np.pi / r
        u_theta = 0

        return self._to_cartesian_velocity(u_r, u_theta, r, theta)


class Doublet(BaseFlow):
    """
    Doublet flow class.

    Defines the potential flow functions for a doublet flow.
    """
    def __init__(self, x_0: int, y_0: int, strength: float) -> None:
        """
        Initialize the doublet flow class.

        :param x_0: x position of the center of the doublet.
        :param y_0: y position of the center of the doublet.
        :param strength: strength of the doublet.
        """
        self.strength = strength

        super().__init__(x_0, y_0)

    def stream_function(self, x: int, y: int) -> float:
        # check if the given coordinate is at the center of the doublet
        if self._is_center(x, y):
            return 0

        # transform to the local coordinate system
        x, y = self._transform(x, y)

        r, theta = self._to_polar_coordinates(x, y)

        return -self.strength * np.sin(theta) / 2 / np.pi / r

    def potential_function(self, x: int, y: int) -> float:
        # check if the given coordinate is at the center of the doublet
        if self._is_center(x, y):
            return 0

        # transform to the local coordinate system
        x, y = self._transform(x, y)

        r, theta = self._to_polar_coordinates(x, y)

        return self.strength * np.cos(theta) / 2 / np.pi / r

    def velocity(self, x: int, y: int) -> tuple[float, float]:
        # check if the given coordinate is at the center of the doublet
        if self._is_center(x, y):
            return 0, 0

        # transform to the local coordinate system
        x, y = self._transform(x, y)

        r, theta = self._to_polar_coordinates(x, y)

        u_r = self.strength * np.cos(theta) / r ** 2
        u_theta = self.strength * np.sin(theta) / r ** 3

        return self._to_cartesian_velocity(u_r, u_theta, r, theta)





