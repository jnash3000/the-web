"""Investigation 04: if capacities come from a graph, which entanglement patterns are allowed?

If the entanglement of any region equals the narrowest cut through a web of
links (P1), entropies cannot take arbitrary values. Every graph obeys
"monogamy of mutual information" (MMI, Hayden-Headrick-Maloney 2011):

    I3(A:B:C) = I(A:B) + I(A:C) - I(A:BC) <= 0

(knowing about B and knowing about C can't both be "the same" information A
shares). General quantum states can violate it. A violation marks a state whose
entanglement cannot come from cuts through any web of links.

Run:  python investigations/04-finite-configurations/run.py
"""

from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import networkx as nx
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))

from theweb import plotstyle as ps  # noqa: E402
from theweb import quantum as q  # noqa: E402
from theweb import spin_models as sm  # noqa: E402
from theweb import tensor_network as tn  # noqa: E402

ps.apply()
import matplotlib.pyplot as plt  # noqa: E402

OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(404)
summary: dict = {}
t0 = time.time()
TOL = 1e-9


def i3_from_entropy(S, a, b, c):
    """Tripartite information from an entropy function S(list_of_sites)."""
    return (S(a) + S(b) + S(c) - S(a + b) - S(a + c) - S(b + c) + S(a + b + c))


# ---------------------------------------------------------------------------
# E1. Pure graphs: entropies defined as min-cuts never violate MMI
# ---------------------------------------------------------------------------
def graph_mincut_entropy(g, terminals):
    """S(X) = min weighted cut separating the terminal nodes of X from all other terminals."""
    def S(parts):
        parts = set(parts)
        if not parts or len(parts) == len(terminals):
            return 0.0
        h = g.copy()
        for k, t in enumerate(terminals):
            if k in parts:
                h.add_edge("SRC", t, capacity=float("inf"))
            else:
                h.add_edge(t, "SNK", capacity=float("inf"))
        return nx.maximum_flow_value(h, "SRC", "SNK")
    return S


graph_trials, graph_viol, graph_max = 1500, 0, -np.inf
for _ in range(graph_trials):
    n = int(rng.integers(5, 12))
    p = float(rng.uniform(0.25, 0.7))
    und = nx.gnp_random_graph(n, p, seed=int(rng.integers(1 << 30)))
    g = nx.DiGraph()
    for u, v in und.edges():
        w = float(rng.uniform(0.05, 1.0))
        g.add_edge(u, v, capacity=w)
        g.add_edge(v, u, capacity=w)
    g.add_nodes_from(range(n))
    terminals = [int(t) for t in rng.choice(n, size=4, replace=False)]  # A, B, C, and purifier D
    S = graph_mincut_entropy(g, terminals)
    val = i3_from_entropy(S, [0], [1], [2])
    graph_max = max(graph_max, val)
    graph_viol += val > TOL
summary["E1_graph_cuts"] = {"random_weighted_graphs": graph_trials, "mmi_violations": int(graph_viol),
                            "largest_I3": float(graph_max)}

# ---------------------------------------------------------------------------
# E2. Random webs (tensor networks): violations fade as links grow
# ---------------------------------------------------------------------------
n_legs = 6
triples = [(a, b, c) for a, b, c in itertools.combinations(range(n_legs), 3)]
tn_rows = []
for D in (2, 3, 4, 5):
    viol = tot = 0
    worst = -np.inf
    for _ in range(25):
        net = tn.random_graph_network(10, 3, n_legs, D, rng).randomize(rng)
        psi = net.state()
        dims = [D] * n_legs
        cache = {}

        def S(r):
            key = tuple(sorted(r))
            if key not in cache:
                cache[key] = q.entanglement_entropy(psi, dims, list(key))
            return cache[key]

        for a, b, c in triples:
            v = i3_from_entropy(S, [a], [b], [c]) / np.log2(D)
            tot += 1
            viol += v > 1e-6
            worst = max(worst, v)
    tn_rows.append({"D": D, "fraction_violating": viol / tot, "largest_I3_in_links": float(worst),
                    "checks": tot})
summary["E2_random_webs"] = tn_rows

# ---------------------------------------------------------------------------
# E3. Physical and special states
# ---------------------------------------------------------------------------
def block_triples(n, max_len=3, max_count=600):
    """Disjoint contiguous blocks A, B, C on a ring (rest is the purifier)."""
    out = []
    for la, lb, lc in itertools.product(range(1, max_len + 1), repeat=3):
        for sa in range(n):
            A = [(sa + i) % n for i in range(la)]
            for gap1 in range(0, n):
                sb = (sa + la + gap1) % n
                B = [(sb + i) % n for i in range(lb)]
                for gap2 in range(0, n):
                    sc = (sb + lb + gap2) % n
                    C = [(sc + i) % n for i in range(lc)]
                    if len(set(A) | set(B) | set(C)) == la + lb + lc and la + lb + lc < n:
                        out.append((A, B, C))
    rng.shuffle(out)
    seen, uniq = set(), []
    for t in out:
        key = tuple(tuple(sorted(x)) for x in t)
        if key not in seen:
            seen.add(key)
            uniq.append(t)
        if len(uniq) >= max_count:
            break
    return uniq


