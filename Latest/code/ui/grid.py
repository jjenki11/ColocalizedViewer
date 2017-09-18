
import vtk

from point import Point
from line import Line
from dimension import Dimension
from matrix import Matrix4

#   3d grid
class Grid(object):

    def __init__(self, _origin=None, _dims=None, _res=None):
        self.resolution = None
        self.extents = None
        self.Dimension = None

        self.BBox = {}

        if(_origin):
            self.origin = Point(_origin)
        else:
            self.origin = Point([0.0, 0.0, 0.0])
        if(_res):
            self.resolution = _res
        else:
            self.resolution = [10, 10, 10]
        if (_dims):
            self.dimensions = Dimension(_dims[0], _dims[1], _dims[2])
        else:
            self.dimensions = Dimension(20, 20, 20)

        self.SetBoundingBox()


    def SetBoundingBox(self):

        self.h_neg_x = self.origin.x() - self.dimensions.GetWidth()/2
        self.h_pos_x = self.origin.x() + self.dimensions.GetWidth()/2

        self.h_neg_y = self.origin.y() - self.dimensions.GetHeight()/2
        self.h_pos_y = self.origin.y() + self.dimensions.GetHeight()/2

        self.h_neg_z = self.origin.z() - self.dimensions.GetDepth()/2
        self.h_pos_z = self.origin.z() + self.dimensions.GetDepth()/2

        # create bounding box
        #   letter key:
        #       u - up, d - down, r - right, l - left, f - front, b - back

        self.BBox['ulb'] = Point([self.h_neg_x, self.h_pos_y, self.h_neg_z])
        self.BBox['ulf'] = Point([self.h_neg_x, self.h_pos_y, self.h_pos_z])
        self.BBox['urb'] = Point([self.h_pos_x, self.h_pos_y, self.h_neg_z])
        self.BBox['urf'] = Point([self.h_pos_x, self.h_pos_y, self.h_pos_z])
        self.BBox['dlb'] = Point([self.h_neg_x, self.h_neg_y, self.h_neg_z])
        self.BBox['dlf'] = Point([self.h_neg_x, self.h_neg_y, self.h_pos_z])
        self.BBox['drb'] = Point([self.h_pos_x, self.h_neg_y, self.h_neg_z])
        self.BBox['drf'] = Point([self.h_pos_x, self.h_neg_y, self.h_pos_z])





    def BuildLine(self, p1, rgb):

        # Setup the colors array
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")

        # Add the colors we created to the colors array
        colors.InsertNextTupleValue(rgb)

        _min = p1.ToArray()[0]
        _max = p1.ToArray()[1]

        points = vtk.vtkPoints()

        #points.InsertNextPoint(o.ToArray())
        points.InsertNextPoint(_min)
        points.InsertNextPoint(_max)

        lines = vtk.vtkCellArray()
        for i in range(2):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, i+1)
            lines.InsertNextCell(line)

        linesPolyData = vtk.vtkPolyData()
        linesPolyData.SetPoints(points)
        linesPolyData.SetLines(lines)
        linesPolyData.GetCellData().SetScalars(colors)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(linesPolyData)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        return actor

    def BuildGrid(self, rgb):

        x_num_steps = 10
        y_num_steps = 10
        z_num_steps = 10

        grid_lines = []

        a = self.BBox['ulb']
        b = self.BBox['urb']

        x_offset = float(1 / x_num_steps)
        y_offset = float(1 / y_num_steps)
        z_offset = float(1 / z_num_steps)

        new_a = a
        new_a.SetY(a.y()-y_offset)
        new_b = b
        new_b.SetY(b.y()-y_offset)


        print("NEW A ")
        new_a.Print()

        print("NEW B ")
        new_b.Print()

        new_line = Line(Point(new_a), Point(new_b))

        xl = self.BuildLine(new_line, rgb)

        return [xl, xl, xl]


    def SetExtents(self, e):
        self.extents = e

    def SetResolution(self, r):
        self.resolution = r

    def ConstructBoundingBox(self):
        a = Line(self.BBox['ulb'], self.BBox['urb'])
        b = Line(self.BBox['ulf'], self.BBox['urf'])
        c = Line(self.BBox['dlb'], self.BBox['drb'])
        d = Line(self.BBox['dlf'], self.BBox['drf'])

        e = Line(self.BBox['ulb'], self.BBox['ulf'])
        f = Line(self.BBox['urb'], self.BBox['urf'])
        g = Line(self.BBox['dlb'], self.BBox['dlf'])
        h = Line(self.BBox['drb'], self.BBox['drf'])

        i = Line(self.BBox['ulb'], self.BBox['dlb'])
        j = Line(self.BBox['urb'], self.BBox['drb'])
        k = Line(self.BBox['ulf'], self.BBox['dlf'])
        l = Line(self.BBox['urf'], self.BBox['drf'])

        bb_lines = []
        white = [255, 255, 255]
        bb_lines.append(self.BuildLine(a, white))
        bb_lines.append(self.BuildLine(b, white))
        bb_lines.append(self.BuildLine(c, white))
        bb_lines.append(self.BuildLine(d, white))

        bb_lines.append(self.BuildLine(e, white))
        bb_lines.append(self.BuildLine(f, white))
        bb_lines.append(self.BuildLine(g, white))
        bb_lines.append(self.BuildLine(h, white))

        bb_lines.append(self.BuildLine(i, white))
        bb_lines.append(self.BuildLine(j, white))
        bb_lines.append(self.BuildLine(k, white))
        bb_lines.append(self.BuildLine(l, white))

        return bb_lines

    def ConstructViewVolume(self):
        gray = [255, 255, 255]

        the_grid = self.BuildGrid(gray)

        return the_grid

    def ConstructAxes(self):
        # Setup two colors - one for each line
        red   = [255, 0, 0]
        green = [0, 255, 0]
        blue  = [0, 0, 255]

        #   center grid lines (keep out of loop to make different colors
        x_axis = Line( \
            Point([self.h_neg_x, self.origin.y(), self.origin.z()]), \
            Point([self.h_pos_x, self.origin.y(), self.origin.z()]) \
            )

        y_axis = Line( \
            Point([self.origin.x(), self.h_neg_y, self.origin.z()]), \
            Point([self.origin.x(), self.h_pos_y, self.origin.z()]) \
            )

        z_axis = Line( \
            Point([self.origin.x(), self.origin.y(), self.h_neg_z]), \
            Point([self.origin.x(), self.origin.y(), self.h_pos_z]) \
            )

        xline = self.BuildLine(x_axis, red)
        yline = self.BuildLine(y_axis, green)
        zline = self.BuildLine(z_axis, blue)

        return [xline, yline, zline]

    def Get(self):
        return self

    def Rotate(self, rot):
        pass

    def Translate(self, trn):
        pass

    def Scale(self, scl):
        pass
