

class RevoluteJoint():
    def __init__(self,parent,child,axis, position=None):
        self.type = 'revolute'
        self.parent = parent
        self.child = child
        self.name = f'{self.parent.name}_{self.child.name}'
        self.axis = axis
        self.position = position