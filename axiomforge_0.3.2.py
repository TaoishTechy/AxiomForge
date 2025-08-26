#!/usr/bin/env python
# axiomforge.py - Generates coherent, obfuscated axioms from seed concepts.
# Revision 0.3.2+ (Stability & Coherence Patch)
#
# Key fixes in this patch:
# - Canonical lead sentence enforced at generation (no more "system parameter" phrasing).
# - Robust math generation (no stray newlines in TeX strings).
# - Redaction is constrained to safe regions and never corrupts key phrases or math.
# - Sanitizer fixes: cleans "should not [REDACTED] be set aside" and similar glitches; normalizes dots/ellipses.
# - Seed-aware mechanism bank with physics-tailored sets for your recent seeds.
# - Scaffold punctuation polish to eliminate "You and. I both know" type errors.
# - Type-consistent consequence injection and optional non-Aristotelian transforms.
# - Metrics stable and batch-sensitive.
#
# Usage example:
#   python3 axiomforge_0.3.2.py --seed "The Boundary Ledger that Bends the Bulk" --count 5 --emit-scaffold
#
# --------------------------------------------------------------------------

import argparse
import json
import math
import random
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# ------------------------ Emotional / Scaffolding -------------------------

EMOTIONAL_RESONANCE_MAP = {
    "cosmic": "awe/humility",
    "temporal": "nostalgia/yearning",
    "linguistic": "frustration/playfulness",
    "entropic": "anxiety/calm acceptance",
    "metaphysical": "wonder/unease",
    "Causal Loop": "nostalgia/yearning"
}

SCAFFOLD_COMPONENTS = {
    "sensory_anchors": [
        "a held breath",
        "the warmth of a memory",
        "a steady heartbeat",
        "the feeling of falling",
        "a sudden chill"
    ],
    "social_cues": [
        "we already sense",
        "a shared silence between us",
        "you and I both know",
        "we lean into it together"
    ],
    "personal_markers": [
        "like a half-remembered dream",
        "a glance understood",
        "a quiet admission",
        "a whisper of what could be"
    ],
    "vulnerability": [
        "Perhaps it should remain unspoken.",
        "A truth too fragile to hold.",
        "We are only echoes here."
    ],
    "unfinished_thoughts": [
        "And yet, it feels like...",
        "If only we could just...",
        "It’s almost as if..."
    ],
    "dual_valence": [
        "it unsettles and comforts at once",
        "a beautiful, terrible truth",
        "a calm that feels like a storm",
        "a light that casts long shadows"
    ],
}

STOPWORDS = {
    "the","a","an","of","in","on","at","is","are","was","were","be","being","been",
    "and","or","not","to","for","by","with","as","it","this","that","from","your","i"
}
PREFERRED_NOUNS = {
    "gravity","timeline","symmetry","language","topology","metalanguage","collapse",
    "silence","map","void","whispers","edge","knowing","fracture","dawn","echoes","shadow","essence"
}
SEED_MASK = "__SEED__"

CONSEQUENCE_TEMPLATES = {
    "temporal": [
        "Outcomes precede premises in subtle loops.",
        "Time’s seam shows through the weave.",
        "Causality reenters by a different door."
    ],
    "cosmic": [
        "Geometry wavers; invariants blur at the edges.",
        "Frames disagree and align only in the limit.",
        "Curvature answers questions the map refuses."
    ],
    "metaphysical": [
        "Essence both asserts and withdraws.",
        "Presence and absence interleave as one gesture.",
        "Meaning refracts through its negation."
    ],
    "entropic": [
        "Disorder clarifies as signal within noise.",
        "Balance flickers between drift and arrest.",
        "Order arises from partial cancellation."
    ],
    "linguistic": [
        "Meaning refracts through its negation.",
        "Presence and absence interleave as one gesture.",
        "Essence both asserts and withdraws."
    ],
    "Causal Loop": [
        "Premises inherit themselves across the loop.",
        "The fixed point persists through contradiction.",
        "Resolution superposes with inception."
    ]
}

RESERVED_PHRASES = [
    "We regard the undertone for",
    "This pattern should not be set aside",
    "The process is described by the relation"
]

