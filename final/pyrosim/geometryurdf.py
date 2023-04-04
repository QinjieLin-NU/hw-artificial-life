from pyrosim.commonFunctions import Save_Whitespace

class GEOMETRY_URDF: 

    def __init__(self,size,geometry_type):

        self.depth   = 3

        self.string1 = '<geometry>'

        if geometry_type=="box":
            sizeString = str(size[0]) + " " + str(size[1]) + " " + str(size[2])
            self.string2 = '    <box size="' + sizeString + '" />'
        elif geometry_type=="sphere":
            r = size[0]
            self.string2 = '    <sphere radius="' + str(r/2.0) + '" />'
        elif geometry_type=="cylinder":
            r, l = size[0], size[2]
            self.string2 = '    <cylinder length="' +  str(l/1.1) + '" radius="' + str(r/2.1) + '" />'
        else:
            sizeString = str(size[0]) + " " + str(size[1]) + " " + str(size[2])
            self.string2 = '    <box size="' + sizeString + '" />'

        self.string3 = '</geometry>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
