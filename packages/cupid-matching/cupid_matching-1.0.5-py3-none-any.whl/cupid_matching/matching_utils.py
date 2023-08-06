""" matching-related utilities """
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

import numpy as np

from cupid_matching.utils import (
    NestsList,
    TwoArrays,
    bs_error_abort,
    print_stars,
    test_matrix,
    test_vector,
)


def _get_singles(muxy: np.ndarray, n: np.ndarray, m: np.ndarray) -> TwoArrays:
    """Computes the numbers of singles from the matches and the margins."""
    mux0 = n - np.sum(muxy, 1)
    mu0y = m - np.sum(muxy, 0)
    return mux0, mu0y


def _compute_margins(
    muxy: np.ndarray, mux0: np.ndarray, mu0y: np.ndarray
) -> TwoArrays:
    """Computes the margins from the matches and the singles."""
    n = np.sum(muxy, 1) + mux0
    m = np.sum(muxy, 0) + mu0y
    return n, m


@dataclass
class Matching:
    """stores the numbers of couples and singles of every type;

    muxy is an (X,Y)-matrix
    n is an X-vector
    m is an Y-vector
    mux0 and mu0y are generated as the corresponding numbers of singles
    """

    mux0: np.ndarray = field(init=False)
    mu0y: np.ndarray = field(init=False)
    muxy: np.ndarray
    n: np.ndarray
    m: np.ndarray

    def __str__(self):
        X, Y = self.muxy.shape
        n_couples = np.sum(self.muxy)
        n_men, n_women = np.sum(self.n), np.sum(self.m)
        repr_str = (
            f"This is a matching with {n_men}  men, {n_women} single women.\n"
        )
        repr_str += f"   with {n_couples} couples,\n \n"
        repr_str += f" We have {X} types of men and {Y} of women."
        print_stars(repr_str)

    def __post_init__(self):
        X, Y = test_matrix(self.muxy)
        Xn = test_vector(self.n)
        Ym = test_vector(self.m)
        if Xn != X:
            bs_error_abort(
                f"muxy is a ({X}, {Y}) matrix but n has {Xn} elements."
            )
        if Ym != Y:
            bs_error_abort(
                f"muxy is a ({X}, {Y}) matrix but m has {Ym} elements."
            )
        self.mux0, self.mu0y = _get_singles(self.muxy, self.n, self.m)

    def unpack(self):
        muxy, mux0, mu0y = self.muxy, self.mux0, self.mu0y
        min_xy, min_x0, min_0y = np.min(muxy), np.min(mux0), np.min(mu0y)
        if min_xy < 0.0:
            breakpoint()
            bs_error_abort(f"The smallest muxy is {min_xy}")
        if min_x0 < 0.0:
            breakpoint()
            bs_error_abort(f"The smallest mux0 is {min_x0}")
        if min_0y < 0.0:
            breakpoint()
            bs_error_abort(f"The smallest mux0 is {min_0y}")
        return muxy, mux0, mu0y, self.n, self.m


MatchingFunction = Callable[[Matching], np.ndarray]

MatchingFunctionParam = Callable[[Matching, list[Any]], np.ndarray]
"""Same with a list of additional parameters
"""


def _get_margins(mus: Matching) -> TwoArrays:
    """computes the numbers of each type from the matching patterns"""
    _, _, _, n, m = mus.unpack()
    return n, m


def _simulate_sample_from_mus(
    mus: Matching, n_households: int, seed: Optional[int] = None
) -> Matching:
    """Draw a sample of n_households form the matching patterns in mus

    Args:
        mus: the matching patterns
        n_households: the number of households requested
        seed: an integer seed for the random number generator

    Returns:
        the sample matching patterns
    """
    rng = np.random.default_rng(seed)
    muxy, mux0, mu0y, _, _ = mus.unpack()
    X, Y = muxy.shape
    # stack all probabilities
    XY = X * Y
    num_choices = XY + X + Y
    pvec = np.zeros(num_choices)
    pvec[:XY] = muxy.reshape(XY)
    pvec[XY : (XY + X)] = mux0
    pvec[(XY + X) :] = mu0y
    pvec /= np.sum(pvec)
    matches = rng.multinomial(n_households, pvec)
    muxy_sim = matches[:XY].reshape((X, Y))
    mux0_sim = matches[XY : (XY + X)]
    mu0y_sim = matches[(XY + X) :]
    # make sure we have no zeros
    _MU_EPS = min(1, int(1e-3 * n_households))
    muxy_sim += _MU_EPS
    mux0_sim += _MU_EPS
    mu0y_sim += _MU_EPS
    n_sim, m_sim = _compute_margins(muxy_sim, mux0_sim, mu0y_sim)
    mus_sim = Matching(muxy=muxy_sim, n=n_sim, m=m_sim)
    return mus_sim