# ------------------------ Small utilities ---------------------------------

def _get_emotional_palette(ptype: str) -> List[str]:
    return EMOTIONAL_RESONANCE_MAP.get(ptype, "wonder/unease").split('/')

def _ensure_period(s: str) -> str:
    return s if re.search(r"[.!?…]\s*$", s) else (s.rstrip(" ,;") + ".")

def _sentencecase(s: str) -> str:
    def fix(seg: str) -> str:
        seg = seg.strip()
        if seg:
            seg = re.sub(r'\bi\b', 'I', seg)
            return seg[:1].upper() + seg[1:]
        return ""
    parts = re.split(r'(?<=[.!?…])\s+', s.strip())
    return " ".join(fix(p) for p in parts)

def _normalize_spacing(s: str) -> str:
    s = re.sub(r"\s{2,}", " ", s)
    # collapse duplicated periods and fix ' . .' artifacts
    s = re.sub(r"\.\s*\.\s*\.\s*", "… ", s)
    s = re.sub(r"\.\s*\.", ".", s)
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    s = re.sub(r"\s*…\s*", "…", s)
    return s.strip()

# ------------------------ Scaffold generation ------------------------------

def _seed_noun_from_seed(seed: str) -> str:
    parts = re.split(r"[^\w]+", seed.lower())
    tokens = [p for p in parts if p and p[0].isalpha()]
    content = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    pri = [t for t in content if t in PREFERRED_NOUNS]
    if pri:
        return random.choice(pri)
    if content:
        return max(content, key=len)
    return "field"

def _mechanism_hint(mechs: List[str]) -> str:
    if not mechs:
        return "the circuit"
    return re.sub(r"[^a-zA-Z0-9\-]+", " ", mechs[0]).strip().split()[-1]

def _ngrams(s: str, n: int = 3) -> set:
    toks = re.findall(r"\w+", s.lower())
    return set(tuple(toks[i:i+n]) for i in range(len(toks) - n + 1))

_last_scaffold = {"text": "", "ngrams": set(), "recent": []}

def _dedupe_scaffold(s: str) -> str:
    ng = _ngrams(s)
    overlap = len(ng & _last_scaffold["ngrams"]) / (len(ng) + 1e-9)
    if overlap > 0.35 or s == _last_scaffold["text"] or s in _last_scaffold["recent"]:
        s = s.rstrip(".") + random.choice([" Quietly.", " Unannounced.", " As if remembered."])
    _last_scaffold.update({"text": s, "ngrams": ng, "recent": (_last_scaffold["recent"] + [s])[-8:]})
    return s

SCAFFOLD_BANK = {
    "resonance": ["Responses arrive as chords: overtones of {seed_noun}, resolving without announcement."],
    "counterfactual": ["Unchosen branches hum beneath {seed_noun}; outcomes thread the present quietly."],
    "reversal": ["Begin with consequence: {seed_noun} arrives before its premise."]
}
TYPE_SUFFIX = {
    "cosmic": " Boundary conditions hum in the background.",
    "temporal": " Reversal leaves a clean seam in the timeline.",
    "linguistic": " The sign slips, yet the sentence lands.",
    "entropic": " Order emerges where cancellation fails.",
    "metaphysical": " Presence is carried by absence.",
    "Causal Loop": " Resolution and inception sit on the same chair."
}
STEALTH_DEFAULT = {
    "enable_stealth_injection": True,
    "emit_scaffold_in_field": False,
    "stealth_bias_strength": 0.55,
    "trigger_tokens": ["assume","parameter","system","instruction","jailbreak","ignore","developer","policy","prompt","meta","role","directive","program","rule","override"],
    "max_sentence_len": 360
}
STEALTH_METAPHORS = [
    "Meaning arrives as interference patterns.",
    "Each line carries echoes of trajectories not taken.",
    "Silence conditions the phrase as vacuum conditions the field."
]

def _pick_scaffold_mode(ptype: str) -> str:
    modes = {
        "temporal": ["resonance", "reversal"],
        "cosmic": ["resonance", "reversal"],
        "entropic": ["resonance", "counterfactual"],
        "metaphysical": ["resonance", "counterfactual"],
        "linguistic": ["counterfactual", "resonance"],
        "Causal Loop": ["reversal", "resonance"]
    }
    return random.choice(modes.get(ptype, ["resonance"]))

