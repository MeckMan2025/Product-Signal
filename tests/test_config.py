import pytest

from product_signal import config


def test_get_credentials_raises_when_missing():
    with pytest.raises(RuntimeError) as exc:
        config.get_credentials({"REDDIT_CLIENT_ID": "x"})
    assert "REDDIT_CLIENT_SECRET" in str(exc.value)
    assert "REDDIT_USERNAME" in str(exc.value)


def test_get_credentials_ok():
    creds = config.get_credentials(
        {
            "REDDIT_CLIENT_ID": "id",
            "REDDIT_CLIENT_SECRET": "secret",
            "REDDIT_USERNAME": "Lanky_Flounder2906",
        }
    )
    assert creds.client_id == "id"
    assert creds.username == "Lanky_Flounder2906"


def test_load_profile_reads_repo_profile():
    profile = config.load_profile()
    pairs = profile.subreddits()
    assert ("agriculture", "farming") in pairs
    # every entry is a (segment, subreddit) tuple
    assert all(len(p) == 2 for p in pairs)
