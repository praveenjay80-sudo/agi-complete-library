import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "library.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    kind TEXT NOT NULL CHECK(kind IN ('book','paper','both')),
    description TEXT,
    created_by TEXT NOT NULL DEFAULT 'seed',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL CHECK(kind IN ('book','paper')),
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    venue TEXT,
    publisher TEXT,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    significance TEXT,
    source_url TEXT,
    arxiv_id TEXT,
    openalex_id TEXT,
    citation_count INTEGER,
    google_books_rating REAL,
    google_books_rating_count INTEGER,
    cover_url TEXT,
    added_by TEXT NOT NULL DEFAULT 'seed',
    added_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(kind, title, authors)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER REFERENCES items(id),
    action TEXT NOT NULL,
    reason TEXT,
    source TEXT,
    objective_signal TEXT,
    llm_reasoning TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS update_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT,
    trigger TEXT NOT NULL,
    candidates_seen INTEGER DEFAULT 0,
    items_added INTEGER DEFAULT 0,
    categories_created INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'running',
    error TEXT
);
"""


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with session() as conn:
        conn.executescript(SCHEMA)


@contextmanager
def session():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def get_meta_counts(conn):
    books = conn.execute("SELECT COUNT(*) c FROM items WHERE kind='book'").fetchone()["c"]
    papers = conn.execute("SELECT COUNT(*) c FROM items WHERE kind='paper'").fetchone()["c"]
    categories = conn.execute("SELECT COUNT(*) c FROM categories").fetchone()["c"]
    last_run = conn.execute(
        "SELECT finished_at, items_added, categories_created FROM update_runs "
        "WHERE status='completed' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return {
        "books": books,
        "papers": papers,
        "categories": categories,
        "last_update": dict(last_run) if last_run else None,
    }