def mmi_profile(psi, n, triples_):
    dims = [2] * n
    cache = {}

    def S(r):
        key = tuple(sorted(r))
        if key not in cache:
            cache[key] = q.entanglement_entropy(psi, dims, list(key))
        return cache[key]

    vals = np.array([i3_from_entropy(S, list(a), list(b), list(c)) for a, b, c in triples_])
    return {"fraction_violating": float(np.mean(vals > 1e-6)), "largest_I3_bits": float(vals.max()),
            "smallest_I3_bits": float(vals.min()), "triples": len(vals)}, vals


N = 12
trip = block_triples(N)
states = {}
for label, h in (("Ising ring, paramagnet (h=2)", 2.0), ("Ising ring, critical (h=1)", 1.0),
                 ("Ising ring, cat-like (h=0.5)", 0.5)):
    states[label] = sm.ground_state(sm.tfim_hamiltonian(N, sm.ring_couplings(N), h), rng)[1]
states["Ising ring, critical, nudged (g=0.1)"] = sm.ground_state(
    sm.tfim_hamiltonian(N, sm.ring_couplings(N), 1.0, g=0.1), rng)[1]
ghz = np.zeros(2**N, complex); ghz[0] = ghz[-1] = 1 / np.sqrt(2)
states["GHZ (cat) state"] = ghz
w = np.zeros(2**N, complex)
for k in range(N):
    w[1 << k] = 1 / np.sqrt(N)
states["W state"] = w
states["Random state"] = q.random_state(2**N, rng)
phys = {}
dists = {}
for label, psi in states.items():
    phys[label], dists[label] = mmi_profile(psi, N, trip)
CLEAR = 0.01  # bits; below this, positive I3 is indistinguishable from zero for our purposes
for label in phys:
    phys[label]["fraction_clearly_violating"] = float(np.mean(dists[label] > CLEAR))
summary["E3_states"] = phys
summary["E3_note"] = (f"{len(trip)} random triples of disjoint blocks (1-3 sites each) on a {N}-site ring; "
                      f"'clearly violating' means I3 > {CLEAR} bits")

# ---------------------------------------------------------------------------
# E4. Is it the cat? Nudge the system to pick one branch and re-check
# ---------------------------------------------------------------------------
nudges = [0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3]
nudge_rows = {}
for label, h in (("critical (h=1)", 1.0), ("cat-like (h=0.5)", 0.5)):
    rows = []
    for gval in nudges:
        psi = sm.ground_state(sm.tfim_hamiltonian(N, sm.ring_couplings(N), h, g=gval), rng)[1]
        prof, vals = mmi_profile(psi, N, trip)
        rows.append({"g": gval, "largest_I3_bits": prof["largest_I3_bits"],
                     "fraction_clearly_violating": float(np.mean(vals > CLEAR))})
    nudge_rows[label] = rows
summary["E4_symmetry_breaking_nudge"] = nudge_rows
summary["runtime_seconds"] = round(time.time() - t0, 1)
(OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=float))

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.6, 4.2))
labels = list(phys)
fr = [phys[k]["fraction_clearly_violating"] for k in labels]
colors = [ps.SERIES[0] if f < 0.01 else ps.SERIES[1] for f in fr]
y = np.arange(len(labels))[::-1]
ax.barh(y, fr, color=colors, height=0.6, edgecolor=ps.SURFACE, linewidth=2)
for yy, f in zip(y, fr):
    ax.text(f + 0.01, yy, f"{100 * f:.0f}%", va="center", color=ps.INK, fontsize=9)
ax.set_yticks(y, labels)
ax.set_xlim(0, 1.1)
ax.set_xlabel(f"Share of region triples that clearly break the web pattern (I₃ > {CLEAR} bits)")
ax.grid(axis="y", visible=False)
ps.titled(ax, "Which states could come from a web of links?",
          f"Monogamy of mutual information on a {N}-spin ring; every graph obeys it ({graph_trials:,} random graphs, 0 violations)")
fig.savefig(OUT / "fig1_which_states_fit.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(7.2, 3.8))
for i, (label, rows) in enumerate(nudge_rows.items()):
    xs_ = [max(r["g"], 3e-4) for r in rows]
    ax.plot(xs_, [r["largest_I3_bits"] for r in rows], color=ps.SERIES[i], marker="o", markersize=5,
            label=f"Ising ring, {label}")
ax.axhline(0, color=ps.AXIS, linewidth=1)
ax.axhspan(0, -0.1, color=ps.SERIES[2], alpha=0.08, linewidth=0)
ax.text(0.28, -0.05, "fits the web pattern", ha="right", va="center", color=ps.INK_2, fontsize=8.5)
ax.set_xscale("log")
ax.set_xticks([3e-4, 1e-3, 1e-2, 1e-1], ["0", "0.001", "0.01", "0.1"])
ax.set_ylim(-0.1, 1.05)
ax.set_xlabel("Nudge toward one branch (longitudinal field g)")
ax.set_ylabel("Largest I₃ over all triples (bits)")
ax.legend(loc="upper right")
ps.titled(ax, "The pattern-breaking part is the cat, and it's fragile",
          "A tiny nudge makes the system pick one branch; what remains obeys the web pattern")
fig.savefig(OUT / "fig2_cat_is_fragile.png")
plt.close(fig)


print(json.dumps(summary, indent=2, default=float))
