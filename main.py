import os
import time
import re

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
if not API_KEY:
    raise SystemExit("Missing GOOGLE_PLACES_API_KEY in .env")

TEXTSEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
import os
import time
import re

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
if not API_KEY:
    raise SystemExit("Missing GOOGLE_PLACES_API_KEY in .env")

TEXTSEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

HELSINKI_LOCATION = "60.1699,24.9384"

DISCOVERY_QUERIES = [
    "new restaurant Helsinki",
    "newly opened restaurant Helsinki",
    "grand opening restaurant Helsinki",
    "new café Helsinki",
    "new coffee shop Helsinki",
]

CHAIN_KEYWORDS = [
    "mcdonald", "subway", "hesburger", "burger king", "kfc", "pizza hut",
    "boneless", "starbucks",
]

def normalize_name(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9äöå\s-]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

def is_chain_like(name: str) -> bool:
    n = normalize_name(name)
    return any(k in n for k in CHAIN_KEYWORDS)

def text_search(query: str):
    params = {
        "query": query,
        "key": API_KEY,
        "location": HELSINKI_LOCATION,
        "radius": 15000,
    }
    r = requests.get(TEXTSEARCH_URL, params=params, timeout=30)
    return r.json()

def place_details(place_id: str):
    fields = [
        "name",
        "formatted_address",
        "types",
        "url",
        "website",
        "editorial_summary",
    ]
    params = {
        "place_id": place_id,
        "fields": ",".join(fields),
        "key": API_KEY,
    }
    r = requests.get(DETAILS_URL, params=params, timeout=30)
    return r.json()

def build_description(res: dict) -> str:
    editorial = res.get("editorial_summary")
    if isinstance(editorial, dict) and editorial.get("overview"):
        return editorial["overview"].strip()

    types = res.get("types") or []
    if types:
        pretty = ", ".join(types[:5]).replace("_", " ")
        return f"Venue types: {pretty}."
    return "No description available."

def build_tags(res: dict) -> str:
    types = res.get("types") or []
    tags = [t.replace("_", " ") for t in types][:10]
    return "|".join(tags)

def main():
    seen = set()
    rows = []

    for q in DISCOVERY_QUERIES:
        print(f"Searching: {q}")
        data = text_search(q)
        status = data.get("status")

        if status not in ("OK", "ZERO_RESULTS"):
            print("  -> status:", status, "|", data.get("error_message", ""))
            continue

        for item in data.get("results", []):
            place_id = item.get("place_id")
            if not place_id or place_id in seen:
                continue
            seen.add(place_id)

            name = (item.get("name") or "").strip()
            if not name or is_chain_like(name):
                continue

            det = place_details(place_id)
            if det.get("status") != "OK":
                continue

            res = det.get("result", {})

            rows.append({
                "name": res.get("name", name),
                "address": res.get("formatted_address") or item.get("formatted_address", ""),
                "description": build_description(res),
                "tags": build_tags(res),
                "google_maps_url": res.get("url", ""),
                "website": res.get("website", ""),
                "source_query": q,
            })

            time.sleep(0.1)

    if not rows:
        print("No rows found.")
        return

    df = pd.DataFrame(rows)
    df["name_norm"] = df["name"].astype(str).str.lower().str.strip()
    df["addr_norm"] = df["address"].astype(str).str.lower().str.strip()
    df = df.drop_duplicates(subset=["name_norm", "addr_norm"]).drop(columns=["name_norm", "addr_norm"])

    os.makedirs("output", exist_ok=True)
    os.makedirs("data/snapshots", exist_ok=True)

    # Save all candidates
    all_path = "output/helsinki_all_candidates.csv"
    df.to_csv(all_path, index=False)
    print(f"Saved: {all_path} ({len(df)} rows)")

    # Snapshot diff
    snapshot_path = "data/snapshots/helsinki_seen.csv"

    current = df[["name", "address"]].copy()
    current["key"] = (
        current["name"].astype(str).str.lower().str.strip()
        + "||"
        + current["address"].astype(str).str.lower().str.strip()
    )

    if os.path.exists(snapshot_path):
        prev = pd.read_csv(snapshot_path)
        prev["key"] = (
            prev["name"].astype(str).str.lower().str.strip()
            + "||"
            + prev["address"].astype(str).str.lower().str.strip()
        )
        prev_keys = set(prev["key"].tolist())
    else:
        prev_keys = set()

    new_mask = ~current["key"].isin(prev_keys)
    new_df = df.loc[new_mask.values].copy()

    new_path = "output/helsinki_new_since_last_run.csv"
    new_df.to_csv(new_path, index=False)
    print(f"Saved: {new_path} ({len(new_df)} rows)")

    current[["name", "address"]].drop_duplicates().to_csv(snapshot_path, index=False)
    print(f"Updated snapshot: {snapshot_path}")

if __name__ == "__main__":
    main()

