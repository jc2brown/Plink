from world import *
from bullet import *
from mover import *


# The Gun class models a device that accelerates a Bullet to a specified velocity

class Gun(Mover):   
    
    # Initially empty
    def __init__(self, pos):
        Mover.__init__(self, pos)
        self.bullet = None
        self.ammo_out = True
    
    # The gun requests ammo from the world, setting ammo_out appropriately
    def reload(self):
        self.bullet = self.world.requestAmmo()
        self.ammo_out = ( self.bullet == None )
        
    # BOOM!
    def fire(self):