class Front:

    def __init__(self, chest_width, armhole_depth, underarm_to_hem_length) 
        self.chest_width = chest_width
        self.armhole_depth = armhole_depth
        self.underarm_to_hem_length = underarm_to_hem_length
        #on commence a tricoter a plat pour avoir une encolure plus haute derriere que devant 
        #au debut il n'y a que 2 mailles de de chaque cote devant, puis on augmente petit a petit, jusqu'a ce que le total 
        #des mailles devant_gauche + devant_droit soit egal au nombre de mailles derriere
        #ca permet de faire un col en "V", plus on augmente vite, moins le V est profond
        self.left = 2
        self.rigth = 2
        self.chest_stitches = 0
        self.rows_to_underarm = 0
        self.rows_to_hem = 0

    def getWristCircumference(self):
        return self.chest_width

    def getArmholeDepth(self):
        return self.armhole_depth

    def getUnderArmToHemLength(self):
        return self.underarm_to_hem_length

    # def setLeftStitches(self, increase):
    #     self.left = self.left + increase

    # def setRightStitches(self, increase):
    #     self.right = self.right + increase

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
        return f"Le devant mesure {self.armhole_depth}CM depuis l'encolure jusqu'a l'aisselle et {self.underarm_to_hem_length}CM de l'aisselle jusqu'a l'ourlet. Le tour de poitrine est {self.chest_width}
