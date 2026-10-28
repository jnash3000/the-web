"""Bell correlations as geometry.

Two parties, Alice and Bob, each pick one of several measurement settings and get
an outcome of +1 or -1. The correlation E[x, y] is the average product of outcomes
when Alice uses setting x and Bob uses setting y. A Bell expression is a weighted
sum  sum_xy M[x, y] * E[x, y].

Three kinds of correlations:

* classical (pre-set instructions): every outcome is fixed in advance, so
  E[x, y] = a_x * b_y with a_x, b_y in {+1, -1}. Geometrically: "arrows" that can
  only point forward or backward on a line.
* quantum: Tsirelson's theorem says the quantum-achievable correlations are
  exactly E[x, y] = <u_x, v_y> for unit vectors u_x, v_y in some real vector space.
  Geometrically: arrows that can point in any direction.
* no-signalling "PR box" (Popescu-Rohrlich): reaches the algebraic maximum, but
  cannot be written as inner products of unit vectors in any space.
"""

from __future__ import annotations

import itertools

import numpy as np

CHSH = np.array([[1.0, 1.0], [1.0, -1.0]])  # E00 + E01 + E10 - E11


def chained_bell(n: int) -> np.ndarray:
    """Chained Bell expression with n settings per side (n=2 is CHSH).

    Classical max 2n-2, quantum max 2n cos(pi / 2n) (Braunstein & Caves 1990).
    """
    m = np.zeros((n, n))
    for k in range(n):
        m[k, k] = 1.0
        if k + 1 < n:
            m[k + 1, k] = 1.0
    m[0, n - 1] = -1.0
    return m


def classical_value(m: np.ndarray) -> float:
    """Maximum of a^T M b over a, b in {+1,-1}^n (exhaustive over Alice's choices)."""
    best = -np.inf
    for a in itertools.product([-1.0, 1.0], repeat=m.shape[0]):
        best = max(best, float(np.abs(np.asarray(a) @ m).sum()))
    return best


