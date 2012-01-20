from numpy import *
from convenience import * 
from pygame import Color, draw, mouse
import sys, pygame
from matext import *
from test import *


# Returns a screen coordinate
#     point3d: a point in 3-space
def toScreenCoord(point3d, camera, viewer):
    point = applyCameraRotation(point3d, camera)
    point2d = applyDepthScaling(point, viewer.position)
    point2d = applyClipping(point2d, viewer)
    return point2d



def getRotationForVector(v):
    
    
    cos = [ math.cos(cpt) for cpt in v ]
    sin = [ math.sin(cpt) for cpt in v ]
    c1t = matrix([[ 1,      0,       0], 
                 [ 0, cos[0], -sin[0]], 
                 [ 0, sin[0], cos[0]]]).transpose()
    c2t = matrix([[  cos[1],  0,  sin[1]],
                 [       0,  1,       0],
                 [ -sin[1],  0,  cos[1]]]).transpose()
    c3t = matrix([[ cos[2], -sin[2],  0],
                 [ sin[2],  cos[2],  0],
                 [      0,       0,  1]]).transpose()
                 
    
    ''' 

    m = magnitude(*v.xyz())
    z = direction(v)
    y = direction(Transfrom(rotate))
    z1, z2, z3 = z.xyz()
    y1, y2, y3 = Transform.rotate(unit, vector((a, math.pi,b)), zero_vector).xyz()
   
    
    b = math.acos(-z2 / math.sqrt((1-z3**2)))
    a = math.acos(z3)
    c = math.acos(y3 / math.sqrt((1-z3**2)))
    '''
    
    a, b, c = c3t * c2t * c1t * v
    ret = vector((a, b, c))
    #print "rvec:"
    #print ret
    return ret
    
    

# Ruturns a point in 3-space
#     point3d: a point in 3-space
#     rot: a rotation vector 
#     offset: the origin of point3d w.r.t the world origin
def rotate(point3d, rot, offset=zero_vector):
    # Rotation indexes: h/eading, e/levation, t/wist
    h, e, t = 0, 1, 2
    cos = [ math.cos(cpt) for cpt in rot.xyz() ]
    sin = [ math.sin(cpt) for cpt in rot.xyz() ]
    
    elevation = matrix(  [[      1,      0,      0], 
                          [      0, cos[e],-sin[e]], 
                          [      0, sin[e], cos[e]]])
    
    heading = matrix(    [[ cos[h],      0,-sin[h]],
                          [      0,      1,      0],
                          [ sin[h],      0, cos[h]]])
    
    twist = matrix(      [[ cos[t], sin[t],      0],
                          [-sin[t], cos[t],      0],
                          [      0,      0,      1]])
    
    ret = heading.dot(elevation).dot(twist)
    return (ret * (point3d - offset)) + offset

# Returns p, rotated about axis through angle theta
#     p: a point in 3-space
#     axis: a 2ple of points in 3-space specifying an axis of rotation
#     theta: rotation angle in radians
def rotateOnAxis(p, axis, theta):
    point = matrix([[p.x()], [p.y()], [p.z()], [0.0]])
    p1, p2 = axis
    x1, y1, z1 = p1.xyz()
    u = (p2 - p1).direction()
    a, b, c = u.xyz()
                
    # Translate to the origin
    t = matrix([[1,0,0,-x1],[0,1,0,-y1],[0,0,1,-z1],[0,0,0,1]])
    t_inv = t.I     #matrix([[1,0,0,x1],[0,1,0,y1],[0,0,1,z1],[0,0,0,1]])
    
    # Rotation about X. We first assume none is needed...
    rx = matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    rx_inv = rx.I   #matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    
    # Check if our assumption was wrong. If so, we need to update rx
    d = math.sqrt(b**2 + c**2)
    if d > 0.0:
        rx = matrix([[1,0,0,0],[0,c/d,-b/d,0],[0,b/d,c/d,1],[0,0,0,1]])
        rx_inv = rx.I   #matrix([[1,0,0,0],[0,c/d,b/d,0],[0,-b/d,c/d,1],[0,0,0,1]])
    
    # Rotate about Y so the rotation axis lies along Z
    ry = matrix([[d,0,-a,0],[0,1,0,0],[a,0,d,0],[0,0,0,1]])
    ry_inv = ry.I       #matrix([[d,0,a,0],[0,1,0,0],[-a,0,d,0],[0,0,0,1]])
    
    # Finally, rotate about Z as desired
    rz = matrix([[math.cos(theta),-math.sin(theta),0,0],[math.sin(theta),math.cos(theta),0,0],[0,0,1,0],[0,0,0,1]])

    # Do and undo
    x, y, z = point.xyz()
    ret = t_inv*rx_inv*ry_inv*rz*ry*rx*t*point
    # 3D from 4D
    ret = vector((ret.xyz()))
    return ret
    
    
# Returns a point in 3-space having undergone a rotation
# with respect to the camera's position and orientation
#     point3d: a point in 3-space
#     camera: an instance of the Camera class
def applyCameraRotation(point3d, camera):
    return rotate(point3d, camera.rotation, camera.position)

# Returns a point in 2-space representing the projection
# of point3d with respect to the perspective of viewer
#     point3d: a point in 3-space
#     viewer: an instance of the Viewer class
def applyDepthScaling(point, vpos):
    scale = vpos.z() / point.z()
    p = point * scale
    return p.twoDee()

# Returns a screen/display coordinate by first scaling 
# normalized point2d, then shifting 
#     point2d: a a point in 2-space
#     viewer: an instance of the Viewer class
def applyClipping(point2d, view):
    scale = view.dimensions.y() * view.scale
    qdim = 0.5 * view.dimensions.twoDee()   # quadrant dimensions for the given viewport
    #print scale
    return scale * point2d + qdim


def test():
    p1 = vector((0,0,1))
    rX = vector((0,-pi/2,0))
    rY = vector((-pi/2,0,0))
    rZ = vector((0,0,pi/2))
    
    assert rotate(p1, rX) == vector((0,1,0)),       'rotate() 1'
    assert rotate(p1, rY) == vector((1,0,0)),       'rotate() 2'
    assert rotate(p1, rZ) == vector((0,0,1)),       'rotate() 3'
    
    a1 = vector((0,1,0))
    a2 = vector((0,-1,0))
    axis = (a1, a2)
    
    assert rotateOnAxis(p1, axis, pi/2) == vector((-1,0,0)),     'rotateOnAxis() 1'
    
    
Test().register('transform', test)
Test().test()