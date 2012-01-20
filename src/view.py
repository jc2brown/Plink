from convenience import * 
import pygame
from mover import *

# The View class models the screen onto which a Camera's image is projected
# As a mover, it inherits position, velocity and acceleration, and a few other fields
# These attributes are in the program window space, and are, as such, 2-dimensional
#     dimensions: a vector in 2-space, the components of which represent the width and height of the display surface
#     camera: the Camera instance from which the image is projected
#     scale: a 2x2 matrix which enables scaling to a particular (default 1:1) aspect ratio. e.g. [ [(16/9), 0], [0, 1] ]
class View(Mover):
    def __init__(self, camera, dim, pos, distance = 1.0, rot = zero_vector):
        Mover.__init__(self, pos)
        self.distance = distance
        self.dimensions = dim        
        self.camera = camera
        self.display = pygame.Surface(self.dimensions.xy())
        self.scale = matrix([[1.0, 0.0], [0.0, 1.0]])
        #self.reposition(self.camera)                            # use this, but remove if problems arise?
        self.overlay = []
        self.visible = True
        self.canzoom = True

    # Modify distance such that a field of view angle fov 
    # is visible on the display surface when projected from camera 
    def setFOV(self, fov, camera):
        self.distance = -1.0 / math.tan( fov / 2.0 )    
        
    # Scopes should use this instead of setting distance directly
    # Returns the actual power after attempting to modify it
    def setPower(self, power):
        if self.canzoom and power >= 1.0:
            self.distance = power
            self.reposition(self.camera)
        return self.distance
        
    
    # Update the reference to camera and reposition the view directly behind its line of sight
    def reposition(self, camera):
        self.camera = camera
        x, y = self.position.xy()
        z = camera.getViewpoint(self.distance).z()
        self.position = vector((x, y, z))
        
        
    # Retreive and draw image data from camera
    def updateDisplay(self):
        self.display.fill(white)
        self.camera.capture(self)
        
    def drawOverlay(self, args):
        [ f(args) for f in self.overlay ]
        
    # Draws the entire display surface + any overlay onto anther surface
    #     surface: the surface on which to draw
    #     position: offset from the upper left corner
    #     args: arguments for the overlay
    def draw(self, surface, args = ()):
        if self.visible:
            self.drawOverlay(args)
            surface.blit(self.display, self.position.xy())
        
        