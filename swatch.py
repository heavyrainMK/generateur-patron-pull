class Swatch:
    def __init__(self, stitches, rows):
        self.stitches = stitches
        self.rows = rows

    def getStitches(self):
        return self.stitches

    def getRows(self):
        return self.rows

    def __str__(self):
        return f"the swatch is {self.stitches} stitches and {self.rows} rows for a 10cm square"