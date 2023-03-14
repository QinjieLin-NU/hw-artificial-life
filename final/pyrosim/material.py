from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, color="0 1.0 1.0 1.0", color_name="Cyan"):

        self.depth  = 3

        self.string1 = f'<material name="{color_name}">'

        self.string2 = f'    <color rgba="{color}"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