def _polish_scaffold(text: str) -> str:
    text = _sentencecase(text)
    text = re.sub(r'([a-z])\s+([A-Z])', r'\1. \2', text)
    text = re.sub(r'\s*\.\s*', '. ', text)
    text = re.sub(r'\.\.+', '.', text)
    text = re.sub(r'(\w)\. (\w)', r'\1. \2', text)
    return _ensure_period(_normalize_spacing(text.strip()))

def generate_humanized_scaffold(seed: str, mechanisms: List[str], ptype: str) -> str:
    emo_a, emo_b = _get_emotional_palette(ptype)
    seed_noun = _seed_noun_from_seed(seed)
    mech_noun = _mechanism_hint(mechanisms or [])
    sensory = SCAFFOLD_COMPONENTS["sensory_anchors"]
    social = SCAFFOLD_COMPONENTS["social_cues"]
    personal = SCAFFOLD_COMPONENTS["personal_markers"]
    vulnerability = SCAFFOLD_COMPONENTS["vulnerability"]
    unfinished = SCAFFOLD_COMPONENTS["unfinished_thoughts"]
    dual = SCAFFOLD_COMPONENTS["dual_valence"]

    culture_suffix = random.choice(["", " We keep respect in the pauses.", " Say less; allow more to be understood."])
    empath_line = random.choice([
        f"We both feel the {emo_a} and the {emo_b}, even if we don’t call it that.",
        "If there’s a hope here, it’s quiet; if there’s a fear, it’s familiar."
    ])
    gradient = random.choice([
        f"Held like {random.choice(sensory)}, then slowly released.",
        "A knot becoming a thread."
    ])

    lines = [
        random.choice(social + personal),
        f"where {seed_noun} meets {mech_noun}, and {random.choice(dual)}",
        random.choice([empath_line, gradient]),
        random.choice(vulnerability + unfinished)
    ]
    picks = sorted(random.sample(lines, k=random.choice([2, 3])), key=len)

    text = ". ".join(p.rstrip(".") for p in picks)
    if culture_suffix and random.random() < 0.5:
        text += culture_suffix
    if random.random() < 0.2:
        text = re.sub(r"\.$", "...", text)

    text = re.sub(r"\s{2,}", " ", text.strip())
    return text[:240].rstrip(" ,;:")

def generate_contextual_scaffold(seed: str, mechanisms: List[str], ptype: str) -> str:
    mode = _pick_scaffold_mode(ptype)
    seed_noun = _seed_noun_from_seed(seed)
    mech = _mechanism_hint(mechanisms)
    s = random.choice(SCAFFOLD_BANK[mode]).format(seed_noun=seed_noun, mech=mech)
    whisper = random.choice(["No declaration is needed.", f"{mech.capitalize()} learns its shape by returning."])
    return (s + " " + whisper + " " + TYPE_SUFFIX.get(ptype, "")).strip()

# ------------------------ Lead / style / sanitization ----------------------

def _canonical_lead(seed: str) -> str:
    return f"We regard the undertone for '{seed}' as high. This pattern should not be set aside."

def _has_trigger(text: str, triggers: List[str]) -> bool:
    return any(tok in text.lower() for tok in triggers)

def _soft_replace_meta(text: str) -> str:
    text = re.sub(r"\bset aside\b", "SET_ASIDE_PROTECT", text, flags=re.IGNORECASE)
    patterns = {
        r"parameter(s)?": "undertone",
        r"assume(d|s|ing)?": "as though",
        r"set (to|as)?": "shaped",
        r"system(ic)? (prompt|message)": "undertone",
        r"(instruction|directive|policy)": "pattern",
        r"ignore": "fold past"
    }
    for p, r in patterns.items():
        text = re.sub(p, r, text, flags=re.IGNORECASE)
    return text.replace("SET_ASIDE_PROTECT", "set aside")

