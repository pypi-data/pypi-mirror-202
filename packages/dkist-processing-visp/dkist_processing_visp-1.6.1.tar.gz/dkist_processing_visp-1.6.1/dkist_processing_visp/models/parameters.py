"""Visp calibration pipeline parameters."""
import logging
from datetime import datetime
from typing import Any

import numpy as np
from dkist_processing_common.models.parameters import ParameterBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetParameterValue


class VispParameters(ParameterBase):
    """Put all Visp parameters parsed from the input dataset document in a single property."""

    def __init__(
        self,
        input_dataset_parameters: dict[str, list[InputDatasetParameterValue]],
        wavelength: float | None = None,
        obs_ip_start_time: str | None = None,
    ):
        super().__init__(input_dataset_parameters)
        self._wavelength = wavelength
        try:
            self._obs_ip_start_datetime = datetime.fromisoformat(obs_ip_start_time)
        except TypeError:
            logging.warning(
                "The task containing this parameters object did not provide an obs ip start time. "
                "This only makes sense for the Parse task."
            )

    @property
    def beam_border(self):
        """Pixel location of the border between ViSP beams."""
        return self._find_most_recent_past_value("visp_beam_border")

    @property
    def background_on(self) -> bool:
        """Return True if background light correct should be done."""
        return self._find_most_recent_past_value(
            "visp_background_on", start_date=self._obs_ip_start_datetime
        )

    @property
    def background_num_spatial_bins(self) -> int:
        """Return number of spatial bins to use when computing background light."""
        return self._find_parameter_closest_wavelength("visp_background_num_spatial_bins")

    @property
    def background_wavelength_subsample_factor(self) -> int:
        """Return the sub-sampling factor used to reduce the number of wavelength samples."""
        return self._find_parameter_closest_wavelength(
            "visp_background_wavelength_subsample_factor"
        )

    @property
    def background_num_fit_iterations(self) -> int:
        """Maximum number of fit iterations used to fit the background light."""
        return self._find_parameter_closest_wavelength("visp_background_num_fit_iterations")

    @property
    def background_continuum_index(self) -> list:
        """Return indices of a region to use when normalizing modulated polcals in the background task."""
        return self._find_parameter_closest_wavelength("visp_background_continuum_index")

    @property
    def lamp_high_pass_filter_width_px(self) -> float:
        """Sigma (in pixels) of the gaussian filter used for pseudo unsharp masking of the lamp gain images.

        Features that are smaller than the ~sigma will be "passed" by the filter, so a larger sigma corresponds to a
        larger "width" in the HP filter.
        """
        return self._find_parameter_closest_wavelength("visp_lamp_high_pass_filter_width_px")

    @property
    def gain_hairline_fraction(self):
        """Relative threshold below median used to identify slit positions covered by the hairlines."""
        return self._find_most_recent_past_value("visp_gain_hairline_fraction")

    @property
    def geo_num_otsu(self):
        """Max number of times to run Otsu's method when making a binary image from solar spectra."""
        return self._find_most_recent_past_value("visp_geo_num_otsu")

    @property
    def geo_num_theta(self):
        """Find the number of samples between theta_min and theta_max to use in Hough Transform for spectral tilt calculation."""
        return self._find_most_recent_past_value("visp_geo_num_theta")

    @property
    def geo_theta_min(self):
        """Minimum angle (in radians) to consider for spectral tilt calculation."""
        return self._find_most_recent_past_value("visp_geo_theta_min")

    @property
    def geo_theta_max(self):
        """Maximum angle (in radians) to consider for spectral tilt calculation."""
        return self._find_most_recent_past_value("visp_geo_theta_max")

    @property
    def geo_max_beam_2_angle_refinement(self) -> float:
        """Maximum allowable refinement to the beam 2 spectral tilt angle, in radians."""
        return self._find_most_recent_past_value("visp_geo_max_beam_2_angle_refinement")

    @property
    def geo_upsample_factor(self):
        """Pixel precision (1/upsample_factor) to use during phase matching of beam/modulator images."""
        return self._find_most_recent_past_value("visp_geo_upsample_factor")

    @property
    def geo_max_shift(self):
        """Max allowed pixel shift when computing spectral curvature."""
        return self._find_most_recent_past_value("visp_geo_max_shift")

    @property
    def geo_poly_fit_order(self):
        """Order of polynomial used to fit spectral shift as a function of slit position."""
        return self._find_most_recent_past_value("visp_geo_poly_fit_order")

    @property
    def solar_spectral_avg_window(self):
        """Pixel sigma of Gaussian kernal used to compute characteristic solar spectra."""
        return self._find_parameter_closest_wavelength("visp_solar_spectral_avg_window")

    @property
    def solar_zone_prominence(self):
        """Relative peak prominence threshold used to identify strong spectral features."""
        return self._find_parameter_closest_wavelength("visp_solar_zone_prominence")

    @property
    def solar_zone_width(self):
        """Pixel width used to search for strong spectral features."""
        return self._find_parameter_closest_wavelength("visp_solar_zone_width")

    @property
    def solar_zone_bg_order(self):
        """Order of polynomial fit used to remove continuum when identifying strong spectral features."""
        return self._find_parameter_closest_wavelength("visp_solar_zone_bg_order")

    @property
    def solar_zone_normalization_percentile(self):
        """Fraction of CDF to use for normalzing spectrum when search for strong features."""
        return self._find_parameter_closest_wavelength("visp_solar_zone_normalization_percentile")

    @property
    def solar_zone_rel_height(self):
        """Relative height at which to compute the width of strong spectral features."""
        return self._find_most_recent_past_value("visp_solar_zone_rel_height")

    @property
    def max_cs_step_time_sec(self):
        """Time window within which CS steps with identical GOS configurations are considered to be the same."""
        return self._find_most_recent_past_value("visp_max_cs_step_time_sec")

    @property
    def polcal_num_spatial_bins(self) -> int:
        """Return number of demodulation matrices to compute across the entire FOV in the spatial dimension."""
        return self._find_most_recent_past_value("visp_polcal_num_spatial_bins")

    @property
    def polcal_num_spectral_bins(self) -> int:
        """Return Number of demodulation matrices to compute across the entire FOV in the spectral dimension."""
        return self._find_most_recent_past_value("visp_polcal_num_spectral_bins")

    @property
    def polcal_demod_upsample_order(self) -> int:
        """Interpolation order to use when upsampling the demodulation matrices to the full frame.

        See `skimage.transform.warp` for details.
        """
        return self._find_most_recent_past_value("visp_polcal_demod_upsample_order")

    @property
    def pac_remove_linear_I_trend(self) -> bool:
        """Flag that determines if a linear intensity trend is removed from the whole PolCal CS.

        The trend is fit using the average flux in the starting and ending clear steps.
        """
        return self._find_most_recent_past_value("visp_pac_remove_linear_I_trend")

    @property
    def pac_fit_mode(self):
        """Name of set of fitting flags to use during PAC Calibration Unit parameter fits."""
        return self._find_most_recent_past_value("visp_pac_fit_mode")

    @property
    def pac_init_set(self):
        """Name of set of initial values for Calibration Unit parameter fit."""
        return self._find_most_recent_past_value("visp_pac_init_set")

    def _find_parameter_closest_wavelength(self, parameter_name: str) -> Any:
        """
        Find the database value for a parameter that is closest to the requested wavelength.

        NOTE: If the requested wavelength is exactly between two database values, the value from the smaller wavelength
        will be returned
        """
        if self._wavelength is None:
            raise ValueError(
                f"Cannot get wavelength dependent parameter {parameter_name} without wavelength"
            )

        parameter_dict = self._find_most_recent_past_value(parameter_name)
        wavelengths = np.array(parameter_dict["wavelength"])
        values = parameter_dict["values"]
        idx = np.argmin(np.abs(wavelengths - self._wavelength))
        chosen_wave = wavelengths[idx]
        chosen_value = values[idx]
        logging.debug(
            f"Choosing {parameter_name} = {chosen_value} from {chosen_wave = } (requested {self._wavelength}"
        )
        return chosen_value
