"""Shared test fixtures: a fake PRAW client backed by recorded sample data.

These let us exercise fetch logic end-to-end with NO live Reddit access.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from product_signal.config import Profile

FIXTURE_DIR = Path(__file__).parent / "fixtures"


class FakeSubmission:
    """Mimics the PRAW submission attributes that fetch.normalize_submission reads."""

    def __init__(self, data: dict):
        self.id = data["id"]
        self.title = data["title"]
        self.selftext = data["selftext"]
        self.subreddit = data["subreddit"]
        self.permalink = data["permalink"]
        self.score = data.get("score", 0)
        self.num_comments = data.get("num_comments", 0)
        self.created_utc = data.get("created_utc", 0.0)

    @property
    def fullname(self) -> str:
        return "t3_" + self.id


class FakeSubredditView:
    def __init__(self, submissions: list[FakeSubmission]):
        self._submissions = submissions

    def _listing(self, limit: int):
        return list(self._submissions)[:limit]

    def hot(self, limit: int = 25):
        return self._listing(limit)

    def new(self, limit: int = 25):
        return self._listing(limit)

    def rising(self, limit: int = 25):
        return self._listing(limit)

    def top(self, limit: int = 25):
        return self._listing(limit)


class FakeReddit:
    """Stand-in for praw.Reddit. read_only mirrors how we configure the real one."""

    def __init__(self, by_subreddit: dict[str, list[FakeSubmission]]):
        self._by_subreddit = by_subreddit
        self.read_only = True

    def subreddit(self, name: str) -> FakeSubredditView:
        return FakeSubredditView(self._by_subreddit.get(name, []))


@pytest.fixture
def sample_data() -> dict:
    return json.loads((FIXTURE_DIR / "sample_posts.json").read_text())


@pytest.fixture
def fake_reddit(sample_data) -> FakeReddit:
    by_subreddit = {
        sub: [FakeSubmission(post) for post in posts] for sub, posts in sample_data.items()
    }
    return FakeReddit(by_subreddit)


@pytest.fixture
def sample_profile() -> Profile:
    return Profile(
        segments={
            "agriculture": {"subreddits": ["farming"]},
            "turf_landscape": {"subreddits": ["lawncare"]},
        },
        manufacturers={},
    )