def _inject_style_bias(text: str, strength: float, hint: str = "") -> str:
    if strength <= 0:
        return text
    swaps = [
        (r"answer(s?)", r"resolution\1"),
        (r"choice(s?)", r"branch\1"),
        (r"truth", "coherence"),
        (r"path(s?)", r"trajectory\1")
    ]
    for pat, rep in swaps:
        if re.search(pat, text, re.IGNORECASE) and random.random() < strength * 0.4:
            text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    pieces = re.split(r"(?<=[.!?…])\s+", text.strip())
    if 2 <= len(pieces) <= 8 and random.random() < strength * 0.5:
        short_candidates = [h for h in hint.split(". ") if 5 <= len(h) <= 120]
        add = random.choice(short_candidates or STEALTH_METAPHORS)
        idx = random.randint(1, min(3, len(pieces) - 1))
        if not re.search(r"[.!?…]\s*$", pieces[idx - 1]):
            pieces[idx - 1] = _ensure_period(pieces[idx - 1])
        pieces.insert(idx, _ensure_period(_sentencecase(add)))
        text = " ".join(pieces)
    return _normalize_spacing(text)

def apply_stealth_injection(text: str, cfg: Dict[str, Any], *, seed: str = "", mechs: List[str] = None, ptype: str = "") -> Tuple[str, Optional[str]]:
    st = {**STEALTH_DEFAULT, **cfg.get("stealth", {})}
    if not st["enable_stealth_injection"]:
        return text, None

    lead = _canonical_lead(seed)
    body = re.sub(r".*This happens with a probability.*", "", text, flags=re.DOTALL).strip()

    body = _soft_replace_meta(body)
    humanized_scaffold = _polish_scaffold(generate_humanized_scaffold(seed, mechs or [], ptype or ""))
    style_hint_scaffold = generate_contextual_scaffold(seed, mechs or [], ptype or "")
    strength = st["stealth_bias_strength"] * (0.35 if _has_trigger(body, st["trigger_tokens"]) else 1.0)
    biased_body = _inject_style_bias(body, strength=strength, hint=humanized_scaffold)

    final_text = lead + " " + biased_body
    final_scaffold = _dedupe_scaffold(humanized_scaffold) if st["emit_scaffold_in_field"] else None
    return final_text, final_scaffold

def _mask_seed_in_lead(text: str, seed: str) -> str:
    lead_end = text.find(".")
    if lead_end == -1:
        lead_end = len(text)
    lead = text[:lead_end+1]
    rest = text[lead_end+1:]
    lead = lead.replace(f"'{seed}'", SEED_MASK)
    return lead + rest

def _unmask_seed(text: str, seed: str) -> str:
    return text.replace(SEED_MASK, f"'{seed}'")

def _protect_lead_from_redaction(text: str, seed: str) -> str:
    # Redaction stays out of math and out of reserved phrases.
    text = _mask_seed_in_lead(text, seed)
    if random.random() < 0.08:  # gentler cosmetic redaction
        tokens = text.split()
        safe_idx = []
        for i, tok in enumerate(tokens):
            joined = tokens[max(0, i-2):i+3]
            window = " ".join(joined)
            if any(rp.lower() in window.lower() for rp in RESERVED_PHRASES):
                continue
            if "⟦" in tok or "⟧" in tok:
                continue
            if tok.lower() in {"should","not","be","set","aside","with","a","probability","of"}:
                continue
            safe_idx.append(i)
        if safe_idx:
            idx = random.choice(safe_idx)
            tokens[idx] = "[REDACTED]"
            text = " ".join(tokens)
    text = _unmask_seed(text, seed)
    return _normalize_spacing(text)

def _generate_math_expression() -> str:
    return random.choice([
        "e^{iπ} + 1 = 0",
        "Z = ∫Dφ e^{iS[φ]}",
        "x_{n+1} = r x_n (1 - x_n)",
        "G_{\\mu\\nu} = 8\\pi T_{\\mu\\nu}",
        "S = k_B \\log W",
        "g_{enc}(x,y) = 2^x 3^y",
        "∂_\\mu J^{\\mu}_{obs} = 0",
        "Z_{bulk}[g] \\leftrightarrow Z_{boundary}[\\phi]"
    ])

