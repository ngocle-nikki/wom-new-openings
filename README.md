# WoM Part 1 — New Openings (Helsinki)

This script fetches candidate “new openings” in Helsinki using Google Places API and exports results to CSV.

Because reliable opening dates are not consistently available in venue datasets, the script treats “new openings” as candidates discovered via 
query signals (e.g., “new restaurant Helsinki”) and supports automation via snapshot-diffing: places that appear for the first time are flagged 
as new since the last run.

## Setup

1. Create a Google Places API key (Billing enabled) and restrict it to **Places API**.
2. Create a `.env` file:

```bash
GOOGLE_PLACES_API_KEY=YOUR_KEY_HERE
```
3. Install dependencies:
- python3 -m venv .venv
- source .venv/bin/activate
- pip install requests python-dotenv pandas

## Run
- python3 main.py

## Outputs
- output/helsinki_all_candidates.csv: full candidate list (deduped)
- output/helsinki_new_since_last_run.csv: new candidates since previous snapshot (proxy for new openings)
- data/snapshots/helsinki_seen.csv: snapshot store (name + address)

## Notes / limitations
- Opening dates are not consistently available via Places APIs, so “opened in the last 6 months” is approximated using discovery queries + 
snapshot diffing (“first seen”).
- Chain filtering uses a simple keyword blacklist and can be expanded.


