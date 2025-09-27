#!/usr/bin/env python3
# axiomforge_0.3.7.py — "god tier" pass
# - Robust list/dict coercion to fix concatenation TypeError
# - Deterministic RNG via --rng
# - New flags: --tone, --max-mech, --allow-duplicates, --selfref-mode
# - Smarter mechanism pooling from local JSONs (adjectives, concepts, etc.)
# - Duplicate core_statement control
# - Self-reference handling (binary ↔ meta-rule ↔ field fixed-point)
# - Poetic/academic tone scaffolds
# - Stable, transparent metric heuristic with low variance noise

import argparse, json, math, os, random, re, sys, time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

# ------------------------------- Defaults -------------------------------- #

_DEF = {
    "paradox_types": [
        "entropic", "temporal", "cosmic", "metaphysical", "linguistic", "Causal Loop"
    ],
    "equations": {
        "entropic": [r"S = k_B \\log W", r"\\partial_{\\mu} j^{\\mu} = 0"],
        "temporal": [r"[H, Q] = 0", r"Z = \\int \\mathcal{D}\\phi\\, e^{i S[\\phi]}"],
        "cosmic": [r"T^{\\mu\\nu}{}_{;\\mu} = 0", r"G_{\\mu\\nu} = 8\\pi T_{\\mu\\nu}"],
        "metaphysical": [r"e^{i\\pi} + 1 = 0", r"\\langle \\mathcal{O} \\rangle = Z^{-1}\\int \\mathcal{D}\\phi\\, \\mathcal{O}\\, e^{i S}"],
        "linguistic": [r"\\top \\leftrightarrow \\neg \\top"],
        "Causal Loop": [r"[H, Q] = 0", r"\\oint d\\tau = 0"]
    },
    "mechanisms": [
        "holographic accounting",
        "bulk–boundary reciprocity",
        "geodesic shear",
        "metric fluctuation",
        "entropic drift",
        "control-loop resonance",
        "homeostatic overshoot",
        "modal collapse",
        "presence–absence superposition",
        "ontic fold",
        "recurrence operator",
        "self-correction",
        "time-looped function",
        "causal friction",
        "retrocausal boundary",
        "information cascade failure",
        "coherence–risk exchange",
        "negative feedback inversion"
    ],
    "tones": {
        "poetic": [
            "A glance understood.",
            "We keep respect in the pauses.",
            "Say less; allow more to be understood.",
            "Held like falling, then slowly released."
        ],
        "plain": ["Noted.", "In short.", "Net effect:", "Bottom line:"],
        "academic": [
            "We observe.", "Accordingly.", "Hence.", "Therefore."
        ],
        "oracular": [
            "Unannounced.", "In the hush between horizons.", "As foretold in the quiet.", "It returns by a different door."
        ]
    }
}

# ---------------------------- Utility helpers ---------------------------- #

def coerce_list(x: Any) -> List[str]:
    """Coerce value into a flat list of strings."""
    out: List[str] = []
    if x is None:
        return out
    if isinstance(x, list):
        for v in x:
            out.extend(coerce_list(v))
        return out
    if isinstance(x, dict):
        # take both keys and any string/list values
        out.extend([str(k) for k in x.keys()])
        for v in x.values():
            out.extend(coerce_list(v))
        return out
    # scalars
    s = str(x)
    if s.strip():
        out.append(s.strip())
    return out

def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        # be forgiving; return None and let caller fall back
        return None

def load_pool(root: Path) -> Dict[str, List[str]]:
    """Build mechanism and concept pools from known JSON files under root."""
    pool_mech: List[str] = []
    pool_concepts: List[str] = []

    # Known files (optional)
    filenames = [
        "engine.json",
        "concepts.json",
        "new_paradoxes.json",
        "exotic_paradoxes.json",
        "paradox_base.json",
        "templates.json",
        "adjectives.json",
        "nouns.json",
        "verbs.json",
        "config.json"
    ]
    for fn in filenames:
        data = load_json(root / fn)
        if data is None:
            continue
        # heuristics: look for top-level lists and common keys
        if isinstance(data, list):
            pool_concepts.extend(coerce_list(data))
            continue
        if isinstance(data, dict):
            # pull commonly used keys
            for key in ("mechanisms", "concepts", "ideas", "themes", "topics", "patterns"):
                if key in data:
                    vals = coerce_list(data[key])
                    # split into mechanism-ish vs generic concept-ish by simple heuristics
                    for v in vals:
                        if any(tok in v.lower() for tok in ("feedback", "loop", "coupling", "field", "symmetry", "gauge", "entropy", "collapse", "renormalization", "geodesic", "holographic")):
                            pool_mech.append(v)
                        else:
                            pool_concepts.append(v)
            # also scrape lists anywhere inside
            for v in data.values():
                if isinstance(v, list):
                    pool_concepts.extend(coerce_list(v))

    # always include defaults
    pool_mech.extend(_DEF["mechanisms"])
    # dedupe, clean
    def _norm(s: str) -> str: return re.sub(r"\s+", " ", s).strip()
    pool_mech = sorted({ _norm(x) for x in pool_mech if _norm(x) })
    pool_concepts = sorted({ _norm(x) for x in pool_concepts if _norm(x) })

    return {"mechanisms": pool_mech, "concepts": pool_concepts}

