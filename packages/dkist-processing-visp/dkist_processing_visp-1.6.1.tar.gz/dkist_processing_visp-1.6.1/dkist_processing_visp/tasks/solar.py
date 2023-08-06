"""ViSP solar calibration task."""
import logging

import numpy as np
import peakutils
import scipy.ndimage as spnd
import scipy.optimize as spo
import scipy.signal as sps
from dkist_processing_common.tasks.mixin.quality import QualityMixin
from dkist_processing_math.arithmetic import divide_arrays_by_array
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.mixin.corrections import CorrectionsMixin
from dkist_processing_visp.tasks.mixin.input_frame_loaders import InputFrameLoadersMixin
from dkist_processing_visp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)
from dkist_processing_visp.tasks.visp_base import VispTaskBase


class SolarCalibration(
    VispTaskBase,
    IntermediateFrameHelpersMixin,
    InputFrameLoadersMixin,
    CorrectionsMixin,
    QualityMixin,
):
    """
    Task class for generating Solar Gain images for each beam/modstate.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    record_provenance = True

    def run(self) -> None:
        """
        For each beam.

            For each modstate:
                - Do dark, background, lamp, and geometric corrections
                - Compute the characteristic spectra
                - Re-apply the spectral curvature to the characteristic spectra
                - Re-apply angle and state offset distortions to the characteristic spectra
                - Remove the distorted characteristic solar spectra from the original spectra
                - Write master solar gain

        Returns
        -------
        None

        """
        for beam in range(1, self.constants.num_beams + 1):
            for modstate in range(1, self.constants.num_modstates + 1):
                apm_str = f"{beam = } and {modstate = }"
                logging.info(f"Dark/lamp/geometric corrections for {apm_str}")
                with self.apm_processing_step(f"Initial corrections for {apm_str}"):
                    self.do_initial_corrections(beam=beam, modstate=modstate)

                with self.apm_processing_step(f"Computing characteristic spectra for {apm_str}"):
                    char_spec = self.compute_characteristic_spectra(beam=beam, modstate=modstate)
                    self.intermediate_frame_helpers_write_arrays(
                        arrays=char_spec, beam=beam, modstate=modstate, task="SC_DEBUG_CHAR_SPEC"
                    )

                with self.apm_processing_step(
                    f"Refining characteristic spectral shifts for {apm_str}"
                ):
                    reshifted_char_spec = self.refine_gain_shifts(
                        char_spec=char_spec, beam=beam, modstate=modstate
                    )
                    self.intermediate_frame_helpers_write_arrays(
                        arrays=reshifted_char_spec,
                        beam=beam,
                        modstate=modstate,
                        task="SC_DEBUG_CHAR_SPEC_SHIFT",
                    )

                with self.apm_processing_step(f"Removing solar signal from {apm_str}"):
                    gain = self.remove_solar_signal(
                        char_solar_spectra=reshifted_char_spec, beam=beam, modstate=modstate
                    )
                    self.intermediate_frame_helpers_write_arrays(
                        arrays=gain,
                        beam=beam,
                        modstate=modstate,
                        task="SC_DEBUG_PERFECT_GAIN",
                    )

                with self.apm_processing_step(f"Reshifting gain spectra for {apm_str}"):
                    spec_shift = self.intermediate_frame_helpers_load_spec_shift(beam=beam)
                    reshifted_gain = next(
                        self.corrections_remove_spec_geometry(
                            arrays=gain, spec_shift=-1 * spec_shift
                        )
                    )
                    self.intermediate_frame_helpers_write_arrays(
                        arrays=reshifted_gain,
                        beam=beam,
                        modstate=modstate,
                        task="SC_DEBUG_NEW_GAIN_SPEC_SHIFT",
                    )

                with self.apm_processing_step(
                    f"Re-distorting characteristic spectra for {apm_str}"
                ):
                    distorted_gain = self.distort_characteristic_spectra(
                        char_spec=reshifted_gain, beam=beam, modstate=modstate
                    )
                    self.intermediate_frame_helpers_write_arrays(
                        arrays=distorted_gain,
                        beam=beam,
                        modstate=modstate,
                        task="SC_DEBUG_NEW_GAIN_SHIFT_DISTORT",
                    )

                with self.apm_writing_step(f"Writing solar gain for {apm_str}"):
                    self.write_solar_gain_calibration(
                        gain_array=distorted_gain, beam=beam, modstate=modstate
                    )

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_solar_frames: int = self.scratch.count_all(
                tags=[
                    VispTag.input(),
                    VispTag.frame(),
                    VispTag.task("SOLAR_GAIN"),
                ],
            )

            self.quality_store_task_type_counts(
                task_type="SOLAR_GAIN", total_frames=no_of_raw_solar_frames
            )

    def unshifted_geo_corrected_modstate_data(self, beam: int, modstate: int) -> np.ndarray:
        """
        Array for a single beam/modstate that has dark, lamp, angle, and state offset corrections.

        Parameters
        ----------
        beam : int
            The beam number for this array

        modstate : int
            The modulator state for this array


        Returns
        -------
        np.ndarray
            Array with dark signal, lamp signal, angle and state offset removed

        """
        array_generator = self.intermediate_frame_helpers_load_intermediate_arrays(
            beam=beam, task="SC_GEO_NOSHIFT", modstate=modstate
        )
        return next(array_generator)

    def geo_corrected_modstate_data(self, beam: int, modstate: int) -> np.ndarray:
        """
        Array for a single beam/modstate that has dark, lamp, and ALL of the geometric corrects.

        Parameters
        ----------
        beam : int
            The beam number for this array

        modstate : int
            The modulator state for this array


        Returns
        -------
        np.ndarray
            Array with dark signal, and lamp signal removed, and all geometric corrections made
        """
        array_generator = self.intermediate_frame_helpers_load_intermediate_arrays(
            beam=beam, task="SC_GEO_ALL", modstate=modstate
        )
        return next(array_generator)

    def do_initial_corrections(self, beam: int, modstate: int) -> None:
        """
        Do dark, lamp, and geometric corrections for all data that will be used.

        At two intermediate points the current arrays are saved because they'll be needed by various helpers:

        SC_BG_ONLY - The solar gain arrays with only a dark and background correction.

        SC_GEO_NOSHIFT - The solar gain arrays after dark, lamp, angle, and state offset correction. In other words,
                         they do not have spectral curvature removed. These are used to reshift the characteristic
                         spectra to the original spectral curvature.

        Parameters
        ----------
        beam : int
            The beam number for this array

        modstate : int
            The modulator state for this array


        Returns
        -------
        None
        """
        for exp_time in self.constants.solar_exposure_times:
            try:
                dark_array = self.intermediate_frame_helpers_load_dark_array(
                    beam=beam, exposure_time=exp_time
                )
            except StopIteration:
                raise ValueError(f"No matching dark found for {exp_time = } s")

            try:
                background_array = self.intermediate_frame_helpers_load_background_array(beam=beam)
            except StopIteration:
                if self.constants.correct_for_polarization and self.parameters.background_on:
                    raise ValueError(f"No matching background light found for {beam = }")

                logging.info("Skipping background light correction")
                background_array = np.zeros(dark_array.shape)

            logging.info(
                f"Doing dark, background, lamp, and geo corrections for {beam=} and {modstate=}"
            )
            ## Load frames
            input_solar_arrays = self.input_frame_loaders_solar_gain_array_generator(
                beam=beam, modstate=modstate, exposure_time=exp_time
            )
            lamp_array = self.intermediate_frame_helpers_load_lamp_gain_array(
                beam=beam, modstate=modstate
            )

            ## Average
            avg_solar_array = average_numpy_arrays(input_solar_arrays)

            ## Dark correction
            dark_corrected_solar_array = subtract_array_from_arrays(
                arrays=avg_solar_array, array_to_subtract=dark_array
            )

            ## Residual background correction
            background_corrected_solar_array = next(
                subtract_array_from_arrays(dark_corrected_solar_array, background_array)
            )

            # Save the only-dark-corr because this will be used to make the final Solar Gain object
            self.intermediate_frame_helpers_write_arrays(
                arrays=background_corrected_solar_array,
                beam=beam,
                modstate=modstate,
                task="SC_BG_ONLY",
            )

            ## Lamp correction
            lamp_corrected_solar_array = next(
                divide_arrays_by_array(
                    arrays=background_corrected_solar_array, array_to_divide_by=lamp_array
                )
            )

            ## Geo correction
            angle = self.intermediate_frame_helpers_load_angle(beam=beam)
            state_offset = self.intermediate_frame_helpers_load_state_offset(
                beam=beam, modstate=modstate
            )
            spec_shift = self.intermediate_frame_helpers_load_spec_shift(beam=beam)

            geo_corrected_array = next(
                self.corrections_correct_geometry(lamp_corrected_solar_array, state_offset, angle)
            )
            # We need unshifted, but geo-corrected arrays for reshifting and normalization
            self.intermediate_frame_helpers_write_arrays(
                arrays=geo_corrected_array, beam=beam, modstate=modstate, task="SC_GEO_NOSHIFT"
            )
            # re_distorted_array = self.distort_characteristic_spectra(geo_corrected_array, beam=beam, modstate=modstate)
            # self.intermediate_frame_helpers_write_arrays(arrays=re_distorted_array, beam=beam, modstate=modstate,
            #                                              task="SC_DEBUG_REDISTORTED_OBS")

            # Now finish the spectral shift correction
            spectral_corrected_array = next(
                self.corrections_remove_spec_geometry(geo_corrected_array, spec_shift)
            )
            self.intermediate_frame_helpers_write_arrays(
                arrays=spectral_corrected_array, beam=beam, modstate=modstate, task="SC_GEO_ALL"
            )

    def compute_characteristic_spectra(self, beam: int, modstate: int) -> np.ndarray:
        """
        Compute the characteristic spectrum by taking the median of all spatial positions.

        First identify and ignore hairlines, which might not be necessary.

        Parameters
        ----------
        beam : int
            The beam number for this array

        modstate : int
            The modulator state for this array


        Returns
        -------
        np.ndarray
            Characteristic spectra array
        """
        spectral_avg_window = self.parameters.solar_spectral_avg_window
        hairline_fraction = self.parameters.gain_hairline_fraction

        logging.info(
            f"Computing characteristic spectra for {beam = } and {modstate = } with {spectral_avg_window = } and {hairline_fraction = }"
        )
        full_spectra = self.geo_corrected_modstate_data(beam=beam, modstate=modstate)

        # Find hairlines by looking for slit position where the deviation in signal from the median is large
        med_spec = np.nanmedian(full_spectra, axis=1)
        ratio = full_spectra / med_spec[:, None]
        lidx = np.where(ratio < hairline_fraction)

        # Replace identified hairlines with data from the median spectrum
        # This might all be unnecessary
        full_spectra[lidx] = med_spec[lidx[0]]

        # Actually compute the median spectrum and explode it across the full shape
        char_spec = spnd.gaussian_filter1d(full_spectra, spectral_avg_window, axis=1)

        return char_spec

    def refine_gain_shifts(self, char_spec: np.ndarray, beam: int, modstate: int) -> np.ndarray:
        """
        Refine the spectral shifts when matching characteristic spectra to the rectified input spectra.

        An important detail of this functino is that the goodness of fit metric is the final gain image (i.e., raw
        input with solar spectrum removed). We minimize the residuals in the gain image.

        Parameters
        ----------
        char_spec : np.ndarray
            Computed characteristic spectra

        beam : int
            The beam number for this array

        modstate : int
            The modulator state for this array


        Returns
        -------
        np.ndarray
            Characteristic spectra array with refined spectral shifts
        """
        # Grab rectified input spectra that will be the shift target
        target_spectra = self.geo_corrected_modstate_data(beam=beam, modstate=modstate)
        num_spec = target_spectra.shape[1]

        logging.info(f"Computing line zones for {beam=} and {modstate=}")
        zone_kwargs = {
            "prominence": self.parameters.solar_zone_prominence,
            "width": self.parameters.solar_zone_width,
            "bg_order": self.parameters.solar_zone_bg_order,
            "normalization_percentile": self.parameters.solar_zone_normalization_percentile,
            "rel_height": self.parameters.solar_zone_rel_height,
        }
        zones = self.compute_line_zones(char_spec, **zone_kwargs)
        logging.info(f"Found {zones=} for {beam=} and {modstate=}")
        if len(zones) == 0:
            raise ValueError(f"No zones found for {beam=} and {modstate=}")

        reshift_char_spec = np.zeros(char_spec.shape)
        logging.info(f"Refining shifts for {beam=} and {modstate=}")
        for i in range(num_spec):
            ref_spec = target_spectra[:, i]
            spec = char_spec[:, i]
            shift = SolarCalibration.refine_shift(spec, ref_spec, zones=zones, x_init=0.0)
            reshift_char_spec[:, i] = spnd.shift(char_spec[:, i], shift, mode="reflect")

        return reshift_char_spec

    def distort_characteristic_spectra(
        self, char_spec: np.ndarray, beam: int, modstate: int
    ) -> np.ndarray:
        """
        Re-apply angle and state offset distortions to the characteristic spectra.

        Parameters
        ----------
        char_spec : np.ndarray
            Computed characteristic spectra

        beam : int
            The beam number for this array

        modstate : int
            The modulator state for this array


        Returns
        -------
        np.ndarray
            Characteristic spectra array with angle and offset distortions re-applied
        """
        logging.info(f"Re-distorting characteristic spectra for {beam=} and {modstate=}")
        angle = self.intermediate_frame_helpers_load_angle(beam=beam)
        state_offset = self.intermediate_frame_helpers_load_state_offset(
            beam=beam, modstate=modstate
        )

        distorted_spec = next(
            self.corrections_correct_geometry(char_spec, -1 * state_offset, -1 * angle)
        )

        return distorted_spec

    def remove_solar_signal(
        self, char_solar_spectra: np.ndarray, beam: int, modstate: int
    ) -> np.ndarray:
        """
        Remove the distorted characteristic solar spectra from the original spectra.

        This also has the effect of normalizing the gain image.

        Parameters
        ----------
        char_solar_spectra : np.ndarray
            Characteristic solar spectra

        beam : int
            The beam number for this array

        modstate : int
            The modulator state for this array


        Returns
        -------
        np.ndarray
            Original spectral array with characteristic solar spectra removed

        """
        logging.info(f"Removing characteristic solar spectra from {beam=} and {modstate=}")
        input_gain = self.geo_corrected_modstate_data(beam=beam, modstate=modstate)

        final_gain = input_gain / char_solar_spectra

        return final_gain

    def write_solar_gain_calibration(
        self, gain_array: np.ndarray, beam: int, modstate: int
    ) -> None:
        """
        Write a solar gain array for a single beam and modstate.

        Parameters
        ----------
        gain_array: np.ndarray
            Solar gain array

        beam : int
            The beam number for this array

        modstate : int
            The modulator state for this array


        Returns
        -------
        None
        """
        logging.info(f"Writing final SolarGain for {beam=} and {modstate=}")
        self.intermediate_frame_helpers_write_arrays(
            arrays=gain_array, beam=beam, modstate=modstate, task="SOLAR_GAIN"
        )

        # These lines are here to help debugging and can be removed if really necessary
        filename = next(
            self.read(
                tags=[
                    VispTag.intermediate(),
                    VispTag.beam(beam),
                    VispTag.modstate(modstate),
                    VispTag.task("SOLAR_GAIN"),
                ]
            )
        )
        logging.info(f"Wrote solar gain for {beam=} and {modstate=} to {filename}")

    @staticmethod
    def compute_line_zones(
        spec_2d: np.ndarray,
        prominence: float = 0.2,
        width: float = 2,
        bg_order: int = 22,
        normalization_percentile: int = 99,
        rel_height=0.97,
    ) -> list[tuple[int, int]]:
        """
        Identify spectral regions around strong spectra features.

        Parameters
        ----------
        spec_2d : np.ndarray
            Data

        prominence : float
            Zone prominence threshold used to identify strong spectral features

        width : float
            Zone width

        bg_order : int
            Order of polynomial fit used to remove continuum when identifying strong spectral features

        normalization_percentile : int
            Compute this percentile of the data along a specified axis



        Returns
        -------
        List
            List of regions to remove

        """
        logging.info(
            f"Finding zones using {prominence=}, {width=}, {bg_order=}, {normalization_percentile=}, and {rel_height=}"
        )
        # Compute average along slit to improve signal. Line smearing isn't important here
        avg_1d = np.mean(spec_2d, axis=1)

        # Convert to an emission spectrum and remove baseline continuum so peakutils has an easier time
        em_spec = -1 * avg_1d + avg_1d.max()
        em_spec /= np.nanpercentile(em_spec, normalization_percentile)
        baseline = peakutils.baseline(em_spec, bg_order)
        em_spec -= baseline

        # Find indices of peaks
        peak_idxs = sps.find_peaks(em_spec, prominence=prominence, width=width)[0]

        # Find the rough width based only on the height of the peak
        #  rips and lips are the right and left borders of the region around the peak
        _, _, rips, lips = sps.peak_widths(em_spec, peak_idxs, rel_height=rel_height)

        # Convert to ints so they can be used as indices
        rips = np.floor(rips).astype(int)
        lips = np.ceil(lips).astype(int)

        # Remove any regions that are contained within another region
        ranges_to_remove = SolarCalibration.identify_overlapping_zones(rips, lips)
        rips = np.delete(rips, ranges_to_remove)
        lips = np.delete(lips, ranges_to_remove)

        return list(zip(rips, lips))

    @staticmethod
    def identify_overlapping_zones(rips: np.ndarray, lips: np.ndarray) -> list[int]:
        """
        Identify line zones that overlap with other zones. Any overlap greater than 1 pixel is flagged.

        Parameters
        ----------
        rips : np.ndarray
            Right borders of the region around the peak

        lips : np.ndarray
            Left borders of the region around the peak

        Returns
        -------
        List
            List of ranges to be removed
        """
        all_ranges = [np.arange(zmin, zmax) for zmin, zmax in zip(rips, lips)]
        ranges_to_remove = []
        for i in range(len(all_ranges)):
            target_range = all_ranges[i]
            for j in range(i + 1, len(all_ranges)):
                if (
                    np.intersect1d(target_range, all_ranges[j]).size > 1
                ):  # Allow for a single overlap just to be nice
                    if target_range.size > all_ranges[j].size:
                        ranges_to_remove.append(j)
                        logging.info(
                            f"Zone ({all_ranges[j][0]}, {all_ranges[j][-1]}) inside zone ({target_range[0]}, {target_range[-1]})"
                        )
                    else:
                        ranges_to_remove.append(i)
                        logging.info(
                            f"Zone ({target_range[0]}, {target_range[-1]}) inside zone ({all_ranges[j][0]}, {all_ranges[j][-1]})"
                        )

        return ranges_to_remove

    @staticmethod
    def refine_shift(
        spec: np.ndarray, target_spec: np.ndarray, zones: list[tuple[int, int]], x_init: float
    ) -> float:
        """
        Refine the shift for a single spatial position back to the rectified input spectra.

        Line zones are used to increase the SNR of the chisq and the final shift is the mean of the shifts computed
        for each zone.

        Parameters
        ----------
        spec : np.ndarray
            The 1D spectrum to shift back

        target_spec : np.ndarray
            The reference spectrum. This should be the un-shifted, raw spectrum at the same position as `spec`

        zones : List
            List of zone borders (in px coords)

        x_init: float
            Initial guess for the shift. This is used to shift the zones so it needs to be pretty good, but not perfect.

        Returns
        -------
        float
            The shift value
        """
        shifts = np.zeros(len(zones))
        for i, z in enumerate(zones):
            if z[1] + int(x_init) >= spec.size:
                logging.info(f"Ignoring zone {z} with init {x_init} because it's out of range")
                continue
            idx = np.arange(z[0], z[1]) + int(x_init)
            shift = spo.minimize(
                SolarCalibration.shift_func,
                np.array([x_init]),
                args=(target_spec, spec, idx),
                method="nelder-mead",
            ).x[0]
            shifts[i] = shift

        return np.mean(shifts)

    @staticmethod
    def shift_func(
        par: list[float], ref_spec: np.ndarray, spec: np.ndarray, idx: np.ndarray
    ) -> float:
        """
        Non-chisq based goodness of fit calculator for computing spectral shifts.

        Instead of chisq, the metric approximates the final Gain image.

        Parameters
        ----------
        par : List
            List of parameters for minimization

        ref_spec : np.ndarray
            Reference spectra

        spec : np.ndarray
            Data

        idx : np.ndarray
            Range of wavelength pixels that will be compared in fit

        Returns
        -------
        float
            Goodness of fit metric

        """
        shift = par[0]
        shifted_spec = spnd.shift(spec, shift, mode="constant", cval=np.nan)
        final_gain = (ref_spec / shifted_spec)[idx]
        slope = (final_gain[-1] - final_gain[0]) / final_gain.size
        bg = slope * np.arange(final_gain.size) + final_gain[0]
        subbed_gain = np.abs((final_gain) - bg)
        fit_metric = np.nansum(subbed_gain[np.isfinite(subbed_gain)])
        return fit_metric
