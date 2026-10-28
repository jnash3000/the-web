"""Random tensor networks on graphs: the simplest precise version of a "web".

A network is a set of vertices joined by bonds. Each bond, and each dangling
"leg" sticking out of the network, carries an index of dimension D. Every vertex
holds a random tensor with one index per incident bond or leg. Contracting all
bonds leaves a quantum state on the legs (the "boundary").

Key fact (the structure-limited capacity of P1): cutting the network into two
pieces through k bonds shows the state's Schmidt rank across that cut is at most
D**k. So the entanglement entropy of a boundary region A obeys

    S(A) <= mincut(A) * log2(D)   bits,

where mincut(A) is the fewest bonds (or legs) you must cut to separate A from the
rest of the boundary. The capacity is set entirely by the graph's shape.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import networkx as nx
import numpy as np

from .quantum import entanglement_entropy, normalize

MAX_INTERMEDIATE = 2**26  # refuse contractions with intermediate tensors larger than this


@dataclass
class Network:
    n_vertices: int
    bonds: list[tuple[int, int]]  # internal bonds; repeats allowed (parallel bonds)
    legs: list[int]  # legs[k] = vertex that boundary leg k hangs off
    D: int = 2
    name: str = ""
    tensors: list[np.ndarray] = field(default_factory=list, repr=False)

    # ------------------------------------------------------------------ build
    def _vertex_labels(self, v: int) -> list[tuple[str, int]]:
        labels = [("b", i) for i, (a, b) in enumerate(self.bonds) if v in (a, b)]
        labels += [("l", k) for k, w in enumerate(self.legs) if w == v]
        return labels

    def randomize(self, rng: np.random.Generator) -> "Network":
        """Fill every vertex with an independent complex Gaussian tensor."""
        self.tensors = []
        for v in range(self.n_vertices):
            shape = (self.D,) * len(self._vertex_labels(v))
            t = rng.normal(size=shape) + 1j * rng.normal(size=shape)
            self.tensors.append(t)
        return self

    # -------------------------------------------------------------- contract
    def state(self) -> np.ndarray:
        """Contract all bonds; return the normalized state on the legs (leg 0 first)."""
        if not self.tensors:
            raise ValueError("call randomize() first")
        remaining = set(range(self.n_vertices))
        start = max(remaining, key=lambda v: sum(1 for w in self.legs if w == v))
        cur = self.tensors[start]
        cur_labels = self._vertex_labels(start)
        remaining.remove(start)
        while remaining:
            # greedy: absorb the vertex that leaves the fewest open indices
            def cost(v):
                vl = self._vertex_labels(v)
                shared = len(set(vl) & set(cur_labels))
                return (len(cur_labels) + len(vl) - 2 * shared, -shared)

            v = min(remaining, key=cost)
            vl = self._vertex_labels(v)
            shared = [lab for lab in cur_labels if lab in vl]
            ax_cur = [cur_labels.index(lab) for lab in shared]
            ax_v = [vl.index(lab) for lab in shared]
            new_labels = [l for l in cur_labels if l not in shared] + [l for l in vl if l not in shared]
            if self.D ** len(new_labels) > MAX_INTERMEDIATE:
                raise MemoryError(f"intermediate tensor too large ({len(new_labels)} indices)")
            cur = np.tensordot(cur, self.tensors[v], axes=(ax_cur, ax_v))
            cur_labels = new_labels
            remaining.remove(v)
        # self-bonds (both ends contracted already) cannot occur; any leftover
        # bond label would mean a bond to a vertex outside the network
        assert all(l[0] == "l" for l in cur_labels), cur_labels
        order = [cur_labels.index(("l", k)) for k in range(len(self.legs))]
        return normalize(np.transpose(cur, order).reshape(-1))

    # ---------------------------------------------------------------- graphs
    def graph(self) -> nx.MultiGraph:
        """Vertices plus one node per leg ('leg', k)."""
        g = nx.MultiGraph()
        g.add_nodes_from(range(self.n_vertices))
        g.add_edges_from(self.bonds)
        for k, v in enumerate(self.legs):
            g.add_edge(("leg", k), v)
        return g

    def min_cut(self, region: list[int]) -> int:
        """Fewest bonds/legs to cut to separate boundary legs `region` from the rest."""
        region = set(region)
        if not region or len(region) == len(self.legs):
            return 0
        flow = nx.DiGraph()
        for a, b in list(self.bonds) + [(("leg", k), v) for k, v in enumerate(self.legs)]:
            for u, w in ((a, b), (b, a)):
                cap = flow[u][w]["capacity"] + 1 if flow.has_edge(u, w) else 1
                flow.add_edge(u, w, capacity=cap)
        for k in range(len(self.legs)):
            if k in region:
                flow.add_edge("SRC", ("leg", k), capacity=float("inf"))
            else:
                flow.add_edge(("leg", k), "SNK", capacity=float("inf"))
        return int(round(nx.maximum_flow_value(flow, "SRC", "SNK")))

    def leg_distances(self) -> np.ndarray:
        """Shortest-path distance (number of bonds) between every pair of legs."""
        g = nx.Graph(self.graph())
        n = len(self.legs)
        d = np.zeros((n, n))
        for i in range(n):
            lengths = nx.single_source_shortest_path_length(g, ("leg", i))
            for j in range(n):
                d[i, j] = lengths[("leg", j)]
        return d

    def entropy(self, psi: np.ndarray, region: list[int], alpha: float = 1.0) -> float:
        return entanglement_entropy(psi, [self.D] * len(self.legs), region, alpha)


# ---------------------------------------------------------------- examples
def two_clusters(m: int, k: int, D: int) -> Network:
    """Two rings of m vertices (one leg each) joined by k bonds: a pipe of width k."""
    bonds = [(i, (i + 1) % m) for i in range(m)] + [(m + i, m + (i + 1) % m) for i in range(m)]
    bonds += [(i % m, m + (i % m)) for i in range(k)]
    return Network(2 * m, bonds, legs=list(range(2 * m)), D=D, name=f"two_clusters(m={m},k={k})")


def chain(n: int, D: int) -> Network:
    """Open chain of n vertices, one leg each (a matrix product state)."""
    return Network(n, [(i, i + 1) for i in range(n - 1)], list(range(n)), D, name=f"chain({n})")


def binary_tree(depth: int, D: int) -> Network:
    """Complete binary tree with 2**depth leaves, one leg per leaf (tree tensor network)."""
    n_int = 2**depth - 1
    bonds = [(v, c) for v in range(n_int) for c in (2 * v + 1, 2 * v + 2) if c < 2 ** (depth + 1) - 1]
    leaves = list(range(n_int, 2 ** (depth + 1) - 1))
    return Network(2 ** (depth + 1) - 1, bonds, leaves, D, name=f"binary_tree(depth={depth})")


def random_graph_network(n: int, degree: int, n_legs: int, D: int, rng: np.random.Generator) -> Network:
    """Random regular graph on n vertices with legs on n_legs randomly chosen vertices."""
    seed = int(rng.integers(0, 2**31 - 1))
    g = nx.random_regular_graph(degree, n, seed=seed)
    legs = sorted(rng.choice(n, size=n_legs, replace=False).tolist())
    return Network(n, list(g.edges()), legs, D, name=f"random_{degree}-regular(n={n})")
