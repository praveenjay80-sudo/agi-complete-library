"""Real, grounded discovery clients. No invented data -- every field returned
here comes directly from the source API's own response."""

import random
from datetime import datetime, timezone

import httpx

USER_AGENT = "agi-library/1.0 (https://github.com/praveenjay80-sudo/agi-library; mailto:praveen.jay80@gmail.com)"

OPENALEX_WORKS_URL = "https://api.openalex.org/works"

# AI/ML/AGI terms for OpenAlex's relevance search, combined with a real
# citation-count filter -- discovery starts from papers that are ALREADY
# demonstrably cited, rather than sampling arXiv's newest submissions and
# hoping a few turn out cited. Confirmed live: "newest arXiv first" always
# returns same-day preprints with zero citations (no time to accrue any),
# and even a random older arXiv slice mostly returns uncited papers --
# citation counts follow a power law, so most papers never get cited at
# all. Starting from OpenAlex's own citation ranking is the only reliable
# way to find papers with a real importance signal.
AI_SEARCH_TERMS = (
    "artificial general intelligence OR large language model OR deep learning "
    "OR reinforcement learning OR transformer architecture OR neural network "
    "OR machine learning"
)
CITED_PAPERS_MIN_CITATIONS = 15
# A handful of OpenAlex records carry implausible citation counts relative
# to their age/venue (confirmed live: two Dagstuhl/LIPIcs proceedings
# entries showing 70k+ and 13k+ citations within ~2 years of publication --
# almost certainly a data merge artifact, not real impact). Papers that
# genuinely hit this citation velocity are rare, well-known landmarks
# (already in the seed set) -- so cap trust rather than propagate the
# artifact into the library.
IMPLAUSIBLE_CITATION_VELOCITY_PER_YEAR = 3000

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"


def _reconstruct_abstract(inverted_index: dict | None) -> str:
    """OpenAlex gives abstracts as a word -> [positions] inverted index
    (a copyright-driven quirk of their API), not plain text."""
    if not inverted_index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, idxs in inverted_index.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)


async def discover_cited_papers(max_results: int = 25, api_key: str | None = None) -> list[dict]:
    """Already-cited AI/ML/AGI papers straight from OpenAlex's own citation
    ranking -- title, authors, venue, year, citation count, and abstract
    all come directly from this one query, no separate per-candidate
    lookup needed. Picks a random recent-ish publication year (giving real
    citation-accrual time) and a random results page each call so repeated
    Update Now runs sample different parts of the ranking."""
    now_year = datetime.now(timezone.utc).year
    # 1-4 years old: old enough for citations to have accrued, recent
    # enough to still be "regular updates" to the library.
    year = random.choice([now_year - 1, now_year - 2, now_year - 3, now_year - 4])
    params = {
        "search": AI_SEARCH_TERMS,
        "filter": f"type:article,publication_year:{year},cited_by_count:>{CITED_PAPERS_MIN_CITATIONS}",
        "sort": "cited_by_count:desc",
        "per-page": max_results,
        "page": random.randint(1, 4),
        "select": "id,title,publication_year,cited_by_count,authorships,primary_location,ids,abstract_inverted_index",
    }
    if api_key:
        params["api_key"] = api_key
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(OPENALEX_WORKS_URL, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
        resp.raise_for_status()
        results = resp.json().get("results", [])

    papers = []
    for r in results:
        pub_year = r.get("publication_year") or year
        citations = r.get("cited_by_count") or 0
        years_old = max(1, now_year - pub_year)
        if citations / years_old > IMPLAUSIBLE_CITATION_VELOCITY_PER_YEAR:
            continue  # likely a data artifact, not real impact -- see module docstring note above

        authors = [a["author"]["display_name"] for a in r.get("authorships", [])]
        venue = ((r.get("primary_location") or {}).get("source") or {}).get("display_name")
        doi = r.get("ids", {}).get("doi")
        papers.append({
            "title": r["title"],
            "abstract": _reconstruct_abstract(r.get("abstract_inverted_index")),
            "authors": ", ".join(authors),
            "year": pub_year,
            "venue": venue,
            "citation_count": citations,
            "openalex_id": r["id"].rsplit("/", 1)[-1],
            "source_url": doi or r["id"],
        })
    return papers


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
