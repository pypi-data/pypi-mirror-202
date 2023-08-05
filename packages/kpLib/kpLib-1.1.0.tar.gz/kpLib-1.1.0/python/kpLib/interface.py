from sys import maxsize as max_int
import numpy as np
#from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import spglib
from kpLib.lib import KPointLattice, KPointLatticeGenerator, INCLUDE_GAMMA

SYMPREC = 1e-5

def get_kpoints(
    lattice,
    fractional_coords,
    atomic_numbers,
    min_distance,
    min_total_kpoints=1,
    include_gamma="auto",
    symprec=SYMPREC,
    use_scale_factor=False,
):
    """
    Generate an optimized generalized Monkhorst-Pack K-point girds.

    This is a thin Python interface to the underlying C++ kpLib library. The heavy work is done
    by the underlying C++ library.

    Args:
        lattice (numpy.ndarray): A 3 x 3 array representing the lattice vectors. Each vector is stored
                                 in a row.
        fractional_coords (numpy.ndarray): An array of fractional atomic coordinates (as fractions
                                           of the a, b, c lattice vectors).
        atomic_numbers (numpy.ndarray): An array of atomic numbers, in the same order of the atoms'
                                        apperance in the frac_coords.
        include_gamma (str): Whether generate a gamma-centered K-point grid. Use `true` to generate
                             grids with the Gamma point. Use `false` to generate a grid without
                             the Gamma point. Use `auto` to let kpLib choose the one with the 
                             smaller number of symmetrically distinct K-points. If the 
                             Gamma-centered grid and the shifted grid
                             have the same number distinct k-point, choose the grid with the larger
                             effective minimum distance.
        symprec (float): Precision for the symmetry searching function of Spglib.
        use_scale_factor (bool): Enable the use of a scaling factor. It speeds up the generation
                                 when requiring a very dense grids (i.e. very large `min_distance`
                                 value, e.g. >100 Angstroms). When this option is enabled, kpLib
                                 will try to find the best grid for a smaller `min_distance` and
                                 then scales the grid up to satify the input requirement.
        min_distance(float): Minimum distance in real-space between any pair of lattice points in 
                             the correspondin real-space superlattice. Note this is not distance in
                             recriprocal space.
        min_total_kpoint(int): Minimum number of required total k-points.
    """
    
    # For a full list of keys in the spglib dataset, see:
    # https://spglib.readthedocs.io/en/latest/python-spglib.html#method-standardization-and-finding-primitive
    spglib_cell = (lattice, fractional_coords, atomic_numbers)
    spglib_dataset = spglib.get_symmetry_dataset(spglib_cell, symprec=symprec, angle_tolerance=-1)
    spacegroup = spglib_dataset['number']
    conventional_lattice = spglib.standardize_cell(spglib_cell, to_primitive=False, no_idealize=True,
            symprec=symprec, angle_tolerance=-1)[0]
    rotations = np.array(spglib_dataset["rotations"], dtype=np.int32)

    # For trigonal systems, we use the hP lattice setting. I.e. conventional lattice
    # is always a hexagonal lattice. The original input lattice vectors won't be
    # changed and the rotational operations are still in the basis of the input lattice vectors.
    is_conventional_hex = 143 <= spacegroup <= 194

    # The monoclinic system (2/m Laue class) should use the 2-fold axis
    # as the 3rd-vector in the conventional lattice. In international convention (used by
    # spglib), the centered lattice point in face-centered monoclinic lattice is on the a-b plane,
    # i.e. C-centered representation, while the rotational axes of the 2-fold rotation and
    # the normal of the mirror plane is along the b-vector. In our library, we always want the 
    # the direction with the highest symmetry to be along the c-vector. Therefore, the lattice
    # vectors are rotated in the order: a->b, b->c, c->a. By this rotation, the centered lattice
    # is in the new a-c plane and the new c-vector has the highest symmetry.
    if 3 <= spacegroup <= 15:
        # Note: the C-API of spglib store lattice vector as column vectors, while their python
        # interface represent them as row vectors. So rotation should be performed along the 
        # row axis.
        conventional_lattice = np.roll(conventional_lattice, 1, axis=0)
    
    # Ensure there is an inversion operator in the set
    inv_op = np.array([[-1.0, 0, 0], [0, -1.0, 0], [0, 0, -1.0]])
    if not any(np.allclose(rot, inv_op) for rot in rotations):
        inv_rotations = np.zeros((rotations.shape[0], 3, 3)).astype(int)
        for i, rot in zip(range(rotations.shape[0]), rotations):
            inv_rotations[i] = rotations[i].dot(inv_op)
        rotations = np.concatenate((rotations, inv_rotations)).astype(int)

    kpt_gen = KPointLatticeGenerator(
        spglib_cell[0],
        conventional_lattice,
        rotations.transpose(0, 2, 1),
        rotations.shape[0],
        is_conventional_hex,
    )

    include_gamma = include_gamma.lower()
    # For backward compatibility
    if include_gamma == "true" or include_gamma == "gamma" or include_gamma[0] == "g":
        kpt_gen.includeGamma(INCLUDE_GAMMA.TRUE)
    elif include_gamma == "false" or include_gamma == "shifted" or include_gamma[0] == "s":
        kpt_gen.includeGamma(INCLUDE_GAMMA.FALSE)
    else:
        kpt_gen.includeGamma(INCLUDE_GAMMA.AUTO)

    if use_scale_factor:
        kpt_gen.useScaleFactor(spacegroup)

    lattice = kpt_gen.getKPointLattice(min_distance, min_total_kpoints)

    if lattice.getNumDistinctKPoints() == max_int:
        raise Exception(
            "Error: There is a problem generating k-point grid based "
            "on your input. If you have activated scale factor, please "
            "check your request doesn't exceed the maximum allowed "
            "number of k-points."
        )

    periodic_distance = lattice.getMinPeriodicDistance()
    num_distinct_kpts = lattice.getNumDistinctKPoints()
    num_total_kpts = lattice.numTotalKPoints()
    coords = lattice.getKPointCoordinates()
    weights = lattice.getKPointWeights()
    distinct_coords, distinct_weights = zip(
        *[
            (coord, weight)
            for (coord, weight) in zip(coords, weights)
            if weight > 0
        ]
    )

    return {
        "min_periodic_distance": periodic_distance,
        "num_distinct_kpts": num_distinct_kpts,
        "num_total_kpts": num_total_kpts,
        "coords": coords,
        "weights": weights,
        "distinct_coords": distinct_coords,
        "distinct_weights": distinct_weights
    }
