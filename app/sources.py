"""Real, grounded discovery clients. No invented data -- every field returned
here comes directly from the source API's own response."""

import xml.etree.ElementTree as ET

import httpx

USER_AGENT = "agi-library/1.0 (https://github.com/praveenjay80-sudo/agi-library; mailto:praveen.jay80@gmail.com)"

ARXIV_API_URL = "https://export.arxiv.org/api/query"
ARXIV_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.NE", "cs.RO"]

OPENALEX_WORKS_URL = "https://api.openalex.org/works"

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"

_ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


async def fetch_new_arxiv_papers(days_back: int = 7, max_results: int = 50) -> list[dict]:
    """Real new submissions from arXiv's own API, sorted by submission date.
    No filtering/scoring happens here -- that's the curator's job."""
    cat_query = " OR ".join(f"cat:{c}" for c in ARXIV_CATEGORIES)
    params = {
        "search_query": cat_query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(ARXIV_API_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)

    papers = []
    for entry in root.findall("atom:entry", _ATOM_NS):
        arxiv_id = entry.find("atom:id", _ATOM_NS).text.rsplit("/", 1)[-1]
        title = entry.find("atom:title", _ATOM_NS).text.strip().replace("\n", " ")
        summary = entry.find("atom:summary", _ATOM_NS).text.strip().replace("\n", " ")
        authors = [a.find("atom:name", _ATOM_NS).text for a in entry.findall("atom:author", _ATOM_NS)]
        published = entry.find("atom:published", _ATOM_NS).text
        primary_cat_el = entry.find("arxiv:primary_category", _ATOM_NS)
        primary_cat = primary_cat_el.get("term") if primary_cat_el is not None else None
        papers.append({
            "arxiv_id": arxiv_id,
            "title": title,
            "abstract": summary,
            "authors": ", ".join(authors),
            "year": int(published[:4]),
            "primary_category": primary_cat,
            "source_url": f"https://arxiv.org/abs/{arxiv_id}",
        })
    return papers


async def lookup_openalex_work(title: str, author: str | None = None, api_key: str | None = None) -> dict | None:
    """Looks up a work by title (optionally filtered by author name) and
    returns its real citation count, venue, and OpenAlex id. Returns None
    if no confident match found. Deliberately does NOT just take the top
    title-search result -- confirmed live that naive title search can
    return book reviews or unrelated same-title works instead of the real
    item (e.g. Bostrom's "Superintelligence" top-matched a book review with
    2000 citations and zero listed authors, not the actual book).

    OpenAlex's public API works fine with no key at all (the User-Agent's
    mailto already gets us the "polite pool" rate limit) -- api_key is only
    for users on OpenAlex's premium tier who want its higher limits;
    omit it entirely and nothing changes."""
    params = {
        "filter": f"title.search:{title}",
        "select": "id,title,publication_year,type,cited_by_count,authorships,primary_location",
        "per-page": 10,
    }
    if api_key:
        params["api_key"] = api_key
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(OPENALEX_WORKS_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=20)
        resp.raise_for_status()
        results = resp.json().get("results", [])

    if not author:
        return _first_real_match(results)

    author_lower = author.lower()
    for r in results:
        names = [a["author"]["display_name"].lower() for a in r.get("authorships", [])]
        if any(author_lower in n or n in author_lower for n in names):
            return _to_openalex_summary(r)
    return None


def _first_real_match(results: list[dict]) -> dict | None:
    # Prefer entries that actually have a listed author over review/other
    # types with no authorships -- a weak heuristic, not a guarantee, which
    # is exactly why book citation counts are treated as a soft signal.
    for r in results:
        if r.get("authorships"):
            return _to_openalex_summary(r)
    return _to_openalex_summary(results[0]) if results else None


def _to_openalex_summary(r: dict) -> dict:
    venue = None
    loc = r.get("primary_location") or {}
    source = loc.get("source") or {}
    venue = source.get("display_name")
    return {
        "openalex_id": r["id"].rsplit("/", 1)[-1],
        "title": r["title"],
        "year": r.get("publication_year"),
        "type": r.get("type"),
        "citation_count": r.get("cited_by_count"),
        "venue": venue,
    }


async def lookup_google_books(title: str, author: str | None, api_key: str) -> dict | None:
    """Real rating/cover/publisher data. Confirmed live that rating volume
    is thin (e.g. 4 ratings for Bostrom's Superintelligence) -- treat as a
    weak corroborating signal, not a gate, and don't over-index on it.
    Requires a real key -- anonymous/shared-IP requests hit a hard 429
    quota wall (quota_limit_value "0"), confirmed live."""
    q = title if not author else f"{title} {author}"
    params = {"q": q, "key": api_key}
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(GOOGLE_BOOKS_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=20)
        resp.raise_for_status()
        items = resp.json().get("items", [])

    if not items:
        return None
    vi = items[0]["volumeInfo"]
    image_links = vi.get("imageLinks", {})
    return {
        "title": vi.get("title"),
        "authors": vi.get("authors"),
        "publisher": vi.get("publisher"),
        "published_date": vi.get("publishedDate"),
        "rating": vi.get("averageRating"),
        "rating_count": vi.get("ratingsCount"),
        "cover_url": image_links.get("thumbnail") or image_links.get("smallThumbnail"),
        "description": vi.get("description"),
    }
