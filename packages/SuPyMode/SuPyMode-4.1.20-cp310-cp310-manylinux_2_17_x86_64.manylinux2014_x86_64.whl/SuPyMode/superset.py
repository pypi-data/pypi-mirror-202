#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import pickle
import numpy
import logging
import matplotlib.pyplot as plt
from dataclasses import dataclass
from pathlib import Path
from itertools import combinations

# Third-party imports
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
import pyvista

# Local imports
from SuPyMode.supermode import SuperMode
from SuPyMode.slice_structure import SliceStructure
from SuPyMode.tools import plot_style
from SuPyMode.profiles import AlphaProfile
from SuPyMode.tools import directories
from MPSPlots.Render2D import Scene2D, Axis, Multipage, Line, ColorBar, Mesh
from MPSPlots import colormaps


@dataclass
class SuperSet(object):
    """
    Solver to which is associated the computed SuperSet Modes

    .. note::
        This class is a representation of the fiber optic structures set of supermodes, hence the name.
        This class has not ling to c++ codes, it is pure Python.
        The items of this class are the supermodes generated from within the SuPySolver

    """
    parent_solver: object
    wavelength: float

    def __post_init__(self):
        self.wavenumber = 2 * numpy.pi / self.wavelength
        self._transmission_matrix = None
        self.supermodes = []
        self._itr_to_slice = interp1d(self.itr_list, numpy.arange(self.itr_list.size))

    def __getitem__(self, idx: int):
        return self.supermodes[idx]

    def __setitem__(self, idx: int, value):
        self.supermodes[idx] = value

    @property
    def geometry(self):
        """
        Return geometry of the coupler structure
        """
        return self.parent_solver.geometry

    @property
    def itr_list(self):
        """
        Return list of itr value that are used to compute the supermodes
        """
        return self.parent_solver.itr_list

    @property
    def coordinate_system(self):
        """
        Return axes object of the geometry
        """
        return self.parent_solver.geometry.coordinate_system

    @property
    def transmission_matrix(self) -> numpy.ndarray:
        """
        Return supermode transfert matrix
        """
        if self._transmission_matrix is None:
            self.compute_transmission_matrix()

        return self._transmission_matrix

    def itr_to_slice(self, itr_list: list[int], floor_down: bool = True) -> list[int]:
        """
        Return slice number associated to itr value

        :param      itr_list:      Inverse taper ration value to evaluate the slice.
        :type       itr_list:      { type_description }

        :returns:   List of itr values,
        :rtype:     list[float]
        """
        itr_list = numpy.asarray(itr_list)
        itr_i = self.itr_list[0]
        itr_f = self.itr_list[-1]

        assert numpy.all((itr_list >= itr_f) & (itr_i >= itr_list)), \
            f"ITR evaluation: {itr_list} is outside the boundaries!"

        if floor_down:
            return numpy.floor(self._itr_to_slice(itr_list)).astype(int)

        else:
            return numpy.ceil(self._itr_to_slice(itr_list)).astype(int)

    def slice_to_itr(self, slice_list: list[int]) -> list[float]:
        """
        Return slice number associated to itr value

        :param      slice_list:      Value of the slice to which evaluate the itr.
        :type       slice_list:      list[int]

        :returns:   List of itr values,
        :rtype:     list[float]
        """
        return [self.itr_list[i] for i in slice_list]

    def label_supermodes(self, *label_list, auto=False) -> None:
        for n, label in enumerate(label_list):
            self[n].label = label
            setattr(self, label, self[n])

        return [getattr(self, label) for label in label_list]

    def swap_supermode_order(self, idx0: int, idx1: int) -> "SuperSet":
        """
        Swap two supermodes.
        it doesn't change any of their characteristic, it only changes the
        order on whihc they will appear, notably for the plots.

        :param      idx0:            Index of the first mode to swap
        :type       idx0:            int
        :param      idx1:            Index of the second mode to swap
        :type       idx1:            int
        """
        self.supermodes[idx0], self.supermodes[idx1] = self.supermodes[idx1], self.supermodes[idx0]

        return self

    def get_slice_structure(self, itr: int, add_symmetries: bool = True) -> SliceStructure:
        x, y = self.supermodes[0].get_axis_vector()

        output_slice = SliceStructure(
            parent_superset=self,
            itr=itr,
            supermodes=self.supermodes,
            add_symmetries=add_symmetries
        )

        return output_slice

    def compute_transmission_matrix(self) -> None:
        """
        Calculates the transmission matrix with only the propagation constant included.

        :returns:   The transmission matrix.
        :rtype:     numpy.ndarray
        """
        shape = [
            len(self.supermodes),
            len(self.supermodes),
            len(self.itr_list)
        ]

        self._transmission_matrix = numpy.zeros(shape)

        for mode in self.supermodes:
            self._transmission_matrix[mode.mode_number, mode.mode_number, :] = mode.beta._data * 2.0 * numpy.pi

    def add_coupling_to_t_matrix(self,
                                 t_matrix: numpy.ndarray,
                                 adiabatic_factor: numpy.ndarray
                                 ) -> numpy.ndarray:
        """
        Add the coupling coefficients to the transmission matrix.

        :returns:   The transmission matrix.
        :rtype:     numpy.ndarray
        """

        size = t_matrix.shape[-1]

        t_matrix = t_matrix.astype(complex)
        for mode_0, mode_1 in combinations(self.supermodes, 2):
            coupling = mode_0.normalized_coupling.get_values(mode_1)[:size] * adiabatic_factor

            t_matrix[mode_0.mode_number, mode_1.mode_number, :] = - coupling
            t_matrix[mode_1.mode_number, mode_0.mode_number, :] = + coupling

        return t_matrix

    def compute_coupling_factor(self, coupler_length: float) -> numpy.ndarray:
        r"""
        Compute the coupling factor defined as:
        .. math::
            f_c = \frac{1}{\rho} \frac{d \rho}{d z}

        :param      coupler_length:     The length of the coupler
        :type       coupler_length:     float

        :returns:   The amplitudes as a function of the distance in the coupler
        :rtype:     numpy.ndarray
        """

        dx = coupler_length / (self.itr_list.size)

        ditr = numpy.gradient(numpy.log(self.itr_list), axis=0)

        return ditr / dx

    def get_transmision_matrix_from_profile(self,
                                            profile: AlphaProfile,
                                            with_coupling: bool = True,
                                            coupling_factor: float = 1
                                            ) -> tuple:
        """
        Gets the transmision matrix from profile.

        :param      profile:          The z-profile of the coupler
        :type       profile:          object
        :param      with_coupling:    Adding the mode coupling or not to the propagation problem
        :type       with_coupling:    bool
        :param      coupling_factor:  Factor to be mutliplied to the coupling coefficients
        :type       coupling_factor:  float
        """
        final_slice = self.itr_to_slice(itr_list=profile.smallest_itr, floor_down=True)

        sub_t_matrix = self.transmission_matrix[..., :final_slice]

        sub_itr_vector = self.itr_list[: final_slice]

        array_coupling_factor = profile.evaluate_adiabatic_factor(itr=sub_itr_vector)

        if with_coupling:
            sub_t_matrix = self.add_coupling_to_t_matrix(
                t_matrix=sub_t_matrix,
                adiabatic_factor=array_coupling_factor * coupling_factor
            )

        sub_distance = profile.evaluate_distance_vs_itr(sub_itr_vector)

        return sub_distance, sub_itr_vector, sub_t_matrix

    def propagate(self,
                  profile: AlphaProfile,
                  initial_amplitude: list,
                  max_step: float = None,
                  with_coupling: bool = True,
                  coupling_factor: float = 1,
                  method: str = 'RK45',
                  **kwargs) -> numpy.ndarray:
        """
        Returns the amplitudes value of the supermodes in the coupler.

        :param      initial_amplitude:  The initial amplitude
        :type       initial_amplitude:  list
        :param      profile:            The z-profile of the coupler
        :type       profile:            object
        :param      max_step:           The maximum stride to use in the solver
        :type       max_step:           float
        :param      with_coupling:      Adding the mode coupling or not to the propagation problem
        :type       with_coupling:      bool
        :param      kwargs:             The keywords arguments to be passed to the solver
        :type       kwargs:             dictionary

        :returns:   The amplitudes as a function of the distance in the coupler
        :rtype:     numpy.ndarray
        """
        initial_amplitude = numpy.asarray(initial_amplitude).astype(complex)

        if max_step is None:
            max_step = self.parent_solver.wavelength / 200

        sub_distance, sub_itr_vector, sub_t_matrix = self.get_transmision_matrix_from_profile(
            profile=profile,
            with_coupling=with_coupling,
            coupling_factor=coupling_factor
        )

        z_to_itr = interp1d(
            profile.distance,
            profile.itr_list,
            bounds_error=False,
            fill_value='extrapolate',
            axis=-1
        )

        itr_to_t_matrix = interp1d(
            sub_itr_vector,
            sub_t_matrix,
            bounds_error=False,
            fill_value='extrapolate',
            axis=-1
        )

        def model(z, y):
            itr = z_to_itr(z)
            return 1j * itr_to_t_matrix(itr).dot(y)

        sol = solve_ivp(
            model,
            y0=initial_amplitude,
            t_span=[0, profile.length],
            vectorized=True,
            max_step=max_step,
            method=method,
            **kwargs
        )

        norm = (numpy.abs(sol.y)**2).sum(axis=0)

        if not numpy.all(numpy.isclose(norm, 1.0, atol=1e-1)):
            logging.warning(f'Warning Power conservation is not acheived [tol: 1e-1]. You should considerate reducing the max step size [{max_step}]')

        return sol.t, sol.y, z_to_itr(sol.t)

    def interpret_initial_input(self, initial_amplitude):

        if isinstance(initial_amplitude, SuperMode):
            return initial_amplitude.amplitudes
        else:
            return numpy.asarray(initial_amplitude).astype(complex)

    def plot_propagation(self,
                         profile: AlphaProfile,
                         initial_amplitude,
                         max_step: float = None,
                         with_coupling: bool = True,
                         coupling_factor: float = 1,
                         method: str = 'RK45',
                         sub_sampling: int = 5,
                         save_directory: str = 'new_figure.gif',
                         **kwargs) -> tuple:

        initial_amplitude = self.interpret_initial_input(
            initial_amplitude=initial_amplitude
        )

        z, amplitudes, itr_list = self.propagate(
            initial_amplitude=initial_amplitude,
            profile=profile,
            with_coupling=with_coupling,
            max_step=max_step,
            method=method
        )

        slc = slice(None, None, sub_sampling)
        figure, ax = plt.subplots(1, 1, figsize=(16, 6))

        for n, mode in enumerate(self.supermodes):
            ax.plot(z[slc], abs(amplitudes[n][slc])**2, label=mode.stylized_label)

        ax1 = ax.twinx()

        ax1.plot(z, itr_list, 'k--', label='coupler profile')

        ax1.legend()
        ax.legend()

        ax.set_xlabel('Propagation distance z')
        ax.set_ylabel('Mode power distribution')
        ax1.set_ylabel('Inverse taper ratio')
        plt.tight_layout()
        plt.savefig(f'{save_directory}')
        plt.show()

        return z, amplitudes, itr_list

    def generate_propagation_gif(self,
                                 profile: AlphaProfile,
                                 initial_amplitude,
                                 max_step: float = None,
                                 with_coupling: bool = True,
                                 coupling_factor: float = 1,
                                 method: str = 'RK45',
                                 sub_sampling: int = 5,
                                 factor: float = 1,
                                 save_directory: str = 'new_figure.gif',
                                 delta_azimuth: float = 0,
                                 **kwargs) -> tuple:
        """
        Generates a gif video of the mode propagation.

        :param      initial_amplitude:  The initial amplitude
        :type       initial_amplitude:  list
        :param      coupler_length:     The length of the coupler
        :type       coupler_length:     float
        :param      max_step:           The maximum stride to use in the solver
        :type       max_step:           float
        :param      sub_sampling:       Propagation undersampling factor for the video production
        :type       sub_sampling:       int
        :param      kwargs:             The keywords arguments
        :type       kwargs:             dictionary
        """

        initial_amplitude = self.interpret_initial_input(
            initial_amplitude=initial_amplitude
        )

        z_list, amplitudes_list, itr_list = self.propagate(
            initial_amplitude=initial_amplitude,
            profile=profile,
            with_coupling=with_coupling,
            max_step=max_step,
            method=method
        )

        self.generate_propagation_gif_from_values(
            amplitudes_list=amplitudes_list,
            itr_list=itr_list,
            z_list=z_list,
            factor=factor,
            save_directory=save_directory,
            delta_azimuth=delta_azimuth,
            sub_sampling=sub_sampling
        )

        return z_list, amplitudes_list, itr_list

    def generate_propagation_gif_from_values(self,
                                             amplitudes_list: numpy.ndarray,
                                             itr_list: numpy.ndarray,
                                             z_list: numpy.ndarray,
                                             sub_sampling: int = 10000,
                                             factor: float = -100,
                                             delta_azimuth: float = 0,
                                             save_directory: str = 'new_figure.gif',
                                             colormap: str = 'bwr',
                                             **kwargs) -> None:
        """
        Generates a gif video of the mode propagation.

        :param      initial_amplitude:  The initial amplitude
        :type       initial_amplitude:  list
        :param      coupler_length:     The length of the coupler
        :type       coupler_length:     float
        :param      max_step:           The maximum stride to use in the solver
        :type       max_step:           float
        :param      sub_sampling:       Propagation undersampling factor for the video production
        :type       sub_sampling:       int
        :param      kwargs:             The keywords arguments
        :type       kwargs:             dictionary
        """
        amplitudes_list = amplitudes_list[:, ::sub_sampling]
        itr_list = itr_list[::sub_sampling]
        z_list = z_list[::sub_sampling]

        structure = self.get_slice_structure(itr=1.0, add_symmetries=True)
        total_field = structure.get_field_combination(amplitudes_list[:, 0], Linf_normalization=True) * factor

        x, y = numpy.mgrid[0: total_field.shape[0], 0: total_field.shape[1]]
        grid = pyvista.StructuredGrid(x, y, total_field)

        plotter = pyvista.Plotter(notebook=False, off_screen=True)
        plotter.open_gif(save_directory, fps=20)
        plotter.view_isometric()
        # plotter.set_background('black', top='white')

        plotter.add_mesh(
            grid,
            scalars=total_field,
            style='surface',
            show_edges=True,
            edge_color='k',
            colormap=colormap,
            show_scalar_bar=False,
            clim=[-100, 100]
        )

        pts = grid.points.copy()
        azimuth = 0
        for z, amplitudes, itr in zip(z_list, amplitudes_list.T, itr_list):
            print(f'itr: {itr}')
            plotter.camera.elevation = -20
            plotter.camera.azimuth = azimuth
            azimuth += delta_azimuth

            structure = self.get_slice_structure(itr=itr, add_symmetries=True)
            total_field = structure.get_field_combination(amplitudes, Linf_normalization=True) * factor

            pts[:, -1] = total_field.T.ravel()
            plotter.update_coordinates(pts, render=True)
            plotter.update_scalars(total_field.T.ravel(), render=False)
            plotter.add_title(f'ITR: {itr: .3f}\t  z: {z: .3e}', font='courier', color='w', font_size=20)

            plotter.write_frame()

        plotter.close()

    def _sorting_modes_(self, *ordering_list) -> None:
        """
        Generic mode sorting method

        :param      ordering_parameters:  The ordering list to sort the supermodes
        :type       ordering_parameters:  list
        """
        order = numpy.lexsort(ordering_list)

        supermodes = [self.supermodes[idx] for idx in order]

        for n, supermode in enumerate(supermodes):
            supermode.mode_number = n

        return supermodes

    def sorting_modes_beta(self) -> None:
        """
        Re-order modes to sort them in descending value of propagation constant.
        """
        return self._sorting_modes_([-mode.beta[-1] for mode in self.supermodes])

    def sorting_modes(self, sorting_method: str = "beta", keep_only: int = None) -> None:
        """
        Re-order modes according to a sorting method, either "beta" or "symmetry+beta".
        The final mode selection will also be filter to keep only a certain number of modes
        """
        assert sorting_method.lower() in ["beta", "symmetry+beta"], \
            f"Unrecognized sortingmethod: {sorting_method}, accepted values are ['beta', 'symmetry+beta']"

        match sorting_method.lower():
            case "beta":
                supermodes = self.sorting_modes_beta()
            case "symmetry+beta":
                supermodes = self.sorting_modes_solver_beta()

        self.all_supermodes = supermodes

        self.supermodes = supermodes[:keep_only]

    def sorting_modes_solver_beta(self):
        """
        Re-order modes to sort them in with two parameters:
        ascending cpp_solver number and descending value of propagation constant.
        """
        return self._sorting_modes_(
            [-mode.beta[-1] for mode in self.supermodes],
            [mode.solver_number for mode in self.supermodes],
        )

    def _interpret_itr_slice_list_(self, slice_list: list, itr_list: list):
        slice_list = [*slice_list, *self.itr_to_slice(itr_list)]

        if len(slice_list) == 0:
            slice_list = [0, -1]

        itr_list = self.slice_to_itr(slice_list)

        itr_list = numpy.sort(itr_list)[::-1]

        return self.itr_to_slice(itr_list), itr_list

    @staticmethod
    def single_plot(plot_function):
        def wrapper(self, *args, **kwargs):
            figure = Scene2D(unit_size=(16, 6))
            ax = Axis(row=0, col=0)
            figure.add_axes(ax)
            plot_function(self, ax=ax, *args, **kwargs)

            return figure

        return wrapper

    @single_plot
    def plot_index(self, ax: Axis) -> Scene2D:
        """
         Plot effective index for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.index)

        for mode in self.supermodes:
            y = mode.index.get_values()

            artist = Line(
                x=self.itr_list,
                y=y,
                label=f'{mode.stylized_label}'
            )

            ax.add_artist(artist)

    @single_plot
    def plot_beta(self, ax: Axis) -> Scene2D:
        """
         Plot propagation constant for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.beta)

        for mode in self.supermodes:
            y = mode.beta.get_values()

            artist = Line(
                x=self.itr_list,
                y=y,
                label=f'{mode.stylized_label}'
            )

            ax.add_artist(artist)

    @single_plot
    def plot_eigen_value(self, ax: Axis) -> Scene2D:
        """
         Plot propagation constant for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.eigen_value)

        for mode in self.supermodes:
            y = mode.eigen_value.get_values()
            artist = Line(x=self.itr_list, y=y, label=f'{mode.stylized_label}')
            ax.add_artist(artist)

    @single_plot
    def plot_normalized_coupling(self,
                                 ax: Axis,
                                 mode_of_interest: list = [],
                                 mode_selection='all'
                                 ) -> Scene2D:
        """
         Plot coupling value for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.normalized_coupling)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                y = numpy.abs(mode_0.normalized_coupling.get_values(other_supermode=mode_1))
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_label} - {mode_1.stylized_label}')
                ax.add_artist(artist)

    @single_plot
    def plot_overlap(self,
                     ax: Axis,
                     mode_of_interest: list = [],
                     mode_selection='all'
                     ) -> Scene2D:
        """
         Plot overlap value for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.overlap)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                y = mode_0.overlap.get_values(other_supermode=mode_1)
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_label} - {mode_1.stylized_label}')
                ax.add_artist(artist)

    @single_plot
    def plot_beating_length(self,
                            ax: Axis,
                            mode_of_interest: list = [],
                            mode_selection='all'
                            ) -> Scene2D:
        """
         Plot coupling value for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.beating_length)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                y = mode_0.beating_length.get_values(other_supermode=mode_1)
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_label} - {mode_1.stylized_label}')
                ax.add_artist(artist)

    @single_plot
    def plot_adiabatic(self,
                       ax: Axis,
                       mode_of_interest: list = [],
                       mode_selection: str = 'all',
                       add_profile: AlphaProfile = None
                       ) -> Scene2D:
        """
         Plot adiabatic criterion for each mode as a function of itr

        :param      pair_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       pair_of_interest:  list
        :param      mode_selection:    The type of combination to be plotted, either 'specific/all/pairs'
        :type       mode_selection:    str

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.adiabatic)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                y = mode_0.adiabatic.get_values(other_supermode=mode_1)
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_label} - {mode_1.stylized_label}')
                ax.add_artist(artist)

        if add_profile is not None:
            add_profile._render_adiabatic_factor_vs_itr_on_ax_(ax)

    @single_plot
    def plot_normalized_adiabatic(self,
                                  ax: Axis,
                                  mode_of_interest: list = [],
                                  mode_selection: str = 'all',
                                  ) -> Scene2D:
        """
         Plot adiabatic criterion for each mode as a function of itr

        :param      pair_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       pair_of_interest:  list
        :param      mode_selection:    The type of combination to be plotted, either 'specific/all/pairs'
        :type       mode_selection:    str

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.adiabatic)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                n0 = mode_0.index._data
                n1 = mode_1.index._data
                beating_length = mode_0.wavelength / abs(n0 - n1)
                y = mode_0.adiabatic.get_values(other_supermode=mode_1) * beating_length

                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_label} - {mode_1.stylized_label}')
                ax.add_artist(artist)

    def interpret_combinations(self, mode_of_interest: list, mode_selection: str):
        assert mode_selection in ['all', 'pairs', 'specific'], f"mode_selection: {mode_selection} not recoginized, argument have to be in ['all', 'pairs', 'specific']"
        match mode_selection:
            case 'all':
                combination = combinations(self.supermodes, 2)
            case 'pairs':
                combination = self.interpret_pair_of_interest(mode_of_interest)
            case 'specific':
                combination = self.interpret_mode_of_interest(mode_of_interest)

        return combination

    def interpret_pair_of_interest(self, mode_of_interest: list):
        """
        Interpret the argument mode_of_interest to isolate the
        only the pairs containing both of the mode of interests.

        :param      mode_of_interest:  The mode of interest
        :type       mode_of_interest:  list
        """
        combination = []
        for mode_0, mode_1 in combinations(mode_of_interest, 2):
            if mode_0.is_computation_compatible(mode_1):
                combination.append((mode_0, mode_1))

        return self.remove_duplicate_in_combination(combination)

    def interpret_mode_of_interest(self, mode_of_interest: list):
        """
        Interpret the argument mode_of_interest to isolate the
        only combinations that contains the modes of interests.

        :param      mode_of_interest:  The mode of interest
        :type       mode_of_interest:  list
        """
        combination = []
        for mode_0 in mode_of_interest:
            for mode_1 in self.supermodes:
                if mode_0.is_computation_compatible(mode_1):
                    combination.append((mode_0, mode_1))

        return self.remove_duplicate_in_combination(combination)

    def remove_duplicate_in_combination(self, combination: list):
        """
        Removes a duplicate tuple of modes pair in combination.

        :param      combination:  The cleaned combination
        :type       combination:  list
        """
        new_combination = []
        for mode_0, mode_1 in combination:
            couple = mode_0, mode_1
            if (mode_0, mode_1) not in new_combination and (mode_1, mode_0) not in new_combination:
                new_combination.append(couple)

        return new_combination

    def plot_field(self, itr_list: list[float] = [], slice_list: list[int] = []) -> Scene2D:
        """
        Plot each of the mode field for different itr value or slice number.

        :param      itr_list:    List of itr value to evaluate the mode field
        :type       itr_list:    list
        :param      slice_list:  List of integer reprenting the slice where the mode field is evaluated
        :type       slice_list:  list

        :returns:   The figure
        :rtype:     Scene2D
        """
        figure = Scene2D(unit_size=(3, 3))

        slice_list, itr_list = self._interpret_itr_slice_list_(slice_list, itr_list)

        for m, mode in enumerate(self.supermodes):
            for n, (itr, slice) in enumerate(zip(itr_list, slice_list)):
                ax = Axis(
                    row=n,
                    col=m,
                    title=f'{mode.stylized_label}\n[slice: {slice}  ITR: {itr:.4f}]'
                )

                ax.colorbar = ColorBar(symmetric=True, position='right')

                x, y, field = mode.field.get_field_with_boundaries(slice=slice)

                artist = Mesh(x=x, y=y, scalar=field, colormap=colormaps.blue_black_red)

                ax.add_artist(artist)

                ax.set_style(**plot_style.field)
                figure.add_axes(ax)

        return figure

    def plot(self, plot_type: str, **kwargs) -> Scene2D:
        """
        Generic plot function.

        Args:
            type: Plot type ['index', 'beta', 'adiabatic', 'normalized-adiabatic', 'overlap', 'coupling', 'field', 'beating-length']
        """
        match plot_type.lower():
            case 'index':
                return self.plot_index(**kwargs)
            case 'beta':
                return self.plot_beta(**kwargs)
            case 'eigen-value':
                return self.plot_eigen_value(**kwargs)
            case 'normalized-coupling':
                return self.plot_normalized_coupling(**kwargs)
            case 'overlap':
                return self.plot_overlap(**kwargs)
            case 'adiabatic':
                return self.plot_adiabatic(**kwargs)
            case 'field':
                return self.plot_field(**kwargs)
            case 'beating-length':
                return self.plot_beating_length(**kwargs)
            case 'normalized-adiabatic':
                return self.plot_normalized_adiabatic(**kwargs)

        plot_type_list = [
            'index',
            'beta',
            'eigen_value',
            'adiabatic',
            'overlap'
            'normalized-adiabatic',
            'normalized-coupling',
            'field',
            'beating-length'
        ]

        raise ValueError(f"plot type: {plot_type} not recognized, accepted values are: {plot_type_list}")

    def generate_report(self,
                        filename: str = "report",
                        directory: str = '.',
                        itr_list: list[float] = [],
                        slice_list: list[int] = [],
                        dpi: int = 200,
                        mode_of_interest: list = None,
                        mode_selection: str = 'all') -> None:
        """
        Generate a full report of the coupler properties as a .pdf file

        :param      filename:          Name of the Report file to be outputed.
        :type       filename:          str
        :param      itr_list:          List of itr value to evaluate the mode field.
        :type       itr_list:          Array
        :param      slice_list:        List of slice value to evaluate the mode field.
        :type       slice_list:        Array
        :param      dpi:               Pixel density for the image included in the report.
        :type       dpi:               int
        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   { description_of_the_return_value }
        :rtype:     None
        """
        if directory == 'auto':
            directory = directories.reports_directory

        filename = Path(directory).joinpath(filename).with_suffix('.pdf')

        logging.info(f"Saving report pdf into: {filename}")

        figures = []
        figures.append(self.geometry.plot()._render_())

        figures.append(self.plot_field(itr_list=itr_list, slice_list=slice_list)._render_())

        figures.append(self.plot_index()._render_())

        figures.append(self.plot_beta()._render_())

        figures.append(self.plot_normalized_coupling(mode_of_interest=mode_of_interest, mode_selection=mode_selection)._render_())

        figures.append(self.plot_adiabatic(mode_of_interest=mode_of_interest, mode_selection=mode_selection)._render_())

        Multipage(filename, figs=figures, dpi=dpi)

        for figure in figures:
            figure.close()

    def save_instance(self, filename: str, directory: str = '.'):
        """
        Saves the superset instance as a serialized pickle file.

        :param      filename:  The directory where to save the file, 'auto' options means the superset_instance folder
        :type       filename:  str
        :param      filename:  The filename
        :type       filename:  str
        """
        if directory == 'auto':
            directory = directories.instance_directory

        filename = Path(directory).joinpath(filename).with_suffix('.pickle')

        logging.info(f"Saving pickled superset into: {filename}")

        with open(filename, 'wb') as output_file:
            pickle.dump(self, output_file, pickle.HIGHEST_PROTOCOL)

# -
