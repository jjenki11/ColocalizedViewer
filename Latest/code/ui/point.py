import itk


class Point(object):
    def __init__(self, pts=None):
        if(pts):
            self.X = float(pts[0])
            self.Y = float(pts[1])
            self.Z = float(pts[2])
        else:
            self.X = float(0.0)
            self.Y = float(0.0)
            self.Z = float(0.0)

    def __add__(self, _p):
        return Point([(self.X + _p.X), (self.Y + _p.Y), (self.Z + _p.Z)])

    def __sub__(self, _p):
        return Point([(self.X - _p.X), (self.Y - _p.Y), (self.Z - _p.Z)])

    def __mul__(self, _p):
        return Point([(self.X * _p.X), (self.Y * _p.Y), (self.Z * _p.Z)])

    def __div__(self, _p):
        return Point([(self.X / _p.X), (self.Y / _p.Y), (self.Z / _p.Z)])

    def SetPoint(self, p):
        self.X = p[0]
        self.Y = p[1]
        self.Z = p[2]

    def __setitem__(self, index, val):
        if(index == 0):
            self.X = val
        if(index == 1):
            self.Y = val
        if(index == 2):
            self.Z = val

    def __getitem__(self, index):
        if(index == 0):
            return self.x()
        if(index == 1):
            return self.y()
        if(index == 2):
            return self.z()


    def SetX(self, _x):
        self.X = _x

    def SetY(self, _y):
        self.Y = _y

    def SetZ(self, _z):
        self.Z = _z

    def x(self):
        return self.X

    def y(self):
        return self.Y

    def z(self):
        return self.Z

    def Get(self):
        return self

    def ToArray(self):
        return [self.x(), self.y(), self.z()]

    def ToItk(self):
        dim = 3
        type = itk.D
        VectorType = itk.Vector[type, dim]
        val = VectorType()
        val[0] = (self.x())
        val[1] = (self.y())
        val[2] = (self.z())
        return val

    def Print(self):
        print("("+str(self.x())+", "+str(self.y())+", "+str(self.z())+")")


'''
a = Point([1,1,1])
b = Point([5,5,5])
c = a + b
a.Print()
b.Print()
c.Print()
'''

