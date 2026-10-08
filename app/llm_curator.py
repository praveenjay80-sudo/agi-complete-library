"""Grounded LLM curation: decide include/category/significance for a candidate
item using ONLY real fetched metadata (title, abstract, venue, citations,
publisher, objective_signal already determined). The LLM never invents facts
-- it classifies and summarizes what's given, and every call is logged to
audit_log with its full reasoning for retroactive review."""

import json

import httpx

ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODELS_URL = "https://api.anthropic.com/v1/models"
ANTHROPIC_VERSION = "2023-06-01"

# No hardcoded model-id allowlist on purpose -- Anthropic renames/deprecates
# model ids over time (confirmed concern: a fixed list here would silently
# break). Instead /api/anthropic/models (see main.py) queries Anthropic's
# own live model list at request time and the frontend's dropdown is
# populated from that response, filtered to the sonnet/opus/haiku families
# by substring match on the id -- not a fixed set of exact strings. The only
# validation left here is a light sanity check that the model id we were
# handed actually looks like a Claude model, to catch obvious mistakes
# without needing a code change whenever Anthropic ships a new version.
_ALLOWED_FAMILY_SUBSTRINGS = ("sonnet", "opus", "haiku")


def _validate_model(model: str) -> None:
    if not any(fam in model.lower() for fam in _ALLOWED_FAMILY_SUBSTRINGS):
        raise ValueError(
            f"model '{model}' doesn't look like a Sonnet/Opus/Haiku model id -- "
            "refusing to call an unexpected model"
        )


async def list_available_models(api_key: str) -> list[dict]:
    """Live-queries Anthropic's own model list (not hardcoded) and filters
    to Sonnet/Opus/Haiku by substring match on the id, so new model
    versions appear automatically and deprecated ones silently disappear
    from the dropdown instead of breaking the app."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            ANTHROPIC_MODELS_URL,
            headers={"x-api-key": api_key, "anthropic-version": ANTHROPIC_VERSION},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
    models = data.get("data", [])
    return [
        {"id": m["id"], "display_name": m.get("display_name", m["id"])}
        for m in models
        if any(fam in m["id"].lower() for fam in _ALLOWED_FAMILY_SUBSTRINGS)
    ]


def _category_rubric(conn, kind: str, limit_per_category: int = 3) -> str:
    """Builds a few-shot rubric from REAL existing items already in each
    category, so the LLM pattern-matches against established precedent
    rather than free-floating opinion."""
    cats = conn.execute(
        "SELECT id, name, description FROM categories WHERE kind=? OR kind='both' ORDER BY name",
        (kind,),
    ).fetchall()
    lines = []
    for c in cats:
        examples = conn.execute(
            "SELECT title, significance FROM items WHERE category_id=? ORDER BY RANDOM() LIMIT ?",
            (c["id"], limit_per_category),
        ).fetchall()
        ex_text = "; ".join(f'"{e["title"]}" -- {e["significance"]}' for e in examples) or "(no examples yet)"
        lines.append(f'- {c["name"]}: {c["description"] or ""}\n  Examples already included: {ex_text}')
    return "\n".join(lines)


async def judge_candidate(
    conn,
    api_key: str,
    model: str,
    kind: str,
    title: str,
    authors: str,
    year: int | None,
    venue: str | None,
    abstract_or_description: str,
    objective_signal: str,
) -> dict:
    """Returns {"include": bool, "category": str, "is_new_category": bool,
    "new_category_description": str|None, "significance": str, "reasoning": str}.
    Raises on API failure -- caller decides whether to skip or retry."""
    _validate_model(model)

    rubric = _category_rubric(conn, kind)

    prompt = f"""You are curating an AGI/AI research library. You will decide whether a real candidate item (fetched from a real API, not invented) belongs in the library, and if so, which category.

CANDIDATE (real metadata, not invented):
Kind: {kind}
Title: {title}
Authors: {authors}
Year: {year or "unknown"}
Venue/Publisher: {venue or "unknown"}
Abstract/Description: {abstract_or_description[:2000]}

Objective signal already confirmed (real, not your judgment): {objective_signal}

EXISTING CATEGORIES AND REAL EXAMPLES ALREADY IN THIS LIBRARY (your rubric -- match this bar, don't invent a stricter or looser one):
{rubric}

Instructions:
- Base your decision ONLY on the real metadata given above. Do not invent facts, citation counts, or claims not present in the abstract/description.
- You MAY propose a genuinely new category if this item doesn't fit any existing one well AND represents a real distinct cluster (not just one oddball item) -- the library is meant to expand its taxonomy over time, not force everything into stale buckets.
- Err toward inclusion when the objective signal is real and the abstract plausibly fits an AGI/AI-research library -- this library aims to be broad and current, not narrowly gatekept.
- Write "significance" as a one-sentence paraphrase of what the abstract/description itself claims -- do not add outside claims.

Respond with ONLY a JSON object, no markdown fences, no preamble:
{{
  "include": true or false,
  "category": "exact existing category name, or a new proposed name",
  "is_new_category": true or false,
  "new_category_description": "one sentence, only if is_new_category is true, else null",
  "significance": "one sentence grounded in the abstract/description",
  "reasoning": "1-2 sentences on why you included/excluded and chose this category"
}}"""

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            ANTHROPIC_MESSAGES_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": ANTHROPIC_VERSION,
                "content-type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

    text = data["content"][0]["text"].strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON object in LLM response: {text[:200]}")
    return json.loads(text[start : end + 1])


async def propose_book_candidates(conn, api_key: str, model: str, n: int = 10) -> list[dict]:
    """Asks the LLM to name real, already-published books it is confident
    exist and that would fit this library, which aren't in it yet. This is
    the one place the LLM free-recalls rather than classifies given data --
    so every proposal is treated as unverified and must be independently
    confirmed against Google Books (see pipeline.py) before it can be
    judged or added. A title Google Books can't find is discarded, which
    is what catches hallucinated titles/authors."""
    _validate_model(model)

    existing = conn.execute("SELECT title, authors FROM items WHERE kind='book'").fetchall()
    existing_text = "\n".join(f"- {r['title']} by {r['authors']}" for r in existing)

    prompt = f"""You are helping expand a library of real, published books about AGI, AI, machine learning, philosophy of mind, cognitive science, and AI ethics/governance.

BOOKS ALREADY IN THE LIBRARY (do not repeat these):
{existing_text}

Name {n} more REAL, ALREADY-PUBLISHED books (not forthcoming/rumored) that belong in this library and are not in the list above. Only name books you are confident actually exist and were written by the author you name -- every one of these will be independently verified against Google Books and discarded if not found, so do not guess or pad the list with uncertain titles.

Respond with ONLY a JSON array, no markdown fences, no preamble:
[{{"title": "...", "author": "..."}}, ...]"""

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            ANTHROPIC_MESSAGES_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": ANTHROPIC_VERSION,
                "content-type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()

    text = data["content"][0]["text"].strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON array in LLM response: {text[:200]}")
    return json.loads(text[start : end + 1])
