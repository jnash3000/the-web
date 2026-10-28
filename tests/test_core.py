"""Sanity checks for the shared tools. Run with:  python -m pytest -q"""

import numpy as np
import pytest

from theweb import correlations as cor
from theweb import embedding as emb
from theweb import quantum as q
from theweb import spin_models as sm
from theweb import tensor_network as tn

RNG = np.random.default_rng(1234)
BELL = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)


# ------------------------------------------------------------------ quantum
def test_bell_and_product_entropy():
    assert q.entanglement_entropy(BELL, [2, 2], [0]) == pytest.approx(1.0)
    prod = np.kron([1, 0], [0, 1]).astype(complex)
    assert q.entanglement_entropy(prod, [2, 2], [0]) == pytest.approx(0.0, abs=1e-12)


def test_schmidt_matches_density_matrix():
    psi = q.random_state(2**5, RNG)
    dims = [2] * 5
    for region in ([0], [1, 3], [0, 2, 4]):
        s1 = q.entanglement_entropy(psi, dims, region)
        s2 = q.von_neumann(q.reduced_density_matrix(psi, dims, region))
        assert s1 == pytest.approx(s2, abs=1e-9)


def test_bell_mutual_information():
    mi = q.mutual_information_matrix(BELL, [2, 2])
    assert mi[0, 1] == pytest.approx(2.0)


def test_page_formula_matches_sampling():
    da, db = 4, 8
    samples = [q.entanglement_entropy(q.random_state(da * db, RNG), [da, db], [0]) for _ in range(400)]
    assert np.mean(samples) == pytest.approx(q.page_entropy(da, db), abs=0.02)


# ------------------------------------------------------------- correlations
def test_chsh_values():
    assert cor.classical_value(cor.CHSH) == pytest.approx(2.0)
    assert cor.vector_value(cor.CHSH, 1, RNG, restarts=20)[0] == pytest.approx(2.0)
    assert cor.vector_value(cor.CHSH, 2, RNG, restarts=20)[0] == pytest.approx(2 * np.sqrt(2), abs=1e-9)


def test_chained_bell_known_values():
    for n in (2, 3, 4, 5):
        m = cor.chained_bell(n)
        assert cor.classical_value(m) == pytest.approx(2 * n - 2)
        assert cor.vector_value(m, n, RNG, restarts=30)[0] == pytest.approx(2 * n * np.cos(np.pi / (2 * n)), abs=1e-8)


def test_qubit_realization_reaches_tsirelson():
    e = cor.qubit_chsh([0, np.pi / 2], [np.pi / 4, -np.pi / 4])
    assert np.sum(cor.CHSH * e) == pytest.approx(2 * np.sqrt(2))


def test_pr_box_has_no_vector_realization():
    lam, _, _ = cor.best_gram_eigenvalue(cor.CHSH)  # PR box correlators are E = CHSH pattern
    assert lam < -0.1
    lam_q, _, _ = cor.best_gram_eigenvalue(cor.CHSH / np.sqrt(2))
    assert lam_q > -1e-6


def test_tlm_on_random_vectors():
    for _ in range(200):
        u = RNG.normal(size=(2, 4)); u /= np.linalg.norm(u, axis=1, keepdims=True)
        v = RNG.normal(size=(2, 4)); v /= np.linalg.norm(v, axis=1, keepdims=True)
        assert cor.tlm_holds(u @ v.T)
    assert not cor.tlm_holds(cor.CHSH)


# ----------------------------------------------------------- tensor networks
def test_contraction_matches_einsum():
    net = tn.Network(2, [(0, 1)], legs=[0, 0, 1], D=3).randomize(RNG)
    a, b = net.tensors  # a: (bond, leg0, leg1), b: (bond, leg2)
    manual = np.einsum("kij,kl->ijl", a, b).reshape(-1)
    assert np.allclose(net.state(), manual / np.linalg.norm(manual))


def test_entropy_never_exceeds_min_cut_capacity():
    for D in (2, 3):
        for _ in range(5):
            net = tn.random_graph_network(10, 3, 6, D, RNG).randomize(RNG)
            psi = net.state()
            for region in ([0], [0, 1], [0, 2, 4], [1, 2, 3]):
                bound = net.min_cut(region) * np.log2(D)
                assert net.entropy(psi, region) <= bound + 1e-9


def test_min_cut_examples():
    net = tn.two_clusters(4, 2, 2)
    assert net.min_cut([0, 1, 2, 3]) == 2
    assert net.min_cut([0]) == 1
    tree = tn.binary_tree(3, 2)
    assert tree.min_cut(list(range(4))) == 1  # half the leaves: cut one bond at the root


# -------------------------------------------------------------- spin models
def test_tfim_matches_dense_construction():
    n, h = 3, 0.7
    z = np.diag([1.0, -1.0]); x = np.array([[0.0, 1.0], [1.0, 0.0]]); i2 = np.eye(2)

    def op(o, k):
        mats = [o if s == k else i2 for s in range(n)]
        out = mats[0]
        for m in mats[1:]:
            out = np.kron(out, m)
        return out

    dense = -sum(op(z, i) @ op(z, (i + 1) % n) for i in range(n)) - h * sum(op(x, i) for i in range(n))
    sparse = sm.tfim_hamiltonian(n, sm.ring_couplings(n), h).toarray()
    assert np.allclose(dense, sparse)


# ---------------------------------------------------------------- embedding
def test_mds_recovers_circle():
    ang = np.linspace(0, 2 * np.pi, 12, endpoint=False)
    pts = np.c_[np.cos(ang), np.sin(ang)]
    d = np.linalg.norm(pts[:, None] - pts[None], axis=-1)
    w, coords = emb.mds(d, 2)
    d2 = np.linalg.norm(coords[:, None] - coords[None], axis=-1)
    assert np.allclose(d, d2, atol=1e-8)
    assert emb.effective_dimension(w) == 2
