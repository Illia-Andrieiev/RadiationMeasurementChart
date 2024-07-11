import pandas as pd


class LevelData:
    def __init__(self):
        self.moda = 0
        self.min = 0
        self.max = 0
        self.average = 0
        self.dispersion = 0
        self.height = 0
        self.data = []

    def print(self):
        print(f" height: {self.height}, moda: {self.moda}, min: {self.min}, "
              f" max: {self.max}, average: {self.average}, dispertion: {self.dispersion},  "
              f"data: {self.data}")

    def calculate_statistics(self):
        df = pd.DataFrame({'data': self.data})

        # Calculate statistics
        self.moda = df['data'].mode().iloc[0]
        self.min = df['data'].min()
        self.max = df['data'].max()
        self.average = df['data'].mean()
        self.dispersion = df['data'].var()


class Point:
    def __init__(self, nomer):
        self.cpsdata = []
        self.Svdata = []
        self.nomer = nomer

    def calculate_statistics(self):
        for level in self.cpsdata:
            level.calculate_statistics()
        for level in self.Svdata:
            level.calculate_statistics()

    def print(self):
        print(f"Point {self.nomer}:")
        print("CPS Data:")
        for i, level in enumerate(self.cpsdata):
            print(f"  Level {i + 1}:")
            level.print()
        print("SV Data:")
        for i, level in enumerate(self.Svdata):
            print(f"  Level {i + 1}:")
            level.print()
