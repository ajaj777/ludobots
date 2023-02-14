

class RevoluteJoint():
    def __init__(self,parent,child,axes):
        self.type = 'revolute'
        self.parent = parent
        self.child = child
        self.name = f'{self.parent.name}_{self.child.name}'
        self.axes = axes