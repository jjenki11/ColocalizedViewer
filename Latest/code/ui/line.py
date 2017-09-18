from point import Point

from vtk import vtk


class Line(object):
    def __init__(self, pt1=None, pt2=None):
        if(pt1 != None)  and (pt2 != None):
            if(isinstance(pt1, Point) and isinstance(pt2, Point)):
                self.P1 = pt1
                self.P2 = pt2
            else:
                self.P1 = Point(pt1)
                self.P2 = Point(pt2)
                print("Created real points")
        else:
            self.P1 = Point()
            self.P2 = Point()
            print("Created 000 ponits)")

    def __add__(self, _l):
        return Line(self.P1 + _l.P1, self.P2 + _l.P2)

    def __sub__(self, _l):
        return Line(self.P1 - _l.P1, self.P2 - _l.P2)

    def __mul__(self, _l):
        return Line(self.P1 * _l.P1, self.P2 * _l.P2)

    def __div__(self, _l):
        return Line(self.P1 / _l.P1, self.P2 / _l.P2)

    def SetPoint1(self, p):
        self.P1.X = p.X
        self.P1.Y = p.Y
        self.P1.Z = p.Z

    def SetPoint2(self, p):
        self.P2.X = p.X
        self.P2.Y = p.Y
        self.P2.Z = p.Z

    def p1(self):
        return self.P1

    def p2(self):
        return self.P2

    def Get(self):
        return self

    def ToArray(self):
        return [self.p1().ToArray(), self.p2().ToArray()]

    def Print(self):
        print("p1 -> " )
        self.P1.Print()
        print("p2 -> ")
        self.P2.Print()


'''
p1 = [2, 2, 2]
p2 = [5, 5, 5]
p3 = [5, 5, 5]
p4 = [2, 2, 2]

l1 = Line(p1, p2)
l2 = Line(p3, p4)

l3 = l1 / l2
l3.Print()
'''