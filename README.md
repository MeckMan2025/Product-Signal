# Product-Signal

A personal, non-commercial research tool that listens to **public** equipment-owner
discussion across several industry segments and organizes the common **product
pain points** by topic and manufacturer — entirely on local hardware.

> **Status:** early rebuild (v2). Pending Reddit Data API access approval under the
> [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy).
> No live data is collected until access is granted.

## What it does

1. **Read** public posts/comments from a fixed set of equipment-related subreddits
   (agriculture, construction, turf/landscaping, property care) via the Reddit
   Data API — **read-only**.
2. **Classify** each item locally with a pre-trained, on-device language model:
   segment, manufacturer(s) mentioned, product, and a product pain-point summary.
3. **Organize** the results locally — by topic and by manufacturer — into a private
   summary for personal analysis.

It does **not** post, comment, vote, or message. It has no interactive presence on
Reddit.

## Design principles & Reddit compliance

This project is built to operate as a legitimate, approved Data API application:

- **Approval first.** No API calls until Reddit grants access. Access is requested
  through Reddit's official process, not worked around.
- **Read-only.** No writes of any kind. App-only OAuth (`client_credentials`).
- **Inference, not training.** A pre-trained model *classifies* posts. Reddit data
  is **never** used to train or fine-tune any model, and no scraped dataset is
  built or shared.
- **Privacy by design.** The analysis is about **products and brands, not people.**
  Usernames are not stored, no Reddit data is linked to any off-platform identity,
  and no sensitive characteristics about users are inferred.
- **Non-commercial.** Personal research use only.
- **Polite by default.** Narrow subreddit scope, low request volume, rate-limit
  aware.

## Tech

Python · [PRAW](https://praw.readthedocs.io/) (Reddit Data API) · on-device LLM
inference · SQLite · config-driven profiles.

## Layout

```
config/        Segment / subreddit / manufacturer profile (editable)
src/product_signal/   Application package
tests/         Unit tests (Reddit + model mocked in CI)
.github/       CI
```

## Development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # fill in once API access is granted
pytest
```

## License & use

**© 2026 Andrew Meckley. All rights reserved. Proprietary — no license granted.**

This repository is public for reference and transparency only. **You may not use,
copy, modify, or distribute any part of this code without prior written
permission.** Viewing it on GitHub grants no rights. To request permission,
contact the owner via [GitHub](https://github.com/MeckMan2025). See [LICENSE](LICENSE).
