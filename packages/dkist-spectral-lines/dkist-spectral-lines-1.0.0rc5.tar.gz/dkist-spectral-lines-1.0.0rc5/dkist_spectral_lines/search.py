"""Search for spectral lines."""
from dkist_spectral_lines.lines import SPECTRAL_LINES
from dkist_spectral_lines.models import SpectralLine


def get_spectral_lines(wavelength_min: float, wavelength_max: float) -> list[SpectralLine]:
    """Get all spectral lines found in the wavelength range inclusive of the extremes."""
    result = [
        line
        for line in SPECTRAL_LINES
        if wavelength_min <= line.rest_wavelength_in_air <= wavelength_max
    ]
    return result


def get_closest_spectral_line(wavelength: float) -> SpectralLine:
    """Get the spectral line that is closest to reference wavelength."""
    return min(SPECTRAL_LINES, key=lambda x: abs(x.rest_wavelength_in_air - wavelength))
