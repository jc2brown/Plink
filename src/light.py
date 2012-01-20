from mover import *


class Light(Mover):
    
    def __init__(self, pos, lux=10000.0):
        Mover.__init__(self, pos)
        self.lux = lux      # Technically lumens... oh well.
        
    def getFlux(self, plane):
        pass