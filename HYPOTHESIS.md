# The Web Hypothesis

**Current version: v0.3** (see [version history](#version-history) below)

> Beneath space and time is a web of connection. Its structure sets both distance and how much entanglement is possible between any two parts, and quantum mechanics' limits are the geometry of that web.

This is a working hypothesis, not a theory. Most of its parts restate known physics or existing research programs in a particular arrangement. The point of writing it down precisely is to find out which parts are already true, which are open, and which could fail.

---

## Postulates

| # | Postulate | Plain version |
|---|-----------|---------------|
| **P0** | **Nodes need a reader.** The web doesn't come pre-divided into parts. "Nodes" are distinguished by a reading system, and the natural carving is the one in which the web's links are local. | What counts as a separate thing depends on who, or what, is looking. |
| **P1** | **Structure-limited capacity.** The entanglement possible between two parts is bounded by the narrowest bottleneck in the web separating them. There is no separately imposed constant, and the "shared budget" (monogamy) is a consequence: a node's capacity is the cut around it. | The pipe's width sets the flow, and the pipe is just the shape of the web. |
| **P3** | **Correlations are geometry.** The maximum strength of correlations (e.g. the Tsirelson bound, 2√2 in the CHSH test) is a geometric fact about the space correlations live in, not an extra rule. | The limit is "whatever is geometrically possible." |
| **P4** | **Space is downstream.** Distance between two parts reflects how weakly they are connected in the web. | Near = strongly linked. Far = weakly linked. |
| **P5** | **One web, two jobs.** The *same* structure determines both distances (P4) and entanglement limits (P1). | Measure one, and you can predict the other. |

(P2, "shared budget," was merged into P1 in v0.3. The numbering is kept so older notes still line up.)

**Consequences**

- **C1.** If space (and therefore gravity, the geometry of space) comes from the web, gravity must be able to create entanglement between masses.
- **C2.** If capacities are cuts through a web, entanglement patterns must obey graph constraints such as monogamy of mutual information. States that break them (GHZ/cat-like states) can't be purely web-like.

P5 is what keeps the hypothesis from being unfalsifiable. Without it, any observation can be explained as "whatever the web's shape allowed." With it, the web has to do two jobs at once, and the two can be checked against each other.

---

## Status of each part

| Part | Status | Evidence in this repo |
|------|--------|------------------------|
| P0 | **Matches an open research question** (subsystems are "observable-induced": Zanardi, Lidar & Lloyd 2004; "quantum mereology": Carroll & Singh 2021). | [03](investigations/03-one-web-two-jobs/): re-carving the same state into far-apart nodes destroys its geometry in one step; neighbouring re-carvings mostly preserve it. |
| P1 | **True in tensor-network models**: a rigorous ceiling (entropy ≤ min-cut × log D), nearly reached by random webs with larger links. Monogamy is established physics (Coffman–Kundu–Wootters 2000). | [02](investigations/02-capacity-from-structure/): 0 violations in 4,100 checks; entanglement follows pipe width; fill rises from 54% (D=2) to 92% (D=6). |
| P3 | **Established mathematically** for two-outcome, two-party correlations (Tsirelson's theorem). Open beyond that (the "almost quantum" problem). | [01](investigations/01-tsirelson-geometry/): 1D arrows give 2, 2D arrows give 2√2 to 15 digits, geometry runs out at exactly 1/√2 visibility. |
| P4 | **Active research program** (Van Raamsdonk 2010; Cao, Carroll & Michalakis 2017). Not established. | [03](investigations/03-one-web-two-jobs/): ring and grid redrawn from entanglement alone (rank agreement 0.99, correct dimension); scrambled ring recovered blind. |
| P5 | **Partly realized in holography** (Ryu–Takayanagi). This repo's main angle. | [03](investigations/03-one-web-two-jobs/): in the grid's ground state, the same links predict both distances and region entanglement (correlation 0.99 with boundary links vs 0.70 with size). |
| C1 | **Untested.** Gravity-mediated entanglement experiments are proposed but not yet feasible. | [docs/literature.md](docs/literature.md) |
| C2 | **Partly confirmed, with a twist.** Graphs never violate MMI; GHZ, W and cat-like Ising states do. But the violation lives entirely in the cat part, and a tiny symmetry-breaking nudge removes it. | [04](investigations/04-finite-configurations/) |

---

## What would count against it

- **Gravity fails to entangle.** A sufficiently sensitive experiment showing masses interacting only through gravity do *not* become entangled would put P4 and C1 in serious trouble.
- **Robust entanglement that ignores structure.** If, in systems whose geometry we know independently, robust (non-cat) entanglement systematically breaks graph constraints or fails to track the structure separating regions, P1/P5 weaken. (Known complications: volume-law entanglement in excited states, and cat-like global correlations; see open questions.)
- **No geometric account of the full quantum boundary.** If no definition of "web geometry" reproduces exactly the set of correlations quantum mechanics allows (rather than a slightly larger set), P3 is incomplete.
- **A Bell violation above 2√2.** This would break standard quantum mechanics and P3 as stated.

## What it does not claim

- It does not currently predict any deviation from standard quantum mechanics at laboratory scale. (v0.1 did; see below.)
- It does not claim the web is literally a tensor network. Tensor networks are used here as a test bed: the simplest mathematical objects where "structure sets capacity" can be made precise.
- It does not claim cat-like states are impossible. They exist and labs make them. The claim is that they aren't web-like.

---

## Version history

**v0.3 (current).** Two refinements from the repo owner. (1) Capacity isn't a fixed budget that gets shared out; it's determined by the web's structure, so monogamy is a consequence of P1, not a separate postulate. (2) Nodes need a "reader" to be distinguished (P0). Also added C2 after noticing that a finite set of nodes allows only certain connection patterns, which implies testable constraints on entanglement.

**v0.2.** Capacity is limited by the web's own structure, "whatever is geometrically possible," not by a hard number. The previous postulate predicting a ceiling below quantum mechanics was dropped, because quantum mechanics' own limits can be read as the geometry. Trade-off: the hypothesis lost its most direct quantum-computer test, and gained P5 as its consistency requirement.

**v0.1 (superseded).** "Finite Capacity Hypothesis." Beneath space and time there's a web of connection with limited capacity; entanglement allocates it; distance is weak allocation; correlations cost capacity. Point 4 claimed the total capacity of any system is smaller than standard quantum mechanics allows, which would show up as an entanglement-specific error floor in quantum computers. Existing results already constrain this: Google's 2019 random-circuit experiment (53 qubits, near-maximal entanglement) found no extra penalty beyond component error rates.

See [docs/origins.md](docs/origins.md) for how the idea developed.
