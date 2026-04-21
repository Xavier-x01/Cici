# Synthesis: The Unified Architecture Behind rq-001, rq-002, rq-003

**Status:** prepared-context/synthesis — revisable, not governed  
**Tier:** Primarily [C] synthesis from [B] evidence. All claims annotated inline.  
**Date:** 2026-04-21  
**Author:** Claude Code (claude/enhance-cici-features-1UZZf)  
**Promotion path:** Needs Xavier verification → Tier B. Then proposal under a new surface if governed.

---

## Summary [C]

Xavier's three research questions are not independent lines of inquiry. They describe three interlocking components of a single architecture: an AI system that can *execute long-horizon goals* (rq-003), *know when computation is worthwhile* (rq-002), and *modify its own architecture without human supervision* (rq-001). Each question's open frontier converges on the same mechanism not yet demonstrated in the literature: **reliable in-context self-modeling without training supervision**.

---

## The Three-Layer Architecture [C]

```
┌────────────────────────────────────────────────────────────────┐
│                  SELF-MODIFICATION LAYER  (rq-001)             │
│  Autonomously generate → verify → integrate architectural       │
│  optimizations. Requires: a world model of the model itself.   │
└───────────────────────────┬────────────────────────────────────┘
                            │ feeds back verified improvements
                            ▼
┌────────────────────────────────────────────────────────────────┐
│                  META-COGNITIVE LAYER  (rq-002)                │
│  Inference-to-Utility optimization. Decides: when to simulate, │
│  when to act, when to invoke deeper reasoning.                 │
└───────────────────────────┬────────────────────────────────────┘
                            │ allocates compute budget to
                            ▼
┌────────────────────────────────────────────────────────────────┐
│                  EXECUTION LAYER  (rq-003)                     │
│  Decompose abstract goals → ground to executable actions →     │
│  maintain consistent world model across execution horizon.     │
└────────────────────────────────────────────────────────────────┘
```

**Dependency structure [C]:**

- The **execution layer** (rq-003) requires a world model to avoid greedy myopic commitment — step-wise reasoning induces early commitments that compound into failure [B: arxiv:2601.22311].
- The **meta-cognitive layer** (rq-002) determines *when* the execution layer should invoke expensive world model simulation — this is the precise bottleneck identified empirically in [B: arxiv:2601.03905]: "agents struggle to decide when to simulate, how to interpret predicted outcomes, and how to integrate foresight."
- The **self-modification layer** (rq-001) applies the execution layer's own mechanism back to the system: verifying whether an architectural change improves the model *requires simulating its future behavior* — which is a world model of the model itself [C].

---

## The Convergent Open Gap

Each question reaches a different surface of the same wall:

| Question | Specific open frontier | Shared form |
|---|---|---|
| rq-001 | Verifying architectural changes without human-curated benchmarks [B: arxiv:2601.03905, DGM safety note] | Accurate self-model of the model's own behavior, constructed in context |
| rq-002 | Emergent cost-awareness at inference time without training supervision [B: arxiv:2602.10329 partial result] | Accurate self-model of the model's own computational costs, in context |
| rq-003 | Dynamic world model construction and update without domain-specific training [B: arxiv:2601.03905] | Accurate model of the environment, constructed and revised in context |

All three require an agent to build and maintain an accurate model of some system — its own architecture, its own costs, or the external environment — **in context, without being explicitly trained to do so**.

---

## Proposed Name: In-Context Self-Modeling (ISM) [C]

ISM is the capability of building and updating an accurate model of a target system from contextual evidence at inference time, without a dedicated training signal for that target.

Three sub-variants, one per research question:

| Variant | Target system | Required for |
|---|---|---|
| ISM-arch | The model's own architecture and weights | rq-001 verification without benchmarks |
| ISM-cost | The model's own computational footprint | rq-002 I/U optimization without cost supervision |
| ISM-env | The external environment and its dynamics | rq-003 consistent world model without domain training |

**Key distinction from existing work [C]:** Current approaches train a separate module to perform one of these functions. ISM proposes that a sufficiently capable base model should be able to perform all three *in context* — the same way it can reason about a novel domain without being trained on it. The hypothesis is that ISM is a *general capability* that transfers across variants, not three separate engineering problems.

---

