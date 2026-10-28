"""Basic quantum-information tools for pure states of composite systems.

A pure state of n sites is stored as a flat complex vector `psi` together with
a list `dims` of local dimensions (e.g. [2]*n for qubits). Site 0 is the most
significant index, matching numpy's C-order reshape.
"""

from __future__ import annotations

import numpy as np

LOG_BASE = 2.0  # entropies are reported in bits throughout the repo


def _log(x: np.ndarray) -> np.ndarray:
    return np.log(x) / np.log(LOG_BASE)


def normalize(psi: np.ndarray) -> np.ndarray:
    return psi / np.linalg.norm(psi)


def schmidt_values(psi: np.ndarray, dims: list[int], region: list[int]) -> np.ndarray:
    """Squared Schmidt coefficients of psi across the cut region | rest."""
    n = len(dims)
    region = sorted(set(region))
    rest = [k for k in range(n) if k not in region]
    t = psi.reshape(dims)
    t = np.transpose(t, region + rest)
    da = int(np.prod([dims[k] for k in region])) if region else 1
    m = t.reshape(da, -1)
    s = np.linalg.svd(m, compute_uv=False)
    p = s**2
    return p / p.sum()


def entropy_from_probs(p: np.ndarray, alpha: float = 1.0) -> float:
    """Rényi-alpha entropy (alpha=1 gives von Neumann/Shannon), in bits."""
    p = p[p > 1e-15]
    if alpha == 1.0:
        return float(-(p * _log(p)).sum())
    return float(_log(np.array([(p**alpha).sum()]))[0] / (1.0 - alpha))


def entanglement_entropy(psi, dims, region, alpha: float = 1.0) -> float:
    """Entanglement entropy (bits) of `region` in the pure state psi."""
    if len(region) == 0 or len(region) == len(dims):
        return 0.0
    return entropy_from_probs(schmidt_values(psi, dims, region), alpha)


def reduced_density_matrix(psi, dims, keep: list[int]) -> np.ndarray:
    """Reduced density matrix on sites `keep` (in the given order)."""
    n = len(dims)
    rest = [k for k in range(n) if k not in keep]
    t = np.transpose(psi.reshape(dims), list(keep) + rest)
    dk = int(np.prod([dims[k] for k in keep]))
    m = t.reshape(dk, -1)
    return m @ m.conj().T


def von_neumann(rho: np.ndarray) -> float:
    w = np.linalg.eigvalsh(rho)
    return entropy_from_probs(np.clip(w.real, 0, None))


def mutual_information_matrix(psi, dims) -> np.ndarray:
    """I(i:j) = S(i) + S(j) - S(ij) for all pairs of sites, in bits."""
    n = len(dims)
    s1 = np.array([von_neumann(reduced_density_matrix(psi, dims, [i])) for i in range(n)])
    mi = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            sij = von_neumann(reduced_density_matrix(psi, dims, [i, j]))
            mi[i, j] = mi[j, i] = max(s1[i] + s1[j] - sij, 0.0)
    return mi


def random_state(dim: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-random pure state of the given dimension."""
    v = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    return normalize(v)


def haar_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-random d x d unitary (QR of a complex Gaussian matrix with phase fix)."""
    z = (rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))) / np.sqrt(2)
    qm, r = np.linalg.qr(z)
    ph = np.diag(r) / np.abs(np.diag(r))
    return qm * ph


def apply_two_site(psi: np.ndarray, dims: list[int], i: int, j: int, u: np.ndarray) -> np.ndarray:
    """Apply a (dims[i]*dims[j]) x (dims[i]*dims[j]) unitary to sites i and j."""
    t = np.moveaxis(psi.reshape(dims), [i, j], [0, 1])
    sh = t.shape
    t = (u @ t.reshape(dims[i] * dims[j], -1)).reshape(sh)
    return np.moveaxis(t, [0, 1], [i, j]).reshape(-1)


def page_entropy(da: int, db: int) -> float:
    """Average entanglement entropy (bits) of a Haar-random state, da <= db (Page 1993)."""
    if da > db:
        da, db = db, da
    s = sum(1.0 / k for k in range(db + 1, da * db + 1)) - (da - 1) / (2 * db)
    return s / np.log(LOG_BASE)
