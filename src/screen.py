from view import * 
from convenience import *
from pygame import font

# The Screen class represents the physical display device, a.k.a the program window
class Screen(View):
    def __init__(self, camera, dim, distance):
        View.__init__(self, camera, dim, zero_vector, distance)
        
        # Show us our frames per second
        self.overlay = [ lambda(fps): self.display.blit(font.SysFont("arial", 16).render(str(fps), True, black), (100,100)), ]
