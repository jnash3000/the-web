# Literature background

This note collects the published physics behind the-web's hypothesis: that space and time sit on top of a web of connections, and that the web's structure sets both distance and how much entanglement two parts can share. It is written for a smart non-specialist, but it tries to be exact about what is established, what is an active research programme, and what is speculation. Each theme gives a plain-language summary, then key papers with a note on why each matters here, then a verdict on whether the work **supports**, **constrains** or **challenges** the hypothesis. All citations were checked in October 2026 against arXiv abstract pages, publisher or library records, or indexing services. The details that could not be confirmed are listed in [section 10](#10-verification-notes).

One theme recurs: much of the hypothesis restates physics that already exists, often in sharper form. That is useful, because it isolates the parts that are actually new and testable.

## Contents

0. [A few terms](#0-a-few-terms)
1. [Bell's theorem and Bell tests](#1-bells-theorem-and-bell-tests)
2. [The Tsirelson bound and its geometry](#2-the-tsirelson-bound-and-its-geometry)
3. [Principles that try to derive the quantum limit](#3-principles-that-try-to-derive-the-quantum-limit)
4. [Monogamy of entanglement](#4-monogamy-of-entanglement)
5. [Holography, min-cuts and capacity](#5-holography-min-cuts-and-capacity)
6. [Space from entanglement](#6-space-from-entanglement)
7. [Gravity-mediated entanglement](#7-gravity-mediated-entanglement)
8. [Older and philosophical ideas](#8-older-and-philosophical-ideas)
9. [Quantum hardware and "limited entanglement"](#9-quantum-hardware-and-limited-entanglement)
10. [Verification notes](#10-verification-notes)

---

## 0. A few terms

- **CHSH value (S):** one number from a standard two-party Bell test. Pre-set local instructions allow |S| ≤ 2. Quantum mechanics allows up to 2√2 ≈ 2.83 (the Tsirelson bound). "No faster-than-light signalling" alone allows up to 4.
- **Ebit:** one maximally entangled pair of qubits.
- **Entanglement entropy:** for a pure state split into A and B, how many ebits' worth of entanglement cross the split.
- **Mutual information I(A:B):** total correlation, classical plus quantum, in bits.
- **Max-flow / min-cut:** in a network of links with capacities, the most that can flow between two sides equals the total capacity of the narrowest set of links that separates them.

---

## 1. Bell's theorem and Bell tests

In 1964 John Bell proved that no theory in which outcomes are fixed in advance by shared local instructions can reproduce all of quantum mechanics' predictions. Clauser, Horne, Shimony and Holt (CHSH) turned this into a practical test: two parties each choose one of two settings, record ±1, and combine four correlations into S. Experiments by Clauser (1972), Aspect (1982) and Zeilinger's group (1998) found violations, but left loopholes: a signal might have passed between the stations, or missed detections might have skewed the data. In 2015 three groups closed both main loopholes at once. Delft used electron spins 1.3 km apart (S = 2.42 ± 0.20 over 245 trials); Vienna and NIST used photons and reached far higher statistical significance. The 2022 Nobel Prize went to Aspect, Clauser and Zeilinger for this line of work.

The conclusion is now settled: nature's correlations cannot come from pre-set local instructions. They also do not weaken with distance; a satellite test found S of about 2.37 between stations 1,203 km apart (Yin et al., *Science* 356, 1140, 2017, arXiv: [1707.01339](https://arxiv.org/abs/1707.01339)). Any hidden influence carrying the correlations would have to move at least about 10,000 times faster than light, assuming a plausible preferred reference frame (Salart et al., *Nature* 454, 861, 2008, arXiv: [0808.3316](https://arxiv.org/abs/0808.3316)), and any finite-speed influence of this kind would allow faster-than-light signalling (Bancal et al. 2012). Entanglement and Bell violation are also different properties: some entangled mixed states admit a local-instructions model for all standard (projective) measurements (Werner, *Phys. Rev. A* 40, 4277, 1989).

**Key papers**

- **Bell, J. S. (1964).** "On the Einstein Podolsky Rosen paradox." *Physics Physique Fizika* 1, 195–200. No arXiv version. Shows that "pre-set answers" pictures of entanglement are testable and, if quantum mechanics is right, false.
- **Clauser, J. F., Horne, M. A., Shimony, A. & Holt, R. A. (1969).** "Proposed experiment to test local hidden-variable theories." *Phys. Rev. Lett.* 23, 880–884. No arXiv version. Defines S and the classical limit of 2 used throughout this repo.
- **Hensen, B. et al. (2015).** "Loophole-free Bell inequality violation using electron spins separated by 1.3 kilometres." *Nature* 526, 682–686. arXiv: [1508.05949](https://arxiv.org/abs/1508.05949). First loophole-free test. It used entanglement swapping, so the two spins never interacted directly.
- **Giustina, M. et al. (2015).** "Significant-loophole-free test of Bell's theorem with entangled photons." *Phys. Rev. Lett.* 115, 250401. arXiv: [1511.03190](https://arxiv.org/abs/1511.03190). Photonic confirmation at overwhelming significance.
- **Shalm, L. K. et al. (2015).** "Strong loophole-free test of local realism." *Phys. Rev. Lett.* 115, 250402. arXiv: [1511.03189](https://arxiv.org/abs/1511.03189). Independent NIST confirmation; three platforms agreeing makes the result robust.
- **Nobel Prize in Physics 2022 (Aspect, Clauser, Zeilinger).** Awarded for entangled-photon experiments establishing Bell violations and pioneering quantum information science ([Physics World report](https://physicsworld.com/a/alain-aspect-john-clauser-and-anton-zeilinger-win-the-2022-nobel-prize-for-physics/)). Marks the result as mainstream, settled physics.
- **Brunner, N., Cavalcanti, D., Pironio, S., Scarani, V. & Wehner, S. (2014).** "Bell nonlocality." *Rev. Mod. Phys.* 86, 419. arXiv: [1303.2849](https://arxiv.org/abs/1303.2849). The standard review; the best single entry point for sections 1–3.
- **Bancal, J.-D., Pironio, S., Acín, A., Liang, Y.-C., Scarani, V. & Gisin, N. (2012).** "Quantum non-locality based on finite-speed causal influences leads to superluminal signalling." *Nature Physics* 8, 867. arXiv: [1110.3795](https://arxiv.org/abs/1110.3795). Rules out explaining the correlations by any signal travelling through space, however fast.

**Relevance to the-web: constrains.** The web cannot be a store of pre-set answers, and it cannot be a medium that carries influences through space at any finite speed. A connection "beneath" spacetime is compatible with the data, but so is standard quantum mechanics, which predicts them exactly. These results set a floor any version of the hypothesis must meet; they do not favour it. One concrete requirement: whatever the web is, a pair's correlation strength must not depend on its spatial separation.

---

## 2. The Tsirelson bound and its geometry

Boris Tsirelson (Cirel'son) proved in 1980 that quantum mechanics caps S at 2√2, and the reason is geometric. For ±1-valued measurements, every quantum correlation between Alice's setting and Bob's setting equals the dot product of two unit-length arrows (vectors), and any such set of dot products can be realised by some quantum state. S then becomes u₁·(v₁+v₂) + u₂·(v₁−v₂), which is at most |v₁+v₂| + |v₁−v₂|. The parallelogram law fixes the sum of the squares of those two lengths at 4, so their sum is largest when each equals √2, giving 2√2. One ebit with suitably chosen measurement directions reaches it. In 1994 Popescu and Rohrlich showed that no-signalling alone does not explain this limit: their hypothetical "PR box" reaches S = 4 without allowing any signalling. That leaves three nested sets of correlations (local inside quantum inside no-signalling) and the open question of why nature stops at the middle one.

The exact quantum set is hard to describe. Navascués, Pironio and Acín (NPA) built a ladder of computable outer approximations that converges to it. Its first rung (Q₁) already gives 2√2 for CHSH but is too generous in other scenarios. A rung just above it, the "almost-quantum" set, is strictly larger than quantum yet passes every proposed physical principle (section 3). The MIP* = RE result (2020) showed that the edge of the quantum set even depends on modelling choices, finite-dimensional systems versus a more general operator definition. Two points matter most here. More entanglement does not raise the bound: no number of shared ebits, and no dimension of system, pushes CHSH past 2√2. And partially entangled states are often more nonlocal than maximally entangled ones (Methot & Scarani 2006, arXiv: [quant-ph/0601210](https://arxiv.org/abs/quant-ph/0601210)). How strongly a state can violate a Bell inequality is a property of the shape of the quantum set, not of the amount of entanglement.

**Key papers**

- **Cirel'son, B. S. (1980).** "Quantum generalizations of Bell's inequality." *Lett. Math. Phys.* 4, 93–100. No arXiv version. Proves the 2√2 bound via the dot-product picture: the precise sense in which "the limit is geometry".
- **Popescu, S. & Rohrlich, D. (1994).** "Quantum nonlocality as an axiom." *Found. Phys.* 24, 379–385. Not on arXiv; the related 1995 paper "Nonlocality as an axiom for quantum theory" is arXiv: [quant-ph/9508009](https://arxiv.org/abs/quant-ph/9508009). Introduces the PR box: relativity alone does not explain the quantum limit.
- **Navascués, M., Pironio, S. & Acín, A. (2007).** "Bounding the set of quantum correlations." *Phys. Rev. Lett.* 98, 010401. arXiv: [quant-ph/0607119](https://arxiv.org/abs/quant-ph/0607119). The standard tool for computing what quantum mechanics allows in any Bell scenario.
- **Navascués, M., Pironio, S. & Acín, A. (2008).** "A convergent hierarchy of semidefinite programs characterizing the set of quantum correlations." *New J. Phys.* 10, 073013. arXiv: [0803.4290](https://arxiv.org/abs/0803.4290). Proves the ladder converges, so the geometry of the quantum set is computable in practice.
- **Navascués, M., Guryanova, Y., Hoban, M. J. & Acín, A. (2015).** "Almost quantum correlations." *Nature Communications* 6, 6288. arXiv: [1403.4621](https://arxiv.org/abs/1403.4621). A slightly larger-than-quantum set that satisfies the usual principles. Any derivation of the quantum limit must exclude it.
- **Ji, Z., Natarajan, A., Vidick, T., Wright, J. & Yuen, H. (2020).** "MIP* = RE." arXiv: [2001.04383](https://arxiv.org/abs/2001.04383). The quantum set's edge depends on finite versus infinite modelling, a choice a web of finitely many nodes would implicitly make.

**Relevance to the-web: supports the intuition, challenges the "capacity" reading.** "The quantum limit is geometry" is correct, but the geometry is that of measurement directions in Hilbert space, which is textbook physics. The challenge: 2√2 is reached by one ebit, at any distance, and more entanglement never exceeds it. A bottleneck limiting *how many* ebits two regions share cannot by itself explain *why* each ebit stops at 2√2. To add something new, a web model must reproduce the whole quantum set, not just the number. The sharpest target is to predict whether nature is exactly quantum or almost quantum, which suitable Bell experiments can in principle tell apart.

---

## 3. Principles that try to derive the quantum limit

Since about 2005, researchers have looked for a simple information rule that would single out exactly the quantum correlations. Van Dam showed that perfect PR boxes would make *communication complexity* trivial: two parties could compute any joint function of their data by exchanging one bit. Brassard and colleagues showed the same happens for noisy boxes that win the CHSH game more than (3+√6)/6 ≈ 90.8% of the time. Quantum mechanics wins at most cos²(π/8) ≈ 85.4%, so this rule closes part of the gap but not all of it. *Information causality* (Pawłowski et al. 2009) says that if Alice sends Bob m bits, he can learn at most m bits about her data, whatever correlations they share. Classical and quantum physics obey it, and it excludes super-quantum correlations in the standard CHSH family, recovering 2√2 there. It is the closest published formalisation of the-web's "the connection has a cost" idea.

Other proposals cover the rest of the ground. *Macroscopic locality* (coarse-grained statistics of many copies must look classical) gives exactly the first NPA rung Q₁. It recovers 2√2 but is too generous elsewhere. Oppenheim and Wehner showed that a theory's nonlocality is fixed by its uncertainty principle together with its ability to "steer" remote states. *Local orthogonality* reduces to no-signalling for two parties but comes close to the quantum limit with several parties or copies. Toner and Bacon gave a classical exchange rate: one bit of communication plus shared randomness exactly reproduces an ebit's projective-measurement correlations. The current state of play is that no principle singles out exactly the quantum set. The almost-quantum set satisfies all of them (information causality numerically), so whether nature is exactly quantum remains open (survey: Oas & de Barros, arXiv: [1506.05515](https://arxiv.org/abs/1506.05515)).

**Key papers**

- **van Dam, W. (2005; published 2013).** "Implausible consequences of superstrong nonlocality." *Natural Computing* 12, 9–12. arXiv: [quant-ph/0501159](https://arxiv.org/abs/quant-ph/0501159). Perfect super-quantum correlations would make distributed computing nearly free, a first reason nature stops short of S = 4.
- **Brassard, G., Buhrman, H., Linden, N., Méthot, A. A., Tapp, A. & Unger, F. (2006).** "Limit on nonlocality in any world in which communication complexity is not trivial." *Phys. Rev. Lett.* 96, 250401. arXiv: [quant-ph/0508042](https://arxiv.org/abs/quant-ph/0508042). Puts a number (about 90.8%) on the "cost" argument, which falls short of 2√2.
- **Pawłowski, M., Paterek, T., Kaszlikowski, D., Scarani, V., Winter, A. & Żukowski, M. (2009).** "Information causality as a physical principle." *Nature* 461, 1101–1104. arXiv: [0905.2292](https://arxiv.org/abs/0905.2292). Recovers Tsirelson for CHSH from a bits-sent-versus-bits-learned rule.
- **Navascués, M. & Wunderlich, H. (2009).** "A glance beyond the quantum model." *Proc. R. Soc. A* 466, 881–890. arXiv: [0907.0372](https://arxiv.org/abs/0907.0372). Shows that a "classical at large scales" requirement yields 2√2 but not the full quantum set.
- **Oppenheim, J. & Wehner, S. (2010).** "The uncertainty principle determines the nonlocality of quantum mechanics." *Science* 330, 1072–1074. arXiv: [1004.2507](https://arxiv.org/abs/1004.2507). A structural explanation of the limit, the kind the-web is after.
- **Fritz, T., Sainz, A. B., Augusiak, R., Bohr Brask, J., Chaves, R., Leverrier, A. & Acín, A. (2013).** "Local orthogonality as a multipartite principle for quantum correlations." *Nature Communications* 4, 2263. arXiv: [1210.3018](https://arxiv.org/abs/1210.3018). Some limits appear only with many parties, which matters for an inherently many-node web.
- **Toner, B. F. & Bacon, D. (2003).** "Communication cost of simulating Bell correlations." *Phys. Rev. Lett.* 91, 187904. arXiv: [quant-ph/0304076](https://arxiv.org/abs/quant-ph/0304076). Gives a concrete price, one classical bit per ebit, for faking entanglement.

**Relevance to the-web: supports the spirit, constrains the novelty.** "The limit comes from a cost or capacity" is a published idea, and information causality is its most developed form. The-web would add something only if its structure *derived* a correlation set that either equals the quantum set exactly (solving an open problem) or differs from it measurably, for example matching Q₁ or the almost-quantum set, in which case experiment could decide.

---

## 4. Monogamy of entanglement

Entanglement is *monogamous*: if qubit A is maximally entangled with B, it cannot be entangled with anything else. Coffman, Kundu and Wootters (CKW) made this quantitative for three qubits. Measured by the "tangle", A's entanglement with B plus its entanglement with C cannot exceed its entanglement with B and C together. Osborne and Verstraete proved it for any number of qubits. (Not every entanglement measure obeys this additive form, so the choice of measure matters.) Bell correlations are monogamous too: Toner and Verstraete showed that S_AB² + S_AC² ≤ 8, which reduces to the Tsirelson bound when C is uncorrelated. That is the clearest published sense in which Tsirelson is a special case of a sharing rule. But Masanes, Acín and Gisin showed that monogamy follows from no-signalling plus nonlocality alone, so even super-quantum PR boxes are monogamous. Monogamy does not single out quantum mechanics.

Holography adds a stronger kind. Hayden, Headrick and Maloney showed that when entropies come from minimal surfaces (section 5), mutual information is monogamous: I(A:BC) ≥ I(A:B) + I(A:C), equivalently the "tripartite information" I₃ ≤ 0. General quantum states break this. In a 4-qubit GHZ state, every one- or two-qubit subset has 1 bit of entropy, so I₃ = 3 − 3 + 1 = +1. Monogamy of mutual information is therefore a fingerprint of geometric, min-cut-like entanglement.

**Key papers**

- **Coffman, V., Kundu, J. & Wootters, W. K. (2000).** "Distributed entanglement." *Phys. Rev. A* 61, 052306. arXiv: [quant-ph/9907047](https://arxiv.org/abs/quant-ph/9907047). The original "entanglement is a budget" inequality.
- **Osborne, T. J. & Verstraete, F. (2006).** "General monogamy inequality for bipartite qubit entanglement." *Phys. Rev. Lett.* 96, 220503. arXiv: [quant-ph/0502176](https://arxiv.org/abs/quant-ph/0502176). Extends the budget picture to any number of qubits.
- **Toner, B. & Verstraete, F. (2006).** "Monogamy of Bell correlations and Tsirelson's bound." arXiv: [quant-ph/0611001](https://arxiv.org/abs/quant-ph/0611001). The tightest formal link between sharing and 2√2; testable with three parties.
- **Masanes, Ll., Acín, A. & Gisin, N. (2006).** "General properties of nonsignaling theories." *Phys. Rev. A* 73, 012112. arXiv: [quant-ph/0508016](https://arxiv.org/abs/quant-ph/0508016). Monogamy is generic to nonlocal no-signalling theories, so it is not evidence for any particular web.
- **Hayden, P., Headrick, M. & Maloney, A. (2013).** "Holographic mutual information is monogamous." *Phys. Rev. D* 87, 046003. arXiv: [1107.2940](https://arxiv.org/abs/1107.2940). Min-cut entropies obey an extra rule that GHZ states break, a clean test for strict min-cut webs.
- **Dhar, H. S., Pal, A. K., Rakshit, D., Sen(De), A. & Sen, U. (2017).** "Monogamy of quantum correlations — a review." In *Lectures on General Quantum Correlations and their Applications* (Springer). arXiv: [1610.01069](https://arxiv.org/abs/1610.01069). A survey of which correlation measures are monogamous.

**Relevance to the-web: supports, but not distinctively, and supplies a sharp test.** "Entanglement is a shared, limited budget" is established. It holds in any nonlocal no-signalling theory, so it cannot count as evidence for the web. The holographic rule gives a falsification test: if every entanglement pattern were a graph min-cut, GHZ states could not exist. They are routinely made (section 9), so a strict min-cut web must be limited to certain states or allow multi-way links.

---

## 5. Holography, min-cuts and capacity

The max-flow min-cut theorem (Ford and Fulkerson 1956) says that the most that can flow through a network equals the capacity of its narrowest cut. In one area of physics, entanglement provably behaves this way. In the AdS/CFT correspondence, a non-gravitational theory on a boundary is equivalent to a gravitational one in a higher-dimensional "bulk". There, Ryu and Takayanagi (RT) found that a boundary region's entanglement entropy equals the area of the smallest bulk surface enclosing it, divided by 4G (G is Newton's constant). Freedman and Headrick recast this exactly as max-flow. "Bit threads" of roughly Planck-scale thickness, each carrying one unit of entanglement, run out of the region, and the minimal surface is the bottleneck that limits how many fit. Within holography, "capacity is set by the bottleneck" is a theorem.

Tensor networks give discrete, graph-like versions. Swingle observed that MERA, a network used for critical quantum systems, has the geometry of a discretised hyperbolic (AdS-like) space. In any tensor network, the entanglement across a cut is at most the number of links cut times the log of each link's dimension. The "HaPPY" networks of Pastawski, Yoshida, Harlow and Preskill reach this bound for many regions and double as quantum error-correcting codes. Hayden et al. showed that random networks with large links reproduce RT generically. The limits are real. In general networks the quantum max-flow can fall below the min-cut (Cui et al.). Min-cut entropies obey only a restricted set of inequalities, the "holographic entropy cone" (Bao et al.), which many quantum states violate. And all of this is established for anti-de Sitter space and toy models, not for our universe.

**Key papers**

- **Ford, L. R. & Fulkerson, D. R. (1956).** "Maximal flow through a network." *Canadian J. Math.* 8, 399–404. No arXiv version. The theorem behind the "bottleneck" intuition.
- **Ryu, S. & Takayanagi, T. (2006).** "Holographic derivation of entanglement entropy from AdS/CFT." *Phys. Rev. Lett.* 96, 181602. arXiv: [hep-th/0603001](https://arxiv.org/abs/hep-th/0603001). Entanglement equals minimal area, the central entanglement–geometry link.
- **Swingle, B. (2012).** "Entanglement renormalization and holography." *Phys. Rev. D* 86, 065007. arXiv: [0905.1317](https://arxiv.org/abs/0905.1317). A network built purely from entanglement structure yields an emergent geometry: a working "web gives space" example.
- **Pastawski, F., Yoshida, B., Harlow, D. & Preskill, J. (2015).** "Holographic quantum error-correcting codes: toy models for the bulk/boundary correspondence." *JHEP* 06 (2015) 149. arXiv: [1503.06237](https://arxiv.org/abs/1503.06237). An exactly solvable min-cut network, a ready template for this repo's simulations.
- **Hayden, P., Nezami, S., Qi, X.-L., Thomas, N., Walter, M. & Yang, Z. (2016).** "Holographic duality from random tensor networks." *JHEP* 11 (2016) 009. arXiv: [1601.01694](https://arxiv.org/abs/1601.01694). Min-cut behaviour is generic for large random networks; spells out when it fails.
- **Freedman, M. & Headrick, M. (2017).** "Bit threads and holographic entanglement." *Commun. Math. Phys.*, DOI 10.1007/s00220-016-2796-3. arXiv: [1604.00354](https://arxiv.org/abs/1604.00354). Holographic entanglement as max-flow equals min-cut, the closest match to the hypothesis's wording.
- **Cui, S. X., Freedman, M. H., Sattath, O., Stong, R. & Minton, G. (2016).** "Quantum max-flow/min-cut." *J. Math. Phys.* 57, DOI 10.1063/1.4954231. arXiv: [1508.04644](https://arxiv.org/abs/1508.04644). Quantum max-flow equals min-cut only under conditions, so "capacity = bottleneck" is not automatic.
- **Bao, N., Nezami, S., Ooguri, H., Stoica, B., Sully, J. & Walter, M. (2015).** "The holographic entropy cone." *JHEP* 09 (2015) 130. arXiv: [1505.07839](https://arxiv.org/abs/1505.07839). The full list of inequalities that min-cut entropies obey, a checklist for testing graph webs.

**Relevance to the-web: strongly supports the bottleneck idea, constrains its scope.** In holographic settings, "capacity between two regions equals the narrowest cut" is established (RT plus bit threads), and the hypothesis restates it. It holds exactly only for special states. It is an upper bound in general networks. It is unproven for our universe. Simulations here should build on the HaPPY and random-network constructions rather than starting from scratch.

---

## 6. Space from entanglement

Van Raamsdonk argued in 2010, within AdS/CFT, that removing entanglement between two halves of the boundary theory makes the corresponding regions of space pull apart and pinch off. Maldacena and Susskind's "ER = EPR" conjecture goes further: entangled black holes are joined by wormholes, and something similar may hold for any entangled pair. Cao, Carroll and Michalakis tried to do without AdS. They take a quantum state split into parts, treat mutual information as closeness, and reconstruct a best-fit geometry and dimension. Jacobson showed that assuming vacuum entanglement in small regions is in equilibrium (at a maximum for fixed volume) yields Einstein's equation, under stated assumptions.

"Close means strongly entangled" works only because of *area laws*. Ground states of locally interacting systems typically have entanglement that scales with a region's boundary, not its volume (review: Eisert, Cramer and Plenio). Random states are the opposite: Page showed they are nearly maximally entangled across every cut (a "volume law"), with no meaningful notion of near or far. Entanglement entropy is now measurable in the lab. Islam et al. interfered two copies of an ultracold-atom many-body state, and Brydges et al. used random measurements on up to 20 trapped ions. Both make "distance from mutual information" computable from real data.

**Key papers**

- **Van Raamsdonk, M. (2010).** "Building up spacetime with quantum entanglement." *Gen. Rel. Grav.* 42, 2323–2329. arXiv: [1005.3035](https://arxiv.org/abs/1005.3035). The clearest statement that spatial connectedness is entanglement; essentially the hypothesis's first sentence, set in AdS.
- **Maldacena, J. & Susskind, L. (2013).** "Cool horizons for entangled black holes." *Fortsch. Phys.* 61, 781–811. arXiv: [1306.0533](https://arxiv.org/abs/1306.0533). ER = EPR: entanglement and geometric connection may be the same thing. A conjecture, not established.
- **Cao, C., Carroll, S. M. & Michalakis, S. (2017).** "Space from Hilbert space: recovering geometry from bulk entanglement." *Phys. Rev. D* 95, 024031. arXiv: [1606.08444](https://arxiv.org/abs/1606.08444). A reusable algorithm (mutual information, then distance, then embedding) for checking whether a web yields a sensible space.
- **Jacobson, T. (2016).** "Entanglement equilibrium and the Einstein equation." *Phys. Rev. Lett.* 116, 201101. arXiv: [1505.04753](https://arxiv.org/abs/1505.04753). Links gravity's field equation to an entanglement-balance condition.
- **Eisert, J., Cramer, M. & Plenio, M. B. (2010).** "Colloquium: Area laws for the entanglement entropy." *Rev. Mod. Phys.* 82, 277. arXiv: [0808.3773](https://arxiv.org/abs/0808.3773). Explains why physical ground states have local entanglement, which emergent geometry depends on.
- **Page, D. N. (1993).** "Average entropy of a subsystem." *Phys. Rev. Lett.* 71, 1291. arXiv: [gr-qc/9305007](https://arxiv.org/abs/gr-qc/9305007). The volume-law baseline against which geometric entanglement stands out.
- **Islam, R., Ma, R., Preiss, P. M., Tai, M. E., Lukin, A., Rispoli, M. & Greiner, M. (2015).** "Measuring entanglement entropy in a quantum many-body system." *Nature* 528, 77–83. arXiv: [1509.01160](https://arxiv.org/abs/1509.01160) (arXiv title differs). First direct measurement of many-body entanglement entropy and mutual information.
- **Brydges, T., Elben, A., Jurcevic, P., Vermersch, B., Maier, C., Lanyon, B. P., Zoller, P., Blatt, R. & Roos, C. F. (2019).** "Probing Rényi entanglement entropy via randomized measurements." *Science* 364, 260. arXiv: [1806.05747](https://arxiv.org/abs/1806.05747) (arXiv title differs). A scalable method that could supply real data for mutual-information geometry tests.

**Relevance to the-web: supports, and largely anticipates, the hypothesis.** "Space emerges from entanglement" is a serious, active programme, and the-web's core picture tracks Van Raamsdonk and Cao–Carroll–Michalakis closely. Outside AdS/CFT it is still speculative. Only area-law states give a sensible geometry, so a web model must explain why our world is in one. Combining the Cao–Carroll–Michalakis algorithm with simulated or measured entropies gives a concrete testbed for "one web sets both distance and entanglement".

---

## 7. Gravity-mediated entanglement

Two 2017 papers, published back to back in *Physical Review Letters*, proposed a lab test of whether gravity is quantum. Bose et al. imagined two microdiamonds, each in a superposition of two locations and each carrying a spin, interacting only through gravity. Marletto and Vedral gave the general argument: a classical go-between acting locally cannot create entanglement, so if the masses become entangled, gravity must be non-classical. Bose et al. estimated masses of about 10⁻¹⁴ kg, superpositions about 250 µm wide, a closest approach of about 200 µm, and about 2 seconds of undisturbed evolution.

**Status as of late October 2026: no experiment has observed gravitationally induced entanglement.** The smallest source mass whose gravity has been measured is about 90 mg (Westphal et al. 2021), and gravity has been sensed on a 0.4 mg levitated particle (Fuchs et al., *Science Advances* 2024, arXiv: [2303.03545](https://arxiv.org/abs/2303.03545)). The heaviest mechanical objects in clearly quantum states are around 16 µg (Bild et al. 2023), and not in large spatial superpositions. A July 2026 *Physics Today* feature by Aspelmeyer and Carney judges a direct test plausible perhaps within the next couple of decades. Recent milestones are steps toward it, not the result itself. They include a levitated nanosphere entangled with light at room temperature (Florence, *Science*, October 2026) and spin forces moving a centimetre-scale levitated diamond (OIST, *Science Advances*, October 2026). The interpretation is also contested. Aziz and Howl (*Nature* 2025) argued that classical gravity can produce a much weaker entanglement; Marletto, Oppenheim, Vedral and Wilson, and separately Diósi, dispute this. Oppenheim's "postquantum classical gravity" is a consistent theory in which gravity cannot entangle. It instead predicts a testable trade-off between decoherence and spacetime jitter (Oppenheim et al., *Nature Communications* 14, 7910, 2023, arXiv: [2203.01982](https://arxiv.org/abs/2203.01982)).

**Key papers**

- **Bose, S., Mazumdar, A., Morley, G. W., Ulbricht, H., Toroš, M., Paternostro, M., Geraci, A. A., Barker, P. F., Kim, M. S. & Milburn, G. (2017).** "Spin entanglement witness for quantum gravity." *Phys. Rev. Lett.* 119, 240401. arXiv: [1707.06050](https://arxiv.org/abs/1707.06050). The concrete protocol and its demanding parameters.
- **Marletto, C. & Vedral, V. (2017).** "Gravitationally induced entanglement between two massive particles is sufficient evidence of quantum effects in gravity." *Phys. Rev. Lett.* 119, 240402. arXiv: [1707.06036](https://arxiv.org/abs/1707.06036). The general "entangling mediator must be non-classical" argument.
- **Bose, S. et al. (2025).** "Massive quantum systems as interfaces of quantum mechanics and gravity." *Rev. Mod. Phys.* 97, 015003. arXiv: [2311.09218](https://arxiv.org/abs/2311.09218). Current review of the experimental landscape and its obstacles.
- **Westphal, T., Hepach, H., Pfaff, J. & Aspelmeyer, M. (2021).** "Measurement of gravitational coupling between millimetre-sized masses." *Nature* 591, 225–228. arXiv: [2009.09546](https://arxiv.org/abs/2009.09546). Benchmarks the smallest measured gravitational source mass, far above what can yet be put in superposition.
- **Bild, M., Fadel, M., Yang, Y., von Lüpke, U., Martin, P., Bruno, A. & Chu, Y. (2023).** "Schrödinger cat states of a 16-microgram mechanical oscillator." *Science*, DOI 10.1126/science.adf7553. arXiv: [2211.00449](https://arxiv.org/abs/2211.00449). Roughly the current mass frontier for quantum mechanical states.
- **Aziz, J. & Howl, R. (2025).** "Classical theories of gravity produce entanglement." *Nature* 646, 813–817. arXiv: [2510.19714](https://arxiv.org/abs/2510.19714). Contested; if right, only entanglement above some size would point to quantum gravity.
- **Marletto, C., Oppenheim, J., Vedral, V. & Wilson, E. (2025).** "Classical gravity cannot mediate entanglement." arXiv: [2511.07348](https://arxiv.org/abs/2511.07348). Rebuttal of Aziz–Howl. Diósi makes a similar case in "No, classical gravity does not entangle quantized matter fields," arXiv: [2511.00852](https://arxiv.org/abs/2511.00852).
- **Oppenheim, J. (2023).** "A postquantum theory of classical gravity?" *Phys. Rev. X* 13, 041040. arXiv: [1811.03116](https://arxiv.org/abs/1811.03116). The main consistent alternative in which gravity stays classical.
- **Aspelmeyer, M. & Carney, D. (2026).** "The elusive signatures of quantum gravity." *Physics Today* 79(7), July 2026 ([article](https://physicstoday.aip.org/features/the-elusive-signatures-of-quantum-gravity)). No arXiv version. Current expert confirmation that gravitational entanglement has not been seen, with realistic timescales.

**Relevance to the-web: consistent, but not a discriminating test.** If gravity is part of the geometry the web produces, it must be able to carry entanglement. Standard quantum treatments of gravity predict the same, so a positive result would not favour the-web over them. A clean negative result, with decoherence demonstrably controlled, would challenge it and favour classical-gravity models. The test is likely decades away and its interpretation is still disputed, so it should not be this repo's main test.

---

## 8. Older and philosophical ideas

David Bohm's *Wholeness and the Implicate Order* (1980) argued that the separate objects we see (the "explicate order") unfold from a deeper "implicate order" in which everything is enfolded in everything else. He used the analogy of a hologram, where each part of the plate holds information about the whole image. It is philosophy of physics, not a theory with new predictions, and it is separate from Bohm's pilot-wave interpretation. John Wheeler's "it from bit" (1989) proposed that every physical thing ultimately derives from the answers to yes-or-no questions: information comes first and matter is derived. The slogan helped motivate the information-based approaches to spacetime in sections 5 and 6, down to the name "bit threads".

**Key works**

- **Bohm, D. (1980).** *Wholeness and the Implicate Order.* London: Routledge & Kegan Paul. ISBN 0-7100-0366-8. No arXiv version. The best-known earlier statement that separation is secondary to an underlying wholeness, very close in spirit to the-web.
- **Wheeler, J. A. (1989/1990).** "Information, physics, quantum: the search for links." *Proc. 3rd Int. Symp. Foundations of Quantum Mechanics* (Tokyo, 1989); reprinted in W. H. Zurek (ed.), *Complexity, Entropy and the Physics of Information* (Addison-Wesley, 1990). No arXiv version. The origin of "it from bit", the intuition that information comes before geometry.

**Relevance to the-web: historical precedent only.** These works show the intuition is old and respected. Neither makes quantitative predictions that could be checked against the web.

---

## 9. Quantum hardware and "limited entanglement"

The-web's v0.1 predicted an entanglement-specific error floor: if total capacity were smaller than quantum mechanics allows, heavily entangled computations should fail more often than their parts predict. Google's 2019 "quantum supremacy" experiment ran random circuits on 53 qubits, 20 cycles deep. Such circuits produce near-maximal, volume-law entanglement. The whole-circuit fidelity was small but clearly measurable (above 0.1%). Crucially, it was well predicted by simply multiplying the separately measured fidelities of the individual gates and readouts. Errors acted like independent local events, with no extra penalty for the entanglement. Kalai, Shoham and Voelkmann dispute this agreement as statistically too good to be natural, though their critique does not point to an entanglement penalty either. Google's "Willow" chip (105 qubits) ran surface-code error correction at sizes 3×3, 5×5 and 7×7. Each step up cut the logical error rate by about 2.14×, and the largest logical qubit outlived the best physical qubit by about 2.4×. A separate long-run error floor near 10⁻¹⁰ was traced to rare correlated error bursts, not to entanglement.

In 2025 IBM researchers certified a 120-qubit GHZ ("cat") state at fidelity 0.56 ± 0.03, above the 0.5 threshold for genuine 120-party entanglement, using error detection that kept 28% of runs. A GHZ state has exactly 1 bit of entanglement entropy across *any* split into two parts. It is enormous in the number of parties involved and tiny in capacity across any cut, the opposite of a random-circuit state. As computed in section 4, it also breaks monogamy of mutual information.

**Key papers**

- **Arute, F. et al. (2019).** "Quantum supremacy using a programmable superconducting processor." *Nature* 574, 505–510. arXiv: [1910.11333](https://arxiv.org/abs/1910.11333) (the arXiv entry holds the supplementary information, which contains the error-model analysis). Its finding that fidelity follows the product of component fidelities is the strongest existing constraint on an entanglement penalty.
- **Kalai, G., Shoham, T. & Voelkmann, C. (2025).** "Further statistical study of NISQ experiments." arXiv: [2512.10722](https://arxiv.org/abs/2512.10722). A sceptical reanalysis; a reason not to treat the 2019 constraint as beyond question.
- **Google Quantum AI and Collaborators (2025).** "Quantum error correction below the surface code threshold." *Nature* 638, 920–926. arXiv: [2408.13687](https://arxiv.org/abs/2408.13687). Logical errors fall as the entangled code grows, the opposite of a capacity ceiling at this scale.
- **Javadi-Abhari, A., Martiel, S., Seif, A., Takita, M. & Wei, K. X. (2025).** "Big cats: entanglement in 120 qubits and beyond." arXiv: [2510.09520](https://arxiv.org/abs/2510.09520) (preprint). The largest certified GHZ state, and a direct counterexample to strict pairwise min-cut models.

**Relevance to the-web: constrains v0.1, challenges a strict min-cut web.** No entanglement-specific error floor has been seen. Any capacity ceiling must lie above 53-qubit volume-law states, 120-qubit GHZ states and the scales where surface-code errors still fall. Because certified 120-party GHZ states exist, a web in which every entanglement pattern is a pairwise min-cut is ruled out for general states. It must allow multi-way (hyperedge) links or apply only to special, geometric states.

---

## 10. Verification notes

Everything above was checked in October 2026. Details that could **not** be fully confirmed:

- **Toner & Verstraete (2006), Methot & Scarani (2006), Oas & de Barros (c. 2015), Ji et al. (2020):** arXiv records confirmed; journal versions not confirmed, so only arXiv IDs are given.
- **Freedman & Headrick (2017), Bild et al. (2023), Fuchs et al. (2024):** journal and DOI confirmed; volume and page numbers not confirmed. **Cui et al. (2016):** article number not confirmed.
- **Navascués & Wunderlich:** arXiv gives *Proc. R. Soc. A* 466, 881–890 with year 2009; the printed volume may be dated 2010.
- **Dhar et al. (2017):** arXiv record and year confirmed; the book it appears in is inferred from its Springer DOI prefix.
- **Wheeler (1989/1990):** title, venue and reprint confirmed; page numbers omitted because sources disagree.
- **Popescu & Rohrlich (1994):** confirmed through a university repository; not on arXiv (the linked arXiv paper is a related 1995 follow-up).
- **Google 2019:** the product-of-fidelities finding was confirmed from the published paper's text; arXiv 1910.11333 is the supplementary information.
- **Gravity experiment status:** "not yet observed" rests on the July 2026 *Physics Today* feature, a 2026 levitated-mirror conference talk, news releases from April and October 2026, and 2026 arXiv papers, all describing it as a future goal. Nothing found up to 28 October 2026 reports an observation.
