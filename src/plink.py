from bullet import *
from camera import *
from convenience import *
from numpy import *
from target import *
from transform import *
from view import * 
from world import * 
from pygame import Color, draw, mouse, font
import sys, pygame
from scope import *
from screen import *
import cProfile
from matext import *

'''
v = vector((1.0,1.0,1.0))
m = magnitude(*v.xyz())
r = Transform.getRotationForVector(v)

u = vector((0.0,0.0,m))
ur = Transform.rotate(u, r, zero_vector)
print "Is actually:"
print ur
print "\nShould be:"
print v
'''


def go():
    
                     
    # START
    
    # Fairly obvious, initialize the pygame library
    pygame.init()
    
    # Create the world in which all physical things reside. It is our coordinate system and universe.
    world = World(vector((20.0, 20.0, 2000.0)), vector((-10.0, 0.0, 10.0)))
    
    # Create startup cameras and make the world visible to them
    eyecam = Camera()
    eyecam.registerObject(world)
    scopecam = Camera()
    scopecam.registerObject(world)
    
    # Setup the program window (just a special case of a View)
    screen = Screen(eyecam, vector((1000,800,0)), -1.0)
    screen.display = pygame.display.set_mode((1000, 800))
    
    # Setup the display surfaces to be drawn to screen and list them
    main_dim = vector((1000,800,0.0))
    scope_dim = vector((240,240,0.0))
    mainview = View(eyecam, main_dim, zero_vector, 1.0)
    scopeview = Scope(scopecam, scope_dim, (main_dim - scope_dim) / 2.0, 4.0)
    views = [ mainview, scopeview ]
    
    # Hide the cursor
    mouse.set_visible(False)
    
    # Let's set up some useful variables
    now = pygame.time.get_ticks()   # The current program time
    shot_fired = False              #
    chase_bullet = False
    hide_scope = True
    lock_mouse = False
    power = 100.0
    #mainview.reposition(eyecam)
    scopeview.setPower(power)
    timescale = 1.0
    tot_mag = 0.0
    tot_dur = 0.0
    frames = 0
    
    if lock_mouse:
        mouse.set_pos((scope_dim / 2.0).xy())
    
    while 1:
        
    
    
        last_t = now
        now = pygame.time.get_ticks()
        t_length = float(now - last_t)
        
        if world.has_hit:
            shot_end = now
            #break
        
        if world.bullet.position.z() > world.target.position.z() + 1000.0:
            #world.bullet.position = vector((world.bullet.position.x(), world.bullet.position.y(), world.target.position.z() - 0.01))
            shot_end = now
            break
            #pass
                
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.dict['button'] == 4:
                    power += 1.0
                if event.dict['button'] == 5:
                    power -= 1.0
                power = scopeview.setPower(power)
                print power
            
            if event.type == pygame.QUIT:
                sys.exit()
                
        
        
        sx, sy = (0.5 * mainview.dimensions).xy()
        if lock_mouse:
            mx, my = mouse.get_rel()
            mouse.set_pos(sx, sy)
            r = (1.0 / (10000 * power))* (vector((sx - mx, sy - my, 0)))
            scopecam.rotation += r
            eyecam.rotation += r
        else:
            mx, my = mouse.get_pos()
            r = (1.0 / (1000 * power))* (vector((sx - mx, sy - my,  0)))
            scopecam.rotation = r
            eyecam.rotation = r
        
        world.bullet.rotation = scopecam.rotation
        scopeview.reposition(scopeview.camera)
        mainview.reposition(mainview.camera)
          
        b1, b2, b3 = mouse.get_pressed()
        if b1 and not shot_fired:
            shot_fired = True
            shot_start = now
            world.bullet.velocity = rotate(vector((0.0,0.0,800.0)), (-world.bullet.rotation - scopeview.tweaks))
            print 'Start Velocity: ' + str(world.bullet.velocity.magnitude())
            #mainview.camera.rotation = zero_vector
            mainview.setPower(50.0)
            #scopeview.reposition(view.camera)
            #scopeview.overlay = []    # hide scope
            world.movers += [world.bullet]
            
    
        # Move everything. The world does most of the work once we tell it to,
        # we just need to handle the less tangible stuff.
        world.moveObjects(timescale * (t_length / 1000.0))
            
        # Bullet chasing
        if shot_fired:
            #scopecam.rotation = world.bullet.rotation
            
            if hide_scope:
                scopeview.visible = False
                
            bp = world.bullet.position
            lbp = world.bullet.last_position
            diff = bp - lbp
            mag = diff.magnitude()
            magxz = sqrt(diff.x()**2 + diff.z()**2)
            
            frames += 1
            tot_mag += mag
            tot_dur += t_length * timescale
                        
            if chase_bullet and mag > 0.0:
                h = arctan2(diff.x(), diff.z())
                e = arcsin(diff.y() / mag)
                eyecam.rotation = vector((h, -e, 0))
                eyecam.position = bp & vector((1,1,1))
                mainview.setPower(10.0)
                mainview.reposition(mainview.camera)
            
            #print eyecam.position
            #scopeview.reposition(eyecam)
            
        
        # Grab each view's camera image, then draw them to the program window in sequence
        
        for view in views:
            view.updateDisplay()
            view.draw(screen.display)
        
        # 
        fps = 1000.0 / (t_length + (1 if t_length == 0 else 0))
        screen.drawOverlay((fps,))
        
        
        pygame.display.flip()
             
             
    
    for view in views:
        view.updateDisplay()              
        view.draw(screen.display, (screen.dimensions - view.dimensions) / 2.0)         
             
    pygame.display.flip()
    
    
    print "Flight time: " + str(tot_dur / 1000.0) + " s" 
    print "Impact energy: " + str(.5 * world.bullet.mass * world.bullet.velocity.magnitude() ** 2) + " J"
    
    print 'End Position'
    print world.bullet.position
    print 'End Velocity: ' + str(world.bullet.velocity.magnitude())
    print "Average frame time: " + str((tot_dur / 1000.0) / float(frames))
    print "Average FPS: " + str(float(frames) / tot_dur * 1000)
    print "Average distance per frame: " + str(tot_mag / float(frames))
            
    pygame.time.delay(1000)    
    
    pygame.display.quit()
    pygame.quit()


go()
#cProfile.run('go()')