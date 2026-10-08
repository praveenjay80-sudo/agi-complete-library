"""Orchestrates one full update run: discover candidates, attach a real
objective signal to each, let the LLM judge, write accepted items + a full
audit trail. Used by both the manual "Update Now" endpoint and the
optional scheduled job -- same function either way, so behavior never
diverges between the two triggers."""

import asyncio
import logging

import httpx

from . import llm_curator, sources

logger = logging.getLogger(__name__)

MAX_PAPER_CANDIDATES = 15
MAX_BOOK_CANDIDATES = 10
MAX_COVER_BACKFILL = 80
GOOGLE_BOOKS_THROTTLE_SECONDS = 1.0


async def _lookup_google_books_throttled(title: str, author: str | None, api_key: str):
    """Google Books' free tier trips a per-second burst limit well before
    its daily quota -- confirmed live firing 70 requests back-to-back with
    no delay got a 429 on every single one. One retry-after-backoff plus a
    fixed throttle between calls keeps a full-library backfill reliable."""
    try:
        return await sources.lookup_google_books(title, author, api_key)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            await asyncio.sleep(5)
            return await sources.lookup_google_books(title, author, api_key)
        raise


async def backfill_covers(conn, google_books_key: str) -> dict:
    """Seed books never went through the Google Books lookup (seed.py only
    has what the source PDF printed: title/authors/year/significance), so
    they have no cover_url and render as a placeholder icon in the UI. This
    fills in cover_url (and publisher/rating, when missing) for existing
    books by looking each one up on Google Books -- no LLM call, no
    inclusion judgment, just enrichment of items already in the library."""
    rows = conn.execute(
        "SELECT id, title, authors FROM items WHERE kind='book' AND cover_url IS NULL LIMIT ?",
        (MAX_COVER_BACKFILL,),
    ).fetchall()
    updated = 0
    not_found = 0
    for row in rows:
        try:
            gb = await _lookup_google_books_throttled(row["title"], row["authors"], google_books_key)
        except Exception as e:
            logger.warning("Google Books lookup failed for %r: %s", row["title"], e)
            continue
        await asyncio.sleep(GOOGLE_BOOKS_THROTTLE_SECONDS)
        if not gb or not gb.get("cover_url"):
            not_found += 1
            continue
        conn.execute(
            "UPDATE items SET cover_url=?, "
            "publisher=COALESCE(publisher, ?), "
            "google_books_rating=COALESCE(google_books_rating, ?), "
            "google_books_rating_count=COALESCE(google_books_rating_count, ?) "
            "WHERE id=?",
            (gb["cover_url"], gb.get("publisher"), gb.get("rating"), gb.get("rating_count"), row["id"]),
        )
        # Commit immediately, not after the whole loop -- the write lock
        # must not stay open across the next (throttled, network-bound)
        # iteration, or any other request touching the DB meanwhile times
        # out with "database is locked".
        conn.commit()
        updated += 1
    return {"checked": len(rows), "covers_added": updated, "no_cover_found": not_found}


def _title_exists(conn, kind: str, title: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM items WHERE kind=? AND lower(title)=lower(?)", (kind, title)
    ).fetchone()
    return row is not None


def _resolve_category(conn, kind: str, name: str, is_new: bool, new_description: str | None) -> tuple[int, bool]:
    row = conn.execute("SELECT id FROM categories WHERE lower(name)=lower(?)", (name,)).fetchone()
    if row:
        return row["id"], False
    cur = conn.execute(
        "INSERT INTO categories (name, kind, description, created_by) VALUES (?,?,?,'llm')",
        (name, kind, new_description or ""),
    )
    return cur.lastrowid, True


