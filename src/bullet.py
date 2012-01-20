from convenience import * 
from mover import *

# The Bullet class models a projectile
#     mass: in kilograms
#     radius: in meters
#     color: an instance of the pygame.Color class
#     position: a point in 3-space
#     velocity: a vector in 3-space
#     acceleration: a vector in 3-space
class Bullet(Mover):
    def __init__(self, mass, radius, length, bc, pos, vel = zero_vector, accel = zero_vector):
        Mover.__init__(self, pos, mass, vel, accel)
        self.radius =       radius
        self.length =       length
        self.bc =           bc
        self.last_position = self.position
        self.poslist =      list([])
        self.color =        Color('black')
        
    def draw(self, view, transform, lights):
        #print self.poslist
        #if len(self.poslist) >= 2:
        #    draw.aalines(surface, self.color, False, [ (transform(point).xy()) for point in self.poslist ])
        
        position2d = transform(self.position)
        shift = vector((self.radius, 0, 0))
        a = transform(self.position - shift)
        b = transform(self.position + shift)
        radius2d = (b - a)|0.5  
        #radius2d = self.radius * (world.camera.position.z() - world.view.position.z()) / (self.position.z() - world.camera.position.z())
        return draw.circle(view.display, self.color, position2d, int(radius2d), 0)

    # Returns the force of BOTH wind and air resistance acting on the bullet.
    # Wind is the force of the medium (air) that is moving with respect to the world.
    # Drag is the friction force of the bullet passing through a viscous medium (air) 
    # In other words, drag will always slow a bullet down, while wind may cause it to speed up.
    def f_drag(self, wind_vel):
        # Wind
        rel_vel = wind_vel - self.velocity 
        dir = rel_vel.direction()
        #cd = self.drag_coef
        csa = math.pi * self.radius ** 2
        v2 = rel_vel.magnitude() ** 2
        
        # Drag
        drag = 0.005 * (csa * v2 / self.bc) * dir
        
        
        
        #longcsa = 2 * self.radius * self.length   # csa = cross sectional area
        #shortcsa = math.pi * self.radius**2
        #wind = (0.0336 / longcsa)
        
        return drag
    
    # Append some location tracking to the base move()
    def move(self, dt, force):
        '''
        print "pos"
        print self.position
        print "vel"
        print self.velocity
        print "acc"
        print self.acceleration
        '''
        
        self.last_position = self.position.copy()
        #self.poslist.append( self.position )
        Mover.move(self, dt, force)
        