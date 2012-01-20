from numpy import *
from pygame import Color, draw, mouse, gfxdraw
from matext import *









# GRAPHICS

white = Color('white')
black = Color('black')
magenta = Color(255, 0, 255)    # magenta
cyan = Color(0, 255, 255)

# Draws a polygon to display after applying transform
    #     surface: the surface on which to draw
    #     transform: converts the points in pointlist to screen coordinates
    #     pointlist: a list of points in 3-space but located on the xy-plane
    #     lightlist: a list of Light instances
    #     color: an instance of the pygame.Color class
    #     width: the thickness of the polygon line. Default: fill with color
def drawPoly(view, transform, pointlist, lightlist, color = black, width = 0):  
    lst = [ transform(p).xy() for p in pointlist ]
    draw.aalines(view.display, color, True, lst, True)
    #draw.polygon(view.display, color, lst, width)
    gfxdraw.filled_polygon(view.display, lst, color)
    
    


    
    