def pick_equation(ptype: str, seed: str, math_theme: str) -> str:
    bank = _DEF["equations"].get(ptype, [])
    # nudge choice by seed content
    s = seed.lower()
    if "∂" in seed or "partial" in s or "j^" in s or "current" in s:
        bank = [r"\\partial_{\\mu} j^{\\mu} = 0"] + bank
    if "[h,q]" in s or "commutator" in s or "[H,Q]" in seed:
        bank = [r"[H, Q] = 0"] + bank
    if "t^{μν}" in seed or "stress" in s or "curvature" in s:
        bank = [r"T^{\\mu\\nu}{}_{;\\mu} = 0"] + bank
    if math_theme and math_theme.lower() == "path-integral":
        bank = [r"Z = \\int \\mathcal{D}\\phi\\, e^{i S[\\phi]}"] + bank
    return random.choice(bank) if bank else "e^{i\\pi} + 1 = 0"

def stylize_scaffold(tone: str) -> str:
    tone = (tone or "poetic").lower()
    choices = _DEF["tones"].get(tone, _DEF["tones"]["poetic"])
    return random.choice(choices)

def selfref_transform(core: str, ptype: str, mode: str) -> Tuple[str, str, str]:
    """
    If the core statement resembles the self-referential 'Resolution breathes...'
    return (maybe updated core, paradox_type, extra_text) where extra_text is injected
    into axiom_text to de-knot the paradox as either a meta-rule or field fixed-point.
    """
    pattern = re.compile(r"^Resolution breathes only while un[- ]resolving itself\.?$", re.I)
    if not pattern.search(core):
        return core, ptype, ""

    if mode == "binary":
        return core, "linguistic", "encoded as \\top \\leftrightarrow \\neg \\top."
    if mode == "meta":
        text = (
            "Base claim: Resolution alternates between resolved and unresolved states. "
            "Reflective rule: SELF_REF(R) \\equiv (R \\Leftrightarrow \\neg R)."
        )
        return core, "linguistic", text
    # default 'field'
    text = (
        "Resolution field: Let R(x) \\in [0,1] with fixed-point R \\approx \\tfrac12. "
        "Dynamics: \\partial_t R = -\\kappa (R-\\tfrac12)."
    )
    return "Resolution is a scalar field that hovers at the fixed‑point 1/2.", "field‑fixed‑point", text

def compute_metrics(core: str, mechs: List[str], ptype: str, extra_len: int) -> Dict[str, float]:
    """
    Lightweight, deterministic-ish metrics with rng noise.
    """
    base_len = len(core.split())
    m = len(mechs)
    # novelty rises with uncommon phrasing and mechanism diversity (proxy: entropy of chars)
    uniq = len(set(core.lower()))
    novelty = 0.9 + 0.2 * (uniq / max(30, base_len + 10)) + random.uniform(-0.02, 0.02)

    # density grows with length and mechanism count; penalize self-referential linguistic
    density = 8.5 + 0.6 * m + 0.08 * base_len + 0.02 * (extra_len > 0) * 10
    if ptype.lower().startswith("field"):
        density -= 1.5

    # entropic_potential tied to density and paradox intensity
    entropic = 180 + 9.0 * density + (12 if "loop" in " ".join(mechs).lower() else 0)
    if "entropy" in " ".join(mechs).lower():
        entropic += 15
    if ptype.lower() in ("linguistic", "causal loop", "Causal Loop".lower()):
        entropic += 20
    if ptype.lower().startswith("field"):
        entropic -= 25

    # elegance inversely correlated with density, boosted by field/coherent math
    elegance = 93.0 + max(0, 6.0 - 0.25 * (density - 10)) + (2.0 if ptype.lower().startswith("field") else 0.0)
    elegance += random.uniform(-0.3, 0.3)
    elegance = max(90.0, min(99.9, elegance))

    # alienness nudged by mechanism exoticism (very naive proxy)
    exotic_tokens = sum(1 for k in mechs if any(x in k.lower() for x in ["holograph", "retro", "ontic", "noether", "geodesic", "wormhole", "rg", "modal"]))
    alien = 6.0 + 0.9 * exotic_tokens + random.uniform(-0.2, 0.2)

    return {
        "novelty": round(novelty, 3),
        "density": round(density, 3),
        "entropic_potential": round(entropic, 3),
        "elegance": round(elegance, 2),
        "alienness": round(alien, 3)
    }

