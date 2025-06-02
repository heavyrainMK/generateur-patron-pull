from sleeve import Sleeve
from front import Front
from back import Back
from swatch import Swatch
import math

#don't forget to round up the numbers
def calculStitchesNeeded(self, width):
        return math.ceil(self.swatch.getStitches() / 10 * width)

def calculRowsNeeded(self, length):
        return math.ceil(self.swatch.getRows() / 10 * length)

def calculIncreases(self, width_1, width_2):
        return width_2 - width_1

def calculDecreases(self, width_1, width_2):
        return width_1 - width_2


def main():
    #il faut construire les objets avec les mesures fournis par l'utilisateur
    my_right_sleeve = Sleeve()
    my_left_sleeve = Sleeve()
    my_front = Front()
    my_back = Back()
    my_swatch = Swatch()
    



    if __name__ == "__main__":
    main()

    
