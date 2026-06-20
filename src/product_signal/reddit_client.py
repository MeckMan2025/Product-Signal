"""Reddit Data API client (PRAW). Read-only, app-only OAuth, compliant User-Agent.

We never request write scopes. PRAW is configured read-only and patient under
rate limits (it waits rather than erroring), in line with the Responsible
Builder Policy's "respect the limits" requirement.
"""

from __future__ import annotations

from . import __version__
from .config import RedditCredentials

# Reddit's required format: <platform>:<app id>:<version> (by /u/<username>)
USER_AGENT_TEMPLATE = "macos:com.productsignal.research:v{version} (by /u/{username})"

# Wait up to this long for rate-limit windows instead of raising.
RATELIMIT_SECONDS = 600


def build_user_agent(username: str, version: str = __version__) -> str:
    """Build a Reddit-compliant, descriptive User-Agent string."""
    return USER_AGENT_TEMPLATE.format(version=version, username=username)


def create_reddit(creds: RedditCredentials):
    """Create a read-only PRAW Reddit instance using app-only OAuth.

    PRAW is imported lazily so unit tests / CI don't need it installed or a
    network connection — they inject a fake client instead.
    """
    import praw

    reddit = praw.Reddit(
        client_id=creds.client_id,
        client_secret=creds.client_secret,
        user_agent=build_user_agent(creds.username),
        ratelimit_seconds=RATELIMIT_SECONDS,
    )
    reddit.read_only = True
    return reddit