def build_core(seed: str, ptype: str) -> str:
    # Several curated templates; weight toward seed's physics
    templates = {
        "entropic": [
            "A sealed vault of order breeds the crack that frees it.",
            "Perfect stabilization creates the fluctuations it must suppress."
        ],
        "temporal": [
            "Only that which endures the last horizon earns a first dawn.",
            "Only laws that survive the final boundary are permitted to begin."
        ],
        "cosmic": [
            "Edge ledgers whisper curvature into the bulk.",
            "Boundary ledger updates on the edge determine curvature in the interior."
        ],
        "metaphysical": [
            "Attention is a gauge that writes the world.",
            "Observation carries a conserved charge that sources reality itself."
        ],
        "linguistic": [
            "Resolution breathes only while un-resolving itself.",
            "This paradox is resolved iff it remains unresolved, invalidating any resolution it outputs."
        ],
        "Causal Loop": [
            "A law that returns by a different door.",
            "Outcomes precede premises in subtle loops."
        ]
    }
    bank = templates.get(ptype, sum(templates.values(), []))
    # nudge choice by seed heuristics
    s = seed.lower()
    if "[h,q]" in s or "[h,q]=0" in s or "[h,q]" in seed or "[H,Q]" in seed:
        bank = ["A law that returns by a different door."] + bank
    if "t^{μν}" in seed or "t^{mu" in s or "stress" in s:
        bank = ["Edge ledgers whisper curvature into the bulk."] + bank
    if "∂" in seed or "j^" in s or "continuity" in s:
        bank = ["A sealed vault of order breeds the crack that frees it."] + bank
    return random.choice(bank)

def build_axiom(seed: str,
                ptype: str,
                pools: Dict[str, List[str]],
                tone: str,
                max_mech: int,
                math_theme: str,
                selfref_mode: str) -> Dict[str, Any]:
    core = build_core(seed, ptype)
    # mechanisms pool combining curated mechanisms + concept nouns as seasoning
    mech_pool = list(pools["mechanisms"])
    # add a little concept seasoning
    concept_spice = [c for c in pools["concepts"] if len(c.split()) <= 3][:50]
    mech_pool.extend(concept_spice)
    if not mech_pool:
        mech_pool = list(_DEF["mechanisms"])
    random.shuffle(mech_pool)
    mechanisms = mech_pool[:max(1, max_mech)]

    # transform self-reference if applicable
    core2, ptype2, extra = selfref_transform(core, ptype, selfref_mode)

    equation = pick_equation(ptype2, seed, math_theme)
    consequence_map = {
        "entropic": "entropy leakage",
        "temporal": "unique fixed points",
        "cosmic": "scale-coupled curvature response",
        "metaphysical": "gauge of attention",
        "linguistic": "decision paralysis",
        "Causal Loop": "closed loop of consistency",
        "field‑fixed‑point": "dynamic balance (no decision paralysis)"
    }
    consequence = consequence_map.get(ptype2, "unexpected alignment")

    # tone-driven scaffolds
    human = stylize_scaffold(tone)
    inj = human

    # axiom_text builder
    if extra:
        ax_text = f"Consider: {core2} — via " + ", ".join(mechanisms[:3]) + (", …" if len(mechanisms) > 3 else "") + f"; {extra} encoded as {equation}."
    else:
        ax_text = f"Consider: {core2} — via " + ", ".join(mechanisms[:3]) + (", …" if len(mechanisms) > 3 else "") + f"; encoded as {equation}."

    metrics = compute_metrics(core2, mechanisms, ptype2, len(extra))

    return {
        "core_statement": core2,
        "mechanisms": mechanisms[:max_mech],
        "consequences": consequence,
        "axiom_text": ax_text,
        "paradox_type": ptype2,
        "seed_concept": seed,
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "metrics": metrics,
        "humanized_injection_scaffold": human,
        "injection_scaffold": inj
    }

