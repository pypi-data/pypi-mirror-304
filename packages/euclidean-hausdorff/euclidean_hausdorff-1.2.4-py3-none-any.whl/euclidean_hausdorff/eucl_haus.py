import numpy as np
from scipy import spatial as sp
from itertools import product, starmap
from operator import itemgetter
from collections import Counter
from sortedcontainers import SortedList

from .point_cloud import PointCloud
from .transformation import Transformation


def diam(coords):
    hull = sp.ConvexHull(coords)
    hull_coords = coords[hull.vertices]
    candidate_distances = sp.distance.cdist(hull_coords, hull_coords)

    return candidate_distances.max()


def make_grid(center, h, r, l=None):
    """
    Compile a grid with cell size h covering the intersection of
    the cube [-l/2, l/2]^k + {c} and ball B(0, r).

    :param center: cube center c, k-array
    :param h: side length of a grid cell, float
    :param r: ball radius, float
    :param l: side length of the cube, float
    :return: (?, k)-array of grid points, updated a (for divisibility)
    """
    # Assume the smallest cube containing the ball if not given.
    l = l or 2 * r

    # Reduce cell size without increasing the cell count.
    n_cells = int(np.ceil(l / h))
    h = l / n_cells

    # Calculate covering radius.
    k = len(center)
    covering_rad = np.sqrt(k) * h / 2

    # Calculate grid point positions separately in each dimension.
    offsets_from_center = np.linspace(-(l - h) / 2, (l - h) / 2, n_cells)
    positions = np.add.outer(center, offsets_from_center)

    # Compile grid point coordinates.
    k = len(positions)
    coords = np.reshape(np.meshgrid(*positions), (k, -1)).T

    # Retain only the grid points covering the ball.
    lengths = np.linalg.norm(coords, axis=1)
    is_covering = lengths <= r + covering_rad
    coords = coords[is_covering]
    lengths = lengths[is_covering]

    # Project grid points outside of the ball onto the ball.
    is_outside = lengths > r
    coords[is_outside] /= lengths[is_outside][:, None]

    return coords, h


