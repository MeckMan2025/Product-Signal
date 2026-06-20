"""Read-only fetch of public posts via PRAW: normalize, dedup, be polite.

Privacy by design: the author/username is intentionally NOT captured or stored.
Records describe the issue, not the person — per the Responsible Builder Policy's
zero-tolerance stance on profiling/re-identifying users.
"""

from __future__ import annotations

import time
from collections.abc import Iterable
from datetime import datetime, timezone

from .config import Profile

REDDIT_BASE = "https://reddit.com"
DEFAULT_LIMIT = 25
REQUEST_DELAY = 1.0  # polite pause (seconds) between subreddit reads


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _permalink(rel: str) -> str:
    if not rel:
        return ""
    return rel if rel.startswith("http") else REDDIT_BASE + rel


def normalize_submission(submission, segment: str, fetched_at: str) -> dict:
    """Map a PRAW submission to our normalized record. No author field by design."""
    return {
        "id": submission.fullname,  # stable id, e.g. t3_abc123
        "segment": segment,
        "subreddit": str(submission.subreddit),
        "title": submission.title or "",
        "body": (submission.selftext or "")[:5000],
        "permalink": _permalink(submission.permalink),
        "score": int(getattr(submission, "score", 0) or 0),
        "num_comments": int(getattr(submission, "num_comments", 0) or 0),
        "created_utc": float(getattr(submission, "created_utc", 0) or 0),
        "fetched_at": fetched_at,
        "is_comment": 0,
        "parent_id": None,
    }


def fetch_subreddit(
    reddit,
    subreddit_name: str,
    segment: str,
    existing_ids: Iterable[str],
    *,
    limit: int = DEFAULT_LIMIT,
    sort: str = "hot",
) -> list[dict]:
    """Fetch one subreddit's listing, skipping ids already seen."""
    seen = set(existing_ids)
    fetched_at = _now_iso()
    out: list[dict] = []
    listing = getattr(reddit.subreddit(subreddit_name), sort)(limit=limit)
    for submission in listing:
        record = normalize_submission(submission, segment, fetched_at)
        if record["id"] in seen:
            continue
        seen.add(record["id"])
        out.append(record)
    return out


def fetch_all(
    reddit,
    profile: Profile,
    existing_ids: Iterable[str],
    *,
    limit: int = DEFAULT_LIMIT,
    sort: str = "hot",
    delay: float = REQUEST_DELAY,
    sleep=time.sleep,
) -> list[dict]:
    """Fetch every (segment, subreddit) in the profile, deduped across the run."""
    seen = set(existing_ids)
    results: list[dict] = []
    for segment, subreddit_name in profile.subreddits():
        records = fetch_subreddit(reddit, subreddit_name, segment, seen, limit=limit, sort=sort)
        for record in records:
            seen.add(record["id"])
        results.extend(records)
        if delay:
            sleep(delay)
    return results
