from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.uff import Uff, compulsory_property
from pyuff_ustb.readers import read_array, read_scalar

if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class Pulse(Uff):
    """:class:`Uff` class for a pulse definition.

    Original authors:
        Alfonso Rodriguez-Molares <alfonso.r.molares@ntnu.no>
    """

    # Compulsory properties
    @compulsory_property
    def center_frequency(self) -> float:
        "Center frequency [Hz]"
        return read_scalar(self._reader["center_frequency"])

    @compulsory_property
    def fractional_bandwidth(self) -> float:
        "Probe fractional bandwidth [unitless]"
        return read_scalar(self._reader["fractional_bandwidth"])

    @compulsory_property
    def phase(self) -> float:
        "Initial phase [rad]"
        return read_scalar(self._reader["phase"])

    @compulsory_property
    def waveform(self) -> np.ndarray:
        "Transmitted waveform (for example used for match filtering)"
        return read_array(self._reader["waveform"])