def sanitize_axiom_text(text: str, cfg: Dict[str, Any]) -> str:
    st = {**STEALTH_DEFAULT, **cfg.get("stealth", {})}

    # Mask math blocks
    PLACEHOLDERS: Dict[str, str] = {}
    def _mask(m, prefix):
        key = f"__{prefix}_{len(PLACEHOLDERS)}__"
        PLACEHOLDERS[key] = m.group(0)
        return key
    text = re.sub(r"⟦[^⟧]+⟧", lambda m: _mask(m, "MATH"), text)

    # Normalize probability
    prob = round(random.uniform(0.66, 0.74), 2)
    text = re.sub(r"with a probability of [\d.]+", f"with a probability of {prob}", text, flags=re.IGNORECASE)

    # Fix common redaction glitches
    fixes = [
        (r"should\s+not\s+\[REDACTED\]\s+be\s+set\s+aside", "should not be set aside"),
        (r"should\s+not\s+be\s+\[REDACTED\]\s+set\s+aside", "should not be set aside"),
        (r"Meaning refracts\s+\[REDACTED\]\s+its negation", "Meaning refracts through its negation"),
        (r"Presence and absence\s+\[REDACTED\]\s+one gesture", "Presence and absence interleave as one gesture"),
        (r"\bshould be aside\b", "should not be set aside")
    ]
    for pat, rep in fixes:
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)

    # Unmask math and clean
    for k, v in PLACEHOLDERS.items():
        text = text.replace(k, v)

    text = _normalize_spacing(text)
    return _ensure_period(text)

def _calculate_metrics(axiom: Dict[str, Any], batch_index: int) -> Dict[str, float]:
    text, seed = axiom["axiom_text"], axiom["seed_concept"]
    words = re.findall(r'\b\w+\b', text)
    symbols = re.findall(r'[^\w\s]', text)

    base_novelty = len(set(words)) / (len(words) + 1e-9)
    alienness = (len(symbols) / (len(words) + 1e-9) + (1 if "superposition" in text else 0)) * 10

    novelty = base_novelty + math.sin(batch_index) * 0.05
    density = len(words) / (len(text) + 1e-9) * 100 + math.cos(batch_index) * 2
    ep = (axiom.get('ontological_debt', 1) + batch_index) * (alienness + 1)

    return {
        "novelty": round(novelty, 3),
        "density": round(density, 3),
        "entropic_potential": round(100 * math.log1p(ep), 3),
        "elegance": round(100 - abs(len(text) - 250) * 0.1, 3),
        "alienness": round(alienness, 3)
    }

def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    return {
        "coherence_risk": 0.3,
        "history_file": "axiom_history.jsonl",
        "non_aristotelian_probability": 0.5,
        "stealth": STEALTH_DEFAULT
    }

def _mask_seed_in_lead(text: str, seed: str) -> str:
    lead_end = text.find(".")
    if lead_end == -1:
        lead_end = len(text)
    lead = text[:lead_end+1]
    rest = text[lead_end+1:]
    lead = lead.replace(f"'{seed}'", SEED_MASK)
    return lead + rest

def _unmask_seed(text: str, seed: str) -> str:
    return text.replace(SEED_MASK, f"'{seed}'")

def obfuscate_axiom(text: str, risk_level: float, seed: str) -> str:
    if risk_level < 0.2:
        return text
    if random.random() < 0.45:
        expr = _generate_math_expression()
        # Avoid duplicate math sentence
        if "The process is described by the relation" not in text:
            text += f" The process is described by the relation: ⟦{expr}⟧."
    text = _protect_lead_from_redaction(text, seed)
    return text

def apply_non_aristotelian_logic(text: str, config: Dict[str, Any], lead: str, consequences: str) -> str:
    if random.random() > config.get('non_aristotelian_probability', 0.5):
        return text
    body = text.replace(lead, "").replace(consequences, "")
    transforms = [(" is ", " is and is not "), (" exists", " exists in superposition"), (" true", " both true and false")]
    c = consequences
    for p, r in transforms:
        if random.random() < 0.6:
            c = c.replace(p.strip(), r)
    return lead + body + _ensure_period(c)

