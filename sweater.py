from swatch import Swatch
import math

class Sweater:
    def __init__(self, right_sleeve, left_sleeve, front, back, swatch):
        self.right_sleeve = right_sleeve
        self.left_sleeve = left_sleeve
        self.front = front
        self.back = back
        self.swatch = swatch

    #don't forget to round up the numbers
    def calculStitchesNeeded(self, width):
        return math.ceil(self.swatch.getStitches() / 10 * width)

    def calculRowsNeeded(self, length):
        return  math.ceil(self.swatch.getRows() / 10 * length)

    def calculIncreases(self, width_1, width_2):
        return width_2 - width_1

    def calculDecreases(self, width_1, width_2):
        return width_1 - width_2
    
