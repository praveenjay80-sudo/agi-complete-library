import logging
import os
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import db, llm_curator, pipeline, seed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(title="AGI Complete Library")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


scheduler = AsyncIOScheduler()


@app.on_event("startup")
def startup():
    db.init_db()
    with db.session() as conn:
        result = seed.seed_if_empty(conn)
        if result["seeded"]:
            logger.info("Seeded library: %s", result)

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key:
        scheduler.add_job(_run_scheduled_update, "interval", days=1, id="scheduled_update")
        scheduler.start()
        logger.info("Scheduled daily auto-update enabled (server-side ANTHROPIC_API_KEY configured)")
    else:
        logger.info("No server-side ANTHROPIC_API_KEY configured -- scheduled auto-update disabled; manual Update Now still works")


async def _run_scheduled_update():
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    anthropic_model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
    google_books_key = os.environ.get("GOOGLE_BOOKS_API_KEY")
    openalex_key = os.environ.get("OPENALEX_API_KEY")
    with db.session() as conn:
        try:
            result = await pipeline.run_update(conn, "scheduled", anthropic_key, anthropic_model, google_books_key, openalex_key)
            logger.info("Scheduled update completed: %s", result)
        except Exception:
            logger.exception("Scheduled update failed")


@app.get("/api/meta")
def meta():
    with db.session() as conn:
        return db.get_meta_counts(conn)


@app.get("/api/categories")
def list_categories(kind: str | None = None):
    with db.session() as conn:
        if kind:
            rows = conn.execute(
                "SELECT c.*, (SELECT COUNT(*) FROM items i WHERE i.category_id=c.id) AS item_count "
                "FROM categories c WHERE c.kind=? OR c.kind='both' ORDER BY c.name",
                (kind,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT c.*, (SELECT COUNT(*) FROM items i WHERE i.category_id=c.id) AS item_count "
                "FROM categories c ORDER BY c.name"
            ).fetchall()
        return [dict(r) for r in rows]


@app.get("/api/items")
def list_items(kind: str | None = None, category_id: int | None = None, q: str | None = None):
    query = "SELECT i.*, c.name AS category_name FROM items i JOIN categories c ON c.id = i.category_id WHERE 1=1"
    params: list = []
    if kind:
        query += " AND i.kind=?"
        params.append(kind)
    if category_id:
        query += " AND i.category_id=?"
        params.append(category_id)
    if q:
        query += " AND (i.title LIKE ? OR i.authors LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    query += " ORDER BY (i.year IS NULL), i.year DESC, i.title"
    with db.session() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]


@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    with db.session() as conn:
        row = conn.execute("SELECT i.*, c.name AS category_name FROM items i JOIN categories c ON c.id=i.category_id WHERE i.id=?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(404, "item not found")
        return dict(row)


@app.get("/api/audit_log")
def audit_log(limit: int = 100):
    with db.session() as conn:
        rows = conn.execute(
            "SELECT a.*, i.title AS item_title FROM audit_log a LEFT JOIN items i ON i.id=a.item_id "
            "ORDER BY a.id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


@app.get("/api/update_runs")
def update_runs(limit: int = 20):
    with db.session() as conn:
        rows = conn.execute(
            "SELECT * FROM update_runs ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


class ModelsRequest(BaseModel):
    api_key: str


@app.post("/api/anthropic/models")
async def anthropic_models(req: ModelsRequest):
    try:
        return await llm_curator.list_available_models(req.api_key)
    except Exception as e:
        raise HTTPException(400, f"could not reach Anthropic: {e}")


class BackfillCoversRequest(BaseModel):
    google_books_key: str


@app.post("/api/backfill_covers")
async def backfill_covers(req: BackfillCoversRequest):
    """Fills in cover art for existing books that don't have any yet (e.g.
    the original seed set, which was transcribed from a PDF with no cover
    images). No Anthropic key needed -- this is pure Google Books lookup,
    no LLM judgment involved."""
    with db.session() as conn:
        try:
            return await pipeline.backfill_covers(conn, req.google_books_key)
        except Exception as e:
            raise HTTPException(500, f"backfill failed: {e}")


class UpdateRequest(BaseModel):
    anthropic_key: str
    anthropic_model: str
    google_books_key: str | None = None
    openalex_key: str | None = None


@app.post("/api/update")
async def trigger_update(req: UpdateRequest):
    with db.session() as conn:
        try:
            result = await pipeline.run_update(
                conn, "manual", req.anthropic_key, req.anthropic_model, req.google_books_key, req.openalex_key
            )
        except Exception as e:
            logger.exception("update run failed")
            raise HTTPException(500, f"update failed: {e}")
        return result


@app.post("/api/scheduled_update")
async def scheduled_update():
    """Manually fire the same job the daily scheduler runs, for testing.
    Requires server-side ANTHROPIC_API_KEY to be configured; otherwise use
    the Update Now button, which works regardless via keys from the browser."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(400, "no server-side ANTHROPIC_API_KEY configured; use the manual Update Now button instead")
    await _run_scheduled_update()
    return {"status": "triggered"}


app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
