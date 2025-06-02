from sleeve import Sleeve
from front import Front
from back import Back
from swatch import Swatch
import math

#don't forget to round up the numbers
def calculStitchesNeeded(stitches, width):
        return math.ceil(stitches / 10 * width)

def calculRowsNeeded(rows, length):
        return math.ceil(rows) / 10 * length)

def calculIncreases(width_1, width_2):
        return width_2 - width_1

def calculDecreases(width_1, width_2):
        return width_1 - width_2


def main():
    #il faut construire les objets avec les mesures fournis par l'utilisateur
    my_right_sleeve = Sleeve()
    my_left_sleeve = Sleeve()
    my_front = Front()
    my_back = Back()
    my_swatch = Swatch()


    my_back.setNeckStitches(calculStitchesNeeded(my_swatch.getStitches(), my_back.getNeckWidth()))
    my_right_sleeve.setTopSleeveStitches(calculStitchesNeeded(my_swatch.getStitches(), my_right_sleeve.getTopSleeveWidth()))



    if __name__ == "__main__":
    main()

    