async def run_update(
    conn, trigger: str, anthropic_key: str, anthropic_model: str,
    google_books_key: str | None, openalex_key: str | None = None,
) -> dict:
    cur = conn.execute(
        "INSERT INTO update_runs (trigger, status) VALUES (?, 'running')", (trigger,)
    )
    run_id = cur.lastrowid
    conn.commit()

    candidates_seen = 0
    items_added = 0
    categories_created = 0
    covers_added = 0

    try:
        if google_books_key:
            try:
                backfill = await backfill_covers(conn, google_books_key)
                covers_added = backfill["covers_added"]
            except Exception as e:
                logger.warning("Cover backfill failed: %s", e)

        # ---- Papers: real new arXiv submissions, corroborated with OpenAlex citation data ----
        papers = await sources.fetch_new_arxiv_papers(max_results=MAX_PAPER_CANDIDATES)
        for p in papers:
            candidates_seen += 1
            if _title_exists(conn, "paper", p["title"]):
                continue

            first_author = p["authors"].split(",")[0].strip() if p["authors"] else None
            try:
                oa = await sources.lookup_openalex_work(p["title"], first_author, openalex_key)
            except Exception as e:
                logger.warning("OpenAlex lookup failed for %r: %s", p["title"], e)
                oa = None

            if oa and oa.get("citation_count"):
                objective_signal = f"OpenAlex match: {oa['citation_count']} citations, venue={oa.get('venue') or 'unknown'}"
            else:
                objective_signal = "New arXiv preprint, not yet indexed/cited on OpenAlex"

            try:
                verdict = await llm_curator.judge_candidate(
                    conn, anthropic_key, anthropic_model, "paper",
                    p["title"], p["authors"], p["year"], p.get("primary_category"),
                    p["abstract"], objective_signal,
                )
            except Exception as e:
                logger.warning("LLM judge failed for %r: %s", p["title"], e)
                continue

            if not verdict.get("include"):
                conn.execute(
                    "INSERT INTO audit_log (action, reason, source, objective_signal, llm_reasoning) VALUES "
                    "('reject', ?, 'arxiv', ?, ?)",
                    (p["title"], objective_signal, verdict.get("reasoning")),
                )
                conn.commit()
                continue

            cat_id, created = _resolve_category(
                conn, "paper", verdict["category"], verdict.get("is_new_category", False),
                verdict.get("new_category_description"),
            )
            if created:
                categories_created += 1

            item_cur = conn.execute(
                "INSERT INTO items (kind, title, authors, year, venue, category_id, significance, "
                "source_url, arxiv_id, openalex_id, citation_count, added_by) "
                "VALUES ('paper', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'llm')",
                (
                    p["title"], p["authors"], p["year"], oa.get("venue") if oa else p.get("primary_category"),
                    cat_id, verdict.get("significance"), p["source_url"], p["arxiv_id"],
                    oa.get("openalex_id") if oa else None, oa.get("citation_count") if oa else None,
                ),
            )
            conn.execute(
                "INSERT INTO audit_log (item_id, action, reason, source, objective_signal, llm_reasoning) VALUES "
                "(?, 'add', ?, 'arxiv', ?, ?)",
                (item_cur.lastrowid, p["title"], objective_signal, verdict.get("reasoning")),
            )
            conn.commit()
            items_added += 1

        # ---- Books: LLM proposes real titles, Google Books independently verifies each ----
        if google_books_key:
            try:
                proposals = await llm_curator.propose_book_candidates(conn, anthropic_key, anthropic_model, n=MAX_BOOK_CANDIDATES)
            except Exception as e:
                logger.warning("Book proposal failed: %s", e)
                proposals = []

            for prop in proposals:
                candidates_seen += 1
                title, author = prop.get("title"), prop.get("author")
                if not title or _title_exists(conn, "book", title):
                    continue

                try:
                    gb = await _lookup_google_books_throttled(title, author, google_books_key)
                except Exception as e:
                    logger.warning("Google Books lookup failed for %r: %s", title, e)
                    gb = None
                await asyncio.sleep(GOOGLE_BOOKS_THROTTLE_SECONDS)

                if not gb:
                    conn.execute(
                        "INSERT INTO audit_log (action, reason, source, objective_signal) VALUES "
                        "('reject', ?, 'llm-proposal', 'no Google Books match -- unverifiable, possibly hallucinated')",
                        (title,),
                    )
                    conn.commit()
                    continue

                signal_parts = []
                if gb.get("publisher"):
                    signal_parts.append(f"publisher={gb['publisher']}")
                if gb.get("rating"):
                    signal_parts.append(f"Google Books rating={gb['rating']} ({gb.get('rating_count') or 0} ratings)")
                objective_signal = "Verified on Google Books: " + ("; ".join(signal_parts) or "listing found, no rating data")

                year = None
                if gb.get("published_date"):
                    year = int(str(gb["published_date"])[:4]) if str(gb["published_date"])[:4].isdigit() else None

                try:
                    verdict = await llm_curator.judge_candidate(
                        conn, anthropic_key, anthropic_model, "book",
                        gb.get("title") or title, ", ".join(gb.get("authors") or [author or ""]),
                        year, gb.get("publisher"), gb.get("description") or "", objective_signal,
                    )
                except Exception as e:
                    logger.warning("LLM judge failed for %r: %s", title, e)
                    continue

                if not verdict.get("include"):
                    conn.execute(
                        "INSERT INTO audit_log (action, reason, source, objective_signal, llm_reasoning) VALUES "
                        "('reject', ?, 'google-books', ?, ?)",
                        (title, objective_signal, verdict.get("reasoning")),
                    )
                    conn.commit()
                    continue

                cat_id, created = _resolve_category(
                    conn, "book", verdict["category"], verdict.get("is_new_category", False),
                    verdict.get("new_category_description"),
                )
                if created:
                    categories_created += 1

                item_cur = conn.execute(
                    "INSERT INTO items (kind, title, authors, year, publisher, category_id, significance, "
                    "google_books_rating, google_books_rating_count, added_by, cover_url) "
                    "VALUES ('book', ?, ?, ?, ?, ?, ?, ?, ?, 'llm', ?)",
                    (
                        gb.get("title") or title, ", ".join(gb.get("authors") or [author or ""]), year,
                        gb.get("publisher"), cat_id, verdict.get("significance"),
                        gb.get("rating"), gb.get("rating_count"), gb.get("cover_url"),
                    ),
                )
                conn.execute(
                    "INSERT INTO audit_log (item_id, action, reason, source, objective_signal, llm_reasoning) VALUES "
                    "(?, 'add', ?, 'google-books', ?, ?)",
                    (item_cur.lastrowid, title, objective_signal, verdict.get("reasoning")),
                )
                conn.commit()
                items_added += 1

        conn.execute(
            "UPDATE update_runs SET finished_at=datetime('now'), candidates_seen=?, items_added=?, "
            "categories_created=?, status='completed' WHERE id=?",
            (candidates_seen, items_added, categories_created, run_id),
        )
        conn.commit()
        return {
            "run_id": run_id,
            "candidates_seen": candidates_seen,
            "items_added": items_added,
            "categories_created": categories_created,
            "covers_added": covers_added,
            "status": "completed",
        }
    except Exception as e:
        conn.execute(
            "UPDATE update_runs SET finished_at=datetime('now'), status='failed', error=? WHERE id=?",
            (str(e), run_id),
        )
        conn.commit()
        raise
