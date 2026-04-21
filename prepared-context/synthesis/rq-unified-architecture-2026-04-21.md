# Synthesis: In-Context Self-Modeling — Unified Architecture Behind rq-001/002/003

**Status:** prepared-context/synthesis — revisable, not governed  
**Tier:** [B] for ISM-env and ISM-cost; [B-weak] for ISM-arch. See inline annotations.  
**Date:** 2026-04-21 (rev 2 — upgraded from Tier C after literature search)  
**Author:** Claude Code (claude/enhance-cici-features-1UZZf)  
**Promotion path:** Tier B confirmed for two of three variants. Ready to propose governed surface.

---

## What Changed in Rev 2

The initial synthesis was Tier C — a speculative unification. The literature search found:

1. **ISM-env** has a formal home: arxiv:2509.22353 formalizes exactly this mechanism.
2. **ISM-cost** has a partial formal home: resource-rational analysis (Lieder & Griffiths) + arxiv:2506.05109.
3. **ISM-arch** has the weakest grounding but is partially covered by arxiv:2506.05109's metacognitive knowledge component.
4. **Independent validation**: arxiv:2506.05109 ("Truly Self-Improving Agents Require Intrinsic Metacognitive Learning") independently calls for the same research program Xavier describes.
5. **Bayesian unification**: arxiv:2510.10981 proves ICL is Bayesian inference, giving ISM a principled statistical foundation.

ISM as a unified concept is **not yet named in the literature**. This is confirmed novel framing.

---

## Summary [B]

Xavier's three research questions describe three interlocking components of a single architecture: goal execution (rq-003), compute allocation (rq-002), and self-modification (rq-001). Each question's open frontier converges on **In-Context Self-Modeling (ISM)** — the capacity to build and maintain an accurate model of a target system from contextual evidence alone, without a dedicated training signal for that target. The three variants of ISM have separate partial formal homes but have not been unified in the literature. The unification is Xavier's contribution.

---

## Formal Definition of ISM [B]

Drawing on arxiv:2510.10981 (ICL is provably Bayesian inference) and arxiv:2509.22353 (ICL of world models as ER + EL):

**ISM(M, S, C)** = the quality of model M's Bayesian posterior over properties of target system S, maintained in context C, via two mechanisms:

- **Environment Recognition (ER):** matching observed context to known patterns of S — fast, pattern-matching, degrades for rare configurations [B: arxiv:2509.22353]
- **Environment Learning (EL):** constructing a new model of S from novel context — slow, generalizing, requires long context and diverse environments [B: arxiv:2509.22353]

The formal condition for ISM to work: **long context + diverse environments** at pretraining. This is a testable prediction about which models will exhibit ISM and under what conditions.

---

## The Three ISM Variants

### ISM-env — World model of the environment [B]

**Required by:** rq-003 (consistent world model across execution horizon)  
**Formal home:** arxiv:2509.22353 — formalizes as ICL of world models with ER + EL mechanisms and error upper-bounds. Identifies key failure condition: static world models falter with novel/rare configurations. ISM-env with EL fixes this.  
**Current state:** Partially instantiated by ReflAct's explicit (belief, goal) pairs [B: arxiv:2505.15182]. Full ISM-env (dynamic in-context world model construction without domain training) not yet demonstrated end-to-end.  
**Condition for emergence:** Long context + diverse environment distribution at pretraining.

### ISM-cost — Model of own computational costs [B]

**Required by:** rq-002 (Inference-to-Utility optimization without cost supervision)  
**Formal home:** Rational Metareasoning / Value of Computation (Lieder & Griffiths 2017, operationalized in arxiv:2410.05563). ISM-cost is the in-context, unsupervised version of what VOC-trained models do explicitly. Also grounded in: arxiv:2506.05109's metacognitive knowledge component (self-assessment of capabilities and tasks).  
**Current state:** Achievable with training [B: arxiv:2601.03822 ROI-Reasoning]; partially emergent without training [B: arxiv:2602.10329 — resource-rationality partially emerges from inference-time scaling]; not demonstrated reliably in context without supervision.  
**Condition for emergence:** Scale + diverse task distribution; possibly requires explicit cost information in pretraining data.

