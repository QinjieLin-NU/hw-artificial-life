from pyrosim.commonFunctions import Save_Whitespace


class MASS_SDF: 

    def __init__(self, mass=1.0):

        self.string =  f'<mass>{mass}</mass>'

        self.depth = 4

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write(self.string + '\n' )
