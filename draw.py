import pyglet
import pyglet.graphics as pg
from classes import Boundary, Particle
import random
import noise
import numpy as np

win = pyglet.window.Window(width=800, height=600)
win.set_location(int(1920/4), int(1080/4))

Walls = []
size = win.get_size()
xoff = random.randint(1, 1000)
yoff = random.randint(1, 1000)

Walls.append(Boundary(0, 0, size[0], 0))                # top 
Walls.append(Boundary(size[0], 0, size[0], size[1]))    # right 
Walls.append(Boundary(size[0], size[1], 0, size[1]))    # bottom
Walls.append(Boundary(0, size[1], 0, 0))                # left

particle = Particle()

for i in range(5):                                      # add 5 randomly place walls
    x1 = random.random() * size[0]
    x2 = random.random() * size[0]
    y1 = random.random() * size[1]
    y2 = random.random() * size[1]
    Walls.append(Boundary(x1, y1, x2, y2))

def on_draw(x):
    win.clear()
    global xoff, yoff, particle
    for wall in Walls:
        wall.show()
    
    newX = np.interp(noise.pnoise1(x=xoff, octaves=2), [-1, 1], [0, size[0]])
    newY = np.interp(noise.pnoise1(x=yoff, octaves=2), [-1, 1], [0, size[1]])
    particle.update(newX, newY)
    particle.show()
    particle.look(Walls)
    xoff += 0.01
    yoff += 0.01

pyglet.clock.schedule_interval(on_draw,1/60.0)

if __name__ == '__main__':
    pyglet.app.run()