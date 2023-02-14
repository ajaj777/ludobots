import numpy as np

class Link():
    def __init__(self, random=1, color='green', sensor=1):
        self.random = random
        self.color = color
        self.sensor = sensor

class RectangleLink(Link):
    def __init__(self,**args):
        Link.__init__(random=args['random'],color=args['color'],sensor=args['sensor'])
        if self.random:
            self.generate()
        else:
            self.length = args['length']
            self.width = args['width']
            self.height = args['height']

    def generate(self):
        pass