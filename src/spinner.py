from convenience import *
from transform import *
from matext import *
from pygame import math

class Spinner:
    
    
    def __init__(self, mass, radius, rot, rot_vel = zero_vector, rot_accel = zero_vector):
        self.rotation = rot
        self.rot_vel = rot_vel
        self.rot_accel = rot_accel
        self.static = False
        self.transform = Spinner.axial_transform
        self.rot_axis = self.p, self.q = vector((0.0,-1.0,0.0)), vector((0.0,1.0,0.0))
        self.radius = radius
        self.mass = mass
        self.moment = 0.5 * self.mass * self.radius ** 2    # assume circular moment of inertia
        self.friction = .99
        
    def spin(self, dt, force):
        if not self.static:
            self.rot_accel = force * self.moment
            self.rot_vel += dt * self.rot_accel
            w = self.rot_vel.magnitude()
            #self.rot_vel *= self.friction * (1 - (1 / (w**2 + 1)))
            
            self.rotation += dt * self.rot_vel
            # Keep things at reasonable levels
            #rot = self.rotation.xyz()
            #print self.rotation
            
            #self.rotation %= 2*pi
            self.rotation = vector([ cpt % (2 * pi) for cpt in self.rotation.xyz() ])
    
        
    def axial_transform(self, point, dir = 1):
        return rotateOnAxis(point, self.rot_axis, dir * self.rotation.x())
    
    
    def euler_transform(self, point, dir = 1):
        return rotate(point, dir * self.rotation)