def vector_value(
    m: np.ndarray,
    dim: int,
    rng: np.random.Generator,
    restarts: int = 50,
    iters: int = 500,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Maximize sum_xy M[x,y] <u_x, v_y> over unit vectors in R^dim.

    Uses see-saw (alternating) optimization: with Alice's vectors fixed, each of
    Bob's optimal vectors is the normalized weighted sum of Alice's, and vice
    versa. Each step can only increase the value. Random restarts guard against
    local maxima. dim=1 reproduces the classical value; for dim >= number of
    settings it gives the quantum (Tsirelson) value.
    """
    best, best_u, best_v = -np.inf, None, None
    for _ in range(restarts):
        u = rng.normal(size=(m.shape[0], dim))
        u /= np.linalg.norm(u, axis=1, keepdims=True)
        prev = -np.inf
        for _ in range(iters):
            v = m.T @ u
            v /= np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-300)
            u = m @ v
            u /= np.maximum(np.linalg.norm(u, axis=1, keepdims=True), 1e-300)
            val = float(np.sum(m * (u @ v.T)))
            if val - prev < 1e-13:
                break
            prev = val
        if val > best:
            best, best_u, best_v = val, u.copy(), v.copy()
    return best, best_u, best_v


def gram_matrix(c: np.ndarray, s: float, t: float) -> np.ndarray:
    """Gram matrix of (u0, u1, v0, v1) for a 2x2 correlation matrix c.

    s = <u0, u1> and t = <v0, v1> are the free (unobserved) inner products.
    Unit vectors realizing c exist iff some (s, t) makes this matrix positive
    semidefinite.
    """
    g = np.eye(4)
    g[0, 1] = g[1, 0] = s
    g[2, 3] = g[3, 2] = t
    g[:2, 2:] = c
    g[2:, :2] = c.T
    return g


def best_gram_eigenvalue(c: np.ndarray, grid: int = 401) -> tuple[float, float, float]:
    """Largest achievable minimum eigenvalue over all completions (s, t).

    Negative means no set of unit vectors, in any number of dimensions, can
    produce the correlations c. Grid search, then local refinement.
    """
    from scipy.optimize import minimize

    ss = np.linspace(-1, 1, grid)
    best = (-np.inf, 0.0, 0.0)
    for s in ss:
        for t in ss[:: max(1, grid // 101)]:
            lam = np.linalg.eigvalsh(gram_matrix(c, s, t))[0]
            if lam > best[0]:
                best = (lam, s, t)

    def neg(x):
        s, t = np.clip(x, -1, 1)
        return -np.linalg.eigvalsh(gram_matrix(c, s, t))[0]

    res = minimize(neg, x0=[best[1], best[2]], method="Nelder-Mead",
                   options={"xatol": 1e-10, "fatol": 1e-12})
    if -res.fun > best[0]:
        s, t = np.clip(res.x, -1, 1)
        best = (-res.fun, float(s), float(t))
    return best


def tlm_holds(e: np.ndarray, tol: float = 1e-9) -> bool:
    """Tsirelson-Landau-Masanes test for a 2x2 correlator matrix.

    A 2x2 correlator is quantum iff for every choice of which term carries the
    minus sign, |arcsin E00 + arcsin E01 + arcsin E10 + arcsin E11 - 2 arcsin E_k| <= pi.
    """
    a = np.arcsin(np.clip(e.ravel(), -1, 1))
    tot = a.sum()
    return all(abs(tot - 2 * a[k]) <= np.pi + tol for k in range(4))


def clifford_generators(n: int) -> list[np.ndarray]:
    """n mutually anticommuting Hermitian matrices squaring to identity.

    Built on floor(n/2) qubits (Jordan-Wigner), so they have dimension 2**(n//2).
    """
    k = n // 2
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    z = np.array([[1, 0], [0, -1]], dtype=complex)
    i2 = np.eye(2, dtype=complex)

    def string(ops):
        out = np.eye(1, dtype=complex)
        for o in ops:
            out = np.kron(out, o)
        return out

    gens = []
    for j in range(k):
        for p in (x, y):
            gens.append(string([z] * j + [p] + [i2] * (k - j - 1)))
    if n % 2 == 1:
        gens.append(string([z] * k))
    return gens


def tsirelson_strategy_value(m: np.ndarray, u: np.ndarray, v: np.ndarray) -> tuple[float, int]:
    """Turn unit vectors into an explicit quantum strategy and evaluate it.

    Tsirelson's construction: A_x = sum_k u_xk G_k and B_y = sum_k v_yk G_k^T on a
    maximally entangled state of floor(d/2) qubit pairs gives E[x,y] = <u_x, v_y>.
    Returns (Bell value computed from the actual matrices, number of entangled pairs used).
    """
    d = u.shape[1]
    gens = clifford_generators(d)
    dim = gens[0].shape[0]
    phi = np.eye(dim, dtype=complex).reshape(-1) / np.sqrt(dim)
    total = 0.0
    for xi in range(u.shape[0]):
        a = sum(u[xi, k] * gens[k] for k in range(d))
        assert np.allclose(a @ a, np.eye(dim)), "A_x must be a +/-1 observable"
        for yi in range(v.shape[0]):
            b = sum(v[yi, k] * gens[k].T for k in range(d))
            e = (phi.conj() @ np.kron(a, b) @ phi).real
            total += m[xi, yi] * e
    return float(total), d // 2


def qubit_chsh(angles_a, angles_b) -> np.ndarray:
    """Correlations from the Bell state (|00>+|11>)/sqrt2 with observables in the X-Z plane.

    Observable at angle theta: cos(theta) Z + sin(theta) X. Returns E[x, y] computed
    from the actual 4x4 matrices (not the closed-form cos(a - b)).
    """
    z = np.array([[1, 0], [0, -1]], dtype=float)
    x = np.array([[0, 1], [1, 0]], dtype=float)
    phi = np.array([1, 0, 0, 1], dtype=float) / np.sqrt(2)
    e = np.zeros((len(angles_a), len(angles_b)))
    for i, a in enumerate(angles_a):
        for j, b in enumerate(angles_b):
            op_a = np.cos(a) * z + np.sin(a) * x
            op_b = np.cos(b) * z + np.sin(b) * x
            e[i, j] = phi @ np.kron(op_a, op_b) @ phi
    return e
