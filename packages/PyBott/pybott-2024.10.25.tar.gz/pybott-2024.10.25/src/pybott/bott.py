"""Code to compute the Bott index following the definition given by
T. A. Loring and M. B. Hastings in
https://iopscience.iop.org/article/10.1209/0295-5075/92/67004/meta

The **Bott index** measures the commutativity of projected position operators, 
providing a topological invariant that helps distinguish topological insulators 
from trivial insulators.
"""

import numpy as np
import scipy

def is_pair_of_ordered_reals(variable):
    return isinstance(variable, (tuple, list)) and len(variable) == 2 and all(isinstance(i, (float, int)) for i in variable) and variable[0] < variable[1]

def compute_uv(lattice, eigenvectors, pos_omega, orb):
    """
    Compute Vx and Vy matrices.

    Parameters:
        lattice (ndarray): Array of shape (N_sites, 2) containing the coordinates
    of the lattice sites.
        eigenvectors (ndarray): Array of shape (orb * N_sites, orb * N_sites) containing
    the eigenvectors.
        pos_omega (int): position of the frequency in the ordered list of frequences.
        orb (int): number of orbitals.

    Returns:
        u_proj (ndarray): Array of shape (orb * N_sites, orb * N_sites) representing
                     the projected position operator on x.
        v_proj (ndarray): Array of shape (orb * N_sites, orb * N_sites) representing
                     the projected position operator on y.
    """

    n_sites = lattice.shape[0]
    x_lattice = lattice[:n_sites, 0]
    y_lattice = lattice[:n_sites, 1]
    lx, ly = np.max(x_lattice) - np.min(x_lattice), np.max(y_lattice) - np.min(
        y_lattice
    )
    u_proj = np.zeros((orb * n_sites, orb * n_sites), dtype=complex)
    v_proj = np.zeros((orb * n_sites, orb * n_sites), dtype=complex)

    x_lattice = np.repeat(x_lattice, orb)
    y_lattice = np.repeat(y_lattice, orb)

    w_stack = np.column_stack([eigenvectors[:, i] for i in range(pos_omega)])

    phase_x = np.diag(np.exp(2 * np.pi * 1j * x_lattice / lx))
    phase_y = np.diag(np.exp(2 * np.pi * 1j * y_lattice / ly))
    u_proj = np.conj(w_stack.T) @ phase_x @ w_stack
    v_proj = np.conj(w_stack.T) @ phase_y @ w_stack

    return u_proj, v_proj


def sorting_eigenvalues(eigv, evects, rev=False):
    """Sorting eigenvalues and eigenvectors accordingly"""
    if rev:
        eigv_ind = np.argsort(eigv)[::-1]
    else:
        eigv_ind = np.argsort(eigv)
    return eigv[eigv_ind], evects[:, eigv_ind]


