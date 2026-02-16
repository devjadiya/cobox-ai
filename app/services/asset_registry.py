from pathlib import Path
import pandas as pd
from typing import Optional


class AssetRegistry:
    """
    Production-safe Asset Registry
    - Handles absolute paths
    - Handles missing columns
    - Case insensitive filtering
    - Prevents crashes when CSV is empty
    """

    def __init__(self, path: Optional[str] = None):

        # -------- PATH RESOLUTION --------
        if path:
            csv_path = Path(path)
        else:
            BASE_DIR = Path(__file__).resolve().parent.parent.parent
            csv_path = BASE_DIR / "data" / "library.csv"

        if not csv_path.exists():
            raise FileNotFoundError(f"Asset CSV not found: {csv_path}")

        # -------- LOAD CSV --------
        df = pd.read_csv(csv_path)

        if "AssetToPlace" not in df.columns:
            raise ValueError("CSV missing 'AssetToPlace' column")

        # Normalize column
        df["AssetToPlace"] = df["AssetToPlace"].astype(str)

        self.assets = df

    # ---------------------------------------------------
    # INTERNAL FILTER
    # ---------------------------------------------------
    def _filter(self, keyword: str) -> pd.DataFrame:
        if self.assets.empty:
            return self.assets

        return self.assets[
            self.assets["AssetToPlace"]
            .str.contains(keyword, case=False, na=False)
        ]

    # ---------------------------------------------------
    # CATEGORY METHODS
    # ---------------------------------------------------
    def floors(self) -> pd.DataFrame:
        return self._filter("floor")

    def walls(self) -> pd.DataFrame:
        return self._filter("wall")

    def doors(self) -> pd.DataFrame:
        return self._filter("door")

    def ceilings(self) -> pd.DataFrame:
        return self._filter("ceiling")

    def tracks(self) -> pd.DataFrame:
        return self._filter("track")

    def decors(self) -> pd.DataFrame:
        return self._filter("decor")

    # ---------------------------------------------------
    # RANDOM PICK
    # ---------------------------------------------------
    def random(self, df: pd.DataFrame) -> Optional[str]:
        """
        Safely pick a random asset path.
        Returns None if df empty.
        """
        if df is None or df.empty:
            return None

        row = df.sample(1).iloc[0]
        return row.get("AssetToPlace")
