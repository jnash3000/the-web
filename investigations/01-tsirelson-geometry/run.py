"""Investigation 01: is the Tsirelson bound "whatever is geometrically possible"?

Run:  python investigations/01-tsirelson-geometry/run.py
Writes results/summary.json and figures to results/.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))

from theweb import correlations as cor  # noqa: E402
from theweb import plotstyle as ps  # noqa: E402

ps.apply()
import matplotlib.pyplot as plt  # noqa: E402

OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(2026_10_28)
summary: dict = {}
t0 = time.time()

# ---------------------------------------------------------------------------
# E1. CHSH: arrows on a line vs arrows in a plane vs arrows in 3D and 4D
# ---------------------------------------------------------------------------
e1 = {"classical_enumeration": cor.classical_value(cor.CHSH)}
for d in (1, 2, 3, 4):
    e1[f"vector_dim_{d}"] = cor.vector_value(cor.CHSH, d, rng, restarts=40)[0]
qubit = cor.qubit_chsh([0, np.pi / 2], [np.pi / 4, -np.pi / 4])
e1["qubit_bell_state_value"] = float(np.sum(cor.CHSH * qubit))
_, u2, v2 = cor.vector_value(cor.CHSH, 2, rng, restarts=40)
e1["tsirelson_strategy_from_2d_vectors"], e1["entangled_pairs_used"] = cor.tsirelson_strategy_value(cor.CHSH, u2, v2)
e1["tsirelson_bound_exact"] = 2 * np.sqrt(2)
e1["pr_box_value"] = 4.0

# parallelogram law: |b0+b1|^2 + |b0-b1|^2 = 4 for unit vectors, so CHSH <= |b0+b1| + |b0-b1| <= 2*sqrt(2)
b = rng.normal(size=(100_000, 2, 5))
b /= np.linalg.norm(b, axis=2, keepdims=True)
plus = np.linalg.norm(b[:, 0] + b[:, 1], axis=1)
minus = np.linalg.norm(b[:, 0] - b[:, 1], axis=1)
e1["parallelogram_max_deviation"] = float(np.max(np.abs(plus**2 + minus**2 - 4)))
e1["max_of_plus_plus_minus_sampled"] = float(np.max(plus + minus))
summary["E1_chsh_by_geometry"] = e1

# ---------------------------------------------------------------------------
# E2. Where exactly does geometry run out? Noisy PR box E = v * (PR pattern)
# ---------------------------------------------------------------------------
vis = np.linspace(0, 1, 81)
lam = np.array([cor.best_gram_eigenvalue(v * cor.CHSH, grid=201)[0] for v in vis])
lo, hi = 0.5, 1.0
for _ in range(40):  # bisection for the visibility where vectors stop existing
    mid = 0.5 * (lo + hi)
    if cor.best_gram_eigenvalue(mid * cor.CHSH, grid=101)[0] >= -1e-10:
        lo = mid
    else:
        hi = mid
v_star = 0.5 * (lo + hi)
summary["E2_noisy_pr_box"] = {
    "pr_box_best_min_eigenvalue": float(cor.best_gram_eigenvalue(cor.CHSH)[0]),
    "critical_visibility": v_star,
    "critical_visibility_expected": 1 / np.sqrt(2),
    "critical_chsh_score": 4 * v_star,
    "tlm_criterion_agrees_below": bool(cor.tlm_holds((v_star - 1e-6) * cor.CHSH)),
    "tlm_criterion_agrees_above": not cor.tlm_holds((v_star + 1e-6) * cor.CHSH),
}

# ---------------------------------------------------------------------------
# E3. Chained Bell inequalities: n settings per side
# ---------------------------------------------------------------------------
chain_rows = []
for n in range(2, 11):
    m = cor.chained_bell(n)
    chain_rows.append(
        {
            "n": n,
            "classical": cor.classical_value(m),
            "vector": cor.vector_value(m, n, rng, restarts=20)[0],
            "vector_dim2": cor.vector_value(m, 2, rng, restarts=20)[0],
            "quantum_formula": 2 * n * np.cos(np.pi / (2 * n)),
            "algebraic_max": 2 * n,
        }
    )
summary["E3_chained_bell"] = {
    "rows": chain_rows,
    "max_abs_error_vs_formula": max(abs(r["vector"] - r["quantum_formula"]) for r in chain_rows),
    "max_abs_error_dim2_vs_formula": max(abs(r["vector_dim2"] - r["quantum_formula"]) for r in chain_rows),
}

# ---------------------------------------------------------------------------
# E4. Random games: how much geometric room (= entanglement) do correlations need?
# ---------------------------------------------------------------------------
n_games, size = 60, 6
dims = list(range(1, 9)) + [2 * size]
frac = np.zeros((n_games, len(dims)))
ratios, strat_checks = [], []
for g in range(n_games):
    m = rng.normal(size=(size, size))
    vals = []
    for d in dims:
        val, u, v = cor.vector_value(m, d, rng, restarts=16, iters=400)
        vals.append(val)
        if g < 5 and d in (3, 6):
            real, pairs = cor.tsirelson_strategy_value(m, u, v)
            strat_checks.append(abs(real - val))
    vals = np.maximum.accumulate(vals)  # more room can never hurt; guards against a missed optimum
    q = vals[-1]
    frac[g] = np.array(vals) / q
    ratios.append(q / cor.classical_value(m))
summary["E4_random_games"] = {
    "n_games": n_games,
    "size": size,
    "dims": dims,
    "entangled_pairs_for_dim": [d // 2 for d in dims],
    "mean_fraction_of_quantum_value": frac.mean(axis=0).tolist(),
    "min_fraction_of_quantum_value": frac.min(axis=0).tolist(),
    "quantum_over_classical_mean": float(np.mean(ratios)),
    "quantum_over_classical_max": float(np.max(ratios)),
    "grothendieck_upper_bound_real": 1.7822,
    "tsirelson_strategy_max_mismatch": float(max(strat_checks)),
}
summary["runtime_seconds"] = round(time.time() - t0, 1)


def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    return o


(OUT / "summary.json").write_text(json.dumps(clean(summary), indent=2))

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
# F1: Bell score by geometry
fig, ax = plt.subplots(figsize=(8.2, 3.8))
labels =["Line\n(pre-set answers)", "Plane\n(1 entangled pair)",
          "3D\n(1 entangled pair)", "4D\n(2 entangled pairs)", "PR box\n(no arrows fit)"]
vals = [e1["vector_dim_1"], e1["vector_dim_2"], e1["vector_dim_3"], e1["vector_dim_4"], 4.0]
colors = [ps.SERIES[0]] * 4 + [ps.NEUTRAL]
bars = ax.bar(range(5), vals, color=colors, width=0.6, edgecolor=ps.SURFACE, linewidth=2)
bars[-1].set_hatch("////")
bars[-1].set_edgecolor(ps.MUTED)
for i, v in enumerate(vals):
    ax.text(i, v + 0.06, f"{v:.3f}", ha="center", va="bottom", color=ps.INK, fontsize=9)
ax.set_xticks(range(5), labels, fontsize=8)
ax.set_ylabel("Best CHSH score")
ax.set_ylim(0, 4.5)
ax.grid(axis="x", visible=False)
ps.titled(ax, "The quantum limit is the geometry of arrows",
          "Best score when correlations are angles between unit arrows in each space")
fig.savefig(OUT / "fig1_chsh_by_geometry.png")
plt.close(fig)

# F2: where vectors stop existing
fig, ax = plt.subplots(figsize=(7.2, 3.8))
score = 4 * vis
ax.axhline(0, color=ps.AXIS, linewidth=1)
ax.fill_between(score, lam, 0, where=lam < 0, color=ps.SERIES[7], alpha=0.12, linewidth=0)
ax.plot(score, lam, color=ps.SERIES[0])
for x, txt in ((2.0, "pre-set answers\nmax = 2"), (2 * np.sqrt(2), "Tsirelson\n2√2 ≈ 2.83")):
    ax.axvline(x, color=ps.MUTED, linewidth=1, linestyle=(0, (3, 3)))
    ax.text(x - 0.05, 0.62, txt, ha="right", va="top", color=ps.INK_2, fontsize=8.5)
ax.annotate("No set of arrows\nin any dimension", xy=(3.55, -0.1), xytext=(3.55, 0.38),
            ha="center", va="bottom", color=ps.INK_2, fontsize=8.5,
            arrowprops={"arrowstyle": "-", "color": ps.MUTED, "linewidth": 0.8})
ax.set_xlabel("CHSH score of a noisy PR box (4 × visibility)")
ax.set_ylabel("Best possible smallest eigenvalue\nof the arrows' Gram matrix")
ax.set_xlim(0, 4)
ps.titled(ax, "Geometry runs out exactly at 2√2",
          "Arrows exist only while the Gram matrix can be made non-negative (curve ≥ 0)")
fig.savefig(OUT / "fig2_where_geometry_runs_out.png")
plt.close(fig)

# F3: chained Bell
fig, ax = plt.subplots(figsize=(7.2, 3.8))
ns = [r["n"] for r in chain_rows]
gap = [(r["vector"] - r["classical"]) / (r["algebraic_max"] - r["classical"]) for r in chain_rows]
ax.plot(ns, gap, color=ps.SERIES[0], marker="o")
for n_, g_ in zip(ns, gap):
    if n_ in (2, 10):
        ax.annotate(f"{g_:.2f}", (n_, g_), xytext=(0, 8), textcoords="offset points",
                    ha="center", color=ps.INK, fontsize=9)
ax.set_xlabel("Settings per side (n)")
ax.set_ylabel("Share of the gap closed\n(0 = pre-set answers, 1 = algebraic max)")
ax.set_ylim(0, 1)
ps.titled(ax, "With more settings, quantum closes more of the gap",
          "Chained Bell inequalities; arrows in a plane reproduce 2n·cos(π/2n) exactly")
fig.savefig(OUT / "fig3_chained_bell.png")
plt.close(fig)

# F4: geometric room vs fraction of quantum value
fig, ax = plt.subplots(figsize=(7.2, 3.8))
xs = list(range(len(dims)))
ax.plot(xs, frac.mean(axis=0), color=ps.SERIES[0], marker="o", label="mean over random games")
ax.plot(xs, frac.min(axis=0), color=ps.SERIES[1], marker="o", markersize=5, label="worst game")
ax.set_xticks(xs, [f"{d}\n({d // 2})" for d in dims])
ax.set_xlabel("Dimensions available to the arrows\n(entangled qubit pairs needed)")
ax.set_ylabel("Fraction of full quantum value")
ax.legend(loc="lower right")
ps.titled(ax, "More room for the arrows, stronger correlations, then saturation",
          f"{n_games} random {size}×{size} two-outcome Bell games")
fig.savefig(OUT / "fig4_room_vs_strength.png")
plt.close(fig)

print(json.dumps(clean({k: v for k, v in summary.items() if k != "E3_chained_bell"}), indent=2))
print("chained max error:", summary["E3_chained_bell"]["max_abs_error_vs_formula"])