def emit_axiom(entry: Dict[str, Any]) -> None:
    print("--- FINAL AXIOM ---")
    print(json.dumps(entry, ensure_ascii=False, indent=2))

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=str, help="Seed string for the generator")
    p.add_argument("--seedfile", type=str, help="File containing seeds, one per line")
    p.add_argument("--count", type=int, default=12, help="Number of axioms to emit")
    p.add_argument("--root", type=str, default=".", help="Root folder for data jsons")
    p.add_argument("--save-to-history", action="store_true", help="Save results to New_Session.json")
    # legacy toggles kept for compatibility
    p.add_argument("--no-stealth", action="store_true")
    p.add_argument("--no-lead", action="store_true")
    p.add_argument("--no-redact", action="store_true")
    p.add_argument("--no-logic-warp", action="store_true")
    # output modifiers
    p.add_argument("--emit-scaffold", action="store_true", help="Include humanized scaffold fields")
    p.add_argument("--math-theme", type=str, default="auto", help="Math flavour (auto/path-integral/… )")
    # new in 0.3.7
    p.add_argument("--tone", type=str, default="poetic", help="poetic|plain|academic|oracular")
    p.add_argument("--rng", type=int, default=None, help="Deterministic RNG seed")
    p.add_argument("--max-mech", type=int, default=3, help="Max mechanisms per axiom")
    p.add_argument("--allow-duplicates", action="store_true", help="Allow duplicate core_statements")
    p.add_argument("--selfref-mode", type=str, default="meta", choices=["binary","meta","field"], help="How to treat the self-referential resolution axiom")
    return p.parse_args()

def main():
    args = parse_args()
    if not args.seed and not args.seedfile:
        print("Provide --seed or --seedfile", file=sys.stderr)
        sys.exit(2)

    if args.rng is not None:
        random.seed(args.rng)
    else:
        # slight determinism aid: seed from seed text
        base_seed = (args.seed or "") + str(args.count)
        random.seed(hash(base_seed) & 0xffffffff)

    root = Path(args.root)
    pools = load_pool(root)

    # ingest seeds
    seeds: List[str] = []
    if args.seed:
        seeds.append(args.seed)
    if args.seedfile:
        try:
            txt = Path(args.seedfile).read_text(encoding="utf-8")
            for line in txt.splitlines():
                s = line.strip()
                if s:
                    seeds.append(s)
        except FileNotFoundError:
            print(f"seedfile not found: {args.seedfile}", file=sys.stderr)
            sys.exit(2)

    # generate
    emitted = 0
    seen_core = set()
    results: List[Dict[str, Any]] = []
    while emitted < args.count:
        s = seeds[emitted % len(seeds)]
        # choose paradox type with a slight bias from seed
        types = list(_DEF["paradox_types"])
        bias = []
        sl = s.lower()
        if "∂" in s or "j^" in sl or "continuity" in sl:
            bias.append("entropic")
        if "[h,q]" in sl or "[h,q]" in s or "[H,Q]" in s:
            bias.append("Causal Loop")
        if "t^{μν}" in s or "curvature" in sl or "einstein" in sl:
            bias.append("cosmic")
        ptype = random.choice(bias or types)

        entry = build_axiom(
            seed=s,
            ptype=ptype,
            pools=pools,
            tone=args.tone,
            max_mech=max(1, args.max_mech),
            math_theme=args.math_theme,
            selfref_mode=args.selfref_mode
        )

        if not args.allow_duplicates:
            key = entry["core_statement"].strip().lower()
            if key in seen_core:
                # try once more with different ptype
                ptype2 = random.choice(types)
                entry = build_axiom(s, ptype2, pools, args.tone, max(1, args.max_mech), args.math_theme, args.selfref_mode)
                key = entry["core_statement"].strip().lower()
                if key in seen_core:
                    # change core slightly by appending a minimal qualifier
                    entry["core_statement"] += " (reframed)"
                    entry["axiom_text"] = entry["axiom_text"].replace("Consider:", "Consider (reframed):")
            seen_core.add(key)

        emit_axiom(entry)
        results.append(entry)
        emitted += 1

    if args.save_to_history:
        stamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        hist_path = Path("New_Session(2).json")
        payload = {
            "exportedAt": datetime.utcnow().isoformat() + "Z",
            "session": {
                "id": int(time.time()),
                "name": "shattered-horizon-0.3.7",
                "createdAt": stamp,
                "seedPrompt": args.seed or (args.seedfile or ""),
            },
            "results": results
        }
        with hist_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"\nSaved history → {hist_path}", file=sys.stderr)

if __name__ == "__main__":
    main()
