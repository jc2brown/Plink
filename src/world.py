from convenience import * 
from bullet import *
from target import *
from light import *
from numpy import *
from matext import *
from pygame import Color


# Re: Collisions
# The world will determine the intended path of motion for each object it moves.
# If that motion would cause a collision with some other object, the world calls the 
# collide(other_object, dt) method of the first object
# Otherwise, 
        
# The World class contains all "physical" objects, defends virtual boundaries, 
# enforces the laws of physics, and maintains cleanliness of the grounds
#     movers: a list of objects that have position, velocity, and acceleration vectors 
class World:
    def __init__(self, dimensions, position):
        self.dimensions = dimensions
        length = self.dimensions.z()
        self.position = position
        
        # Domed .177 pellet, 7.9 grain
        self.bullet = Bullet(mass=0.02, radius=0.0022, length=0.006, bc=.26, pos=vector((0.0, -0.1, 0.1)))
        self.target = Target(pos=vector((0.0,0.0,length)), mass=2.0, radius=1.0, rot_vel=vector((0.0,0.0,0.0)))
        self.movers = [ ]
        self.spinners = [ self.target ]
        self.drawers = [ self.target, self.bullet ]
        self.gravity = vector((0.0, -9.8, 0.0))
        self.wind = zero_vector #vector((random.uniform(-0.5,0.5), 0.0, (random.uniform(-0.5,0.5))))
        self.floor = [ vector((-1,-1,.2)), vector((1,-1,.2)), vector((1,-1,length)), vector((-1,-1,length))]
        self.color = Color(100, 100, 100)
        self.has_hit = False
        self.light1 = Light(vector((0.0,100.0,1900.0)))
        #self.light2 = Light(vector((0.0,10.0,1800.0)))
        self.lights = [ self.light1 ]
        self.heading = 0
        self.latitude = pi/2
        self.radius = 6.37e6
        self.rot_axis = rotate(vector((0,0,1)), vector((self.heading, self.latitude, 0)))
        self.rot_vel = rotate(vector((0,0,-2.0*math.pi/86400.0)), vector((self.heading, self.latitude, 0)))
        print self.rot_axis
    
    #Draws all registered objects, as well as any world-specific graphics
    def draw(self, view, transform):
        #drawPoly(view, transform, self.floor, 1, self.color)
        for drawer in sorted(self.drawers, key=lambda drawer: 99999999.0 - (drawer.position.z())):
            drawer.draw(view, transform, self.lights)

    # Attempts to move all registered objects and rotate all spinners the distance/angle prescribed by dt
    # If it is determined that moving an object would cause a collision, inform both objects
    #     dt: the duration in seconds since moveObjects was last called
    def moveObjects(self, dt):
        for mover in self.movers:
            
            
            # Calculate forces and accelerations
            coriolis = -2.0 * self.rot_vel.cross(mover.velocity) 
             
            c = cos(self.heading)
            s = sin(self.heading)
            u = (mover.velocity & vector((c, 0, s))).magnitude()
            v = (mover.velocity & vector((s, 0, c))).magnitude()
            e1 = 2 * self.rot_vel.magnitude() * u * cos(self.latitude)
            e2 = ( u ** 2 + v ** 2 ) / self.radius
            eotvos = vector((0, e1 + e2, 0))
            
            # Consolidate
            forces = mover.f_drag(self.wind)
            accels = self.gravity + coriolis + eotvos
            
            # Apply
            force = forces + (mover.mass * accels)
            mover.move(dt, force)
            
            # Collision detection
            
            hp = self.hit(self.bullet, self.target)
            if hp is not None:
                self.has_hit = True
                print "HIT! ", hp
                #self.target.rot_vel = zero_vector
                self.target.impact(self.bullet)
            
            #for other_mover in self.movers.remove(mover):
                #if mover.wouldHit(other_mover):
                #    mover.collide(other_mover)
            
        for spinner in self.spinners:
            spinner.spin(dt, zero_vector)
            

    # 
    def hit(self, this, other):
        bp = this.position
        lbp = this.last_position
        
        hp = other.getHitPoint(bp, lbp)
        
        return hp
            