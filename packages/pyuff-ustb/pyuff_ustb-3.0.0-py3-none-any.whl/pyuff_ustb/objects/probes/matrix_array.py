from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.probes.probe import Probe
from pyuff_ustb.objects.uff import compulsory_property, optional_property
from pyuff_ustb.readers import read_array, read_scalar

if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property


class MatrixArray(Probe):
    """:class:`Uff` class to define a matrix array probe geometry.

    :class:`MatrixArray` contains defines an 2D array of elements with regularly spaced
    in both dimensions.

    Original authors:
        Alfonso Rodriguez-Molares (alfonsom@ntnu.no)
    """

    # Compulsory properties
    @compulsory_property
    def pitch_x(self) -> float:
        "Distance between the elements in the azimuth direction [m]"
        return read_scalar(self._reader["pitch_x"])

    @compulsory_property
    def pitch_y(self) -> float:
        "Distance between the elements in the elevation direction [m]"
        return read_scalar(self._reader["pitch_y"])

    @compulsory_property
    def N_x(self) -> int:
        "Number of elements in the azimuth direction"
        return int(read_scalar(self._reader["N_x"]))

    @compulsory_property
    def N_y(self) -> int:
        "Number of elements in the elevation direction"
        return int(read_scalar(self._reader["N_y"]))

    # Optional properties
    @optional_property
    def element_width(self) -> float:
        "Width of the elements in the azimuth direction [m]"
        return read_scalar(self._reader["element_width"])

    @optional_property
    def element_height(self) -> float:
        "Height of the elements in the elevation direction [m]"
        return read_scalar(self._reader["element_height"])

    # Override some compulsory properties of Probe
    @compulsory_property
    def geometry(self) -> np.ndarray:
        # Try to read geometry from the file first
        if "geometry" in self._reader:
            return read_array(self._reader["geometry"])

        # If geometry is not set in the file, calculate it based on the fields.
        element_width = self.pitch_x
        element_height = self.pitch_y
        N_x, N_y = int(self.N_x), int(self.N_y)

        # Compute element center location
        x0 = np.arange(0, N_x) * self.pitch_x
        x0 = x0 - np.mean(x0)
        y0 = np.arange(0, N_y) * self.pitch_y
        y0 = y0 - np.mean(y0)

        X, Y = np.meshgrid(x0, y0)

        return np.array(
            [
                X,
                Y,
                np.zeros((N_x, N_y)),
                np.zeros((N_x, N_y)),
                np.zeros((N_x, N_y)),
                element_width * np.ones((N_x, N_y)),
                element_height * np.ones((N_x, N_y)),
            ]
        )
