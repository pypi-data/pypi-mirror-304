from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.uff import Uff, compulsory_property, dependent_property
from pyuff_ustb.readers import read_array

if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class Scan(Uff):
    """:class:`Uff` class to define a scan.

    :class:`Scan` contains the position of a collection of pixels. It is asuperclass for more easy-to-handle classes such as :class:`~pyuff_ustb.objects.scans.linear_scan.LinearScan` or :class:`~pyuff_ustb.objects.scans.sector_scan.SectorScan`.
    """

    # Compulsory properties
    @compulsory_property
    def x(self) -> np.ndarray:
        "Vector containing the x coordinates of each pixel in [m]"
        return read_array(self._reader["x"])

    @compulsory_property
    def y(self) -> np.ndarray:
        "Vector containing the y coordinates of each pixel in [m]"
        return read_array(self._reader["y"])

    @compulsory_property
    def z(self) -> np.ndarray:
        "Vector containing the z coordinates of each pixel in [m]"
        return read_array(self._reader["z"])

    # Dependent properties
    @dependent_property
    def xyz(self) -> np.ndarray:
        "Vector containing the [x, y, z] coordinates of each pixel in [m]"
        y = self.y
        if y is None:
            y = np.array(0.0)
        if y.shape != self.x.shape and y.size == 1:
            y = np.repeat(y, self.x.size)
        return np.stack([self.x, y, self.z], axis=-1)
