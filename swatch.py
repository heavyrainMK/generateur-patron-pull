class Swatch:
    def __init__(self, stitches, rows):
        self.stitches = stitches
        self.rows = rows
        self.stitchesPerCM = self.stitches / 10
        self.rowsPerCM = self.rows / 10

    def getStitches(self):
        return self.stitches

    def getRows(self):
        return self.rows

    def getStitchesPerCM(self):
        return self.stitchesPerCM

    def getRowsPerCM(self):
        return self.rowsPerCM

    def __str__(self):
        return f"the swatch is {self.stitches} stitches and {self.rows} rows for a 10cm square"
