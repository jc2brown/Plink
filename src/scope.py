from view import * 
from convenience import *

# When creating a scope template, areas in magenta will be the objective of the scope
# Areas in cyan will be outside the body of the scope

class Scope(View):
    def __init__(self, camera, dim, pos, distance = 1.0):
        View.__init__(self, camera, dim, pos, distance)
        self.scope_bmp = pygame.image.load("scope.bmp").convert()
        self.scope_bmp.set_colorkey(magenta)
        self.display.set_colorkey(cyan)
        self.overlay = ( lambda(args): self.display.blit(self.scope_bmp, zero_vector.xy()), )
        self.reposition(self.camera)
        self.tweaks = vector((0.0002, 0.01562, 0.0))
        
