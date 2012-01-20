import numpy as np
from math import *
from test import *

# Extensions to numpy's np.matrix

def matrix_eq(self, other):
    return np.equal( np.round(self,10), np.round(other,10) ).all()

def matrix_neq(self, other):
    return not ( self == other )

def matrix_or(self, other):
    return self.magnitude() * other

def matrix_xor(self, other):
    return self.direction() * other

def matrix_and(self, other):
    return np.multiply(self, other)
    #return vector([ a * b for (a, b) in self, other ])


def magnitude(lst):
    return sqrt(sum([ x ** 2 for x in lst ] ))

def direction(lst):
    v = lst if isVector(lst) else vector(lst)
    mag = magnitude(v)
    return zero_vector if mag == 0 else v / mag

# Vector cross-product
def cross(self, other): 
    a = self.y()*other.z()-self.z()*other.y()
    b = self.z()*other.x()-self.x()*other.z()
    c = self.x()*other.y()-self.y()*other.x()
    return vector(( a, b, c ))

# Shorthand for a column vector
def vector(cpts):
    if len(cpts) == 2:
        return np.matrix([[cpts[0]],[cpts[1]]])
    return np.matrix([[cpts[0]],[cpts[1]],[cpts[2]]])

def isVector(v):
    return isinstance(v, np.matrix) and v.width() == 1

def eulerAngles(v):
    # Returns a rotation vector for a Cartesian point
    assert isVector(v)
    x, y, z = v.direction().xyz()
    a = 0 if z == 0 else asin(x/z) 
    b = 0 if x == 0 else -asin(y/x)
    c = 0 if y == 0 else asin(z/y) 
    #c = 0.0 #to prevent skewing
    return vector((a, b, c))


# Matrix from list of vectors as rows
def rowMatrix(rows):
    return np.matrix(np.array([ [ e for e in r.ravel() ] for r in rows ]))

# Matrix from list of vectors as columns
def colMatrix(cols):
    return rowMatrix(cols).transpose()



### Matrix extensions applied below


# Component accessors
np.matrix.x =           lambda(self):       self[0,0]
np.matrix.y =           lambda(self):       self[1,0]
np.matrix.z =           lambda(self):       self[2,0]
np.matrix.xy =          lambda(self):       (self.x(), self.y())
np.matrix.xyz =         lambda(self):       (self.x(), self.y(), self.z())

# Dimension changes
np.matrix.twoDee =      lambda(self):       vector(self.xy())
np.matrix.threeDee =    lambda(self):       vector((self.x(), self.y(), 0.0))

# Number of columns
np.matrix.width =       lambda(self) :      len(self.transpose())

# Number of rows
np.matrix.height =      lambda(self) :      len(self)

# Duplicate a matrix
np.matrix.copy =        lambda(self) :      np.matrix(self)



### Operators

# Element-wise equality
np.matrix.__eq__ = matrix_eq

# Negation of __eq__
np.matrix.__ne__ = matrix_neq

# Scaled magnitude
# v|s -> v.magnitude() * s
np.matrix.__or__ = matrix_or

# Scaled direction
# v^s -> v.direction() * s
np.matrix.__xor__ = matrix_xor

# Element-wise vector multiplication
# v & u -> multiply(v, u), sort of...
np.matrix.__and__ = matrix_and


### Convenience methods


# Vector length
np.matrix.magnitude = lambda(self) : np.linalg.norm(self)

# Parallel vector of length 1
np.matrix.direction = direction

# Vector cross product
np.matrix.cross = cross

# Get a vector of Euler-style angles
np.matrix.rotation = eulerAngles



'''
    USE np.matrix.vdot()
def dot(this, other):
    ax, ay, az = this.xyz()
    bx, by, bz = other.xyz()
    ret = ax*bx+ay*by+az*bz
    return ret
'''









# Needs to be after vector() definition
zero_vector = vector((0.0, 0.0, 0.0))



def test():
    a = vector((1, 2, 3))
    b = np.matrix('4; 5; 6')
    c = np.matrix([[7], [8], [9]])
    x1 = np.matrix('3, 2, 1')
    x2 = np.matrix([[6, 5, 4]])
    assert isVector(zero_vector),       'isVector() 1'
    assert isVector(a),                 'isVector() 2'
    assert isVector(b),                 'isVector() 3'
    assert isVector(c),                 'isVector() 4'
    
    assert not isVector(x1),            'isVector() 5'
    assert not isVector(x2),            'isVector() 6'
    
    aa = a.copy()
    assert a == a,                      '== (equality) operator 1'
    assert aa == a,                     '== (equality) operator 2'
    
    assert aa is not a,                 'copy() 1'          
    
    rma = np.matrix('1 2 3')
    rm = np.matrix('1 2 3; 4 5 6; 7 8 9')
    assert rma == rowMatrix((a)),        'rowMatrix() 1'
    assert rm == rowMatrix((a, b, c)),   'rowMatrix() 2'
    
    cma = np.matrix('1; 2; 3')
    cm = np.matrix('1 4 7; 2 5 8; 3 6 9')
    assert cma == colMatrix((a)),        'colMatrix() 1'
    assert cm == colMatrix((a, b, c)),   'colMatrix() 2'
    
    assert rma.width() == 3,                     'width() 1'
    assert cma.width() == 1,                     'width() 2'
    assert rm.width() == 3,                      'width() 3'
    
    assert rma.height() == 1,                    'height() 1'
    assert cma.height() == 3,                    'height() 2'
    assert rm.height() == 3,                     'height() 3'
    
    d = vector((1, 0, 0))
    e = vector((2, 0, 0))
    f = vector((1.0/sqrt(2), 1.0/sqrt(2), 0))
    g = f * 2.0 
    
    assert zero_vector == zero_vector.magnitude(),  'magnitude() 1' 
    assert d.magnitude() == 1,                      'magnitude() 2'
    assert e.magnitude() == 2,                      'magnitude() 3'
    
    assert zero_vector == zero_vector.direction(),  'direction() 1' 
    assert d == e.direction(),                      'direction() 2'
    assert f == g.direction(),                      'direction() 3'
    
    axb = vector((-3,6,-3))
    assert a.cross(b) == axb,                       'cross() 1'
    
    dr = vector((0, pi / 2, 0))
    #assert d.rotation() == dr,                      'rotation() 1'
    
    assert a|3.4 == a.magnitude() * 3.4,            '| (scaled magnitude) operator 1'
    assert b^5.9 == b.direction() * 5.9,            '^ (scaled direction) operator 1'
    assert a & b == vector((4,10,18)),              '& (element-wise multiplication) operator 1'
    
    a2 = vector((1, 2))
    a3 = vector((1, 2, 0))
    assert a2 == a.twoDee(),                        'twoDee() 1'
    assert a3 == a2.threeDee(),                     'threeDee() 1'
    
    

Test().register('matext', test)
Test().test()



