class Sleeve:
    
    def __init__(self, upperarm_circumference, wrist_circumference, armhole_depth, underarm_to_hem_length): 
        self.upperarm_circumference = upperarm_circumference
        self.wrist_circumference = wrist_circumference
        self.armhole_depth = armhole_depth
        self.underarm_to_hem_length = underarm_to_hem_length
        self.upperarm_stitches = 0
        self.wrist_stitches = 0
        self.rows_to_underarm = 0
        self.rows_to_wrist = 0
        

    def getUpperArmCircumference(self):
        return self.upperarm_circumference

    def getWristCircumference(self):
        return self.wrist_circumference

    def getArmholeDepth(self):
        return self.armhole_depth

    def getUnderArmToHemLength(self):
        return self.underarm_to_hem_length

    def setUpperarmStitches(self, nb_of_stitches):
        self.upperarm_stitches = nb_of_stitches

    def getUpperarmStitches(self):
        return self.upperarm_stitches

    def setWristStitches(self, nb_of_stitches):
        self.wrist_stitches = nb_of_stitches

    def getWristStitches(self):
        return self.wrist_stitches

    def setRowsToUnderarm(self, nb_of_rows):
        self.rows_to_underarm = nb_of_rows

    def getRowsToUnderarm(self):
        return self.rows_to_underarm

    def setSleeveRowsToWrist(self, nb_of_rows):
        self.rows_to_wrist = nb_of_rows

    def getSleeveRowsToWrist(self):
        return self.rows_to_wrist

    def __str__(self):
        return f"La manche mesure {self.armhole_depth}CM depuis l'encolure jusqu'a l'aisselle et {self.underarm_to_hem_length}CM de l'aisselle jusqu'a l'ourlet. Le bras a une circonference de {self.upperarm_circumference}CM au biceps et {self.wrist_circumference}CM au poignet."