def upper(A_coords, B_coords, n_dH_iter=5, n_err_ub_iter=None, target_acc=None,
           target_err=None, proper_rigid=False, p=2, verbose=0):
    """
    Approximate the Euclidean–Hausdorff distance using multiscale grid search. The search
    terminates when additive approximation error is ≤ target_acc*max_diam OR when the
    smallest dH found does not improve after max_n_no_improv iterations (depending on
    whether target_acc or max_n_no_improv is set, accordingly)

    :param A_coords: points of A, (?×k)-array
    :param B_coords: points of B, (?×k)-array
    :param n_dH_iter: number of dH-minimizing iterations, int
    :param n_err_ub_iter: number of error-minimizing iterations, int
    :param target_acc: target (upper bound of) accuracy as a percentage of larger diameter, float
    :param target_err: target (upper bound of) additive approximation error, float
    :param proper_rigid: whether to consider only proper rigid transformations, bool
    :param p: number of parts to split a grid cell into (e.g. 2 for dyadic), int
    :param verbose: detalization level in the output, int
    :return: approximate dEH, upper bound of additive approximation error
    """
    # Initialize point clouds.
    A, B = map(PointCloud, [A_coords, B_coords])
    normalized_coords = np.concatenate([A.coords, B.coords])
    _, k = normalized_coords.shape

    # Check parameter correctness.
    assert k in {2, 3}, 'only 2D and 3D spaces are supported'
    assert n_err_ub_iter is None or target_acc is None or target_err is None, \
        'only one of n_err_ub_iter, target_acc, and target_err can be specified'
    assert n_dH_iter > 0 or (n_err_ub_iter and n_err_ub_iter > 0) or target_acc or target_err, \
        ('at least one of n_dH_iter or n_err_ub_iter must be positive, or else '
         'either of target_acc or target_err must be specified')

    # Infer stopping condition for error-minimizing iterations from inputs.
    n_err_ub_iter = n_err_ub_iter or 0
    if target_acc is not None:
        max_diam = max(map(diam, [A.coords, B.coords]))
        target_err = target_acc * max_diam
    elif target_err is None:
        target_err = np.inf

    # Initialize parameters of the multiscale search grid.
    r = np.linalg.norm(normalized_coords, axis=1).max()
    dim_delta, dim_rho = k, k * (k - 1) // 2
    sigmas = [False] if proper_rigid else [False, True]
    eps_delta = np.sqrt(dim_delta)*2*r  # scale-0 cell radius s.t. #∆=1
    eps_rho = eps_delta / ((2*r) if dim_delta == 2 else r)  # adhering to the optimal balance
    a_delta, a_rho = 2*eps_delta / np.sqrt(dim_delta), 2*eps_rho / np.sqrt(dim_rho)    # scale-0 cell sizes

    def calc_dH(delta, rho):    # calculate (smallest) dH for a translation-rotation combo
        dH = np.inf
        for sigma in sigmas:
            T = Transformation(delta, rho, sigma)
            sigma_dH = max(A.transform(T).asymm_dH(B), B.transform(T.invert()).asymm_dH(A))
            dH = min(dH, sigma_dH)
        return dH

    dH_diff_ubs = dict()    # maximum dH discrepancy in a grid cell w.r.t. the cell center

    def calc_dH_diff_ub(i):   # calculate maximum Lipschitz-based dH discrepancy at scale i
        try:
            dH_diff_ub = dH_diff_ubs[i]
        except KeyError:
            diff_delta, diff_rho = np.array([eps_delta, eps_rho]) / p**i
            dH_diff_ub = diff_delta + np.sqrt(2 * (1 - np.cos(diff_rho))) * r
            dH_diff_ubs[i] = dH_diff_ub
        return dH_diff_ub

    def zoom_in(delta, rho, i):   # refine grid cell centered at (δ, ρ) at scale i
        a_delta_i, a_rho_i = np.array([a_delta, a_rho]) / p**i
        deltas, _ = make_grid(delta, a_delta_i / p, 2*r, l=a_delta_i)
        rhos, _ = make_grid(rho, a_rho_i / p, np.pi, l=a_rho_i)
        return deltas, rhos

    # Initialize queue with the multiscale search grid points.
    Qs = [SortedList()]

    def update_grid(deltas, rhos, i, min_found_dH): # process new grid points at scale i
        # Compute dH at each grid point.
        new_points = list(product(map(tuple, deltas), map(tuple, rhos)))
        new_dHs = np.array(list(starmap(calc_dH, new_points)))
        min_found_dH = min(min_found_dH, np.min(new_dHs))
        new_evaluated_points = zip(new_dHs, new_points)

        # Remove grid points whose cells are wholly no less than the currently best dH.
        new_feasible_evaluated_points = filter(
            lambda x: x[0] < min_found_dH + calc_dH_diff_ub(i), new_evaluated_points)

        # Add grid points to the queue.
        try:
            Q_i = Qs[i]
        except IndexError:
            Q_i = SortedList()
            Qs.append(Q_i)
        Q_i.update(new_feasible_evaluated_points)

        # Find best point at each scale.
        best_points = [(j, Q_j[0][0], Q_j[0][0] - calc_dH_diff_ub(j)) # (scale, dH, possible_dH)
                       for j, Q_j in enumerate(Qs) if Q_j]

        return min_found_dH, best_points

    # Create search grid points of level 0.
    init_deltas, _ = make_grid((0,)*dim_delta, a_delta, 2*r)
    init_rhos, _ = make_grid((0,)*dim_rho, a_rho, np.pi)
    min_found_dH, best_points = update_grid(init_deltas, init_rhos, 0, np.inf)

    if verbose > 0:
        print(f'{r=:.5f}, {n_dH_iter=}, {n_err_ub_iter=}, {target_err=:.5f}')

    # Perform error-minimizing iterations of multiscale search, followed by
    # dH-minimizing iterations.
    dH_iter = err_ub_iter = 0
    min_possible_dH = 0
    while (dH_iter < n_dH_iter or err_ub_iter < n_err_ub_iter or
           min_found_dH - min_possible_dH > target_err):
        # Choose the grid cell to refine as having...
        # ...smallest possible dH, if in an error-minimizing iteration.
        if err_ub_iter < n_err_ub_iter or min_found_dH - min_possible_dH > target_err:
            i, dH, possible_dH = min(best_points, key=itemgetter(2))
            err_ub_iter += 1
            iter_descr = 'error-minimizing'
        # ...smallest dH, if in an dH-minimizing iteration.
        else:
            i, dH, possible_dH = min(best_points, key=itemgetter(1))
            dH_iter += 1
            iter_descr = 'dH-minimizing'

        # Log the iteration if needed.
        if verbose > 2:
            Q_sizes = {j: len(Q_j) for j, Q_j in enumerate(Qs)}
            print(f'({dH_iter + err_ub_iter}: {iter_descr}) {min_found_dH=:.5f}, '
                  f'#Q: {Q_sizes}, zooming in on ({i}, {dH:.5f}, {possible_dH:.5f})')

        # Refine the chosen grid cell.
        _, (delta, rho) = Qs[i].pop(0)
        new_deltas, new_rhos = zoom_in(delta, rho, i)
        min_found_dH, best_points = update_grid(new_deltas, new_rhos, i+1, min_found_dH)

    # Find minimum possible dH to calculate error bound.
    *_, min_possible_dH = min(best_points, key=itemgetter(2))
    min_possible_dH = max(0, min_possible_dH)
    err_ub = max(min_found_dH - min_possible_dH, 0)

    return min_found_dH, err_ub
