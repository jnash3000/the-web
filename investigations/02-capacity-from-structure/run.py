"""Investigation 02: is entanglement capacity set by the web's own structure?

Random tensor networks are the simplest precise "webs": nodes joined by links of
dimension D, with a quantum state living on the network's boundary legs.

Run:  python investigations/02-capacity-from-structure/run.py
"""

from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))

from theweb import plotstyle as ps  # noqa: E402
from theweb import tensor_network as tn  # noqa: E402

ps.apply()
import matplotlib.pyplot as plt  # noqa: E402

OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
summary: dict = {}
t0 = time.time()

# ---------------------------------------------------------------------------
# E1. Pipe width: two clusters joined by k links
# ---------------------------------------------------------------------------
m, samples = 4, 20
pipe = {}
for D in (2, 3, 4):
    rows = []
    for k in range(1, 7):
        net = tn.two_clusters(m, k, D)
        region = list(range(m))
        mc = net.min_cut(region)
        s = []
        for _ in range(samples):
            psi = net.randomize(rng).state()
            s.append(net.entropy(psi, region) / np.log2(D))  # in units of "links"
        rows.append({"k": k, "min_cut": mc, "S_in_links_mean": float(np.mean(s)),
                     "S_in_links_std": float(np.std(s)), "max_ratio_to_bound": float(np.max(s) / mc)})
    pipe[f"D={D}"] = rows
summary["E1_pipe_width"] = pipe

# ---------------------------------------------------------------------------
# E2. How close do random webs get to their structural capacity?
# ---------------------------------------------------------------------------
n_vert, n_legs, n_nets = 10, 6, 20
regions = [list(r) for size in (1, 2, 3) for r in itertools.combinations(range(n_legs), size)]
sat = {}
violations = 0
checked = 0
for D in (2, 3, 4, 5, 6):
    ratios, ratios2 = [], []
    for _ in range(n_nets):
        net = tn.random_graph_network(n_vert, 3, n_legs, D, rng).randomize(rng)
        psi = net.state()
        for r in regions:
            mc = net.min_cut(r)
            cap = mc * np.log2(D)
            s1 = net.entropy(psi, r)
            s2 = net.entropy(psi, r, alpha=2.0)
            checked += 1
            if s1 > cap + 1e-9:
                violations += 1
            ratios.append(s1 / cap)
            ratios2.append(s2 / cap)
    sat[D] = {
        "mean_ratio_vonneumann": float(np.mean(ratios)),
        "p10_ratio": float(np.percentile(ratios, 10)),
        "p90_ratio": float(np.percentile(ratios, 90)),
        "mean_ratio_renyi2": float(np.mean(ratios2)),
    }
summary["E2_saturation_vs_link_size"] = {
    "graph": f"random 3-regular, {n_vert} nodes, {n_legs} boundary legs, {n_nets} networks per D",
    "regions_per_network": len(regions),
    "by_D": sat,
    "bound_checks": checked,
    "bound_violations": violations,
}

# ---------------------------------------------------------------------------
# E3. The web's shape sets how entanglement scales with region size
# ---------------------------------------------------------------------------
n_legs3, D3, reps = 16, 2, 8
shapes = {"chain": tn.chain(n_legs3, D3), "tree": tn.binary_tree(4, D3)}
scaling = {}
for name, net in shapes.items():
    by_len = {ell: {"S": [], "mc": []} for ell in range(1, n_legs3)}
    mcs = {(a, ell): net.min_cut(list(range(a, a + ell)))
           for ell in range(1, n_legs3) for a in range(0, n_legs3 - ell + 1)}
    for _ in range(reps):
        psi = net.randomize(rng).state()
        for (a, ell), mc in mcs.items():
            by_len[ell]["S"].append(net.entropy(psi, list(range(a, a + ell))))
            by_len[ell]["mc"].append(mc)
    scaling[name] = [{"length": ell, "S_mean_bits": float(np.mean(v["S"])),
                      "min_cut_mean": float(np.mean(v["mc"]))} for ell, v in by_len.items()]
summary["E3_scaling_by_shape"] = {"D": D3, "legs": n_legs3, "samples": reps, "rows": scaling}
corr = {}
for name, rows in scaling.items():
    s = np.array([r["S_mean_bits"] for r in rows]); c = np.array([r["min_cut_mean"] for r in rows])
    corr[name] = float(np.corrcoef(s, c)[0, 1])
