## Goal
Automate discovery of “new openings” in Helsinki and export a CSV with name, address, description, and tags.

## Constraint
A reliable “opened in last 6 months” timestamp is not consistently available in common place datasets/APIs, so I treated new openings as 
candidates discovered through “new opening” search signals and tracked “first seen”.

## Approach
- Discovery: run multiple query signals (e.g., “new restaurant Helsinki”, “grand opening restaurant Helsinki”) biased to Helsinki.
- Enrichment: call Place Details for formatted address, types (tags), website/URL, and editorial summary (description when available).
- Quality controls: basic chain keyword blacklist + deduping by normalized (name + address).
- Automation for “newness”: store a snapshot of previously seen venues; export “new since last run” as candidates that appear for the first 
time.

## Outputs
- helsinki_all_candidates.csv (full list)
- helsinki_new_since_last_run.csv (delta vs snapshot)
- helsinki_seen.csv (snapshot)

## Next improvements
- Better chain detection via brand clustering across addresses.
- Add ranking/confidence score for novelty and WoM fit.
- Schedule the script (daily/weekly) to build a stronger history and approximate “last 6 months” via first-seen timestamps.

