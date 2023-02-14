from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self,color="Cyan"):

        self.depth  = 3

        if color == "Cyan":
            self.string1 = '<material name="Cyan">'

            self.string2 = '    <color rgba="0 1.0 1.0 1.0"/>'

            self.string3 = '</material>'
        elif color == 'green':
            self.string1 = '<material name="green">'

            self.string2 = '    <color rgba="0 1.0 0.0 1.0"/>'

            self.string3 = '</material>'
        elif color=='blue':
            self.string1 = '<material name="blue">'

            self.string2 = '    <color rgba="0 0.0 1.0 1.0"/>'

            self.string3 = '</material>'
        else:
            self.string1 = '<material name="black_transparent">'

            self.string2 = '    <color rgba="0 0.0 0.0 0.5"/>'

            self.string3 = '</material>'
        
    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
