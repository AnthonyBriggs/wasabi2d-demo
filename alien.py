import sys

#from wasabi2d import Scene, run, exit, event, keys
import wasabi2d as w2d

import pygame
from pygame import joystick

## These are mainly chosen for feel :)
# pixels per second when running full tilt
ALIEN_SPEED = 1000.0
# acceleration due to gravity when jumping
ALIEN_FALL_ACC = 4000.0

def init_gamepads():
    pygame.joystick.init()
    print("I can see %d joysticks!" % (pygame.joystick.get_count()))
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    controllers = {}
    for stick in joysticks:
        stick.init()
        print((stick.get_name(), stick.get_init()))
        controllers[stick.get_id()] = stick
    return controllers

pygame.init()
controllers = init_gamepads()
print(controllers)


mode_1080p = 1920, 1080
scene = w2d.Scene(
    *mode_1080p,
    title='Wasabi2d Alien Demo',
    fullscreen=True,
    background='black',
    rootdir='.'
)

alien = scene.layers[0].add_sprite(
    'p3_stand',
    pos=(scene.width / 2, scene.height / 2)
)
alien.speed = [0, 0]
alien.move_distance = 0
alien.jumping = False
alien.jump_speed = [0, 0]
alien.start_jump_y = 0

lasers = []

@w2d.event
def on_key_down(key, mod, unicode):
    if key == w2d.keys.ESCAPE:
        # I /think/ this is how you're supposed to quit?
        pygame.quit()
        w2d.game.exit()


def is_stopped(speed):
    return speed[0] == 0 and speed[1] == 0

@w2d.event
def update(t, dt, keyboard):
    global lasers
    
    if alien.jumping:
        alien.image = 'p3_jump'
        alien.x += alien.jump_speed[0] * dt
        alien.y += alien.jump_speed[1] * dt
        alien.jump_speed[1] += ALIEN_FALL_ACC * dt
        if alien.y > alien.start_jump_y:
            # below our starting jump height, so stop
            alien.jumping = False
            alien.y = alien.start_jump_y

    elif is_stopped(alien.speed) or sum(alien.speed) == 0:
        # stopped; reset walk distance and stand
        alien.move_distance = 0
        alien.image = 'p3_stand'

        # call _set_dirty() to force a redraw (workaround for a bug in Wasabi2d)
        alien._set_dirty()

    else:
        # moving
        alien.x += alien.speed[0] * dt
        alien.y += alien.speed[1] * dt
        alien.move_distance += abs(alien.speed[0] * dt) + abs(alien.speed[1] * dt)

        # face left or right if moving
        # (we keep facing the same way when stopped)
        if alien.speed[0] < 0:
            alien.scale_x = -1
        if alien.speed[0] > 0:
            alien.scale_x = 1

        # update walking frame every 12 pixels
        # p3_walk01 to p3_walk11
        walk_pos = (int(alien.move_distance / 12)) % 11 + 1
        alien.image = 'p3_walk{:0>2}'.format(walk_pos)

    if lasers:
        print("%d lasers: %s" % (len(lasers), [(l.x, l.speed) for l in lasers]))
        for laser in lasers:
            laser.x += laser.speed
        # replace lasers with just the ones onscreen
        lasers = [l for l in lasers 
                    if (laser.x > -laser.width and laser.speed < 0)     # right and moving left
                    or (laser.x < scene.width + laser.width and laser.speed > 0)]   # left and moving right

@w2d.event
def on_joybutton_down(joy, button):
    print("Button %s down on joystick %s" % (button, joy))
    if button == 0:
        laser = scene.layers[0].add_sprite(
            'laser',
            pos=alien.pos)
        laser.speed = 40 * alien.scale
        lasers.append(laser)

    if button == 1 and not alien.jumping:
        alien.jumping = True
        # jump height is proportional to how fast we run, but should
        # still be able to jump pretty high when stopped
        jump_y = ALIEN_SPEED + abs(alien.speed[0]) * 0.5
        alien.jump_speed = [alien.speed[0], -jump_y]
        alien.start_jump_y = alien.y + 1

@w2d.event
def on_joybutton_up(joy, button):
    print("Button %s up on joystick %s" % (button, joy))

def sanitise_axis(value):
    # make a small 'dead spot' in the middle or we'll drift
    if -0.05 < value < 0.05:
        return 0
    else:
        return value

# NB: Add the following to wasabi2d's game.py, line 61 if necessary:
#       'on_joyaxis_motion': pygame.JOYAXISMOTION,

@w2d.event
def on_joyaxis_motion(joy, axis, value):
    stick = controllers[joy]
    print("Movement on joystick %s: joy %s, axis: %s, value: %s" % (stick, joy, axis, value))

    if axis == 0:
        alien.speed[0] = sanitise_axis(value) * ALIEN_SPEED

    if axis == 1:
        alien.speed[1] = sanitise_axis(value) * ALIEN_SPEED

        
w2d.run()