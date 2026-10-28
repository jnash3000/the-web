"""Turning "how connected" into "how far": geometry from a mutual-information matrix.

Following the idea in Cao, Carroll & Michalakis (2017), strongly entangled pairs
should be close and weakly entangled pairs far. Two distance definitions:

* direct:   d_ij = -log(I_ij / I_max)
* geodesic: shortest path through the complete graph whose edge lengths are the
            direct distances. Relies on strong (local) links and ignores
            unreliable tiny values of I for far-apart pairs.

Classical multidimensional scaling (MDS) then asks how many spatial dimensions
are needed to place the points so their distances match.
"""

from __future__ import annotations

import numpy as np
from scipy.sparse.csgraph import shortest_path
from scipy.stats import spearmanr


def direct_distance(mi: np.ndarray, floor: float = 1e-12) -> np.ndarray:
    n = mi.shape[0]
    off = mi[~np.eye(n, dtype=bool)]
    imax = off.max()
    d = -np.log(np.clip(mi, floor, None) / imax)
    np.fill_diagonal(d, 0.0)
    return np.clip(d, 0.0, None)


def geodesic_distance(mi: np.ndarray, floor: float = 1e-12, offset: float = 1.0) -> np.ndarray:
    """Shortest paths with edge length offset - log(I/I_max).

    The offset keeps the strongest links at positive length; without it every
    path through maximal-MI neighbours would have length zero.
    """
    d = direct_distance(mi, floor) + offset
    np.fill_diagonal(d, 0.0)
    return shortest_path(d, method="D", directed=False)


def concentration(mi: np.ndarray, k: int | None = None) -> float:
    """Share of total pairwise mutual information carried by the k strongest pairs.

    Needs no ground truth. Geometric (local) states concentrate their mutual
    information in a few strong neighbour links; cat/GHZ-like states spread it
    evenly over all pairs. Default k = number of sites.
    """
    n = mi.shape[0]
    k = k or n
    vals = np.sort(mi[np.triu_indices(n, 1)])[::-1]
    return float(vals[:k].sum() / vals.sum()) if vals.sum() > 0 else float("nan")


def mds(d: np.ndarray, k: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Classical MDS. Returns (eigenvalues sorted descending, coordinates)."""
    n = d.shape[0]
    j = np.eye(n) - np.ones((n, n)) / n
    b = -0.5 * j @ (d**2) @ j
    w, v = np.linalg.eigh(b)
    order = np.argsort(w)[::-1]
    w, v = w[order], v[:, order]
    k = k or n
    coords = v[:, :k] * np.sqrt(np.clip(w[:k], 0, None))
    return w, coords


def effective_dimension(eigs: np.ndarray, frac: float = 0.9) -> int:
    """Fewest MDS dimensions capturing `frac` of the positive spectrum."""
    pos = np.clip(eigs, 0, None)
    if pos.sum() == 0:
        return 0
    c = np.cumsum(pos) / pos.sum()
    return int(np.searchsorted(c, frac) + 1)


def rank_agreement(d1: np.ndarray, d2: np.ndarray) -> float:
    """Spearman rank correlation between two distance matrices (upper triangles)."""
    iu = np.triu_indices(d1.shape[0], 1)
    rho, _ = spearmanr(d1[iu], d2[iu])
    return float(rho)