def bott(lattice, ham, fermi_energy=0, gap=None, orb=1, dagger=False):
    """Compute the Bott index for a given Hamiltonian and lattice.

    This function calculates the Bott index, which is a topological
    invariant, to distinguish topological phases in a system described
    by the Hamiltonian. If the Hamiltonian is not hermitian, compute
    the eigenvectors and eigenvectors yourself and use 'bott_vect'
    instead. If the theoretical width of the gap is provided and the
    Hamiltonian is large, eigenvalues and eigenvectors will be
    computed in a restriction of the Hilbert space to save computation
    time.

    Parameters:

    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.

    ham (ndarray): Hamiltonian matrix of shape (orb * N_sites,orb *
    N_sites). Must be Hermitian.

    fermi_energy (float) (optional): Value of energy for which the
    Bott index is computed, must be in the bulk gap to match the Chern
    number. Not defined outside of the bulk gap but usually gives 0.

    gap (tuple of float) (optional): Energy gap used for filtering
        eigenvalues when calculating the Bott index.  Must be a tuple
        of two ordered real numbers. If None, the entire spectrum is
        computed.

    orb (int) (optional): Number of orbitals considered per lattice
    site. Default is 1.

    dagger (bool): two methods to compute Bott index exist, one with
        dagger of the projected position operator, the other by
        computing the inverse of the said operator.

    Returns:

    float: The computed Bott index.

    Raises:

    ValueError: If the Hamiltonian is not Hermitian, or if gap is not
        a valid tuple of floats.

    """

    if not np.allclose(ham, ham.conj().T):
        raise ValueError(
            "Hamiltonian must be Hermitian. Use 'bott_vect' for non-Hermitian matrices."
        )

    n_ham = ham.shape[0]

    # Compute eigenvalues and eigenvectors for the entire spectrum if
    # Hamiltonian size is small or no gap provided.
    if n_ham < 512 or gap is None:
        evals, evects = np.linalg.eigh(ham)
        return bott_vect(lattice, evects, evals, fermi_energy=fermi_energy, orb=orb, dagger=dagger)

    if not is_pair_of_ordered_reals(gap):
        raise ValueError("Gap must be a tuple of two ordered real numbers.")

    # For bigger Hamiltonian, if the gap is provided, we can compute a
    # subset of the spectrum.
    if gap[0] <= fermi_energy <= gap[1]:
        evals, evects = scipy.linalg.eigh(
            ham, subset_by_value=(gap[0], fermi_energy), driver="evr"
        )
    elif fermi_energy < gap[0]:
        evals, evects = scipy.linalg.eigh(
            ham, subset_by_value=(-np.inf, fermi_energy), driver="evr"
        )
    else:
        evals, evects = scipy.linalg.eigh(
            ham, subset_by_value=(gap[1], fermi_energy), driver="evr"
        )

    return bott_vect(lattice, evects, evals, fermi_energy, gap, orb, dagger)


def bott_vect(
    lattice,
    evects,
    energies,
    fermi_energy=0,
    orb=1,
    dagger=False,
):
    """Compute the Bott index for a given set of eigenvectors and energies.

    Parameters:

    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.

    evects (ndarray): Array of shape (orb * N_sites, orb * N_sites)
    containing the eigenvectors.

    energies (ndarray): Array of shape (orb * N_sites,) containing the
    energies. These energies may differ from the eigenvalues of the
    Hamiltonian for more complex systems beyond tight-binding models.

    fermi_energy (float): Value of energy for which the Bott index is
    computed, must be in the bulk gap to match the Chern number. Not
    defined outside of the bulk gap but usually gives 0.

    orb (int): indicates the number of orbitals to take into account.

    dagger (bool): two methods to compute Bott index exist, one with
        dagger of the projected position operator, the other by
        computing the inverse of the said operator.

    Returns:
        float: The Bott index value. An integer.

    """

    k = np.searchsorted(energies, fermi_energy)
    if k == 0:
        return 0

    u_proj, v_proj = compute_uv(lattice, evects, k, orb)

    return bott_matrix(u_proj, v_proj, dagger)


def bott_matrix(u_mat, v_mat, dagger=False):
    """Compute the Bott index of two invertible matrices"""
    if not dagger:
        try:
            u_inv = np.linalg.inv(u_mat)
            v_inv = np.linalg.inv(v_mat)
        except Exception as exc:
            raise np.linalg.LinAlgError("U or V not invertible, can't compute Bott index.") from exc
        ebott = np.linalg.eigvals(u_mat @ v_mat @ u_inv @ v_inv)

    else:
        ebott = np.linalg.eigvals(u_mat @ v_mat @ np.conj(u_mat.T) @ np.conj(v_mat.T))

    cbott = np.sum(np.log(ebott)) / (2 * np.pi)

    return np.imag(cbott)


