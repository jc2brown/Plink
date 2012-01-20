from convenience import * 
from transform import *
from spinner import *
from numpy import *
from matext import *
from plane import *
from pygame import *

class Target(Spinner, Plane):
    def __init__(self, pos, mass, radius, rot=zero_vector, rot_vel=zero_vector, shape='square'):
        Spinner.__init__(self, mass=mass, radius=radius, rot=rot, rot_vel=rot_vel)
        Plane.__init__(self, pos)
        self.position = pos
        self.scale = matrix([[radius,0.0,0.0],[0.0,radius,0.0],[0.0,0.0,0.0]])
        self.shape = shape
        self.color = Color(0, 0, 255)
        self.numpoints = 4
        self.rings = 3
        self.pointlist = ( vector((5*cos(t * pi / (0.5 * self.numpoints)), sin(t * pi / (0.5 * self.numpoints)), sin(t))) for t in range(self.numpoints) )
        self.last_rotation = self.rotation
    
    # rotates and shifts the template target
    def getWorldPoints(self, scale):
        self.setRotation(self.rotation)
        lst = self.getPoints(lambda(x): (5*cos(x)), sin, self.numpoints, scale=scale)
        #lst = [ self.position + self.axial_transform(self.scale * point) for point in self.pointlist ]
        
        return lst
    
    def setRotation(self, r):
        if self.rotation != self.last_rotation:
            self.last_rotation = self.rotation
            basis = [ rotateOnAxis(v, self.rot_axis, r.magnitude()) for v in Plane.standard_basis]
            self.setBasis(basis)
            
    def spin(self, dt, force):
        Spinner.spin(self, dt, force)
    
    
        
    def draw(self, view, transform, lights):
                
        # Line of sight
        los = self.position - view.camera.position 
        eyeCosTarget = los.transpose().dot(self.normal).x()
        
        # If normal is on the wrong side, invert it
        normal = self.normal
        if eyeCosTarget > 0:
            normal *= -1.0
            
        colorscale = 0.0
        for light in lights:
            # Line of light
            lol = light.position - self.position
            lightCosTarget = lol.transpose().dot(normal).x()
            if lightCosTarget > 0:
                colorscale += (lightCosTarget * light.lux) / ( 4.0 * pi * lol.magnitude()**2)
                

        colorscale = 1.0 - (1.0 / (1+colorscale))
        
        #c = vector((self.color.r, self.color.g, self.color.b))
        
        
        c = Color(int(self.color.r * colorscale), int(self.color.g * colorscale), int(self.color.b * colorscale))
        w = Color(int(255 * colorscale), int(255 * colorscale), int(255 * colorscale))
        col = (c, w)
        
        
        
        for i in range(self.rings):
            pointlist = self.getWorldPoints(self.radius * float(self.rings-i) / float(self.rings))
            drawPoly(view, transform, pointlist, [], col[i%2] )
        
        
    # looks at the average x and y of point1 and point2, then returns the point on the target plane 
    # corresponding to those x and y. In other words, find the hit depth.
    def getHitPoint(self, p1, p2):
        
        line = (p1, p2)
        xpoint = self.intersects(line)
        if xpoint is not None:
            diff = self.position - xpoint
            if diff.magnitude() > self.radius:
                return None
        
        return xpoint
        '''
        no_hit = None
        
        # Rotate the basis
        a = self.transform(self, vector((1.0,0.0,0.0)))
        b = self.transform(self, vector((0.0,1.0,0.0)))
        n = cross(a, b)
        
        # Determine the line equation
        u = point2 - point1             # Vector parallel to lineseg
        
        # Quit if line is parallel to plane
        n_dot_u = u.transpose().dot(n).x()
        if n_dot_u == 0:
            return no_hit
        
        # Otherwise find the LINE's intersection point
        i, j, k = n.xyz()
        x, y, z = point1.xyz()
        
        
        #assert i*x + j*y + k*z == array(n) * array(point1)
        #s = -(i*x + j*y + k*z + self.position.y()) / n_dot_u
        #s = -(array(n) * array(point1) + self.position.y()) / n_dot_u
        s = -(n & point1 + self.position.y()) / n_dot_u
        
        
        
        l_point = point1 + s & u       # The point of intersection relative to the center of the target
        
        # Is that point beyond this line segment?
        for e in s.xyz():
            if 0 > e or e > 1:
                return no_hit
            
        
        # Otherwise, find the PLANE's intersection point
        #ax, ay, az = a.xyz()
        #bx, by, bz = b.xyz()
        basis = colMatrix((a, b))# matrix([[ax,bx],[ay,by],[az,bz]])
        
        c = linalg.lstsq(basis, l_point)[0]
        c1, c2 = c.xy()
        
        # Determine if shot misses
        if a|c1 > self.radius or a|c2 > self.radius:
        #if magnitude(*(c1 * a).xyz()) > self.radius or magnitude(*(c2 * b).xyz()) > self.radius:
        #if magnitude( *((c1 * a)+(c2 * b)).xyz() ) > self.radius: 
            return no_hit
        
        hp = basis * c
        
        return hp + self.position
        
        '''
        '''normal_hitpoint = line
        if magnitude(*(normal_hitpoint.xyz())) > self.radius:            
            return no_hit
        
        print "HIT"
        return normal_hitpoint + self.position
        
        
        #determine what combination of basis vectors sum to a point on the line
        '''
        '''
        point3d = 0.5 * (point1 + point2)
        
        
        vx, vy, vz = v.xyz()
        ux, uy, uz = u.xyz()
        px, py, pz = point3d.xyz()
        
        b = (py - (px * (vy / vx))) / (uy - (ux * (vy / vx)))
        a = (px - (b * ux)) / vx
        
        normal_hitpoint = (a * v + b * u)
        if magnitude(*(normal_hitpoint.xyz())) > self.radius:            
            return 
        
        hitpoint = normal_hitpoint + self.position
        
        
        return hitpoint
        '''
        
    # Effect a collision with a mover.
    # mover's position must be at the hit point
    def impact(self, mover):
        hp = mover.position - self.position
        
        # Determine the new axis of rotation
        un_hp = self.transform(self, hp, -1.0)    # Unrotated hit point. Should be in the xy plane.
        print "unhp: ", un_hp.z()
        #assert abs(un_hp.z()) < 10.0 ** -6
        x, y = un_hp.xy()
        p, q = vector((-y, x, 0.0)), vector((y, -x, 0.0))
        p, q = self.transform(self, p), self.transform(self, q)
        self.normal = p.cross(q)
        self.rot_axis = p, q
        
        # Determine angular velocity
        r = mover.position - self.position
        p = mover.mass * mover.velocity
        n = self.normal
        magp = p.magnitude()
        magn = self.normal.magnitude()
        pcos = p if magp * magn == 0.0 else p * dot(p, n) / (magp * magn)
        i = self.moment
        w = r.cross(pcos) / i
        mag = w.magnitude()
        self.rot_vel = vector((mag,0,0))
        
    