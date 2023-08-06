"""Tests for the SpectralLine data structure and validation"""
import random

import pytest
from pydantic import ValidationError

from dkist_spectral_lines.lines import DiagnosticSpecies
from dkist_spectral_lines.models import SpectralLine


@pytest.mark.parametrize("diagnostic_species", [l for l in DiagnosticSpecies])
def test_spectral_line_valid(diagnostic_species):
    """
    :Given: Diagnostic species and wavelength
    :When: Instantiating a SpectralLine
    :Then: Instance created and name property renders
    """
    # Given
    wavelength = random.random() * 100
    # When
    spectral_line = SpectralLine(
        diagnostic_species=diagnostic_species, rest_wavelength_in_air=wavelength
    )
    # Then
    assert spectral_line.name


@pytest.mark.parametrize(
    "diagnostic_species, wavelength",
    [
        pytest.param("bad line", 1.1, id="diagnostic_species"),
        pytest.param(DiagnosticSpecies.CA_I, "a", id="wavelength"),
        pytest.param("bad line", "a", id="diagnostic_species_and_wavelength"),
        pytest.param(None, 1.1, id="diagnostic_species_required"),
        pytest.param(DiagnosticSpecies.CA_I, None, id="wavelength_required"),
    ],
)
def test_spectral_line_invalid(diagnostic_species, wavelength):
    """
    :Given: Invalid diagnostic species and/or wavelength
    :When: Instantiating a SpectralLine
    :Then: Pydantic Validation error raised
    """
    with pytest.raises(ValidationError):
        SpectralLine(diagnostic_species=diagnostic_species, rest_wavelength_in_air=wavelength)
