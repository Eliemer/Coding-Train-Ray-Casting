import pyglet
import pyglet.graphics as pg
import math

def draw_line(x1, y1, x2, y2, col=None):
    if col == None:
        color = ('c3B', (255, 255, 255, 255, 255, 255))
    else :
        color = col
    pg.draw(
        2,
        pyglet.gl.GL_LINES,
        ('v2f', (x1, y1, x2, y2)),
        color
    )

class Boundary:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def show(self):
        draw_line(self.x1, self.y1, self.x2, self.y2)

class Particle:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.rays = []
        for a in range(0, 360, 3):
            self.rays.append(Ray(self.x, self.y, math.radians(a)))

    def update(self, x, y):
        self.x = x
        self.y = y
        for ray in self.rays:
            ray.update(x, y)

    def show(self):
        pg.draw(
            1,
            pyglet.gl.GL_POINTS,
            ('v2f', (
                self.x, self.y      # center dot
                )
            ),
            ('c3B', (0, 0, 255))
        )
        # for ray in self.rays:
        #     ray.show()
    
    def look(self, walls):
        for ray in self.rays:
            closest = None
            record = 9999
            for wall in walls:
                pt = ray.cast(wall)
                if pt != None:
                    d = Vector.dist(Vector(self.x, self.y), pt)
                    if d < record:
                        record = d
                        closest = pt
            if closest != None:
                draw_line(self.x, self.y, closest.x, closest.y, ('c3B', (0, 255, 0, 0, 255, 255)))


class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.dir = Vector.fromAngle(angle)

    def cast(self, wall):
        x1 = wall.x1
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2

        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dir.x
        y4 = self.y + self.dir.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if t > 0 and t < 1 and u > 0:
            x = x1 + (t *(x2 - x1))
            y = y1 + (t *(y2 - y1))
            return Vector(x, y)
        else:
            return None

    def show(self):
        draw_line(self.x, self.y, 
            self.x + self.dir.x * 10, 
            self.y + self.dir.y * 10,
            ('c3B', (0, 255, 0, 0, 255, 255))
        )

    def update(self, x, y):
        self.x = x
        self.y = y
        # self.dir = Vector.fromAngle(self.angle)

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def set(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def dist(pos1, pos2):
        return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)

    @staticmethod
    def fromAngle(angle, length=1):
        return Vector((length * math.cos(angle)), (length * math.sin(angle)))