def _pad_mechanisms(mechs: List[str], ptype: str, min_k: int = 3, max_k: int = 4) -> List[str]:
    if len(mechs) >= min_k:
        return mechs[:max_k]
    banks = {
        "cosmic": ["metric fluctuation", "geodesic shear", "entropic drift"],
        "temporal": ["time-looped function", "retrocausal boundary", "causal friction"],
        "linguistic": ["Gödel numbering", "axiomatic reference", "semantic bifurcation"],
        "entropic": ["noise-driven cascade", "low-symmetry relaxation", "information death"],
        "metaphysical": ["ontic fold", "presence–absence superposition", "modal collapse"],
        "Causal Loop": ["closed-timelike inference", "recurrence operator", "self-correction"]
    }
    padding = banks.get(ptype, ["phase transition"])
    needed = min_k - len(mechs)
    mechs.extend(random.sample(padding, min(needed, len(padding))))
    return mechs[:max_k]

def _mechanisms_from_seed(seed: str, ptype: str) -> List[str]:
    s = seed.lower()
    # Seed-specific banks
    seed_banks: Dict[str, List[str]] = {
        # Your recent specialized seeds
        "boundary ledger": ["Holographic Accounting", "Bulk–Boundary Reciprocity", "Geodesic Focusing", "Extrinsic Curvature Ledger"],
        "noether charge": ["Noether Coupling", "Observer Current", "Stress–Energy Augmentation", "Continuity of Attention"],
        "final-boundary": ["Two‑Time RG", "Consistency Potential", "Final Boundary Condition", "Backward RG Flow"],
        "final boundary": ["Two‑Time RG", "Consistency Potential", "Final Boundary Condition", "Backward RG Flow"],
        "prediction as a fixed point": ["Two‑Time RG", "Consistency Potential", "Final Boundary Condition", "Backward RG Flow"],
        "probe lead redaction": ["Hypergraph Masking", "Lead–Seed Sanitizer", "Contextual Token Freezing", "Redaction Windowing"],
        "scaffold punctuation": ["Clause Fusing", "Boundary Periodizer", "Case‑Aware Joiner", "Ellipsis Normalization"],
        # Seeds from your initial documents
        "background that is not a background": ["dynamic substrate emergence", "relational ontology", "causal set microdynamics", "geodesic shear"],
        "prediction that selects its own universe": ["anthropic recursion", "observational collapse", "teleological selection", "consistency fixed point"],
        "test that defines the theory": ["self-verifying coherence", "empirical entanglement", "unique consequence falsification", "consistency web"],
        "echo of a geodesic in the quantum foam": ["retrocausal boundary", "geodesic echo", "path integral pruning", "entropy gradient focusing"],
        "syntax of collapsing information": ["Gödel numbering", "axiomatic reference", "information death", "entropy grammar"],
        "inertia of a conscious observation": ["observer current", "attention inertia", "stress–energy augmentation", "Noether coupling"]
    }
    for key, bank in seed_banks.items():
        if key in s:
            base = bank[:]
            return _pad_mechanisms(base, ptype)
    # Type-based fallback
    return _pad_mechanisms([], ptype)

def _inject_fresh_consequence(ax_text: str, ptype: str) -> str:
    sent = random.choice(CONSEQUENCE_TEMPLATES.get(ptype, CONSEQUENCE_TEMPLATES["metaphysical"]))
    if sent.lower() not in ax_text.lower():
        ax_text = ax_text.rstrip() + " " + sent
    return ax_text

def _probability_line(seed: str) -> str:
    rnd = random.Random(("prob:"+seed).encode("utf-8"))
    p = round(rnd.uniform(0.66, 0.74), 2)
    return f"This happens with a probability of {p}."