def all_bott(
    lattice,
        ham,
    orb=1,
    dagger=False,
    stop=0,
):
    """Compute the Bott index for a given Hamiltonian and lattice for
    all energy levels or up to a specified limit.

    This function calculates the Bott index for each energy in the system, sequentially
    from the lowest to the highest energy state, unless a stopping point is specified
    via the `stop` parameter.

    Parameters:

    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.

    ham (ndarray): Hamiltonian matrix of shape (orb * N_sites,orb *
    N_sites). Must be Hermitian.

    orb (int): Number of orbitals considered per lattice site. Default is 1.

    dagger (bool): If `True`, computes the Bott index using the Hermitian conjugate
    (dagger) of the projected position operators. If `False`, computes using the inverse
    of the position operators. Default is `False`.

    stop (int): The number of eigenstates to process. If `stop` is not 0, the
    calculation will only be performed for the first `stop` eigenstates. Default is 0,
    which means the function will compute the Bott index for all energy levels.

    Returns:

    dict: A dictionary where the keys are the energy values and the values are the
    corresponding Bott index calculated for each energy level.

    Notes:

    The function iterates over all the eigenstates (or up to the specified limit) and computes
    the Bott index for each state. This allows one to track the evolution of the topological
    properties of the system across its entire energy spectrum. This can be particularly
    useful in systems with energy-dependent topological transitions.

    Raises:

    ValueError: If the Hamiltonian is not Hermitian.

    """

    if not np.allclose(ham, ham.conj().T):
        raise ValueError(
            "Hamiltonian must be Hermitian. Use 'bott_vect' for non-Hermitian matrices."
        )
    
    n_sites = np.size(lattice, 0)

    evals, evects = np.linalg.eigh(ham)

    u_proj, v_proj = compute_uv(lattice, evects, n_sites, orb)

    botts = {}

    if stop != 0:
        n_sites = stop

    for k in range(n_sites):
        uk, vk = u_proj[0:k, 0:k], v_proj[0:k, 0:k]
        if dagger:
            ebott, _ = np.linalg.eig(uk @ vk @ np.conj(uk.T) @ np.conj(vk.T))
        else:
            ebott, _ = np.linalg.eig(uk @ vk @ np.linalg.inv(uk) @ np.linalg.inv(vk))
        bott_value = np.imag(np.sum(np.log(ebott))) / (2 * np.pi)
        botts[evals[k]] = bott_value

    return botts


def all_bott_vect(
    lattice,
    evects,
    energies,
    orb=1,
    dagger=False,
    stop=0,
):
    """Compute the Bott index for all energy levels or up to a specified limit.

    This function calculates the Bott index for each energy in the system, sequentially
    from the lowest to the highest energy state, unless a stopping point is specified
    via the `stop` parameter.

    Parameters:

    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.

    evects (ndarray): Array of shape (orb * N_sites, orb * N_sites) containing
    the eigenvectors of the system.

    energies (ndarray): Array of shape (orb * N_sites,) containing the
    energy values corresponding to the eigenstates. These energies may
    differ from the eigenvalues of the Hamiltonian for more complex
    systems beyond tight-binding models.

    orb (int): Number of orbitals considered per lattice site. Default is 1.

    dagger (bool): If `True`, computes the Bott index using the Hermitian conjugate
    (dagger) of the projected position operators. If `False`, computes using the inverse
    of the position operators. Default is `False`.

    stop (int): The number of eigenstates to process. If `stop` is not 0, the
    calculation will only be performed for the first `stop` eigenstates. Default is 0,
    which means the function will compute the Bott index for all energy levels.

    Returns:

    dict: A dictionary where the keys are the energy values and the values are the
    corresponding Bott index calculated for each energy level.

    Notes:

    The function iterates over all the eigenstates (or up to the specified limit) and computes
    the Bott index for each state. This allows one to track the evolution of the topological
    properties of the system across its entire energy spectrum. This can be particularly
    useful in systems with energy-dependent topological transitions.
    """
    n_sites = np.size(lattice, 0)

    u_proj, v_proj = compute_uv(lattice, evects, n_sites, orb)

    botts = {}

    if stop != 0:
        n_sites = stop

    for k in range(n_sites):
        uk, vk = u_proj[0:k, 0:k], v_proj[0:k, 0:k]
        if dagger:
            ebott, _ = np.linalg.eig(uk @ vk @ np.conj(uk.T) @ np.conj(vk.T))
        else:
            ebott, _ = np.linalg.eig(uk @ vk @ np.linalg.inv(uk) @ np.linalg.inv(vk))
        bott_value = np.imag(np.sum(np.log(ebott))) / (2 * np.pi)
        botts[energies[k]] = bott_value

    return botts
