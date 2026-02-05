    # --- Snapshot diff: "new since last run" ---
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

import os
import time
import re
...
    # --- Snapshot diff: "new since last run" ---
    snapshot_path = "data/snapshots/helsinki_seen.csv"

    # Identify venue by normalized (name + address)
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

    # Update snapshot (minimal columns)
    current[["name", "address"]].drop_duplicates().to_csv(snapshot_path, index=False)
    print(f"Updated snapshot: {snapshot_path}")
    # --- Snapshot diff: "new since last run" ---
    snapshot_path = "data/snapshots/helsinki_seen.csv"

    # Identify venue by normalized (name + address)
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

    # Update snapshot (minimal columns)
    current[["name", "address"]].drop_duplicates().to_csv(snapshot_path, index=False)
    print(f"Updated snapshot: {snapshot_path}")


