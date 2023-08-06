from FiberFusing import Geometry, BackGround
import FiberFusing
from SuPyMode.solver import SuPySolver
import FiberFusing.fiber_catalogue as fiber_catalogue

from PyFinitDiff.boundaries import Boundaries2D


def workflow(*fiber_list,
             resolution: int = 200,
             wavelength: float = 1.55e-6,
             n_sorted_mode: int = 15,
             plot_geometry: bool = False,
             plot_cladding: bool = False,
             fusion_degree: float = 0.85,
             initial_itr: float = 1.0,
             final_itr: float = 0.05,
             n_step: int = 500,
             plot_field: bool = False,
             plot_adiabatic: bool = False,
             compute_modes: bool = True,
             generate_report: bool = False,
             compute_anti_symmetric: bool = False,
             x_bounds: str = 'centering',
             y_bounds: str = 'centering',
             boundaries: Boundaries2D = Boundaries2D(),
             save_superset: bool = True,
             directory: str = 'auto',
             filename: str = 'auto'):

    match len(fiber_list):
        case 1:
            clad_structure = FiberFusing.Fused1
        case 2:
            clad_structure = FiberFusing.Fused2
        case 3:
            clad_structure = FiberFusing.Fused3
        case 4:
            clad_structure = FiberFusing.Fused4

    silica_index = fiber_catalogue.get_silica_index(wavelength=wavelength)

    clad = clad_structure(
        fiber_radius=62.5e-6,
        index=silica_index,
        core_position_scrambling=0
    )

    for n, fiber in enumerate(fiber_list):
        fiber.set_position(clad.cores[n])

    geometry = Geometry(
        background=BackGround(index=1),
        structures=[clad],
        x_bounds=x_bounds,
        y_bounds=y_bounds,
        n=resolution,
        index_scrambling=0,
        gaussian_filter=None,
        boundary_pad_factor=1.1
    )

    geometry.add_fiber(*fiber_list)

    if plot_geometry:
        geometry.plot().show()

    if not compute_modes:
        return
    solver = SuPySolver(
        geometry=geometry,
        tolerance=1e-5,
        max_iter=1000,
        show_iteration=True,
        accuracy=2,
        show_eigenvalues=False,
        extrapolation_order=1
    )

    solver.init_superset(
        wavelength=wavelength,
        n_step=n_step,
        itr_i=initial_itr,
        itr_f=final_itr
    )

    for boundary in boundaries:
        solver.add_modes(
            n_computed_mode=n_sorted_mode + 10,
            n_sorted_mode=n_sorted_mode,
            auto_labeling=False,
            boundaries=boundary
        )

    solver.superset.sorting_modes('beta')

    if plot_field:
        figure = solver.superset.plot(plot_type='field')
        figure.show_colorbar = False
        figure.show_ticks = False
        figure.x_label = ''
        figure.y_label = ''
        figure.show()

    if plot_adiabatic:
        solver.superset.plot(plot_type='adiabatic').show()

    if filename == 'auto':
        filename = "_".join(
            [clad_structure.__name__] +
            [fiber.__class__.__name__ for fiber in fiber_list] +
            [str(resolution)] +
            [f'wavelength_{wavelength}']
        )

    if save_superset:
        solver.superset.save_instance(
            filename=filename,
            directory=directory
        )

    if generate_report:
        solver.superset.generate_report(
            filename=filename + ".pdf",
            directory=directory,
        )
# -
