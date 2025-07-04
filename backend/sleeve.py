from calculs import Calculs

class Sleeve(Calculs):
    
    def __init__(self, upperarm_circumference, wrist_circumference, underarm_to_hem_length): 
        super().__init__()
        self.upperarm_circumference = upperarm_circumference
        self.wrist_circumference = wrist_circumference
        self.underarm_to_hem_length = underarm_to_hem_length
        self.top_sleeve_width = 3#j'ai mesuré un de mes pulls, je changerai probablement plus tard
        self.top_sleeve_stitches = 0
        self.upperarm_stitches = 0
        self.wrist_stitches = 0
        self.rows_to_wrist = 0
        

    def getTopSleeveWidth(self):
        return self.top_sleeve_width

    def getUpperArmCircumference(self):
        return self.upperarm_circumference

    def getWristCircumference(self):
        return self.wrist_circumference

    def getUnderArmToHemLength(self):
        return self.underarm_to_hem_length

    def setTopSleeveStitches(self, nb_of_stitches):
        self.top_sleeve_stitches = nb_of_stitches

    def getTopSleeveStitches(self):
        return self.top_sleeve_stitches

    def setUpperarmStitches(self, nb_of_stitches):
        self.upperarm_stitches = nb_of_stitches

    def getUpperarmStitches(self):
        return self.upperarm_stitches

    def setWristStitches(self, nb_of_stitches):
        self.wrist_stitches = nb_of_stitches

    def getWristStitches(self):
        return self.wrist_stitches

    def setSleeveRowsToWrist(self, nb_of_rows):
        self.rows_to_wrist = nb_of_rows

    def getSleeveRowsToWrist(self):
        return self.rows_to_wrist

    def __str__(self):
        return f"La manche mesure CM depuis l'encolure jusqu'a l'aisselle et {self.underarm_to_hem_length}CM de l'aisselle jusqu'a l'ourlet. Le bras a une circonference de {self.upperarm_circumference}CM au biceps et {self.wrist_circumference}CM au poignet."


