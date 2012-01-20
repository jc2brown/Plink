from convenience import * 
from transform import *
from mover import *

# The Camera class represents the "eyes" of the scene. Image data is
# collected here and displayed using an instance of the View class
#     position: a point in 3-space
#     rotation: a vector in 3-space
#     objects: the set of objects that are visible to the camera (via registerObject())
class Camera(Mover):
    def __init__(self, pos = zero_vector, rot = zero_vector):
        Mover.__init__(self, pos)
        self.rotation = rot
        self.objects = set()
        
    # Returns a point directly behind the camera at distance d
    def getViewpoint(self, d):
        return self.position + rotate(vector((0.0, 0.0, -d)), self.rotation)
    
    # Returns a function that, given a point in 3-space, produces a screen coordinate respective of camera and view positions
    def getTransform(self, view):
        return lambda(point): toScreenCoord(point, self, view)
    
    # Registered objects will have their draw method invoked during capture
    #     obj: any class instance with a draw(surface, transform(point3d)) method
    def registerObject(self, obj):
        self.objects.add(obj)
        
    # Draw each visible object to view's display
    #     view: an instance of the View class on which to project images
    def capture(self, view):
        for obj in self.objects:
            obj.draw(view, self.getTransform(view))
            