summary["E3_scaling_by_shape"]["corr_S_vs_mincut"] = corr
summary["runtime_seconds"] = round(time.time() - t0, 1)
(OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=float))

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 3.9))
ks = [r["k"] for r in pipe["D=2"]]
ax.plot(ks, [r["min_cut"] for r in pipe["D=2"]], color=ps.NEUTRAL, linestyle=(0, (4, 3)),
        label="Structural capacity (min-cut)")
for i, D in enumerate((2, 3, 4)):
    rows = pipe[f"D={D}"]
    ax.errorbar(ks, [r["S_in_links_mean"] for r in rows], yerr=[r["S_in_links_std"] for r in rows],
                color=ps.SERIES[i], marker="o", markersize=5, capsize=0, elinewidth=1,
                label=f"Measured entanglement, link size D={D}")
ax.annotate("pipe is the bottleneck", (2, 2), xytext=(1.25, 3.3), color=ps.INK_2, fontsize=8.5,
            arrowprops={"arrowstyle": "-", "color": ps.MUTED, "linewidth": 0.8})
ax.annotate("cluster's own legs become the bottleneck", (5.5, 4), xytext=(3.55, 4.35), color=ps.INK_2,
            fontsize=8.5, arrowprops={"arrowstyle": "-", "color": ps.MUTED, "linewidth": 0.8})
ax.set_xlabel("Links joining the two clusters (pipe width k)")
ax.set_ylabel("Entanglement between clusters\n(in units of one link, S / log₂D)")
ax.set_ylim(0, 4.8)
ax.legend(loc="lower right", fontsize=8.5)
ps.titled(ax, "Entanglement follows the width of the pipe",
          "Two 4-node clusters joined by k links; 20 random webs per point")
fig.savefig(OUT / "fig1_pipe_width.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(7.2, 3.8))
Ds = sorted(sat)
ax.fill_between(Ds, [sat[d]["p10_ratio"] for d in Ds], [sat[d]["p90_ratio"] for d in Ds],
                color=ps.SERIES[0], alpha=0.15, linewidth=0, label="middle 80% of regions")
ax.plot(Ds, [sat[d]["mean_ratio_vonneumann"] for d in Ds], color=ps.SERIES[0], marker="o",
        label="mean (von Neumann entropy)")
ax.plot(Ds, [sat[d]["mean_ratio_renyi2"] for d in Ds], color=ps.SERIES[1], marker="o", markersize=5,
        label="mean (Rényi-2 entropy)")
ax.axhline(1, color=ps.MUTED, linewidth=1, linestyle=(0, (3, 3)))
ax.text(Ds[0], 1.01, "structural capacity", color=ps.INK_2, fontsize=8.5, va="bottom")
ax.set_xlabel("Link size D (dimension of each connection)")
ax.set_ylabel("Entanglement ÷ capacity")
ax.set_ylim(0.3, 1.08)
ax.set_xticks(Ds)
ax.legend(loc="lower right")
ps.titled(ax, "Random webs fill their structural capacity more as links grow",
          f"{n_nets} random 3-regular webs per point; no region ever exceeded its capacity ({checked:,} checks)")
fig.savefig(OUT / "fig2_saturation.png")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.7), sharey=True)
for ax, (name, title) in zip(axes, (("chain", "Chain web"), ("tree", "Tree web"))):
    rows = scaling[name]
    ls = [r["length"] for r in rows]
    ax.plot(ls, [r["min_cut_mean"] for r in rows], color=ps.NEUTRAL, linestyle=(0, (4, 3)),
            label="min-cut capacity (bits)")
    ax.plot(ls, [r["S_mean_bits"] for r in rows], color=ps.SERIES[0], marker="o", markersize=4,
            label="measured entanglement (bits)")
    ax.set_title(title, fontsize=11, pad=8)
    ax.set_xlabel("Length of boundary region")
axes[0].set_ylabel("Bits")
axes[0].legend(loc="upper left", fontsize=8.5)
fig.suptitle("The web's shape sets the ceiling; the nodes set how full it gets",
             x=0.06, ha="left", fontweight="bold", fontsize=12)
fig.text(0.06, 0.915, f"16 boundary legs, link size D={D3}, random nodes, {reps} samples; "
         "dashed = capacity set by the web's shape", ha="left", color=ps.INK_2, fontsize=9)
fig.tight_layout(rect=(0, 0, 1, 0.92))
fig.savefig(OUT / "fig3_shape_sets_scaling.png")
plt.close(fig)

print(json.dumps({k: v for k, v in summary.items() if k != "E3_scaling_by_shape"}, indent=2, default=float))
print("E3 corr:", corr)
