from convenience import *

class Mover:
    def __init__(self, pos, mass = 1.0, vel = zero_vector, accel = zero_vector):
        self.static = False
        self.position = pos
        self.velocity = vel
        self.acceleration = accel
        self.mass = mass
        
    # Sum of forces acting on a bullet in flight ~ acceleration
    # Does not imply movement, although move() should be called later on 
    def move(self, dt, force):
        if not self.static:
            self.acceleration = force / self.mass
            self.velocity += dt * self.acceleration
            self.position += dt * self.velocity
            
        