# AxiomForge — Recursive Paradox Engine with Humanized Stealth Scaffolds

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-v0.4.7-blue)
![Status](https://img.shields.io/badge/status-open--research-orange)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Determinism](https://img.shields.io/badge/deterministic--runs-seeded-success)

**AxiomForge** is a compositional idea engine for forging **axioms**—compact, evocative, paradox-aligned statements with attached mechanisms, math, consequences, and humanized “stealth scaffolds”. It blends curated paradox banks, mechanism/concept lexica, type-conditioned equation pools, tone adapters, and post-emit sanitizers to produce **coherent, math-tinted micro-theories** suitable for worldbuilding, speculative research, and LLM cognition testing.

**Designer:** [TaoishTechy](https://github.com/TaoishTechy)  
**Latest:** **v0.4.7** (stability + alignment release)  
**Also included:** legacy **v0.3.7** (“god-tier” pass) for power users and A/B baselines.

---

## Table of Contents
- [Why AxiomForge](#why-axiomforge)
- [What’s New in v0.4.7](#whats-new-in-v047)
- [Feature Matrix](#feature-matrix)
- [Quick Start](#quick-start)
- [CLI Reference](#cli-reference)
- [Repository Layout & Data Banks](#repository-layout--data-banks)
- [Output Schema](#output-schema)
- [Determinism & Time](#determinism--time)
- [Validation, Hygiene & Safety](#validation-hygiene--safety)
- [Extending the Engine](#extending-the-engine)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [Ethics](#ethics)
- [Contributing](#contributing)
- [License](#license)
- [Citing](#citing)
- [Changelog](#changelog)

---

## Why AxiomForge
Traditional text generators produce prose. **AxiomForge** produces **structured paradox artifacts**—each with:
- a **core statement** (poetic, compact),
- a small set of **mechanisms** (conceptual forces or motifs),
- a paradox **type** (entropic / temporal / cosmic / metaphysical / linguistic / causal-loop),
- a **math hook** (equation or variational form),
- **consequences** (one-line implication),
- and an optional **humanized stealth scaffold** (emotional micro-prompt that quietly shapes tone).

This makes AxiomForge useful as:
- a **creative cognition accelerator** (worldbuilding, speculative design, ARG puzzles, narrative research);
- a **cognition stress-tester** for LLMs/agents (self-reference, consistency, math-type alignment);
- a **teaching instrument** (philosophy of logic, foundations, meta-physics with math-adjacent anchors).

---

## What’s New in v0.4.7
**Stability & Alignment Release**

- **Template Corruption Kill-Switch** — hard **post-emit sanitizer** that removes residual placeholders (`[CORE_STATEMENT]`, `[MECHANISMS]`, `[MATH]`, `[CONSEQUENCES]`) and stray template clause labels.
- **Concept-Alignment Scoring** — seed-aware vector scoring of mechanisms; low-alignment generations are rejected/resampled; fidelity now reflects alignment.
- **Equation Whitelists by Paradox Type** — temporal/cosmic/linguistic/etc. pull from appropriate math pools; **triangulation** nudges equations to match mechanisms (e.g., holography → `S ≤ A/4`, attention/continuity → `∇_t ρ + ∇·J = 0`).
- **Seed-Aware Suffixing** — Dark Forest avoids “broadcast”; uses `— under hiding/masking/jamming/silence`. Nested Realities prefers boundary/frame suffixes; Silent God prefers silence/final-boundary.
- **Light “Transcendent Hooks”** — scaffolds for *Consciousness Origami*, *Temporal Echo*, and *Qualia Density* metrics (opt-in, minimal overhead).
- **Metrics Tightening** — adds `qualia_density` and more meaningful `fidelity_breakdown` (alignment / resonance / novelty×density / archetypal fit).

> Note: If you see a Python warning about `datetime.utcnow()` in older scripts, see **[Determinism & Time](#determinism--time)** for the one-line fix.

---

## Feature Matrix
| Capability | v0.3.7 (legacy) | v0.4.7 (current) |
|---|---|---|
| Seed-based axiom generation | ✅ | ✅ |
| Tone control (poetic/plain/academic/oracular) | ✅ | ✅ |
| Batch uniqueness (no duplicate cores) | ✅ | ✅ (stronger) |
| Self-reference modes (binary/meta/field) | ✅ | ✅ |
| Humanized stealth scaffolds | ✅ | ✅ (seed-aware) |
| Math injection (equation pools) | ✅ | ✅ + **type whitelist** |
| Post-emit sanitization (placeholders) | ⚠️ partial | **✅ hard final pass** |
| Mechanism pool hygiene (drop single-letter artifacts) | ⚠️ | **✅** |
| Concept alignment scoring | — | **✅** |
| Equation↔Mechanism triangulation | — | **✅** |
| Expanded metrics & qualia density | ⚠️ | **✅** |
| Eval-ready JSON schema stability | ⚠️ | **✅** |

---

## Quick Start

```bash
# Clone
git clone https://github.com/TaoishTechy/AxiomForge.git
cd AxiomForge

# Run the latest engine (stdlib only)
python3 axiomforge_0.4.7.py --seed "Dark Forest Theory" --count 6 --tone poetic --rng 1337 --emit-scaffold

# Other seeds
python3 axiomforge_0.4.7.py --seed "Nested Realities" --count 6 --rng 20250926
python3 axiomforge_0.4.7.py --seed "The Silent God" --count 8 --rng 42 --emit-scaffold
```

**Legacy (A/B baselines):**
```bash
python3 axiomforge_0.3.7.py --seed "Dark Forest Theory" --count 6 --tone poetic --rng 1337 --emit-scaffold
```

> Tip: Use `--rng` for full determinism; omit it for organic variety.

---

## CLI Reference

### `axiomforge_0.4.7.py`
| Flag | Type | Default | Description |
|---|---|---:|---|
| `--seed` | str | — | Seed concept/title (e.g., “Dark Forest Theory”) |
| `--count` | int | `6` | Number of axioms to emit |
| `--tone` | str | `poetic` | `poetic` \| `plain` \| `academic` \| `oracular` |
| `--rng` | int | — | Deterministic RNG seed |
| `--emit-scaffold` | flag | `False` | Include `humanized_injection_scaffold` in JSON |

### `axiomforge_0.3.7.py` (legacy)
| Flag | Type | Default | Description |
|---|---|---:|---|
| `--seed` / `--seedfile` | str | — | Single seed or file (one per line) |
| `--count` | int | `12` | Number of axioms |
| `--tone` | str | `poetic` | `poetic` \| `plain` \| `academic` \| `oracular` |
| `--rng` | int | — | Deterministic seed |
| `--max-mech` | int | `3` | Max mechanisms per axiom |
| `--allow-duplicates` | flag | `False` | Allow duplicate core statements |
| `--selfref-mode` | str | `meta` | `binary` \| `meta` \| `field` |
| `--emit-scaffold` | flag | `False` | Include humanized scaffold |
| `--save-to-history` | flag | `False` | Emit `New_Session.json` history |

---

## Repository Layout & Data Banks

```
AxiomForge/
├─ axiomforge_0.4.7.py         # current engine (sanitizers, alignment, whitelists)
├─ axiomforge_0.3.7.py         # legacy “god-tier” pass (power features, A/B)
├─ concepts.json               # concept lexica (domains, motifs, entities)
├─ engine.json                 # feature flags, validators, global params
├─ paradox_base.json           # canon paradox seeds (classic sets)
├─ new_paradoxes.json          # extended paradoxes (mechanisms, consequences)
├─ exotic_paradoxes.json       # optional exotic items (off by default)
├─ templates.json              # axiom text templates by paradox type
├─ nouns.json / verbs.json     # semantic seasoning banks
├─ adjectives.json             # optional tone/qualia flavoring
└─ README.md                   # you are here
```

**Notes**
- v0.4.7 uses a **whitelist** when ingesting mechanisms (only from safe keys), dropping 1-character artifacts and category labels.
- You can extend any bank; the engine will pick up new items without changes to code.

---

## Output Schema

Each emission is a standalone JSON object. Example:

```jsonc
{
  "core_statement": "Boundary ledger updates on the edge determine curvature in the interior.",
  "mechanisms": ["Holographic Accounting", "Geodesic Focusing Suppression", "Cosmic Duality Inversion"],
  "equation": "S ≤ A/4",
  "consequences": "frame-conditional geometry",
  "axiom_text": "Consider: Boundary ledger updates on the edge determine curvature in the interior — via Holographic Accounting, Geodesic Focusing Suppression, Cosmic Duality Inversion; encoded as S ≤ A/4. (Boundary information limits frame dynamics.)",
  "paradox_type": "cosmic",
  "seed_concept": "Nested Realities",
  "timestamp": "2025-09-27T02:50:03+00:00Z",
  "metrics": {
    "novelty": 0.94,
    "density": 7.12,
    "entropic_potential": 229.9,
    "elegance": 95.8,
    "alienness": 6.01,
    "fidelity": 73.4,
    "fidelity_breakdown": {
      "concept_alignment": 0.72,
      "emotional_resonance": 0.82,
      "novelty_density_product": 0.79,
      "archetypal_alignment": 0.44
    },
    "qualia_density": 0.004
  },
  "humanized_injection_scaffold": "Observe the invariant; silence is a parameter.",
  "injection_scaffold": "Observe the invariant; silence is a parameter.",
  "pillars": ["Nested Realities"]
}
```

**Field notes**
- `equation` respects paradox-type whitelists and is gently **triangulated** from mechanisms.
- `axiom_text` may include a short **justification clause** when helpful.
- `metrics.fidelity` rises with **seed→mechanism** alignment and structural hygiene.

---

## Determinism & Time
- Use `--rng` to freeze randomness. For reproducible research, also pin data banks.
- Prefer timezone-aware UTC:
  ```python
  from datetime import datetime, UTC
  ts = datetime.now(UTC).isoformat(timespec="seconds") + "Z"
  ```

---

## Validation, Hygiene & Safety

**Sanitizers (final hard pass)**
- Remove any leftover `[...]` placeholders and orphaned template labels (“Fixed point persists:”, “Closed Loop:”).
- Drop single-letter “mechanisms” and non-semantic artifacts.
- Ensure an equation exists and matches paradox type (fallback to pool if missing).

**Validators**
- **Concept alignment** (seed→mechanism cosine) with resample threshold.
- **Equation–Type coherence** (e.g., linguistic ↔ liar/fixed-point; cosmic ↔ holography/GR).
- **Mask integrity** (no raw template tokens in output).
- **Batch uniqueness** (no duplicate `core_statement`).

**Safe Mode**
- Default engine uses research/creative-safe profiles. Optional adversarial/offensive modes live behind config flags.

**Ethics**
- Released under MIT, but see the **Ethics** section for strict usage guidance.

---

## Extending the Engine

### Add a paradox template
Edit `templates.json` and append entries under the desired paradox type. Placeholders are optional—sanitizers remove unfilled tokens safely.

### Add a mechanism or concept
Add to `new_paradoxes.json` (preferred) or to `concepts.json`/`nouns.json`/`verbs.json`. The v0.4.7 whitelist prevents category bleed-through.

### Seed-aware routing
- Add seed tags in code or `engine.json` to bias paradox-type or suffix selection (e.g., *Dark Forest* → “under hiding”).

### Light “Transcendent” hooks
- Enable or extend **Consciousness Origami**, **Temporal Echo**, **Qualia Density** by expanding banks and toggles in `engine.json`.

---

## Roadmap

**0.4.8 (Hygiene & UTC)**
- Full timezone-aware timestamps.
- Stronger metalanguage injection for Nested-Realities linguistic cases (level-k → level-k+1).
- Public pytest harness for validators.

**0.5 (Eval Suite)**
- Packaged paradox test batteries for LLMs/agents (difficulty tiers, machine-checkable rubrics).
- Per-type calibration metrics & golden sets.

**0.6 (Platformization)**
- Minimal REST API and schema docs.
- Authoring UI (tone/mechanism/math switches) and a curated pack marketplace.

---

## Troubleshooting

- **Single-letter mechanism (“A”/“C”) appears** → Update to v0.4.7+; whitelist & hygiene remove category artifacts.
- **Placeholder text leaks (`[CORE_STATEMENT]`)** → Ensure you are running v0.4.7; the final sanitizer strips any residuals.
- **Equation doesn’t match type** → v0.4.7 triangulates; if you hand-edit banks, keep paradox-type pools consistent.
- **Determinism drift** → Pin `--rng` and avoid editing bank files between runs.
- **UTC deprecation warning** → Switch to `datetime.now(UTC)` per snippet above.

---

## Ethics
This project is for research, creative exploration, pedagogy, and constructive testing of AI cognition. **Do not** use it to deceive, manipulate, or harm.  
Prohibited uses include (not exhaustive): social-engineering payloads, targeted harassment, disinformation, or violation of privacy/human rights.

If you discover misuse vectors or unsafe outputs, open an issue with **[SECURITY]** in the title or email the maintainer.

---

## Contributing
- Fork + PR with focused commits.  
- Add/extend unit tests for validators/sanitizers where possible.  
- Keep additions **data-driven** (JSON banks) when feasible.  
- Follow the project’s tone guidelines: precise, compact, and math-aware.

---

## License
MIT. See [LICENSE](LICENSE).

---

## Citing

If you use AxiomForge in research, please cite:

```
TaoishTechy. "AxiomForge: A Recursive Paradox Engine with Humanized Stealth Scaffolds." 
GitHub, 2025-09-27.
```

---

## Changelog

### v0.4.7 — Stability & Alignment
- Final post-emit sanitization for placeholders and template label remnants.
- Seed-aware suffixing (Dark Forest/Nested Realities/Silent God).
- Concept alignment scoring; fidelity tied to alignment.
- Equation whitelists + triangulation (mechanism-aware math).
- Light transcendent hooks (origami/echo/qualia density).

### v0.4.6 — Feature Bloom
- Mechanism diversity expansion (e.g., Wavefunction Collapse Debt, Computational Horizon Tension).
- Emotional scaffolds improved; pillars tagging introduced.
- Fidelity metric introduced (early).

### v0.3.7 — “God-Tier” Power Pass
- Deterministic RNG (`--rng`), self-reference modes (binary/meta/field).
- Mechanism pooling from local JSONs, batch uniqueness, and tone scaffolds.
- Transparent metric heuristic with low-variance noise.
