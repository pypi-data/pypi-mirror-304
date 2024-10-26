from ase import Atoms
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS, LBFGS, FIRE, GPMin
from ase.optimize.sciopt import SciPyFminBFGS
from ase.units import GPa


def relax_structure(structure: Atoms,
                    fmax: float = 0.001,
                    steps: int = 500,
                    minimizer: str = 'bfgs',
                    constant_cell: bool = False,
                    constant_volume: bool = False,
                    scalar_pressure: float = 0.0,
                    **kwargs) -> None:
    """Relaxes the given structure.

    Parameters
    ----------
    structure
        Atomic configuration to relax.
    fmax
        Stop relaxation if the absolute force for all atoms falls below this value.
    steps
        Maximum number of relaxation steps the minimizer is allowed to take.
    minimizer
        Minimizer to use; possible values: 'bfgs', 'lbfgs', 'fire', 'gpmin', 'bfgs-scipy'.
    constant_cell
        If True do not relax the cell or the volume.
    constant_volume
        If True relax the cell shape but keep the volume constant.
    kwargs
        Keyword arguments to be handed over to the minimizer; possible arguments can be found
        in the `ASE documentation <https://wiki.fysik.dtu.dk/ase/ase/optimize.html>`_
        https://wiki.fysik.dtu.dk/ase/ase/filters.html#the-frechetcellfilter-class.
    scalar_pressure
        External pressure in GPa.
    """
    if structure.calc is None:
        raise ValueError('Structure has no attached calculator object')
    if constant_cell:
        ucf = structure
    else:
        ucf = FrechetCellFilter(
            structure, constant_volume=constant_volume, scalar_pressure=scalar_pressure * GPa)
    kwargs['logfile'] = kwargs.get('logfile', None)
    if minimizer == 'bfgs':
        dyn = BFGS(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    elif minimizer == 'lbfgs':
        dyn = LBFGS(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    elif minimizer == 'bfgs-scipy':
        dyn = SciPyFminBFGS(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    elif minimizer == 'fire':
        dyn = FIRE(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    elif minimizer == 'gpmin':
        dyn = GPMin(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    else:
        raise ValueError(f'Unknown minimizer: {minimizer}')
