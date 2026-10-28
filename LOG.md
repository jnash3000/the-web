# Research log

Newest entries first. Each entry records what was done, what was found, and what changed.

## 2026-10-28 — Repo set up, four investigations, hypothesis v0.3

**Set up.** Wrote down the hypothesis, its origins and open questions. Built a small Python package (`src/theweb`) with tested tools for entropies, tensor networks, Bell correlations, spin models and geometry reconstruction. 14 tests pass. A literature background with verified sources is in `docs/literature.md`.

**Findings.**
- *01, Tsirelson geometry:* arrows on a line give 2, arrows in a plane give 2√2 to 15 digits, and the PR box can't be drawn with arrows in any dimension. Geometry runs out at exactly visibility 1/√2. Supports P3 (as expected from Tsirelson's theorem).
- *02, Capacity from structure:* no region ever exceeded its min-cut capacity (4,100 checks). Entanglement follows pipe width. Random webs fill 54% of capacity at link size 2, 92% at 6. Refinement: **structure sets the ceiling; the nodes set how full it gets.**
- *03, One web, two jobs:* ring and grid redrawn from entanglement alone (rank agreement 0.99, right dimension); a scrambled ring recovered blind; in the grid, the same links predict region entanglement (0.99 correlation with boundary links). Re-carving the same state into far-apart nodes destroys the geometry in one step: **the geometry depends on how the reader carves the nodes.**
- *04, Finite configurations:* graphs never break monogamy of mutual information (1,500 random graphs); GHZ, W and cat-like Ising states always do. The violation lives in the cat part: **a tiny symmetry-breaking nudge removes it.**

**What changed.** Hypothesis moved to v0.3: P2 merged into P1 (capacity determined by structure, not a fixed budget), P0 added (nodes need a reader), C2 added (graph constraints on entanglement).

**Environment note.** `cvxpy` could not be installed in the workspace where this started, so SDP-based work (open question 1) is deferred. Everything else uses numpy, scipy, networkx and matplotlib.

**Next steps.**
1. Open question 1 on a machine with `cvxpy`: does any "web capacity" definition give exactly the quantum set?
2. Open question 2: separate the web-like and cat-like parts of a state.
3. Open question 3: find the local carving of a Hamiltonian given as an unlabeled matrix.
