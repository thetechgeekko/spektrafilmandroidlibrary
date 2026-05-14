from dataclasses import dataclass, field
from typing import Any

import numpy as np
import colour
from opt_einsum import contract

from spektrafilm.config import SPECTRAL_SHAPE

def density_to_light(density, light):
    """
    Convert density to light transmittance.

    This function calculates the light transmittance based on the given density
    and light intensity. It uses the formula transmittance = 10^(-density) to 
    compute the transmittance and then multiplies it by the light intensity.

    Parameters:
    density (float or np.ndarray): The density value(s) which affect the light transmittance.
    light (float or np.ndarray): The initial light intensity value(s).

    Returns:
    np.ndarray: The light intensity after passing through the medium with the given density.
    """
    transmitted = 10**(-density)
    transmitted *= light
    transmitted[np.isnan(transmitted)] = 0
    return transmitted

def compute_aces_conversion_matrix(sensitivity, illuminant):            
    """
    Computes the ACES (Academy Color Encoding System) conversion matrix.

    Parameters
    ----------
    sensitivity : array-like
        The spectral sensitivity data.
    illuminant : array-like
        The illuminant spectral distribution.

    Returns
    -------
    numpy.ndarray
        The ACES to raw conversion matrix.
    """
    msds = colour.MultiSpectralDistributions(sensitivity, domain=SPECTRAL_SHAPE.wavelengths)
    M, _ = colour.matrix_idt(msds, illuminant)
    aces_to_raw_conversion_matrix = np.linalg.inv(M)
    return aces_to_raw_conversion_matrix

@dataclass(frozen=True, slots=True)
class AcesIdtParams:
    illuminant: Any
    sensitivity: Any
    midgray_rgb: Any = field(default_factory=lambda: [[[0.184, 0.184, 0.184]]])
    color_space: str = 'sRGB'
    apply_cctf_decoding: bool = True
    aces_conversion_matrix: Any = field(default_factory=list)

def rgb_to_raw_aces_idt(RGB, params: AcesIdtParams):
    """
    Converts RGB values to raw values using ACES IDT (Input Device Transform).

    Parameters:
    RGB (array-like): The input RGB values.
    params (AcesIdtParams): The parameters for the conversion.

    Returns:
    tuple: A tuple containing:
        - raw (array-like): The raw values.
        - raw_midgray (array-like): The raw mid-gray values.
    """
    aces = colour.RGB_to_RGB(RGB, params.color_space, 'ACES2065-1',
                    apply_cctf_decoding=params.apply_cctf_decoding,
                    apply_cctf_encoding=False)
    aces_conversion_matrix = params.aces_conversion_matrix
    if len(aces_conversion_matrix) == 0:
        aces_conversion_matrix = compute_aces_conversion_matrix(params.sensitivity, params.illuminant)
    raw = contract('ijk,lk->ijl', aces, aces_conversion_matrix) / params.midgray_rgb
    raw_midgray = np.array([[[1,1,1]]])
    return raw, raw_midgray

