"""Sparse Hamiltonians for spin-1/2 models on arbitrary interaction graphs.

Transverse-field Ising model:

    H = - sum_{(i,j)} J_ij Z_i Z_j  -  h sum_i X_i

The interaction graph (which pairs (i, j) are coupled, and how strongly) is the
"known geometry" against which Investigation 03 compares geometry reconstructed
from entanglement alone.

Basis convention matches theweb.quantum: site 0 is the most significant bit.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh


def tfim_hamiltonian(n: int, couplings: dict[tuple[int, int], float], h: float,
                     g: float = 0.0) -> sp.csr_matrix:
    """Transverse-field Ising model, optionally with a longitudinal field: - g sum_i Z_i.

    A small g breaks the up/down symmetry, so a finite system picks one branch
    instead of sitting in a cat-like superposition of both.
    """
    dim = 2**n
    states = np.arange(dim, dtype=np.int64)
    bits = ((states[:, None] >> (n - 1 - np.arange(n))[None, :]) & 1).astype(np.int8)
    z = 1 - 2 * bits  # +1 for |0>, -1 for |1>
    diag = -g * z.sum(axis=1).astype(float)
    for (i, j), jij in couplings.items():
        diag -= jij * z[:, i] * z[:, j]
    rows = [states]
    cols = [states]
    vals = [diag]
    for i in range(n):
        flipped = states ^ (1 << (n - 1 - i))
        rows.append(states)
        cols.append(flipped)
        vals.append(np.full(dim, -h))
    return sp.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(dim, dim)
    )


def ground_state(h_mat: sp.csr_matrix, rng: np.random.Generator | None = None) -> tuple[float, np.ndarray]:
    v0 = None
    if rng is not None:
        v0 = rng.normal(size=h_mat.shape[0])
    w, v = eigsh(h_mat, k=1, which="SA", v0=v0, tol=1e-12)
    psi = v[:, 0].astype(complex)
    return float(w[0]), psi / np.linalg.norm(psi)


def ring_couplings(n: int, j: float = 1.0) -> dict[tuple[int, int], float]:
    return {(i, (i + 1) % n): j for i in range(n)}


def torus_couplings(lx: int, ly: int, j: float = 1.0) -> dict[tuple[int, int], float]:
    def idx(x, y):
        return (x % lx) * ly + (y % ly)

    c = {}
    for x in range(lx):
        for y in range(ly):
            for a, b in ((idx(x, y), idx(x + 1, y)), (idx(x, y), idx(x, y + 1))):
                c[tuple(sorted((a, b)))] = j
    return c


def power_law_ring_couplings(n: int, alpha: float, j: float = 1.0) -> dict[tuple[int, int], float]:
    """All-to-all couplings on a ring decaying as 1/r**alpha (r = ring distance).

    Normalized so the nearest-neighbour coupling is j. alpha -> infinity recovers
    the nearest-neighbour ring; alpha -> 0 is uniform all-to-all (no geometry).
    """
    c = {}
    for i in range(n):
        for k in range(i + 1, n):
            r = min(k - i, n - (k - i))
            c[(i, k)] = j / r**alpha
    return c


def couplings_from_graph(edges, j: float = 1.0) -> dict[tuple[int, int], float]:
    return {tuple(sorted(e)): j for e in edges}
