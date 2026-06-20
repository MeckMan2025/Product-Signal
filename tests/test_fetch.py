from product_signal import fetch


def test_normalize_has_no_author_field(fake_reddit):
    records = fetch.fetch_subreddit(fake_reddit, "farming", "agriculture", set())
    assert records, "expected sample submissions"
    record = records[0]
    # Privacy by design: never capture or store the author/username.
    for forbidden in ("author", "username", "user", "author_fullname"):
        assert forbidden not in record


def test_normalize_fields_and_permalink(fake_reddit):
    records = fetch.fetch_subreddit(fake_reddit, "farming", "agriculture", set())
    first = next(r for r in records if r["id"] == "t3_a1")
    assert first["segment"] == "agriculture"
    assert first["subreddit"] == "farming"
    assert first["is_comment"] == 0
    assert first["permalink"].startswith("https://reddit.com/r/farming/")
    assert first["score"] == 42


def test_fetch_subreddit_dedups_existing(fake_reddit):
    records = fetch.fetch_subreddit(fake_reddit, "farming", "agriculture", existing_ids={"t3_a1"})
    ids = {r["id"] for r in records}
    assert "t3_a1" not in ids
    assert "t3_a2" in ids


def test_fetch_all_covers_profile_without_sleeping(fake_reddit, sample_profile):
    calls = []
    records = fetch.fetch_all(fake_reddit, sample_profile, existing_ids=set(), sleep=calls.append)
    ids = {r["id"] for r in records}
    assert ids == {"t3_a1", "t3_a2", "t3_b1"}
    # both segments represented
    assert {r["segment"] for r in records} == {"agriculture", "turf_landscape"}
    # delay invoked once per subreddit (2), but no real time.sleep used
    assert len(calls) == 2


def test_fetch_all_respects_existing_ids(fake_reddit, sample_profile):
    records = fetch.fetch_all(fake_reddit, sample_profile, existing_ids={"t3_a1", "t3_b1"}, delay=0)
    assert {r["id"] for r in records} == {"t3_a2"}
