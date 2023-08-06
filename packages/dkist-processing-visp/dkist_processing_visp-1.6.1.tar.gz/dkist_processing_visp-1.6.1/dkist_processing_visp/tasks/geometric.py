"""Visp geometric calibration task."""
import logging
from typing import Generator

import numpy as np
import peakutils as pku
import scipy.ndimage as spnd
import scipy.optimize as spo
import skimage.metrics as skim
import skimage.registration as skir
from dkist_processing_common.tasks.mixin.quality import QualityMixin
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.feature import find_px_angles
from dkist_processing_math.statistics import average_numpy_arrays
from dkist_processing_math.transform import do_hough
from dkist_processing_math.transform import make_binary
from scipy.fft import fftn
from scipy.optimize import minimize
from skimage.registration._phase_cross_correlation import _upsampled_dft

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.tasks.mixin.corrections import CorrectionsMixin
from dkist_processing_visp.tasks.mixin.input_frame_loaders import InputFrameLoadersMixin
from dkist_processing_visp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)
from dkist_processing_visp.tasks.solar import SolarCalibration
from dkist_processing_visp.tasks.visp_base import VispTaskBase


class GeometricCalibration(
    VispTaskBase,
    IntermediateFrameHelpersMixin,
    InputFrameLoadersMixin,
    CorrectionsMixin,
    QualityMixin,
):
    """
    Task class for computing the spectral geometry. Geometry is represented by three quantities.

      - Angle - The angle (in radians) between slit hairlines and pixel axes. A one dimensional array with two elements- one for each beam.

      - State_offset - The [x, y] shift between each modstate in each beam and a fiducial modstate. For each modstate and each beam two state offset values are computed.

      - Spectral_shift - The shift in the spectral dimension for each beam for every spatial position needed to "straighten" the spectra so a single wavelength is at the same pixel for all slit positions.

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

            - Gather dark corrected frames
            - Calculate spectral tilt (angle)
            - Remove spectral tilt
            - Using the angle corrected array, find the state offset
            - Write state offset
            - Calculate the spectral skew and curvature (spectral shifts)
            - Write the spectral skew and curvature

        Returns
        -------
        None
        """
        # This lives outside the run() loops and has its own internal loops because the angle calculation
        # only happens for a single modstate
        with self.apm_processing_step("Basic corrections"):
            self.do_basic_corrections()

        for beam in range(1, self.constants.num_beams + 1):
            with self.apm_task_step(f"Generating geometric calibrations for {beam = }"):
                with self.apm_processing_step(f"Computing and writing angle for {beam = }"):
                    logging.info(f"Compute and write angle for {beam = }")
                    # TODO: Why not use Lamp gains for angle measurement? They don't have strong spectral lines.
                    angle = self.compute_beam_angle(beam=beam)
                    if beam == 2:
                        with self.apm_processing_step("Refining beam 2 angle"):
                            logging.info("Refining beam 2 angle")
                            ang_corr = self.refine_beam2_angle(angle)
                        logging.info(f"Beam 2 angle refinement = {np.rad2deg(ang_corr)} deg")
                        angle += ang_corr
                        logging.info(f"Final beam 2 angle = {np.rad2deg(angle)} deg")
                    self.write_angle(angle=angle, beam=beam)

                for modstate in range(1, self.constants.num_modstates + 1):
                    with self.apm_processing_step(
                        f"Removing angle from {beam = } and {modstate = }"
                    ):
                        logging.info(f"Removing angle from {beam = } and {modstate = }")
                        angle_corr_array = self.remove_beam_angle(
                            angle=angle, beam=beam, modstate=modstate
                        )

                    with self.apm_processing_step(
                        f"Computing state offset for {beam = } and {modstate = }"
                    ):
                        logging.info(f"Computing state offset for {beam=} and {modstate = }")
                        state_offset = self.compute_modstate_offset(
                            array=angle_corr_array, beam=beam, modstate=modstate
                        )
                        self.write_state_offset(offset=state_offset, beam=beam, modstate=modstate)

                    with self.apm_processing_step(
                        f"Removing state offset for {beam = } and {modstate = }"
                    ):
                        self.remove_state_offset(
                            array=angle_corr_array,
                            offset=state_offset,
                            beam=beam,
                            modstate=modstate,
                        )

                with self.apm_processing_step(f"Computing spectral shifts for {beam = }"):
                    logging.info(f"Computing and writing spectral shifts for {beam = }")
                    spec_shifts = self.compute_spectral_shifts(beam=beam)

                with self.apm_writing_step(f"Writing spectral shifts for {beam = }"):
                    self.write_spectral_shifts(shifts=spec_shifts, beam=beam)

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_geo_frames: int = self.scratch.count_all(
                tags=[
                    VispTag.input(),
                    VispTag.frame(),
                    VispTag.task("SOLAR_GAIN"),
                ],
            )

            self.quality_store_task_type_counts(
                task_type="GEOMETRIC", total_frames=no_of_raw_geo_frames
            )

    def pre_run(self) -> None:
        """Run before run() with Elastic APM span capturing."""
        super().pre_run()
        self._fiducial_array = None
        self._fiducial_mask = None

    def basic_corrected_data(self, beam: int, modstate: int) -> np.ndarray:
        """
        Dark corrected data array for a single beam and modstate.

        Parameters
        ----------
        beam : int
            The current beam being processed
        modstate : int
            The current modulator state

        Returns
        -------
        np.ndarray
            Dark corrected data array
        """
        array_generator = self.intermediate_frame_helpers_load_intermediate_arrays(
            beam=beam, task="GC_BASIC", modstate=modstate
        )
        return next(array_generator)

    @property
    def fiducial_array(self) -> np.ndarray:
        """Target array used for determining state offsets."""
        if self._fiducial_array is None:
            raise ValueError("Fiducial array has not been set. This should never happen.")
        return self._fiducial_array

    @fiducial_array.setter
    def fiducial_array(self, array: np.ndarray) -> None:
        """
        Set the target array used for determining state offsets.

        Parameters
        ----------
        array : np.ndarray
            Fiducial array

        Returns
        -------
        None
        """
        self._fiducial_array = array

    @property
    def fiducial_mask(self) -> np.ndarray:
        """Mask on target array used for determining state offsets.

        Pixels NOT around strong lines are masked out.
        """
        if self._fiducial_mask is None:
            raise ValueError("Fiducial array has not been set. This should never happen.")
        return self._fiducial_mask

    @fiducial_mask.setter
    def fiducial_mask(self, array: np.ndarray) -> None:
        """
        Set the target mask used for determining state offsets.

        Parameters
        ----------
        array : np.ndarray
            Fiducial mask

        Returns
        -------
        None
        """
        self._fiducial_mask = array

    def offset_corrected_array_generator(self, beam: int) -> Generator[np.ndarray, None, None]:
        """
        All modstates for a single beam that have had their state offset applied.

        This is a generator because the arrays will be immediately averaged

        Parameters
        ----------
        beam : int
            The current beam being processed

        Returns
        -------
        Generator[np.ndarray, None, None]
            Generator of state offset corrected arrays

        """
        array_generator = self.intermediate_frame_helpers_load_intermediate_arrays(
            beam=beam, task="GC_OFFSET"
        )
        return array_generator

    def do_basic_corrections(self):
        """
        Apply dark correction to all data that will be used for Geometric Calibration.

        Lamp correction is not applied because it was found to reduce contrast between the spectra and the hairlines
        that are used to find the rotation angle.
        """
        for exp_time in self.constants.solar_exposure_times:
            for beam in range(1, self.constants.num_beams + 1):
                logging.info(f"Starting basic reductions for {exp_time = } and {beam = }")
                try:
                    dark_array = self.intermediate_frame_helpers_load_dark_array(
                        beam=beam, exposure_time=exp_time
                    )
                except StopIteration:
                    raise ValueError(f"No matching dark found for {exp_time = } s")

                for modstate in range(1, self.constants.num_modstates + 1):
                    input_solar_arrays = self.input_frame_loaders_solar_gain_array_generator(
                        beam=beam,
                        modstate=modstate,
                        exposure_time=exp_time,
                    )
                    avg_solar_array = average_numpy_arrays(input_solar_arrays)

                    dark_corrected_solar_array = next(
                        subtract_array_from_arrays(
                            arrays=avg_solar_array, array_to_subtract=dark_array
                        )
                    )

                    logging.info(f"Writing dark corrected data for {beam=}, {modstate=}")
                    self.intermediate_frame_helpers_write_arrays(
                        arrays=dark_corrected_solar_array,
                        beam=beam,
                        modstate=modstate,
                        task="GC_BASIC",
                    )

    def compute_beam_angle(self, beam: int) -> float:
        """
        Find the angle between the slit hairlines and the pixel axes for a single beam.

        Generally, the algorithm is:

         1. Convert the spectra to a binary image that separates the lower-signal hairlines
         2. Use a Hough Transform to identify these hairlines
         3. Fit a peak to the Hough array to find the most prominant angle

        Parameters
        ----------
        beam : int
            The current beam being processed

        Returns
        -------
        float
            Beam angle in radians
        """
        logging.info(f"Finding angle using modstate 1 from beam {beam}")
        beam_array = self.find_brightest_modstate(beam=beam)

        numotsu = self.parameters.geo_num_otsu
        numtheta = self.parameters.geo_num_theta
        theta_min = self.parameters.geo_theta_min
        theta_max = self.parameters.geo_theta_max

        binary = make_binary(beam_array, numotsu=numotsu)
        H, t, r = do_hough(binary, theta_min=theta_min, theta_max=theta_max, numtheta=numtheta)
        peak_theta = -1 * float(find_px_angles(H, t)[0])

        logging.info(f"Beam angle for {beam=}: {np.rad2deg(peak_theta):0.3f} deg")
        return peak_theta

    def refine_beam2_angle(self, beam_2_init_angle: float) -> float:
        """Find the angular adjustment needed to align beam 2's spectra with beam 1.

        Because this angle will apply to all modulation states the comparison is made between averages over all
        modulation states of beam 1 and beam 2. First, a rough, global, offset is computed and then a minimizer
        minimizes the difference between the beams after applying first a rotation, then an offset to beam 2.

        To reduce the influence of low-frequency differences between the beams (e.g., optical gain resonse) the beam
        averages are first put through a high-pass filter that preserves hairlines and spectral features (which are
        sharp).
        """
        beam_1_angle = self.intermediate_frame_helpers_load_angle(beam=1)
        beam_1_hpf, beam_1_mask = self.prep_refine_ang_input(beam=1, angle=beam_1_angle)
        beam_2_hpf, beam_2_mask = self.prep_refine_ang_input(beam=2, angle=beam_2_init_angle)

        logging.info("Computing rough-guess average beam offset")
        x_init, y_init = self.compute_single_state_offset(
            beam_1_hpf, beam_2_hpf, fiducial_mask=beam_1_mask, array_mask=beam_2_mask
        )

        logging.info("Fitting beam 2 angle refinement")
        res = spo.minimize(
            self.refine_ang_func,
            np.array(
                [
                    x_init,
                    y_init,
                    0.0,
                ]
            ),
            args=(beam_1_hpf, beam_2_hpf),
            method="nelder-mead",
        )

        angle = res.x[2]
        if abs(angle) > self.parameters.geo_max_beam_2_angle_refinement:
            logging.info(f"Refining angle is too large ({np.rad2deg(angle)} deg). Not using it.")
            return 0.0

        return angle

    def prep_refine_ang_input(self, beam: int, angle: float) -> tuple[np.ndarray, np.ndarray]:
        """Prepare an averaged, high-pass-filtered array for a single beam.

        Average is over all modulation states.
        """
        logging.info(f"Prepping beam {beam} data for angle refinement")
        arrays = list(
            self.intermediate_frame_helpers_load_intermediate_arrays(beam=beam, task="GC_BASIC")
        )
        angle_corr_arrays = self.corrections_correct_geometry(arrays, angle=angle)
        modstate_avg = np.mean(np.stack(angle_corr_arrays), axis=0)

        mask = self.compute_offset_mask(modstate_avg)
        high_pass_filtered_array = self.high_pass_filter_array(modstate_avg)

        return high_pass_filtered_array, mask

    @staticmethod
    def refine_ang_func(x, target, image) -> float:
        """Rotate and shift beam 2 then compare for similarity with beam 1."""
        xshift, yshift, ang = x
        rotated = next(GeometricCalibration.corrections_correct_geometry(image, angle=ang))
        shifted = next(
            GeometricCalibration.corrections_correct_geometry(
                rotated, shift=np.array([xshift, yshift])
            )
        )
        metric = 1 - skim.structural_similarity(target, shifted)
        return metric

    def remove_beam_angle(self, angle: float, beam: int, modstate: int) -> np.ndarray:
        """
        Rotate a single modstate and beam's data by the beam angle.

        Parameters
        ----------
        angle : float
            The beam angle (in radians) for the current modstate
        beam : int
            The current beam being processed
        modstate : int
            The current modstate

        Returns
        -------
        np.ndarray
            Array corrected for beam angle
        """
        beam_mod_array = self.basic_corrected_data(beam=beam, modstate=modstate)
        corrected_array = next(self.corrections_correct_geometry(beam_mod_array, angle=angle))
        return corrected_array

    def compute_modstate_offset(self, array: np.ndarray, beam: int, modstate: int) -> np.ndarray:
        """
        Higher-level helper function to compute the (x, y) offset between modstates.

        Exists so the fiducial array can be set from the first beam and modstate.

        Parameters
        ----------
        array : np.ndarray
            Beam data
        beam : int
            The current beam being processed
        modstate : int
            The current modstate

        Returns
        -------
        np.ndarray
            (x, y) offset between modstates
        """
        if beam == 1 and modstate == 1:
            logging.info("Set fiducial array")
            self.fiducial_array = self.high_pass_filter_array(array)
            self.fiducial_mask = self.compute_offset_mask(array)
            return np.zeros(2)

        hpf_array = self.high_pass_filter_array(array)
        array_mask = self.compute_offset_mask(array)
        shift = self.compute_single_state_offset(
            fiducial_array=self.fiducial_array,
            array=hpf_array,
            upsample_factor=self.parameters.geo_upsample_factor,
            fiducial_mask=self.fiducial_mask,
            array_mask=array_mask,
        )
        logging.info(
            f"Offset for {beam = } and {modstate = } is {np.array2string(shift, precision=3)}"
        )

        return shift

    def remove_state_offset(
        self, array: np.ndarray, offset: np.ndarray, beam: int, modstate: int
    ) -> None:
        """
        Shift an array by some offset (to make it in line with the fiducial array).

        Parameters
        ----------
        array : np.ndarray
            Beam data
        offset : np.ndarray
            The state offset for the current modstate
        beam : int
            The current beam being processed
        modstate : int
            The current modstate

        Returns
        -------
        None

        """
        corrected_array = next(self.corrections_correct_geometry(array, shift=offset))
        self.intermediate_frame_helpers_write_arrays(
            arrays=corrected_array, modstate=modstate, beam=beam, task="GC_OFFSET"
        )

    def compute_spectral_shifts(self, beam: int) -> np.ndarray:
        """
        Compute the spectral 'curvature'.

        I.e., the spectral shift at each slit position needed to have wavelength be constant across a single spatial
        pixel. Generally, the algorithm is:

         1. Identify the fiducial spectrum as the center of the slit
         2. For each slit position, make an initial guess of the shift via correlation
         3. Take the initial guesses and use them in a chisq minimizer to refine the shifts
         4. Interpolate over those shifts identified as too large
         5. Remove the mean shift so the total shift amount is minimized

        Parameters
        ----------
        beam : int
            The current beam being processed

        Returns
        -------
        np.ndarray
            Spectral shift for a single beam
        """
        max_shift = self.parameters.geo_max_shift
        poly_fit_order = self.parameters.geo_poly_fit_order

        logging.info(f"Computing spectral shifts for beam {beam}")
        beam_generator = self.offset_corrected_array_generator(beam=beam)
        avg_beam_array = average_numpy_arrays(beam_generator)
        num_spec = avg_beam_array.shape[1]

        self.intermediate_frame_helpers_write_arrays(
            arrays=avg_beam_array, beam=beam, task="DEBUG_GC_AVG_OFFSET"
        )

        ref_spec = avg_beam_array[:, num_spec // 2]
        beam_shifts = np.empty(num_spec) * np.nan
        for j in range(num_spec):
            target_spec = avg_beam_array[:, j]

            ## Correlate the target and reference beams to get an initial guess
            corr = np.correlate(
                target_spec - np.nanmean(target_spec),
                ref_spec - np.nanmean(ref_spec),
                mode="same",
            )
            # This min_dist ensures we only find a single peak in each correlation signal
            pidx = pku.indexes(corr, min_dist=corr.size)
            initial_guess = 1 * (pidx - corr.size // 2)

            # These edge-cases are very rare, but do happen sometimes
            if initial_guess.size == 0:
                logging.info(
                    f"Spatial position {j} in {beam=} doesn't have a correlation peak. Initial guess set to 0"
                )
                initial_guess = 0.0

            elif initial_guess.size > 1:
                logging.info(
                    f"Spatial position {j} in {beam=} has more than one correlation peak ({initial_guess}). Initial guess set to mean ({np.nanmean(initial_guess)})"
                )
                initial_guess = np.nanmean(initial_guess)

            ## Then refine shift with a chisq minimization
            shift = minimize(
                self.shift_chisq,
                np.array([float(initial_guess)]),
                args=(ref_spec, target_spec),
                method="nelder-mead",
            ).x[0]
            if np.abs(shift) > max_shift:
                # Didn't find a good peak, probably because of a hairline
                logging.info(
                    f"shift in {beam=} at spatial pixel {j} out of range ({shift} > {max_shift})"
                )
                continue

            beam_shifts[j] = shift

        ## Subtract the average so we shift my a minimal amount
        beam_shifts -= np.nanmean(beam_shifts)

        ## Finally, fit the shifts and return the resulting polynomial
        nan_idx = np.isnan(beam_shifts)
        poly = np.poly1d(
            np.polyfit(np.arange(num_spec)[~nan_idx], beam_shifts[~nan_idx], poly_fit_order)
        )

        return poly(np.arange(num_spec))

    @staticmethod
    def compute_single_state_offset(
        fiducial_array: np.ndarray,
        array: np.ndarray,
        upsample_factor: float = 1000.0,
        fiducial_mask: np.ndarray | None = None,
        array_mask: np.ndarray | None = None,
    ) -> np.ndarray:
        """
        Find the (x, y) shift between the current beam and the reference beam.

        The shift is found by fitting the peak of the correlation of the two beams

        Parameters
        ----------
        fiducial_array : np.ndarray
            Reference beam from mod state 1 data

        array : np.ndarray
            Beam data from current mod state

        Returns
        -------
        numpy.ndarray
            The (x, y) shift between the reference beam and the current beam at hand
        """
        shift = skir.phase_cross_correlation(
            fiducial_array,
            array,
            return_error=False,
            reference_mask=fiducial_mask,
            moving_mask=array_mask,
        )

        if upsample_factor != 1.0:
            logging.info(f"Rough shift = {np.array2string(-1 * shift, precision=3)}")
            shift = GeometricCalibration.refine_modstate_shift(
                shift, fiducial_array, array, upsample_factor=upsample_factor
            )

        # Multiply by -1 so that the output is the shift needed to move from "perfect" to the current state.
        #  In other words, applying a shift equal to the negative of the output of this function will undo the measured
        #  shift.
        return -shift

    @staticmethod
    def refine_modstate_shift(
        shifts: np.ndarray,
        fiducial_array: np.ndarray,
        target_array: np.ndarray,
        upsample_factor: float = 10.0,
    ):
        """Refine a shift from `compute_single_state_offset` using an upsampling technique.

        This is taken directly from the un-masked version of `skimage.registration.phase_cross_correlation`.
        """
        # All comments below are copied from `skimage.registration.phase_cross_correlation`
        src_freq = fftn(fiducial_array)
        target_freq = fftn(target_array)
        image_product = src_freq * target_freq.conj()

        upsample_factor = np.array(upsample_factor, dtype=fiducial_array.dtype)
        shifts = np.round(shifts * upsample_factor) / upsample_factor
        upsampled_region_size = np.ceil(upsample_factor * 1.5)
        # Center of output array at dftshift + 1
        dftshift = np.fix(upsampled_region_size / 2.0)
        # Matrix multiply DFT around the current shift estimate
        sample_region_offset = dftshift - shifts * upsample_factor
        cross_correlation = _upsampled_dft(
            image_product.conj(), upsampled_region_size, upsample_factor, sample_region_offset
        ).conj()
        # Locate maximum and map back to original pixel grid
        maxima = np.unravel_index(np.argmax(np.abs(cross_correlation)), cross_correlation.shape)

        maxima = np.stack(maxima).astype(fiducial_array.dtype, copy=False)
        maxima -= dftshift

        shifts += maxima / upsample_factor

        return shifts

    def compute_offset_mask(self, array: np.ndarray) -> np.ndarray:
        """Generate a 2D mask that exclude non-line regions.

        These masks are then used to greatly improve the accuracy of the phase cross-correlation used in
        `compute_single_state_offset`.
        """
        zone_kwargs = {
            "prominence": self.parameters.solar_zone_prominence,
            "width": self.parameters.solar_zone_width,
            "bg_order": self.parameters.solar_zone_bg_order,
            "normalization_percentile": self.parameters.solar_zone_normalization_percentile,
            "rel_height": self.parameters.solar_zone_rel_height,
        }
        zones = SolarCalibration.compute_line_zones(array, **zone_kwargs)
        logging.info(f"Found {zones = }")
        mask = np.zeros(array.shape).astype(bool)
        for z in zones:
            mask[z[0] : z[1], :] = True

        return mask

    def find_brightest_modstate(self, beam: int) -> np.ndarray:
        """
        Return the array for the modstate with the largest median value.

        The idea here is that the brightest array will have the highest contrast between the spectra and the slit
        hairlines, which helps in the latter's identification. It's very possible that this function doesn't make
        any meaningful difference.
        """
        brightest_array = None
        brightest_modstate = np.nan
        median = -np.inf
        for m in range(1, self.constants.num_modstates + 1):
            array = self.basic_corrected_data(beam=beam, modstate=m)
            new_median = np.median(array)
            logging.info(f"Modstate {m} has median {new_median}")
            if new_median > median:
                median = new_median
                brightest_array = array
                brightest_modstate = m

        logging.info(f"Brightest modstate is {brightest_modstate}")
        return brightest_array

    @staticmethod
    def high_pass_filter_array(array: np.ndarray) -> np.ndarray:
        """Perform a simple high-pass filter to accentuate narrow features (hairlines and spectra)."""
        return array / spnd.gaussian_filter(array, sigma=5)

    @staticmethod
    def shift_chisq(par: np.ndarray, ref_spec: np.ndarray, spec: np.ndarray) -> float:
        """
        Goodness of fit calculation for a simple shift. Uses simple chisq as goodness of fit.

        Less robust than SolarCalibration's `refine_shift`, but much faster.

        Parameters
        ----------
        par : np.ndarray
            Spectral shift being optimized

        ref_spec : np.ndarray
            Reference spectra (from first modstate)

        spec : np.ndarray
            Spectra being fitted

        Returns
        -------
        float
            Sum of chisquared fit

        """
        shift = par[0]
        shifted_spec = spnd.shift(spec, -shift, mode="constant", cval=np.nan)
        chisq = np.nansum((ref_spec - shifted_spec) ** 2 / ref_spec)
        return chisq

    def write_angle(self, angle: float, beam: int) -> None:
        """
        Write the angle component of the geometric calibration for a single beam.

        Parameters
        ----------
        angle : float
            The beam angle (radians) for the current modstate

        beam : int
            The current beam being processed

        Returns
        -------
        None
        """
        array = np.array([angle])
        self.intermediate_frame_helpers_write_arrays(
            arrays=array, beam=beam, task="GEOMETRIC_ANGLE"
        )

    def write_state_offset(self, offset: np.ndarray, beam: int, modstate: int) -> None:
        """
        Write the state offset component of the geometric calibration for a single modstate and beam.

        Parameters
        ----------
        offset : np.ndarray
            The state offset for the current modstate

        beam : int
            The current beam being processed

        modstate : int
            The current modstate

        Returns
        -------
        None

        """
        self.intermediate_frame_helpers_write_arrays(
            arrays=offset, beam=beam, modstate=modstate, task="GEOMETRIC_OFFSET"
        )

    def write_spectral_shifts(self, shifts: np.ndarray, beam: int) -> None:
        """
        Write the spectral shift component of the geometric calibration for a single beam.

        Parameters
        ----------
        shifts : np.ndarray
            The spectral shifts for the current beam

        beam : int
            The current beam being processed

        Returns
        -------
        None

        """
        self.intermediate_frame_helpers_write_arrays(
            arrays=shifts, beam=beam, task="GEOMETRIC_SPEC_SHIFTS"
        )
