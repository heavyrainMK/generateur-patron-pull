class Back:
    
    def __init__(self, neck_width, chest_width, armhole_depth, underarm_to_hem_length):
        self.neck_width = neck_width
        self.chest_width = chest_width
        self.armhole_depth = armhole_depth
        self.underarm_to_hem_length = underarm_to_hem_length
        self.neck_stitches = 0
        self.chest_stitches = 0
        self.rows_to_underarm = 0
        self.rows_to_hem = 0

    def getNeckWidth(self):
        return self.neck_width

    def getChestWidth(self):
        return self.chest_width

    def getArmholeDepth(self):
        return self.armhole_depth

    def getUnderArmToHemLength(self):
        return self.underarm_to_hem_length

    def setNeckStitches(self, nb_of_stitches):
        self.neck_stitches = nb_of_stitches

    def getNeckStitches(self):
        return self.neck_stitches

    def setChestStitches(self, nb_of_stitches):
        self.chest_stitches = nb_of_stitches

    def getChestStitches(self):
        return self.chest_stitches

    def setRowsToUnderarm(self, nb_of_rows):
        self.rows_to_underarm = nb_of_rows

    def getRowsToUnderarm(self):
        return self.rows_to_underarm

    def setRowsToHem(self, nb_of_rows):
        self.rows_to_hem = nb_of_rows

    def getRowsToHem(self):
        return self.rows_to_hem

    def __str__(self):
        return f"Le dos mesure {self.armhole_depth}CM depuis l'encolure jusqu'a l'aisselle et {self.underarm_to_hem_length}CM de l'aisselle jusqu'a l'ourlet. Le tour de poitrine est {self.chest_width}"