def _variance_muhat(muhat: Matching) -> TwoArrays:
    """
    Computes the unweighted variance-covariance matrix of the observed matching patterns

    Args:
        muhat: a Matching object

    Returns:
        * an (XY+X+Y, XY+X+Y) matrix of the variance-covariance
        of $(\\mu_{xy}, \\mu_{x0}, \\mu_{0y})$ (row-major order)
        * and one of (\\mu_{xy}, n_x, m_y)$ (row-major order)
    """
    muxy, mux0, mu0y, n, m = muhat.unpack()

    # normalize all proportions
    n_households = np.sum(n) + np.sum(m) - np.sum(muxy)
    muxy_norm = (muxy / n_households).ravel()
    mux0_norm = mux0 / n_households
    mu0y_norm = mu0y / n_households

    X, Y = muxy.shape
    XY = X * Y
    var_dim = XY + X + Y
    var_muhat = np.zeros((var_dim, var_dim))

    # we start by constructing the variance of (muxy, mux0, mu0y)

    # variance of muxy
    varxy_norm = np.diag(muxy_norm) - np.outer(muxy_norm, muxy_norm)
    var_muhat[:XY, :XY] = varxy_norm
    # covariance of muxy and mux0
    cov_xy_x0 = -np.outer(muxy_norm, mux0_norm)
    var_muhat[:XY, XY : (XY + X)] = cov_xy_x0
    var_muhat[XY : (XY + X), :XY] = cov_xy_x0.T
    # covariance of muxy and mu0y
    cov_xy_0y = -np.outer(muxy_norm, mu0y_norm)
    var_muhat[:XY, (XY + X) :] = cov_xy_0y
    var_muhat[(XY + X) :, :XY] = cov_xy_0y.T
    # variance of mux0
    varx0_norm = np.diag(mux0_norm) - np.outer(mux0_norm, mux0_norm)
    var_muhat[XY : (XY + X), XY : (XY + X)] = varx0_norm
    # covariance of mux0 and mu0y
    cov_x0_0y = -np.outer(mux0_norm, mu0y_norm)
    var_muhat[XY : (XY + X), (XY + X) :] = cov_x0_0y
    var_muhat[(XY + X) :, XY : (XY + X)] = cov_x0_0y.T
    # variance of mu0y
    var0y_norm = np.diag(mu0y_norm) - np.outer(mu0y_norm, mu0y_norm)
    var_muhat[(XY + X) :, (XY + X) :] = var0y_norm

    # change of variables from (muxy, mux0, mu0y)  to (muxy, n, m)
    jac = np.eye(var_dim)
    ix = 0
    for x in range(X):
        jac[XY + x, ix : (ix + Y)] = 1
        ix += Y
    iy = XY + X
    for y in range(Y):
        slice_y = slice(y, XY, Y)
        jac[iy, slice_y] = 1
        iy += 1
    var_munm = jac @ var_muhat @ jac.T

    return n_households * var_muhat, n_households * var_munm


def _variance_diagonal(var_muhat: np.ndarray, X: int, Y: int) -> Matching:
    """extracts the variances of muxy, mux0,mu0y

    Args:
        var_muhat: the variance of muhat as returned by _variance_muhat
        X: the number of types of men
        Y: the number of types of women

    Returns:
        a Matching with the three variances,
        and garbage for the irrelevant last two components
    """
    XY = X * Y
    var_muxy = np.diag(var_muhat[:XY, :XY]).reshape((X, Y))
    var_mux0 = np.diag(var_muhat[XY : (XY + X), XY : (XY + X)])
    var_mu0y = np.diag(var_muhat[(XY + X) :, (XY + X) :])
    # we need to initialize the Matching with the right pseudo-margins
    pseudo_nx = var_mux0 + np.sum(var_muxy, 1)
    pseudo_my = var_mu0y + np.sum(var_muxy, 0)
    var_diag = Matching(var_muxy, pseudo_nx, pseudo_my)
    return var_diag


def _make_XY_K_mat(xyk_array: np.ndarray) -> np.ndarray:
    """Reshapes an (X,Y,K) array to an (XY,K) matrix.

    Args:
        xyk_array: an (X, Y, K) array of bases

    Returns:
        the same,  (XY, K)-reshaped
    """
    X, Y, K = xyk_array.shape
    XY = X * Y
    xy_k_mat = np.zeros((XY, K))
    for k in range(K):
        xy_k_mat[:, k] = xyk_array[:, :, k].ravel()
    return xy_k_mat


def _reshape4_to2(array4: np.ndarray) -> np.ndarray:
    """Reshapes an array (X,Y,Z,T) to a matrix (XY,ZT).

    Args:
        array4: an (X, Y, Z, T) array

    Returns:
        the same,  (XY, ZT)-reshaped
    """
    if array4.ndim != 4:
        bs_error_abort(f"array4 should have 4 dimensions not {array4.ndim}")
    X, Y, Z, T = array4.shape
    XY, ZT = X * Y, Z * T
    array2 = np.zeros((XY, ZT))
    xy = 0
    for x in range(X):
        for y in range(Y):
            array2[xy, :] = array4[x, y, :, :].ravel()
            xy += 1
    return array2


def _change_indices(nests: NestsList):
    """subtracts 1 from the indices within the nest structure

    Args:
        nests: the nest structure

    Returns:
        a similar list
    """
    return [[nest_i - 1 for nest_i in nest] for nest in nests]


def _find_nest_of(nests: NestsList, y: int) -> int:
    """find the index of the nest that contains y, or return -1

    Args:
        nests: a nest structure
        y: the type we are looking for

    Returns:
        the nest of y, or -1 if not found
    """
    for i_n, nest in enumerate(nests):
        if y in nest:
            return i_n
    return -1  # if not found
