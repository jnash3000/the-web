"""Investigation 03: one web, two jobs.

Does the same structure set both distance (reconstructed from entanglement alone)
and how much entanglement regions can have? And does "distance" depend on how a
reader carves the system into nodes?

Run:  python investigations/03-one-web-two-jobs/run.py   (a few minutes)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import networkx as nx
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))

from theweb import embedding as emb  # noqa: E402
from theweb import plotstyle as ps  # noqa: E402
from theweb import quantum as q  # noqa: E402
from theweb import spin_models as sm  # noqa: E402

ps.apply()
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(7)
summary: dict = {}
t0 = time.time()
BLUES = LinearSegmentedColormap.from_list("blues", ["#cde2fb", "#6da7ec", "#2a78d6", "#184f95", "#0d366b"])


def ring_distance(n):
    i = np.arange(n)
    d = np.abs(i[:, None] - i[None])
    return np.minimum(d, n - d).astype(float)


def grid_positions(lx, ly):
    return np.array([(x, y) for x in range(lx) for y in range(ly)], float)


def analyse(mi, true_d=None):
    d = emb.direct_distance(mi)
    w, coords = emb.mds(d, 2)
    out = {
        "effective_dimension": emb.effective_dimension(w),
        "mi_concentration": emb.concentration(mi),
        "total_mi_bits": float(mi[np.triu_indices(mi.shape[0], 1)].sum()),
    }
    out["largest_distance"] = float(d.max())
    if true_d is not None:
        out["rank_agreement_with_true_distance"] = emb.rank_agreement(d, true_d)
    return out, d, coords


# ---------------------------------------------------------------------------
# E1/E2. Geometry from entanglement alone, and states with no geometry
# ---------------------------------------------------------------------------
N = 14
cases = {}
states = {}
for label, h in (("ring_paramagnet_h2", 2.0), ("ring_critical_h1", 1.0), ("ring_cat_h0.5", 0.5)):
    _, psi = sm.ground_state(sm.tfim_hamiltonian(N, sm.ring_couplings(N), h), rng)
    mi = q.mutual_information_matrix(psi, [2] * N)
    cases[label], _, coords = analyse(mi, ring_distance(N))
    states[label] = (psi, mi, coords)

pos = grid_positions(4, 4)
grid = nx.grid_2d_graph(4, 4)
gidx = {v: i for i, v in enumerate(sorted(grid.nodes()))}
grid_edges = [(gidx[a], gidx[b]) for a, b in grid.edges()]
euclid = np.linalg.norm(pos[:, None] - pos[None], axis=-1)
_, psi_grid = sm.ground_state(sm.tfim_hamiltonian(16, sm.couplings_from_graph(grid_edges), 3.0), rng)
mi_grid = q.mutual_information_matrix(psi_grid, [2] * 16)
cases["grid4x4_open_h3"], _, coords_grid = analyse(mi_grid, euclid)

dxy = np.abs(pos[:, None] - pos[None])
dxy = np.minimum(dxy, 4 - dxy)
_, psi_t = sm.ground_state(sm.tfim_hamiltonian(16, sm.torus_couplings(4, 4), 3.0), rng)
mi_t = q.mutual_information_matrix(psi_t, [2] * 16)
cases["torus4x4_h3"], _, _ = analyse(mi_t, np.sqrt((dxy**2).sum(-1)))

ghz = np.zeros(2**N, complex)
ghz[0] = ghz[-1] = 1 / np.sqrt(2)
mi_ghz = q.mutual_information_matrix(ghz, [2] * N)
cases["ghz_14"] = {
    "pairwise_mi_bits_min": float(mi_ghz[np.triu_indices(N, 1)].min()),
    "pairwise_mi_bits_max": float(mi_ghz[np.triu_indices(N, 1)].max()),
    "mi_concentration": emb.concentration(mi_ghz),
    "note": "every pair has exactly 1 bit; all reconstructed distances are zero",
}
rand = q.random_state(2**N, rng)
mi_rand = q.mutual_information_matrix(rand, [2] * N)
cases["haar_random_14"], _, _ = analyse(mi_rand, ring_distance(N))
summary["E1_E2_geometry_from_entanglement"] = cases

# ---------------------------------------------------------------------------
# E3. Scrambled labels: can the hidden ring be found blind?
# ---------------------------------------------------------------------------
perm = rng.permutation(N)  # site k of the scrambled system is ring position perm[k]
coup = {(min(int(np.where(perm == i)[0][0]), int(np.where(perm == (i + 1) % N)[0][0])),
         max(int(np.where(perm == i)[0][0]), int(np.where(perm == (i + 1) % N)[0][0]))): 1.0
        for i in range(N)}
_, psi_s = sm.ground_state(sm.tfim_hamiltonian(N, coup, 1.0), rng)
mi_s = q.mutual_information_matrix(psi_s, [2] * N)
_, coords_s = emb.mds(emb.direct_distance(mi_s), 2)
c = coords_s - coords_s.mean(0)
order = np.argsort(np.arctan2(c[:, 1], c[:, 0]))  # scrambled labels in recovered cyclic order
true_pos = perm[order]
adj_ok = sum(1 for a, b in zip(true_pos, np.roll(true_pos, -1)) if min((a - b) % N, (b - a) % N) == 1)
summary["E3_scrambled_labels"] = {
    "recovered_neighbour_pairs_correct": int(adj_ok),
    "out_of": N,
    "rank_agreement_with_hidden_ring": emb.rank_agreement(
        emb.direct_distance(mi_s), ring_distance(N)[np.ix_(perm, perm)]),
}

# ---------------------------------------------------------------------------
# E4. Re-carving the same state into different "nodes"
# ---------------------------------------------------------------------------
psi0, _, _ = states["ring_paramagnet_h2"]
true_ring = ring_distance(N)
depths = [0, 1, 2, 3, 4, 6, 8, 12]
n_circ = 5
recarve = {"nonlocal": {d: [] for d in depths}, "local": {d: [] for d in depths}}
for kind in recarve:
    for _ in range(n_circ):
        psi = psi0.copy()
        done = 0
        for target in depths:
            while done < target:
                if kind == "nonlocal":
                    p = rng.permutation(N)
                    pairs = [(int(p[2 * k]), int(p[2 * k + 1])) for k in range(N // 2)]
                else:
                    start = done % 2
                    pairs = [(i, (i + 1) % N) for i in range(start, N, 2)]
                for i, j in pairs:
                    psi = q.apply_two_site(psi, [2] * N, i, j, q.haar_unitary(4, rng))
                done += 1
            mi = q.mutual_information_matrix(psi, [2] * N)
            a, _, _ = analyse(mi, true_ring)
            recarve[kind][target].append(a)


def agg(rows, key):
    return float(np.mean([r[key] for r in rows]))


summary["E4_recarving"] = {
    kind: [{"depth": d,
            "rank_agreement": agg(rows, "rank_agreement_with_true_distance"),
            "mi_concentration": agg(rows, "mi_concentration"),
            "effective_dimension": agg(rows, "effective_dimension"),
            "total_mi_bits": agg(rows, "total_mi_bits")} for d, rows in recarve[kind].items()]
    for kind in recarve
}

# ---------------------------------------------------------------------------
# E5. How far-reaching the couplings are decides whether a geometry appears
# ---------------------------------------------------------------------------
N5 = 12
alphas = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, np.inf]
alpha_rows = []
for a in alphas:
    if np.isinf(a):
        cpl = sm.ring_couplings(N5)
    else:
        cpl = sm.power_law_ring_couplings(N5, a)
        tot = sum(v for (i, j), v in cpl.items() if i == 0 or j == 0)
        cpl = {k: 2.0 * v / tot for k, v in cpl.items()}  # same total coupling per site as the plain ring
    _, psi = sm.ground_state(sm.tfim_hamiltonian(N5, cpl, 2.5), rng)
    mi = q.mutual_information_matrix(psi, [2] * N5)
    iu = np.triu_indices(N5, 1)
    flat = np.ptp(mi[iu]) < 1e-6 * max(mi[iu].max(), 1e-30)
    a_res, _, _ = analyse(mi, ring_distance(N5))
    alpha_rows.append({"alpha": "inf" if np.isinf(a) else a,
                       "rank_agreement": float("nan") if flat else a_res["rank_agreement_with_true_distance"],
                       "mi_concentration": a_res["mi_concentration"],
                       "effective_dimension": a_res["effective_dimension"],
                       "all_pairs_identical": bool(flat)})
summary["E5_coupling_range"] = {"N": N5, "h": 2.5, "rows": alpha_rows}

# ---------------------------------------------------------------------------
# E6. The second job: does the same web set how much entanglement regions have?
# ---------------------------------------------------------------------------
def random_connected_region(g, size):
    start = int(rng.integers(len(g)))
    reg = {start}
    while len(reg) < size:
        frontier = sorted({nb for v in reg for nb in g[v]} - reg)
        reg.add(int(rng.choice(frontier)))
    return sorted(reg)


gg = nx.Graph()
gg.add_nodes_from(range(16))
gg.add_edges_from(grid_edges)
seen, regions = set(), []
while len(regions) < 400:
    r = tuple(random_connected_region(gg, int(rng.integers(1, 9))))
    if r not in seen:
        seen.add(r)
        regions.append(list(r))
psi_rand16 = q.random_state(2**16, rng)
rows6 = []
for r in regions:
    rs = set(r)
    cut = sum(1 for a, b in grid_edges if (a in rs) != (b in rs))
    rows6.append({"size": len(r), "boundary": cut,
                  "S_ground": q.entanglement_entropy(psi_grid, [2] * 16, r),
                  "S_random": q.entanglement_entropy(psi_rand16, [2] * 16, r)})


def fit(target):
    x = np.array([[row["boundary"], row["size"], 1.0] for row in rows6])
    y = np.array([row[target] for row in rows6])
    coef, *_ = np.linalg.lstsq(x, y, rcond=None)
    pred = x @ coef
    r2 = 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return {"bits_per_boundary_link": float(coef[0]), "bits_per_site": float(coef[1]),
            "intercept": float(coef[2]), "r2": float(r2),
            "corr_with_boundary": float(np.corrcoef(x[:, 0], y)[0, 1]),
            "corr_with_size": float(np.corrcoef(x[:, 1], y)[0, 1])}


summary["E6_area_law"] = {"regions": len(rows6), "ground_state_fit": fit("S_ground"),
                          "random_state_fit": fit("S_random")}
summary["runtime_seconds"] = round(time.time() - t0, 1)
(OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=float))

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def draw_embedding(ax, coords, edges, colors, title, sub):
    for i, j in edges:
        ax.plot(*coords[[i, j]].T, color=ps.GRID, linewidth=1.2, zorder=1)
    ax.scatter(coords[:, 0], coords[:, 1], c=colors, cmap=BLUES, s=46, zorder=2,
               edgecolors=ps.SURFACE, linewidths=1.5)
    ax.set_title(title, fontsize=10.5, pad=18, loc="left")
    ax.annotate(sub, xy=(0, 1), xycoords="axes fraction", xytext=(0, 5), textcoords="offset points",
                fontsize=8.5, color=ps.INK_2, va="bottom")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_aspect("equal", adjustable="datalim")


fig, axes = plt.subplots(1, 4, figsize=(11.5, 3.6))
ring_edges = [(i, (i + 1) % N) for i in range(N)]
draw_embedding(axes[0], states["ring_critical_h1"][2], ring_edges, np.arange(N), "Ring of 14",
               f"rank agreement {cases['ring_critical_h1']['rank_agreement_with_true_distance']:.2f}, "
               f"{cases['ring_critical_h1']['effective_dimension']}D")
draw_embedding(axes[1], coords_grid, grid_edges, pos[:, 0] * 4 + pos[:, 1], "4×4 grid",
               f"rank agreement {cases['grid4x4_open_h3']['rank_agreement_with_true_distance']:.2f}, "
               f"{cases['grid4x4_open_h3']['effective_dimension']}D")
inv = np.argsort(perm)
s_edges = [(int(inv[i]), int(inv[(i + 1) % N])) for i in range(N)]
draw_embedding(axes[2], coords_s, s_edges, perm, "Ring, labels scrambled",
               f"{adj_ok}/{N} neighbours recovered blind")
draw_embedding(axes[3], states["ring_cat_h0.5"][2], ring_edges, np.arange(N), "Cat-like state",
               f"needs {cases['ring_cat_h0.5']['effective_dimension']}D; widest gap "
               f"{cases['ring_cat_h0.5']['largest_distance']:.2f} vs "
               f"{cases['ring_critical_h1']['largest_distance']:.1f} for the ring")
fig.suptitle("Space drawn from entanglement alone", x=0.01, ha="left", fontweight="bold", fontsize=12)
fig.text(0.01, 0.885, "Each dot is a spin, placed using only mutual information; gray lines show the true "
         "couplings (not used); shading shows true position", ha="left", color=ps.INK_2, fontsize=9)
fig.tight_layout(rect=(0, 0, 1, 0.87))
fig.savefig(OUT / "fig1_space_from_entanglement.png")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(10, 3.9), sharex=True)
for i, (kind, lab) in enumerate((("local", "re-carved using neighbouring pairs"),
                                 ("nonlocal", "re-carved using far-apart pairs"))):
    rows = summary["E4_recarving"][kind]
    dd = [r["depth"] for r in rows]
    axes[0].plot(dd, [r["rank_agreement"] for r in rows], color=ps.SERIES[i], marker="o",
                 markersize=5, label=lab)
    axes[1].plot(dd, [r["effective_dimension"] for r in rows], color=ps.SERIES[i], marker="o",
                 markersize=5, label=lab)
axes[0].axhline(0, color=ps.AXIS, linewidth=1)
axes[0].set_ylim(-0.25, 1.05)
axes[0].set_ylabel("Rank correlation")
axes[0].set_title("Does it still look like the original ring?", fontsize=10.5, loc="left", pad=8)
rand_dim = cases["haar_random_14"]["effective_dimension"]
axes[1].axhline(rand_dim, color=ps.MUTED, linewidth=1, linestyle=(0, (3, 3)))
axes[1].text(0, rand_dim + 0.12, "random state (no geometry)", ha="left", va="bottom",
             color=ps.INK_2, fontsize=8.5)
axes[1].set_ylim(0, rand_dim + 0.8)
axes[1].set_ylabel("Dimensions the drawn\nspace needs")
axes[1].set_title("How space-like is what's left?", fontsize=10.5, loc="left", pad=8)
for ax in axes:
    ax.set_xlabel("Layers of random two-node mixing")
axes[0].legend(loc="upper right", fontsize=8.5)
fig.suptitle("Same state, different nodes: which geometry you see depends on the carving",
             x=0.01, ha="left", fontweight="bold", fontsize=12)
fig.text(0.01, 0.905, f"Ground state of a 14-spin ring, re-split into new nodes; average of {n_circ} random "
         "re-carvings per point", ha="left", color=ps.INK_2, fontsize=9)
fig.tight_layout(rect=(0, 0, 1, 0.9))
fig.savefig(OUT / "fig2_recarving.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(7.4, 3.9))
xs = list(range(len(alpha_rows)))
ax.plot(xs, [r["mi_concentration"] for r in alpha_rows], color=ps.SERIES[0], marker="o")
if alpha_rows[0]["all_pairs_identical"]:
    ax.annotate("α = 0: every pair is coupled equally,\nso every distance is the same (no geometry)",
                (0, alpha_rows[0]["mi_concentration"]), xytext=(3.4, 0.3), fontsize=8.5,
                color=ps.INK_2, arrowprops={"arrowstyle": "-", "color": ps.MUTED, "linewidth": 0.8})
ax.set_xticks(xs, ["0" if r["alpha"] == 0 else ("∞\n(neighbours\nonly)" if r["alpha"] == "inf" else f"{r['alpha']:g}")
                   for r in alpha_rows])
ax.set_xlabel("How quickly couplings fade with distance (α in 1/rᵅ)")
ax.set_ylabel("Share of entanglement in the\n12 strongest links")
ax.set_ylim(0, 1.05)
ps.titled(ax, "Any fading coupling draws the ring; local links draw it sharply",
          "12-spin ring, couplings ∝ 1/rᵅ, same total per spin; for every α > 0 the drawn space is a 2D ring")
fig.savefig(OUT / "fig3_coupling_range.png")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8))
jit = rng.uniform(-0.18, 0.18, len(rows6))
axes[0].scatter([r["boundary"] for r in rows6] + jit, [r["S_ground"] for r in rows6],
                s=14, color=ps.SERIES[0], alpha=0.55, linewidths=0)
axes[0].set_xlabel("Links cut by the region's boundary")
axes[0].set_ylabel("Entanglement of region (bits)")
axes[0].set_title("Ground state of the grid web", fontsize=10.5, loc="left", pad=8)
axes[1].scatter([r["size"] for r in rows6] + jit, [r["S_random"] for r in rows6],
                s=14, color=ps.SERIES[1], alpha=0.55, linewidths=0)
axes[1].set_xlabel("Spins in the region")
axes[1].set_title("Random state (no web)", fontsize=10.5, loc="left", pad=8)
g_fit, r_fit = summary["E6_area_law"]["ground_state_fit"], summary["E6_area_law"]["random_state_fit"]
axes[0].text(0.02, 0.97, f"corr with boundary {g_fit['corr_with_boundary']:.2f}\ncorr with size {g_fit['corr_with_size']:.2f}",
             transform=axes[0].transAxes, va="top", fontsize=8.5, color=ps.INK_2)
axes[1].text(0.02, 0.97, f"corr with size {r_fit['corr_with_size']:.2f}\ncorr with boundary {r_fit['corr_with_boundary']:.2f}",
             transform=axes[1].transAxes, va="top", fontsize=8.5, color=ps.INK_2)
fig.suptitle("The second job: the web's links set how much entanglement a region has",
             x=0.01, ha="left", fontweight="bold", fontsize=12)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(OUT / "fig4_area_law.png")
plt.close(fig)

print(json.dumps({k: v for k, v in summary.items() if k not in ("E4_recarving",)}, indent=2, default=float))
for kind, rows in summary["E4_recarving"].items():
    print(kind, [(r["depth"], round(r["rank_agreement"], 3), round(r["mi_concentration"], 3),
                  round(r["effective_dimension"], 1), round(r["total_mi_bits"], 2)) for r in rows])