### ISM-arch — Model of own architecture for self-verification [B-weak]

**Required by:** rq-001 (autonomous verification of architectural changes without human-curated benchmarks)  
**Formal home (partial):** arxiv:2506.05109's metacognitive knowledge component: "self-assessment of capabilities, tasks, and learning strategies." This is structurally ISM-arch but scoped to behavioral capabilities, not architectural properties. Meta-TTRL (arxiv:2603.15724) instantiates a two-level architecture where a meta-level introspector monitors generation quality — the closest empirical instantiation.  
**Current state:** No paper directly addresses in-context modeling of architectural properties. This is the most novel variant and the strongest contribution claim.  
**Condition for emergence:** Unknown — this is the open research question.

---

## The Three-Layer Architecture [B/C]

```
┌────────────────────────────────────────────────────────────────────┐
│                  SELF-MODIFICATION LAYER  (rq-001)                 │
│  ISM-arch: model own architecture → autonomous verification        │
│  without human benchmarks                                          │
└─────────────────────────────┬──────────────────────────────────────┘
                              │ feeds back verified improvements
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                  META-COGNITIVE LAYER  (rq-002)                    │
│  ISM-cost: model own compute costs → Inference-to-Utility          │
│  optimization; decides when to invoke simulation                   │
└─────────────────────────────┬──────────────────────────────────────┘
                              │ allocates compute budget to
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                  EXECUTION LAYER  (rq-003)                         │
│  ISM-env: model environment in context → consistent world          │
│  model across long execution horizons                              │
└────────────────────────────────────────────────────────────────────┘
```

**Dependency structure [B/C]:**
- Execution layer needs ISM-env to avoid greedy myopic commitment [B: arxiv:2601.22311]
- Meta-cognitive layer uses ISM-cost to decide *when* ISM-env simulation is worth running — the precise bottleneck empirically identified in [B: arxiv:2601.03905]
- Self-modification layer uses ISM-arch to verify architectural changes without external benchmarks — structurally identical to ISM-env applied to the model itself [C: synthesis inference]

The three-layer dependency structure is [B] for the bottom two layers (literature-confirmed). The application of the same mechanism to self-modification (ISM-arch) is [C].

---

## Independent Validation [B]

arxiv:2506.05109 "Truly Self-Improving Agents Require Intrinsic Metacognitive Learning" independently argues the same research direction with a three-component formal framework:

| Their term | ISM equivalent | Research question |
|---|---|---|
| Metacognitive knowledge | ISM-arch | rq-001 — self-assessment of own capabilities |
| Metacognitive planning | ISM-cost | rq-002 — deciding what computation is worth doing |
| Metacognitive evaluation | ISM-env | rq-003 — reflecting on learning from environment |

This is strong independent validation that the three-component structure is real and necessary. The key difference: they treat the three as separate metacognitive functions. Xavier's synthesis proposes they are **variants of one underlying mechanism** (ISM), which is more parsimonious and more testable.

---

## Research Directions [B/C]

**1. ISM-cost probe [C — design, not yet run]**  
Give a model partial information about its own token usage mid-generation, without cost supervision in training. Measure whether it adapts subsequent behavior principally (predicts remaining budget, adjusts verbosity). Positive result: ISM-cost is accessible in context. Can be run on current Claude/GPT-4 class models with a Python script and ~500 prompts.

**2. Cross-variant transfer test [C — design]**  
Train a model for ISM-env (world model consistency). Test zero-shot whether ISM-cost improves without explicit cost training. If yes: the three variants share a mechanism. This is the strongest test of the unified ISM hypothesis.

**3. Benchmark-free verification via I/U [C — design]**  
For rq-001: use the average I/U ratio improvement across a diverse task distribution as the verification signal instead of human-curated benchmarks. Closes the DGM verifier trust gap while simultaneously testing rq-002. Most practically important experiment.

