class LevelData:
    def __init__(self):
        self.moda = 0
        self.min = 0
        self.max = 0
        self.average = 0
        self.dispersion = 0
        self.height = 0
        self.data = []


class Point:
    def __init__(self, nomer):
        self.cpsdata = [LevelData()]
        self.Svdata = [LevelData()]
        self.nomer = nomer

    def countParams(self):
        # Реалізація методу, який рахує параметри
        pass

    def print(self):
        print(f"Point {self.nomer}:")
        print("CPS Data:")
        for i, level in enumerate(self.cpsdata):
            print(f"  Level {i + 1}: moda: {level.moda}, min: {level.min}, max: {level.max}, "
                  f"average: {level.average}, dispertion: {level.dispersion}, height: {level.height}, "
                  f"data: {level.data}")
        print("SV Data:")
        for i, level in enumerate(self.Svdata):
            print(f"  Level {i + 1}: moda: {level.moda}, min: {level.min}, max: {level.max}, "
                  f"average: {level.average}, dispertion: {level.dispersion}, height: {level.height}, "
                  f"data: {level.data}")