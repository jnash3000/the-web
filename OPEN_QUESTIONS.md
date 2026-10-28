# Open questions

Questions the hypothesis has to answer, roughly in order of how much they matter. Each says why it matters and what progress would look like.

## 1. Does "web geometry" pin down exactly the quantum set?

For simple Bell tests, quantum correlations are exactly the inner products of unit vectors, so P3 holds ([Investigation 01](investigations/01-tsirelson-geometry/)). For more complicated scenarios, researchers have found an "almost quantum" set of correlations that satisfies every proposed physical principle but is slightly larger than what quantum mechanics allows.

There's also a sharper challenge from the literature review: 2√2 is reached by a *single* entangled pair at any distance, and more entanglement never raises it (Investigation 01 agrees: arrows in a plane already max out). So a bottleneck limiting *how much* entanglement two regions share can't by itself explain *why* each pair stops at 2√2. P1 (capacity) and P3 (correlation geometry) may be two different things that the hypothesis currently runs together.

**Progress would look like:** a definition of web capacity, made precise, that carves out the quantum set and excludes the almost-quantum points. Testing this needs a semidefinite-programming solver (e.g. `cvxpy` with SCS or MOSEK), which couldn't be installed in the environment where this repo was started. It runs fine on a normal machine.

## 2. What exactly is the "cat layer"?

[Investigation 04](investigations/04-finite-configurations/) found that GHZ-like correlations break the graph pattern, give no geometry, and disappear under the slightest symmetry-breaking nudge. Is there a clean way to split any state into a web-like part and a cat-like part? Does the cat layer correspond to anything physical beyond "fragile superposition," and does decoherence always remove it?

**Progress would look like:** a decomposition (or at least a measure) that separates the two, tested on larger systems and on states with other symmetries.

## 3. How does the reader pick the carving? (P0)

[Investigation 03](investigations/03-one-web-two-jobs/) shows geometry depends on how a state is split into nodes, and the clean carving is the one where couplings are local. But that uses the Hamiltonian, which already assumes a split. Can the right carving be found from the state or the dynamics alone? Carroll & Singh's "quantum mereology" attempts this.

**Progress would look like:** an algorithm that, given only a Hamiltonian as a big matrix (no labels), finds the carving in which it looks local, then checks that the entanglement geometry appears in that carving.

## 4. What about volume-law entanglement?

Ground states of local systems tend to obey an area law: entanglement between a region and the rest scales with the boundary (confirmed in Investigation 03). But highly excited and thermal states of the *same* local systems have entanglement that scales with volume. If the web's structure is fixed, how can the entanglement it supports change so much?

**Possible answers:** (a) the per-link capacity (link size) is large, and the area law reflects how ground states *use* the web rather than what it allows; (b) thermal entropy is a different thing from structural capacity. Investigation 02 gives some support to (a): the ceiling is set by structure, the fill by what's on the nodes.

## 5. Small quantum webs vs graphs

Random quantum webs with small links (D = 2) occasionally break the graph pattern slightly ([Investigation 04](investigations/04-finite-configurations/)) and use only about half their capacity ([Investigation 02](investigations/02-capacity-from-structure/)). Is the "web" in the hypothesis a graph with capacities, or a quantum network whose behaviour only approaches a graph's for large links? These differ for small systems.

## 6. The full entropy cone

Monogamy of mutual information is one of many inequalities graphs obey; more appear with 5+ regions (the holographic entropy cone). Do physical, non-cat states obey the rest too?

## 7. What sets the web's structure, and where does time come in?

If the web determines distance and entanglement, what determines the web? Is it fixed, does it evolve, and is its evolution what we call dynamics or gravity? Every investigation so far uses a fixed snapshot; a version where time also emerges is far harder.

## 8. Can gravity entangle masses? (C1)

The most direct physical test, and it's out of our hands. Track the experimental status (see [docs/literature.md](docs/literature.md)).

## 9. Is the distance reconstruction unique?

Investigation 03 uses distance = −log(relative mutual information). Different formulas could give different geometries. Results should be checked against alternatives (correlation functions, geodesic versions, other normalizations).