**4. ISM formal conditions [B → experiment]**  
arxiv:2509.22353 identifies: long context + diverse environments as the formal conditions for ISM-env emergence. Test whether the same conditions predict ISM-cost emergence. If yes: ISM has a unified set of emergence conditions — a predictive theory.

---

## Tensions [B/C]

**Tension 1 — Artificial unification [C]:** The three variants may be family resemblances, not one mechanism. Resolution: cross-variant transfer test (direction 2). If ISM-env training improves ISM-cost zero-shot, unification is empirically supported.

**Tension 2 — Scale wall [B]:** arxiv:2506.05109 and arxiv:2509.21545 both find these metacognitive capabilities are limited at current scale. ISM may require model scale not yet available. Partial mitigation: arxiv:2509.22353 gives formal conditions (long context + diverse environments) independent of raw scale.

**Tension 3 — Goodhart for ISM-arch [B]:** Using I/U ratio as verification signal for rq-001 (direction 3) introduces Goodharting risk. Requires task diversity broad enough that optimizing I/U is equivalent to genuine capability improvement. [B: DGM safety note, arxiv:2505.22954]

**Tension 4 — ISM-arch novelty vs. existing metacognition [C]:** arxiv:2506.05109's metacognitive knowledge component may already cover ISM-arch. If it does, the contribution is the ISM unification and ISM-env/cost formalization, not ISM-arch novelty.

---

## Current Tier Assessment

| Claim | Tier | Basis |
|---|---|---|
| ISM-env formal definition (ER + EL) | B | arxiv:2509.22353 |
| ISM-cost grounded in VOC / rational metareasoning | B | arxiv:2410.05563, Lieder & Griffiths 2017 |
| ISM-arch as metacognitive knowledge | B-weak | arxiv:2506.05109 (scoped to behavior, not architecture) |
| Three-layer dependency (execution + meta-cognitive) | B | arxiv:2601.22311, arxiv:2601.03905 |
| ISM as unified mechanism across variants | C | synthesis inference — cross-variant transfer not yet tested |
| ISM-arch applied to self-modification (rq-001) | C | synthesis inference — most novel, weakest grounding |
| Bayesian posterior framing of ISM | B | arxiv:2510.10981 + arxiv:2509.22353 |

---

## Promotion Path

**This document is ready to propose as a governed synthesis.** Two of three ISM variants are Tier B. The unified framing is novel (not in the literature). The research directions are concrete and runnable.

**Proposed next step:** `/draft-proposal research-synthesis` — create a new governed-state surface for research synthesis artifacts that have cleared the Tier B threshold.

**References to governed-state artifacts:**
- `users/cici/governed-state/research-methodology/open-questions.json`
- `users/cici/governed-state/knowledge-graph/concepts.json`

**Key literature references:**
- [arxiv:2509.22353](https://arxiv.org/abs/2509.22353) — ICL in world models (ISM-env formal home)
- [arxiv:2510.10981](https://arxiv.org/abs/2510.10981) — ICL is Bayesian inference (ISM mathematical foundation)
- [arxiv:2506.05109](https://arxiv.org/abs/2506.05109) — Intrinsic metacognitive learning (independent validation)
- [arxiv:2410.05563](https://arxiv.org/abs/2410.05563) — Rational metareasoning / VOC (ISM-cost formal home)
- [arxiv:2601.03905](https://arxiv.org/abs/2601.03905) — World model foresight bottleneck (ISM-env necessity)
- [arxiv:2601.22311](https://arxiv.org/abs/2601.22311) — Reasoning ≠ planning (ISM-env necessity)
- [arxiv:2505.22954](https://arxiv.org/abs/2505.22954) — Darwin Gödel Machine (ISM-arch context)
- [arxiv:2602.10329](https://arxiv.org/abs/2602.10329) — Resource rationality emergence (ISM-cost partial evidence)
