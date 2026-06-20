"""Configuration: load + validate credentials and the scope profile.

Fails loudly when required Reddit credentials are missing — the prototype's
silent failure (missing env vars treated as "no posts") is what we're fixing.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv

REQUIRED_ENV = ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROFILE = PROJECT_ROOT / "config" / "profile.yaml"


@dataclass(frozen=True)
class RedditCredentials:
    client_id: str
    client_secret: str
    username: str


@dataclass(frozen=True)
class Profile:
    """The editable scope: which segments/subreddits and manufacturer aliases."""

    segments: dict
    manufacturers: dict

    def subreddits(self) -> list[tuple[str, str]]:
        """Flatten to (segment, subreddit) pairs, preserving order."""
        pairs: list[tuple[str, str]] = []
        for segment, cfg in self.segments.items():
            for sub in (cfg or {}).get("subreddits", []):
                pairs.append((segment, sub))
        return pairs


def load_env(dotenv_path: str | os.PathLike | None = None) -> None:
    """Load .env into the process environment (no-op if the file is absent)."""
    load_dotenv(dotenv_path)


def get_credentials(env: dict | None = None) -> RedditCredentials:
    """Read + validate Reddit credentials. Raises RuntimeError if any are missing."""
    env = env if env is not None else os.environ
    missing = [key for key in REQUIRED_ENV if not env.get(key)]
    if missing:
        raise RuntimeError(
            "Missing required Reddit env var(s): "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill them in (after API access is granted)."
        )
    return RedditCredentials(
        client_id=env["REDDIT_CLIENT_ID"],
        client_secret=env["REDDIT_CLIENT_SECRET"],
        username=env["REDDIT_USERNAME"],
    )


def load_profile(path: str | os.PathLike | None = None) -> Profile:
    """Load the scope profile YAML."""
    profile_path = Path(path) if path else DEFAULT_PROFILE
    data = yaml.safe_load(profile_path.read_text()) or {}
    return Profile(
        segments=data.get("segments") or {},
        manufacturers=data.get("manufacturers") or {},
    )
