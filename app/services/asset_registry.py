import pandas as pd

class AssetRegistry:
    def __init__(self, path):
        df = pd.read_csv(path)
        self.assets = df

    def _filter(self, keyword):
        return self.assets[self.assets["AssetToPlace"].str.contains(keyword)]

    def floors(self):
        return self._filter("Floor")

    def walls(self):
        return self._filter("Wall")

    def doors(self):
        return self._filter("Door")

    def ceilings(self):
        return self._filter("Ceiling")

    def tracks(self):
        return self._filter("Track")

    def decors(self):
        return self._filter("Decor")

    def random(self, df):
        return df.sample(1).iloc[0]["AssetToPlace"]
