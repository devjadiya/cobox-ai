# app/core/asset_loader.py
import csv
import json
from pathlib import Path
from typing import Dict, List


ASSET_CSV_PATH = Path("app/assets/library.csv")
ASSET_JSON_PATH = Path("app/data/assets.json")
ASSET_INDEX_PATH = Path("app/data/asset_index.json")


def load_assets() -> Dict[str, List[dict]]:
    """
    Loads asset CSV → JSON → builds index for fast lookup.
    Runs ONCE at app startup.
    """

    assets = []

    with open(ASSET_CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            assets.append(row)

    ASSET_JSON_PATH.write_text(json.dumps(assets, indent=2))

    index = {}
    for asset in assets:
        key = asset.get("type", "unknown")
        index.setdefault(key, []).append(asset)

    ASSET_INDEX_PATH.write_text(json.dumps(index, indent=2))
    return index
