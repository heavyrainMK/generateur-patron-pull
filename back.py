class Back:

    def __init__(self, chest_width, armhole_depth, underarm_to_hem_length): 
        self.chest_width = chest_width
        self.armhole_depth = armhole_depth
        self.underarm_to_hem_length = underarm_to_hem_length
        self.chest_stitches = 0
        self.rows_to_underarm = 0
        self.rows_to_hem = 0

    def getChestWidth(self):
        return self.chest_width

    def getArmholeDepth(self):
        return self.armhole_depth

    def getUnderArmToHemLength(self):
        return self.underarm_to_hem_length

    def setChestStitches(self, stitches_per_cm):
        self.chest_stitches = self.chest_width * stitches_per_cm

    def getChestStitches(self):
        return self.chest_stitches

    def setRowsToUnderarm(self, rows_per_cm):
        self.rows_to_underarm = self.armhole_depth * rows_per_cm

    def getRowsToUnderarm(self):
        return self.rows_to_underarm

    def setRowsToHem(self, rows_per_cm):
        self.rows_to_hem = self.underarm_to_hem_length * rows_per_cm

    def getRowsToHem(self):
        return self.rows_to_hem

    def __str__(self):
        return f"Le dos mesure {self.armhole_depth}CM depuis l'encolure jusqu'a l'aisselle et {self.underarm_to_hem_length}CM de l'aisselle jusqu'a l'ourlet. Le tour de poitrine est {self.chest_width}"
