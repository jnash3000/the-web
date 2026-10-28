# How the idea developed

This hypothesis came out of a single conversation that started with a claim found online and moved, step by step, toward something testable. The steps are recorded here because each one changed the idea, and the reasons for the changes matter as much as the result.

## 1. The starting claim

A passage online said physicists "have absolutely no idea" what carries forces between distant particles, and that "virtual photons" are a placeholder for that ignorance.

That's mostly wrong. The electromagnetic force is carried by the electromagnetic field, which has measurable properties: it takes time to travel (at the speed of light), it carries energy and momentum, and it outlives its sources. "Virtual photons" are a term from the perturbative math of quantum electrodynamics, the most precisely tested theory in science. What *is* genuinely open is a deeper question: what a field fundamentally is, if it's made of anything at all.

## 2. Entanglement and a shared "base"

The next idea: entangled particles share a common "base" that is prior to space and time. If so, the spatial gap between them is downstream of the connection, and entanglement isn't mysterious.

This matches real lines of thought: Bohm's "implicate order," Van Raamsdonk's "building up spacetime with entanglement," and Maldacena and Susskind's ER=EPR. Two refinements came out of discussing it:

- The base can't just hold **pre-set answers** (like gloves split into two boxes). Bell's theorem and the experiments that earned the 2022 Nobel Prize rule that out.
- Particles that have never interacted can become entangled (**entanglement swapping**). So the base can't be a private link between pairs that were created together. It has to underlie everything.

## 3. Why the limit? "The connection isn't free"

Quantum correlations reach 2√2 ≈ 2.83 in the standard Bell test, more than pre-set instructions allow (2) but less than the math permits (4). The suggestion: the limit kicks in early because the connection has a cost.

This matches several research results: van Dam showed that maximal correlations would make communication almost free; information causality (2009) derives the 2.83 limit from "m bits sent, at most m bits learned"; monogamy says entanglement is a shared budget.

## 4. "Potential," then "bandwidth," then "capacity"

The cost was first framed as **potential**: like a car's theoretical fastest time, always there mathematically but never reached. Discussing this separated two different gaps: lab results falling short of 2.83 (noise, like friction) versus 2.83 falling short of 4 (a structural limit, like the Carnot limit on engines).

The question became: what plays the role of entropy, the thing that always has to be "paid"? The answer offered was **bandwidth**. That connects to information causality, monogamy and the holographic principle (information capacity of a region scales with its boundary area). Since bandwidth implies "per unit time," and the base is supposed to come before time, the word was changed to **capacity**.

## 5. v0.1: The Finite Capacity Hypothesis

Written up with a falsifiable addition: total capacity is smaller than standard quantum mechanics allows. That predicts an entanglement-specific error floor in quantum computers. Existing experiments already push any such ceiling up.

## 6. v0.2: "Whatever is geometrically possible"

The key refinement: capacity is limited by the web's **own structure**, not a hard number. This matches how the 2.83 limit actually arises. Quantum correlations behave like angles between arrows, and the parallelogram law caps the Bell score at √2 + √2. It also matches the max-flow min-cut theorem: the capacity between two parts of a network equals its narrowest bottleneck.

To stop "whatever the geometry allowed" from explaining everything, the hypothesis now requires the **same web to do two jobs**: set distance and set entanglement limits (P5). That's what this repo investigates.

## 7. v0.3: "Determined by structure" and "nodes need a reader"

Two more refinements. First, capacity isn't "finite and shared" like a fixed budget handed out; it's determined by the web's structure. In tensor-network terms, a node's capacity is just the narrowest cut around it, so monogamy follows from structure and no longer needs its own postulate.

Second, a connection needs nodes, and nodes need to be *distinguished*, which is observer-dependent: a reading system picks out the nodes, not the web itself. This matches a real open problem (entanglement is only defined relative to a split into subsystems). And if there are only finitely many nodes, they can only be connected in finitely many ways. That turned into a concrete test: entanglement from graph cuts must obey monogamy of mutual information, which some quantum states (GHZ/cat states) break.

## Credit

The core ideas (the shared pre-spacetime base, the connection having a cost, bandwidth/capacity, and structure-limited rather than hard-limited capacity) came from the repo owner. The connections to existing physics, the formalization and the tests were developed with Claude.
