from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.scans.scan import Scan
from pyuff_ustb.objects.uff import compulsory_property, dependent_property
from pyuff_ustb.readers import read_array

if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class LinearScan(Scan):
    """:class:`Uff` class to define a linear scan.

    Original authors:
        Alfonso Rodriguez-Molares (alfonso.r.molares@ntnu.no)

    See also:
        :class:`~pyuff_ustb.objects.scans.LinearScanRotated`
        :class:`~pyuff_ustb.objects.scans.Linear3DScan`
    """

    # Compulsory properties
    @compulsory_property
    def x_axis(self) -> np.ndarray:
        "Vector containing the x coordinates of the x-axis [m]"
        return read_array(self._reader["x_axis"])

    @compulsory_property
    def z_axis(self) -> np.ndarray:
        "Vector containing the z coordinates of the z-axis [m]"
        return read_array(self._reader["z_axis"])

    # Dependent properties
    @dependent_property
    def N_x_axis(self) -> int:
        "Number of pixels in the x_axis"
        return len(self.x_axis)

    @dependent_property
    def N_z_axis(self) -> int:
        "Number of pixels in the z_axis"
        return len(self.z_axis)

    @dependent_property
    def x_step(self) -> float:
        "The step size in m of the x samples"
        return np.mean(np.diff(self.x_axis))

    @dependent_property
    def z_step(self) -> float:
        "The step size in m of the z samples"
        return np.mean(np.diff(self.z_axis))

    @dependent_property
    def reference_distance(self) -> np.ndarray:
        "Distance used for the calculation of the phase term"
        return self.z

    # Override some compulsory properties of Scan
    @compulsory_property
    def x(self) -> np.ndarray:
        # Try to read x from the file first
        if "x" in self._reader:
            return read_array(self._reader["x"])

        # If x is not set in the file, calculate it based on the fields.
        X, Z = np.meshgrid(self.x_axis, self.z_axis, indexing="ij")
        N_pixels = X.size
        return np.reshape(X, [N_pixels])

    @compulsory_property
    def y(self) -> np.ndarray:
        # Try to read y from the file first
        if "y" in self._reader:
            return read_array(self._reader["y"])

        # If y is not set in the file, calculate it based on the fields.
        N_pixels = self.N_x_axis * self.N_z_axis
        return np.zeros((N_pixels,))

    @compulsory_property
    def z(self) -> np.ndarray:
        # Try to read z from the file first
        if "z" in self._reader:
            return read_array(self._reader["z"])

        # If z is not set in the file, calculate it based on the fields.
        X, Z = np.meshgrid(self.x_axis, self.z_axis, indexing="ij")
        N_pixels = Z.size
        return np.reshape(Z, [N_pixels])
