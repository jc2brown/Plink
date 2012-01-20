from numpy import *
from convenience import *
from matext import *
from pygame import math
from test import *

# The Plane class represents a mathematical plane, as represented by two basis vectors.
# It is useful for determining if and where a line intersects it
# It can also generate points efficiently when given a function of a basis
class Plane:
    
    standard_basis = ( vector((1.0,0.0,0.0)), vector((0.0,1.0,0.0)) )
    
    def __init__(self, pos, basis = standard_basis):
        self.position = pos
        self.setBasis(basis)
        
    def setBasis(self, basis):
        # Force basis vector length to be 1 if things look distorted
        self.basis = basis
        self.basis_matrix = colMatrix(self.basis)
        self.normal = self.basis[0].cross(self.basis[1])
        
    # Returns a parametric generator that produces points according to gx and gy
    def getPoints(self, gx, gy, steps, scale):
        c = 2 * pi / steps
        lst = ( self.position + scale * self.basis_matrix * vector((gx(c * t), gy(c * t))) for t in range(steps) )
        return lst
        
        
        
    # Returns the point of intersection between this plane and line
    #     line: a 2ple of points representing a line segment
    def intersects(self, line):
        
        # For convenience
        p1, p2 = line
        p1, p2 = p1 - self.position, p2 - self.position
        
        # Determine the line equation
        u = p2 - p1            # Vector parallel to line segment
        
        # Quit if line is parallel to plane
        n_dot_u = u.transpose().dot(self.normal)#.x()
        if n_dot_u == 0:
            return None
        
        # Otherwise find the LINE's intersection point
        i, j, k = self.normal.xyz()
        x, y, z = p1.xyz()
        s = -((i*x + j*y + k*z + self.position.y()) / n_dot_u).x()
        point = p1 + s * u       # The point of intersection relative to the position vector of this plane
        
        # Is that point beyond this line segment?
        if 0 > s or s > 1:
            return None
        
        # OK, what combination of basis vectors yields l_point?
        c = linalg.lstsq(self.basis_matrix, point)[0]
        c1, c2 = c.xy()
        
        # Sanity check
        if self.basis_matrix * c != point:
            print 'Something went wrong in Plane.intersects()'
            return None
        
        # Make it so
        return point + self.position
    
    
def test():
    plane = Plane(zero_vector, Plane.standard_basis)
    p1 = vector((-1,1,-1.0))
    p2 = vector((1,-1,1.0))
    
    line1 = (p1, p2)
    assert plane.intersects(line1) == zero_vector,          'intersects() 1'
    
    p3 = vector((-1,1,1))   
    line2 = (p2, p3)    # parallel to plane
    assert plane.intersects(line2) is None,                 'intersects() 2'
    
    lst = [ vector((1,0,0)), vector((0,1,0)), 
           vector((-1,0,0)), vector((0,-1,0)) ]
    assert plane.getPoints(cos, sin, 4, 1) == lst,              'getPoints() 1'
    
    # 45 degree rotation about X
    b1 = vector((1,0,0))
    b2 = vector((0,1,1))
    plane.setBasis((b1, b2))
    
    line1 = (p1, p2)
    assert plane.intersects(line1) == zero_vector,          'intersects() 3'
    
    lst = [ vector((1,0,0)), vector((0,1,1)), 
           vector((-1,0,0)), vector((0,-1,-1)) ]
    assert plane.getPoints(cos, sin, 4, 1) == lst,              'getPoints() 2'
    
    

Test().register('plane', test)
Test().test()
    
        
        