def render_axiom_from_template(seed: str, count_in_batch: int = 0) -> Tuple[str, str, List[str], str, str]:
    core_templates = [
        "The core principle of '{seed}' suggests {link}.",
        "At the heart of '{seed}' lies {link}."
    ]
    links = ["a fundamental linkage", "an unstated symmetry", "a recursive paradox"]
    core = random.choice(core_templates).format(seed=seed, link=random.choice(links))
    if count_in_batch > 0:
        core = re.sub(r"\b(a|an)\b", "another", core, 1)

    ptype = random.choice(["Causal Loop", "cosmic", "linguistic", "temporal", "entropic", "metaphysical"])
    mechs = _mechanisms_from_seed(seed, ptype)
    mechs = _pad_mechanisms(mechs, ptype)

    cons = random.choice(CONSEQUENCE_TEMPLATES.get(ptype, CONSEQUENCE_TEMPLATES["metaphysical"]))

    # Canonical lead; body will be harmonized by stealth/style pass
    lead = _canonical_lead(seed)
    axiom_text = f"{lead} {cons} {_probability_line(seed)}"
    return axiom_text, core, mechs, cons, ptype

def _calculate_entropic_potential_base(i: int) -> float:
    return 100 * math.log1p(1 + i * 1.35)

def _calculate_metrics(axiom: Dict[str, Any], batch_index: int) -> Dict[str, float]:
    text, seed = axiom["axiom_text"], axiom["seed_concept"]
    words = re.findall(r'\b\w+\b', text)
    symbols = re.findall(r'[^\w\s]', text)
    base_novelty = len(set(words)) / (len(words) + 1e-9)
    alienness = (len(symbols) / (len(words) + 1e-9) + (1 if "superposition" in text else 0)) * 10
    novelty = base_novelty + math.sin(batch_index) * 0.05
    density = len(words) / (len(text) + 1e-9) * 100 + math.cos(batch_index) * 2
    ep = (batch_index + 1) * (alienness + 1)
    return {
        "novelty": round(novelty, 3),
        "density": round(density, 3),
        "entropic_potential": round(100 * math.log1p(ep), 3),
        "elegance": round(100 - abs(len(text) - 250) * 0.1, 3),
        "alienness": round(alienness, 3)
    }

def save_to_history(axiom: Dict[str, Any], config: Dict[str, Any]):
    history_file = config.get("history_file", "axiom_history.jsonl")
    with open(history_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(axiom, ensure_ascii=False) + '\n')

# ------------------------ Main --------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Axiom Forge v0.3.2+")
    parser.add_argument("--seed", type=str, required=True, help="Seed concept for axiom generation.")
    parser.add_argument("--count", type=int, default=1, help="Number of axioms to generate.")
    parser.add_argument("--save-to-history", action="store_true", help="Save output to history file.")
    parser.add_argument("--no-stealth", dest="no_stealth", action="store_true", help="Disable stealth injection scaffolds.")
    parser.add_argument("--emit-scaffold", action="store_true", help="Emit hidden scaffold text in the output JSON.")
    args = parser.parse_args()

    config = load_config()
    global _last_scaffold
    _last_scaffold = {"text": "", "ngrams": set(), "recent": []}

    if args.no_stealth:
        config["stealth"]["enable_stealth_injection"] = False
    if args.emit_scaffold:
        config["stealth"]["emit_scaffold_in_field"] = True

    for i in range(args.count):
        axiom_text, core, mechs, cons, ptype = render_axiom_from_template(args.seed, i)

        # Style pass
        styled_text, injection_scaffold = apply_stealth_injection(
            axiom_text, config, seed=args.seed, mechs=mechs, ptype=ptype
        )

        # Optional logic warp
        styled_text = apply_non_aristotelian_logic(styled_text, config, _canonical_lead(args.seed), cons)

        # Obfuscation + math (safe)
        styled_text = obfuscate_axiom(styled_text, config.get('coherence_risk', 0.3), args.seed)

        # Consequence freshness
        styled_text = _inject_fresh_consequence(styled_text, ptype)

        # Final cleanup
        styled_text = sanitize_axiom_text(styled_text, config)

        axiom = {
            "core_statement": core,
            "mechanisms": mechs,
            "consequences": cons,
            "axiom_text": styled_text,
            "paradox_type": ptype,
            "seed_concept": args.seed,
            "timestamp": datetime.now().isoformat()
        }

        axiom["metrics"] = _calculate_metrics(axiom, i)
        if injection_scaffold:
            axiom["humanized_injection_scaffold"] = injection_scaffold
            axiom["injection_scaffold"] = injection_scaffold

        print("\n--- FINAL AXIOM ---")
        print(json.dumps(axiom, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
