# app/core/asset_loader.py

import csv
from pathlib import Path
from typing import Dict, List

ASSET_CSV_PATH = Path("app/assets/library.csv")


def load_asset_index() -> Dict[str, List[dict]]:
    """
    Loads assets from CSV and builds an index like:
    {
        "floor": [...],
        "wall": [...],
        "door": [...],
        "decor": [...],
        "track": [...]
    }
    """

    index: Dict[str, List[dict]] = {
        "floor": [],
        "wall": [],
        "door": [],
        "ceiling": [],
        "decor": [],
        "track": []
    }

    with open(ASSET_CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            asset_path = row.get("AssetToPlace", "").lower()

            if "/floor/" in asset_path:
                index["floor"].append(row)
            elif "/wall/" in asset_path:
                index["wall"].append(row)
            elif "/door/" in asset_path:
                index["door"].append(row)
            elif "/ceiling/" in asset_path:
                index["ceiling"].append(row)
            elif "/tracks/" in asset_path:
                index["track"].append(row)
            else:
                index["decor"].append(row)

    return index
