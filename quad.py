'''
Quadtree implementation in python for use with h3 indices
'''

from random import randint, choice, seed

seed(0)

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y})'

class Rectangle(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return f'Rectangle(x={self.x}, y={self.y}, w={self.w}, h={self.h}'

    def contains(self, point):
        return (point.x >= self.x - self.w and
                point.x < self.x + self.w and
                point.y >= self.y - self.h and
                point.y < self.y + self.h)

    def intersects(self, area):
        return not(area.x - area.w > self.x + self.w or
                   area.x + area.w < self.x - self.w or
                   area.y - area.h > self.y + self.h or
                   area.y + area.h < self.y - self.h)

class Quad(object):
    def __init__(self, boundary, capacity):
        '''
        cap: capacity of number of points in a quadtree
        root: node
        '''
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.ne = None
        self.nw = None
        self.se = None
        self.sw = None
        self.divided = False

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if (len(self.points) < self.capacity):
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
                self.divided = True

        if self.ne.insert(point):
            return True
        elif self.nw.insert(point):
            return True
        elif self.se.insert(point):
            return True
        elif self.sw.insert(point):
            return True

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        ne = Rectangle(x+w/2, y-h/2, w/2, h/2)
        nw = Rectangle(x-w/2, y-h/2, w/2, h/2)
        se = Rectangle(x+w/2, y+h/2, w/2, h/2)
        sw = Rectangle(x-w/2, y+h/2, w/2, h/2)

        self.ne = Quad(ne, self.capacity)
        self.nw = Quad(nw, self.capacity)
        self.se = Quad(se, self.capacity)
        self.sw = Quad(sw, self.capacity)

    def query(self, area):
        return self._query(area, [])

    def _query(self, area, found):
        if not self.boundary.intersects(area):
            return found
        else:
            for p in self.points:
                if area.contains(p):
                    found.append(p)

        if self.divided:
            self.ne._query(area, found)
            self.nw._query(area, found)
            self.se._query(area, found)
            self.sw._query(area, found)

        return found

    def __repr__(self):
        return f'Quad(capacity={self.capacity}, boundary={self.boundary}, points={self.points}, se={self.se}, sw={self.sw}, ne={self.ne}, nw={self.nw}, divided={self.divided})'

if __name__ == '__main__':
    point = Point(0, 0)
    # print(point)
    rect = Rectangle(0, 0, 100, 100)
    # print(rect)
    quad = Quad(rect, 4)
    rand_points = [Point(randint(1, 50), randint(1, 50)) for _ in range(20)]
    # print(rand_points)
    for p in rand_points:
        quad.insert(p)
    print(quad)
    area = Rectangle(10, 10, 20, 20)
    queried = quad.query(area)
    print(queried)
