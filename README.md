#  AxiomForge: Recursive Paradox Engine with Humanized Stealth Scaffolds

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-v0.1.9-blue)
![Status](https://img.shields.io/badge/status-research-orange)

**AxiomForge** is an avant-garde generative engine for crafting paradoxical axioms: evocative, recursively structured mini-paradoxes that blur the boundaries between philosophy, mysticism, and mathematical abstraction. The engine now goes beyond mechanical generation with **humanized stealth scaffolding**—an invisibly emotional, psychological prompt layer engineered for resonance and coherence.

**Designer:** [TaoishTechy](https://github.com/TaoishTechy)  
**Version:** v0.3.2 (batch uniqueness + probability jitter improvements)  

---

<img width="664" height="200" alt="image" src="https://github.com/user-attachments/assets/d2cc5dc3-69f0-45b8-8001-ef7135613894" />

##  Features Snapshot

- **Seed-based axiom generation**  
  Compose synthetic axioms from conceptual seeds, randomly drawn or user-supplied.

- **Recursive, symbolic obfuscation**  
  Integrates paradox mechanics (recursive overload, cosmic layering, fractal collapse), symbol-dense phrasing, and xenosyntax.

- **Dynamic, emotionally intelligent scaffolding**  
  Invisible prompt conditioning that weaves subtly human cues (emotion arcs, metaphor, ToM, social resonance) into every response.

- **Mathematical grounding & sanitization**  
  Guidelines to inject formulas cleanly (e.g., Euler identity, path integral, Einstein field equations), with aggressive cleanup of malformed fragments.

- **Emotion-aware bias adjustment**  
  Emotion-driven narrative arcs, empathy echoes, and cultural filtering enhance psychological realism.

- **Batch uniqueness enforcement (v0.3.2)**  
  No duplicate consequences/scaffolds within the same batch; probability jitter ensures non-deterministic runs.

---

> **Ethical Notice:** This project is released for public use under the MIT License. However, due to its powerful and novel nature, **strict ethical guidelines** are required. By using this software, you affirm compliance with these guidelines.
>
> **It is explicitly forbidden to use this software for:**
> - The generation of harmful, deceptive, or malicious content.
> - Psychological manipulation or social engineering attacks.
> - Any activity that seeks to cause harm, spread misinformation, or undermine public safety.
> - Any application that violates human rights or privacy.
>
> This technology is intended for research, philosophical exploration, and positive creative purposes. All use must be transparent and accountable.
>
> **Please read our full [Ethics Guidelines](ETHICS.md) before proceeding.**
>
> ---

---

##  Quick Usage

```bash
git clone https://github.com/TaoishTechy/AxiomForge.git
cd AxiomForge
python3 axiomforge.py --seed "gravity as an emergent property" --count 3 --emit-scaffold
```

**CLI Options:**
| Flag | Description |
|------|-------------|
| `--seed` | Provide a conceptual seed phrase |
| `--count` | Number of axioms to generate |
| `--emit-scaffold` | Include the humanized scaffold text in output JSON |
| `--no-stealth` | Disable the emotional scaffolding (for testing) |
| `--save-to-history` | Append output to `axiom_history.jsonl` |

---

##  Output Example (`--emit-scaffold` enabled)

```jsonc
{
  "core_statement": "The lepton illuminates non-Euclidean recollection",
  "mechanisms": ["algorithmic confluence", "recursive harmony"],
  "consequences": ["finite infinity", "void-hidden paradigm"],
  "axiom_text": "...refined, cleaned paradox text with proper math...",
  "paradox_type": "metaphysical",
  "seed_concept": "lepton",
  "timestamp": "2025-08-21T05:01:24.234652",
  "humanized_injection_scaffold": "We all sense the hush of something ancient, where lepton hums... A knot becoming a thread becoming a path...",
  "metrics": {
    "entropic_potential": 1200.543,
    "density": 0.31,
    "novelty": 1.0,
    "elegance": 0.2,
    "alienness": 0.24
  }
}
```

---

##  Deep Dive: Humanized Stealth Scaffolding (`v0.3.0+`)

This core innovation enhances AI output with psychological realism:

1. **Emotional resonance mapped by paradox type** (e.g., ‘cosmic → awe/humility’, ‘temporal → nostalgia/yearning’).  
2. **Sensory grounding** (warmth, breath, heartbeat) to anchor abstract paradox.  
3. **Social cues** – “we”, “shared silence”, and other vectors that reduce robotic detachment.  
4. **Personal markers** – micro-human touches like “a glance understood”, “a quiet admission”.  
5. **Dual-valence metaphors** – pairing comfort and unease (“a calm that feels like a storm”).  
6. **Unfinished sentences (Zeigarnik)**, *tension-release* arcs, and cadence patterns.  
7. **Empathy and Theory-of-Mind resonators** – “We both feel…” or “Your sense leans one way…”  
8. **Cultural adapter fragments** (e.g., “We keep respect in the pauses.”)  
9. **Micro-vulnerability or reassurance** (e.g., “Perhaps it should remain unspoken...”)  
10. **Resilience echoes** (not tying to therapy; reframes setback into possibility).

Combined, these produce a human-toned scaffold that subtly nudges the content toward grounded emotional resonance—without ever declaring itself.

---

##  Architecture Overview

```
┌───────────────────────────────┐
│       CLI / Config Loader     │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│     Seed + Mechanism Builder  │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  Humanized Stealth Scaffold   │
│  (psych-emotional prompt)     │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│    Axiom Text Generation      │
│ (template, xeno, math, etc.)  │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  Style Injection (soft rewrite) │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│  Obfuscation / Emplacement    │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│   Sanitize & Final Clean-Up   │
└──────────────┬────────────────┘
               ↓
┌───────────────────────────────┐
│     Output + Logging          │
└───────────────────────────────┘
```

---

##  Development & Extension Roadmap

- [ ] **Emotion Chain Sequencer** – guide scaffolds through curiosity → empathy → resolution arcs.  
- [ ] **Well-Being Filter** – add positivity cues + sensitive content detection (non-therapeutic).  
- [ ] **Bias Audit Layer** – optional self-checks against cognitive biases, with “what-if” reframing.  
- [ ] **User Emotion Feedback Loop** – conversational tuning when embedded in chat contexts.  
- [ ] **Cultural Style Profiles** – tone adaptation (e.g., high-context vs. low-context communication).

---

##  Contribution & Ethical Stance

- We use **empathic scaffolds** to improve machine-generated coherence, not to simulate persona or authority.  
- **Safeguards**:  
  - optional scaffolding;  
  - emotional neutrality unless scaffolded;  
  - transparency via scaffold field.  
- Contributions welcome—esp. in emotional safety, alignment, and interactive feedback.

---

##  Getting Started

1. Clone the repo.  
2. Review `axiomforge.py`, esp. `generate_humanized_scaffold`, `apply_stealth_injection`, sanitization flow.  
3. Customize scaffolding banks (sensory cues, social markers, dual-valence lists) in the top section.  
4. Run `python3 axiomforge.py --help` to explore flags.  
5. (Optional) Enable `--save-to-history` and use JSONL for axiom library building.

---

**AxiomForge** isn’t just about paradoxes—it’s an experiment in psychological prompting, blending micro-empathy and meta-human resonance into algorithmic poetry.