## Literature Support for ISM as a Coherent Research Target [B]

Existing work establishes the trajectory without closing it:

| Paper | Relevance to ISM |
|---|---|
| [arxiv:2505.13763](https://arxiv.org/abs/2505.13763) | Models can detect and report changes in their own internal activations — primitive ISM-arch/cost evidence |
| [arxiv:2509.21545](https://arxiv.org/abs/2509.21545) (ICLR 2026) | Limited but real metacognitive abilities; resolution improves with scale — ISM-cost partially present |
| [arxiv:2602.10329](https://arxiv.org/abs/2602.10329) | Resource-rationality can partially emerge without explicit cost supervision — ISM-cost emerging |
| [arxiv:2505.15182](https://arxiv.org/abs/2505.15182) (ReflAct) | Explicit in-context belief state maintenance improves world model consistency +27.7% — ISM-env via structured prompting |
| [arxiv:2601.03822](https://arxiv.org/abs/2601.03822) (ROI-Reasoning) | Predicts cost AND utility before generating, but requires training — ISM-cost achieved with supervision |

None demonstrate full ISM. Together they show each sub-variant is partially accessible, suggesting the capability exists but lacks a mechanism to activate it reliably across all three variants in context.

---

## Research Directions Implied [C]

**1. ISM probe experiment**
Design a controlled experiment distinguishing ISM from calibrated confidence. Provide a model with partial information about its own token usage or generation statistics mid-sequence; measure whether it adapts subsequent behavior in a principled way without being trained to do so. If it does, that is ISM-cost evidence.

**2. Cross-variant transfer test**
Train a model for ISM-env (world model consistency, rq-003). Test zero-shot whether it also shows ISM-cost improvement (rq-002) without explicit cost training. If the same underlying mechanism generalizes across variants, that supports ISM as a unified capability class.

**3. Benchmark-free verification via I/U**
For rq-001: instead of human-curated benchmarks as the verification signal, use the I/U ratio itself as the ground truth — does an architectural modification improve the average I/U ratio across a diverse task distribution? This uses rq-002's solution to close rq-001's open gap, and is the cleanest test of the three-layer dependency.

**4. Theoretical formalization**
Define ISM formally as a capability class: given a model M, a target system S, and context C, ISM(M, S, C) is the quality of M's model of S constructed from C alone. Characterize what properties of S make ISM tractable. The three questions correspond to S ∈ {model architecture, computational cost, external environment}.

---

## Tensions [B/C]

**Tension 1 — Artificial unification [C]:** The convergent gap framing is elegant but may be forcing three distinct problems into a single mold. The alternative: rq-001/002/003 are coincidentally related but do not share a deep mechanism. ISM may be a family resemblance, not a single capability. *Resolution path:* Formalize ISM and test whether cross-variant transfer exists (research direction 2 above).

**Tension 2 — Scale requirement [B/C]:** arxiv:2509.21545 (ICLR 2026) finds metacognitive abilities are real but limited in resolution at current scale. If ISM requires scale we don't have, the research program may be premature for current models. *Resolution path:* Determine whether the ICLR 2026 limitation applies to all three ISM variants or primarily to ISM-cost.

**Tension 3 — Goodhart risk [B]:** For rq-001, using I/U ratio as the verification signal (research direction 3) introduces a new Goodharting risk: an architectural change could optimize the I/U metric without genuinely improving the model. [B: DGM safety note in arxiv:2505.22954]. *Resolution path:* Requires a diverse task distribution broad enough that Goodharting it is equivalent to actually improving the model.

---

## Promotion Path

**To Tier B:** Requires finding a theoretical framework in the literature that subsumes ISM (e.g., formal connections to bounded rationality, resource-rational analysis, or Bayesian meta-learning) — or conducting the cross-variant transfer test (research direction 2).

**To governed-state:** Requires a proposal under a new `research-synthesis/` surface and Xavier's approval. The synthesis would need at least one ISM variant confirmed to Tier B.

**References to governed-state artifacts:**
- `users/cici/governed-state/research-methodology/open-questions.json` — rq-001, rq-002, rq-003
- `users/cici/governed-state/knowledge-graph/concepts.json` — world-model, goal-decomposition, inference-to-utility-ratio, theory-of-mind-ai, autonomous-verification, architectural-optimization
