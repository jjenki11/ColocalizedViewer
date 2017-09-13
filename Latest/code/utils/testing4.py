#   Jeff Jenkins
#   NIH-NIBIB-QMI
#   9/7/2016 - Date of Latest Revisions
#   This creates a GUI which is a composition of several packages.

# include the packages
from PyQt5 import QtCore, QtGui, QtWidgets
import vtk
import itk
import math
import os
import numpy as np

import nibabel as nib

#from widgets import *


# class to hold all utility functions
class UiUtils(object):
    def __init__(self):
        print('utils.')

        # fills relevant fields when the 'fill' button is pressed

    def FillMriFields(self):
        widget_map['mri_header'] = NiftiFile()
        widget_map['mri_header'].ReadFile(widget_map['mri_file'].GetText())
        widget_map['mri_header'].SetHeader(widget_map['mri_header'].header)
        widget_map['mri_header'].PrintHeader()
        dim_array = widget_map['mri_header'].GetDimensions()
        widget_map['mri_n_voxels_x'].SetText(dim_array[1])
        widget_map['mri_n_voxels_y'].SetText(dim_array[2])
        widget_map['mri_n_voxels_z'].SetText(dim_array[3])
        size_array = widget_map['mri_header'].GetVoxelSize()
        widget_map['mri_s_voxels_x'].SetText(size_array[1])
        widget_map['mri_s_voxels_y'].SetText(size_array[2])
        widget_map['mri_s_voxels_z'].SetText(size_array[3])

    #  Creates a popup
    def CreatePopup(self):
        popup = OkPopup(['setup_window'], ['vtk_options_frame', 'vtk_widget'])

    # opens a file dialog and populates the mrifile field
    def mriopenfile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        str_fname = ''.join(fname[0])
        print str_fname
        widget_map['mri_file'].SetText(str_fname)

    # opens a file dialog and populates the histofile field
    def histoopenfile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        str_fname = ''.join(fname[0])
        print str_fname
        widget_map['histo_file'].SetText(str_fname)



    def SetupHistologyActor(self):
        # create plane as base obj
        widget_map['plane_widget'] = vtk.vtkPlaneSource()
        widget_map['plane_widget'].Update()

        # load tiff file
        tiffFile = vtk.vtkTIFFReader()

        if (home_pc):
            #   much nicer now that we are doing it with anaconda... doesnt require us to put a path relative to python
            tiffFile.SetFileName(os.getcwd() + '\\data\\76.tif')
        elif (from_gui):
            tiffFile.SetFileName(widget_map['histo_file'].GetText())
        else:
            tiffFile.SetFileName('/stbb_home/jenkinsjc/Desktop/LandmarkTesting/76.tif');

        tiffFile.Update()

        min_val = widget_map['mri_nifti_ptr'].GetMin()
        max_val = widget_map['mri_nifti_ptr'].GetMax()
        spacing = widget_map['mri_nifti_ptr'].GetVoxelSize()
        origin = widget_map['mri_nifti_ptr'].GetOrigin()

        mri_center = widget_map['mri_actor'].GetCenter()

        pixel_size = .1
        tiff_dims = tiffFile.GetOutput().GetExtent()

        print(str(tiff_dims))

        cols = tiff_dims[1] + 1
        rows = tiff_dims[3] + 1

        print("ROWS -> " + str(rows))
        print("COLS -> " + str(cols))


        widget_map['plane_widget'].SetPoint1(cols*pixel_size, 0.0, 0.0)
        widget_map['plane_widget'].SetPoint2(0.0, rows*pixel_size, 0.0)

        #widget_map['plane_widget'].SetCenter(rows*pixel_size, cols*pixel_size, 0.0)
        #widget_map['plane_widget'].SetXResolution(int(1 ))
        #widget_map['plane_widget'].SetYResolution(int(1 ))

        widget_map['plane_widget'].Update()


        #print("Position OF plane -> " + str(widget_map['plane_widget'].GetPosition()))
        print("Center OF plane -> " + str(widget_map['plane_widget'].GetCenter()))

        # make a texture out of the tiff file
        tex = vtk.vtkTexture()
        tex.SetInputConnection(tiffFile.GetOutputPort())

        # make a texture mapper for the plane
        map_to_plane = vtk.vtkTextureMapToPlane()
        map_to_plane.SetInputConnection(widget_map['plane_widget'].GetOutputPort())

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(map_to_plane.GetOutputPort())

        # actor
        widget_map['plane_actor'] = vtk.vtkActor()
        widget_map['plane_actor'].SetMapper(mapper)
        widget_map['plane_actor'].SetTexture(tex)

        #widget_map['plane_actor'].SetOrigin(center[0], center[1], center[2])


        widget_map['vtk_widget'].SetParentActor(widget_map['plane_actor'])
        widget_map['v_ren'].AddActor(widget_map['plane_actor'])


    def SetupMriActor(self):
        widget_map['v_ren'].AddVolume(MriVolumeRenderTest())



# global mapping (only in this file) of widget names to their object
widget_map = {}

g_utils = UiUtils()


# GLOBAL props
textbox_width = 50;
filebox_width = 150;
default_min_lut = 0.0;
default_max_lut = 500.0;

home_pc = False;

from_gui = True;


# Register widget by nam e to our global mapping
def RegisterWidget(name, widget):
    widget_map[name] = widget


def ShowWidgets(w_list):
    for w in w_list:
        widget_map[w].show()

def HideWidgets(w_list):
    for w in w_list:
        widget_map[w].hide()


def l2n(l):
    return lambda l: np.array(l)


def n2l(n):
    return lambda n: list(n)


# Subclassed itk matrix
class Matrix(object):
    def __init__(self):
        self.m = itk.Matrix.D44()
        self.m.SetIdentity()

        self.tx = itk.Matrix.D44()
        self.tx.SetIdentity()

        self.ty = itk.Matrix.D44()
        self.ty.SetIdentity()

        self.tz = itk.Matrix.D44()
        self.tz.SetIdentity()

        self.rx = itk.Matrix.D44()
        self.rx.SetIdentity()

        self.ry = itk.Matrix.D44()
        self.ry.SetIdentity()

        self.rz = itk.Matrix.D44()
        self.rz.SetIdentity()

        self.sx = itk.Matrix.D44()
        self.sx.SetIdentity()

        self.sy = itk.Matrix.D44()
        self.sy.SetIdentity()

        self.sz = itk.Matrix.D44()
        self.sz.SetIdentity()

    def Get(self):
        return self.m.GetVnlMatrix()

    def GetTx(self):
        return self.tx

    def GetTy(self):
        return self.ty

    def GetTz(self):
        return self.tz

    def GetRx(self):
        return self.rx

    def GetRy(self):
        return self.ry

    def GetRz(self):
        return self.rz

    def GetSx(self):
        return self.sx

    def GetSy(self):
        return self.sy

    def GetSz(self):
        return self.sz

    def Print(self):
        m = self.Get()
        r1 = str(m.get(0, 0)) + ", " + str(m.get(0, 1)) + ", " + str(m.get(0, 2)) + ", " + str(m.get(0, 3))
        r2 = str(m.get(1, 0)) + ", " + str(m.get(1, 1)) + ", " + str(m.get(1, 2)) + ", " + str(m.get(1, 3))
        r3 = str(m.get(2, 0)) + ", " + str(m.get(2, 1)) + ", " + str(m.get(2, 2)) + ", " + str(m.get(2, 3))
        r4 = str(m.get(3, 0)) + ", " + str(m.get(3, 1)) + ", " + str(m.get(3, 2)) + ", " + str(m.get(3, 3))
        print(r1)
        print(r2)
        print(r3)
        print(r4)
        self.Update()

    def Print(self, m):
        mat = None
        if (m):
            mat = self.Get()
        else:
            mat = m.GetVnlMatrix()

        r1 = str(mat.get(0, 0)) + ", " + str(mat.get(0, 1)) + ", " + str(mat.get(0, 2)) + ", " + str(mat.get(0, 3))
        r2 = str(mat.get(1, 0)) + ", " + str(mat.get(1, 1)) + ", " + str(mat.get(1, 2)) + ", " + str(mat.get(1, 3))
        r3 = str(mat.get(2, 0)) + ", " + str(mat.get(2, 1)) + ", " + str(mat.get(2, 2)) + ", " + str(mat.get(2, 3))
        r4 = str(mat.get(3, 0)) + ", " + str(mat.get(3, 1)) + ", " + str(mat.get(3, 2)) + ", " + str(mat.get(3, 3))
        print("")
        print(r1)
        print(r2)
        print(r3)
        print(r4)
        print("")
        self.Update()

    def RotateX(self, rot):
        self.rx.GetVnlMatrix().set(1, 1, math.cos(rot))
        self.rx.GetVnlMatrix().set(1, 2, -math.sin(rot))
        self.rx.GetVnlMatrix().set(2, 1, math.sin(rot))
        self.rx.GetVnlMatrix().set(2, 2, math.cos(rot))
        self.Update()

    def RotateY(self, rot):
        self.ry.GetVnlMatrix().set(0, 0, math.cos(rot))
        self.ry.GetVnlMatrix().set(0, 2, math.sin(rot))
        self.ry.GetVnlMatrix().set(2, 0, -math.sin(rot))
        self.ry.GetVnlMatrix().set(2, 2, math.cos(rot))
        self.Update()

    def RotateZ(self, rot):
        self.rz.GetVnlMatrix().set(0, 0, math.cos(rot))
        self.rz.GetVnlMatrix().set(0, 1, -math.sin(rot))
        self.rz.GetVnlMatrix().set(1, 0, math.sin(rot))
        self.rz.GetVnlMatrix().set(1, 1, math.cos(rot))
        self.Update()

    def TranslateX(self, trans):
        self.tx.GetVnlMatrix().set(0, 3, trans)
        self.Update()

    def TranslateY(self, trans):
        self.ty.GetVnlMatrix().set(1, 3, trans)
        self.Update()

    def TranslateZ(self, trans):
        self.tz.GetVnlMatrix().set(2, 3, trans)
        self.Update()

    def ScaleX(self, scl):
        self.tx.GetVnlMatrix().set(0, 0, scl)
        self.Update()

    def ScaleY(self, scl):
        self.ty.GetVnlMatrix().set(1, 1, scl)
        self.Update()

    def ScaleZ(self, scl):
        self.tz.GetVnlMatrix().set(2, 2, scl)
        self.Update()


    def Update(self):
        self.m = (self.GetTz() * self.GetTy() * self.GetTx()) \
               * (self.GetRz() * self.GetRy() * self.GetRx()) \
               * (self.GetSz() * self.GetSy() * self.GetSx())

    # be careful about transposing between itk and vtk matrix type
    def ToVtkTransform(self):
        mat = vtk.vtkMatrix4x4()
        m = self.Get()
        mat.SetElement(0, 0, m.get(0, 0))
        mat.SetElement(0, 1, m.get(0, 1))
        mat.SetElement(0, 2, m.get(0, 2))
        mat.SetElement(0, 3, m.get(0, 3))

        mat.SetElement(1, 0, m.get(1, 0))
        mat.SetElement(1, 1, m.get(1, 1))
        mat.SetElement(1, 2, m.get(1, 2))
        mat.SetElement(1, 3, m.get(1, 3))

        mat.SetElement(2, 0, m.get(2, 0))
        mat.SetElement(2, 1, m.get(2, 1))
        mat.SetElement(2, 2, m.get(2, 2))
        mat.SetElement(2, 3, m.get(2, 3))

        mat.SetElement(3, 0, m.get(3, 0))
        mat.SetElement(3, 1, m.get(3, 1))
        mat.SetElement(3, 2, m.get(3, 2))
        mat.SetElement(3, 3, m.get(3, 3))
        vmat = vtk.vtkTransform()
        vmat.Identity()
        vmat.SetMatrix(mat)
        vmat.Update()
        return vmat


# Subclassed vtk volume rendering stuff
class VolumeRenderer(object):
    def __init__(self):
        pass


# Subclassed qframe widget
class Frame(QtWidgets.QFrame):
    def __init__(self, box_type, _contents):
        super(Frame, self).__init__()
        self.layout = None
        self.type = box_type
        self.contents = _contents
        if (self.type == 'h'):
            self.layout = HBox(self.contents)
        if (self.type == 'v'):
            self.layout = VBox(self.contents)
        self.setLayout(self.layout)

    def Append(self, cont):
        self.contents.append(cont)
        if(self.type == 'h'):
            self.layout = HBox(self.contents)
        if (self.type == 'v'):
            self.layout = VBox(self.contents)
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(self.layout)


# Subclassed horizontal container widget
class HBox(QtWidgets.QHBoxLayout):
    def __init__(self, contents):
        super(HBox, self).__init__()
        self.append(contents)

    def append(self, items):
        for item in items:
            self.addWidget(item)


# Subclassed vertical container widget
class VBox(QtWidgets.QVBoxLayout):
    def __init__(self, contents):
        super(VBox, self).__init__()
        self.append(contents)

    def append(self, items):
        for item in items:
            self.addWidget(item)


# Subclassed text box widget
class TextBox(QtWidgets.QLineEdit):
    def __init__(self, txt, size, w_name=None):
        super(TextBox, self).__init__()
        self.SetText(txt)
        self.setFixedWidth(size)
        RegisterWidget(w_name, self)

    def SetText(self, txt):
        self.setText(str(txt))

    def GetText(self):
        return self.text()


# Subclassed label widget
class Label(QtWidgets.QLabel):
    def __init__(self, t, w_name=None):
        super(Label, self).__init__(t)
        self.SetText(t)
        self.name = w_name
        RegisterWidget(w_name, self)

    def SetText(self, lbl):
        self.setText(str(lbl))

    def GetName(self):
        return self.name


# Subclassed button widget
class Button(QtWidgets.QPushButton):
    def __init__(self, t, f, w_name=None):
        super(Button, self).__init__()
        self.Text(t)
        self.clicked.connect(f)
        self.show()
        RegisterWidget(w_name, self)

    def Text(self, t):
        self.setText(t)


# Subclassed slider widget with some global operations
class Slider(QtWidgets.QSlider):
    def __init__(self, _dir, _min, _max, _step, w_name, l_name):
        if (_dir == 'h'):
            super(Slider, self).__init__(QtCore.Qt.Horizontal)
        if (_dir == 'v'):
            super(Slider, self).__init__(QtCore.Qt.Vertical)
        # slider = QSlider(Qt.Horizontal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setTickPosition(self.TicksBothSides)
        self.setMinimum(_min)
        self.setMaximum(_max)
        self.setTickInterval(10)
        self.setSingleStep(_step)
        self.disp_label = widget_map[l_name]
        self.valueChanged[int].connect(self.changeValue)
        self.sliderMoved.connect(self.changeValue)
        RegisterWidget(w_name, self)

    def GetValue(self):
        return self.value()

    def changeValue(self, value):
        print(str(self.disp_label.GetName()))

        if (self.disp_label.GetName() == 'sx_slider_label'):
            self.disp_label.SetText("sX: " + str(value))
            widget_map['model_matrix'].ScaleX(value)
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())
        if (self.disp_label.GetName() == 'sy_slider_label'):
            self.disp_label.SetText("sY: " + str(value))
            widget_map['model_matrix'].ScaleY(value)
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())
        if (self.disp_label.GetName() == 'sz_slider_label'):
            self.disp_label.SetText("sZ: " + str(value))
            widget_map['model_matrix'].ScaleZ(value)
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())



        if (self.disp_label.GetName() == 'theta_slider_label'):
            self.disp_label.SetText("Theta: " + str(value))
            widget_map['model_matrix'].RotateX(math.radians(value))
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())
        if (self.disp_label.GetName() == 'phi_slider_label'):
            self.disp_label.SetText("Phi: " + str(value))
            widget_map['model_matrix'].RotateY(math.radians(value))
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())
        if (self.disp_label.GetName() == 'rho_slider_label'):
            self.disp_label.SetText("Rho: " + str(value))
            widget_map['model_matrix'].RotateZ(math.radians(value))
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())

        if (self.disp_label.GetName() == 'x_slider_label'):
            self.disp_label.SetText("X: " + str(value))
            widget_map['model_matrix'].TranslateX(value)
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())
        if (self.disp_label.GetName() == 'y_slider_label'):
            self.disp_label.SetText("Y: " + str(value))
            widget_map['model_matrix'].TranslateY(value)
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())
        if (self.disp_label.GetName() == 'z_slider_label'):
            self.disp_label.SetText("Z: " + str(value))
            widget_map['model_matrix'].TranslateZ(value)
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())




        if (self.disp_label.GetName() == 'min_lut_label'):
            self.disp_label.SetText("Min: " + str(value))
            widget_map['min_lut_value'] = value

        if (self.disp_label.GetName() == 'max_lut_label'):
            self.disp_label.SetText("Max: " + str(value))
            widget_map['max_lut_value'] = value

        # apply color map
        xferFunc = vtk.vtkPiecewiseFunction()
        xferFunc.AddPoint(widget_map['min_lut_value'], 0.0)
        xferFunc.AddPoint(widget_map['max_lut_value'], 255.0)
        widget_map['mri_volume_property'].SetColor(xferFunc)

        #   apply transformation
        transformation = widget_map['model_matrix'].ToVtkTransform()
        widget_map['mri_actor'].SetUserTransform(transformation)
        widget_map['landmark_list'].Reset()

        for la in widget_map['landmark_actors']:
            la.SetUserTransform(transformation)
            widget_map['landmark_list'].Insert(str(la.GetCenter()))
        widget_map['vtk_widget'].Render()


# Subclassed combo box widget
class DropDown(QtWidgets.QComboBox):
    def __init__(self, s, w_name):
        super(DropDown, self).__init__()
        RegisterWidget(w_name, self)
        self.setMaximumWidth(100)
        self.addItems(s)

    def GetText(self):
        return unicode(self.currentText())


# Subclassed list widget
class List(QtWidgets.QListWidget):
    def __init__(self, it, w_name=None):
        super(List, self).__init__()

        self.items = []
        if (len(it) > 0):
            self.items = it
            self.addItems(self.items)
        RegisterWidget(w_name, self)

    def Reset(self):
        self.items = []
        self.clear()

    def Insert(self, it):
        self.items.append(it)
        self.clear()
        self.addItems(self.items)

    def Remove(self):
        rnum = self.currentRow()
        item = self.takeItem(rnum)
        self.items.pop(rnum)
        del item
        return rnum

    def RemoveIndex(self, rnum):
        item = self.takeItem(rnum)
        self.items.pop(rnum)
        del item
        return rnum

    def GetItems(self):
        ret_items = []
        for index in xrange(self.count()):
            ret_items.append(self.item(index))
        return ret_items

    def GetItemAtIndex(self):
        return self.item(self.currentRow())

    def SetItems(self, items):
        self.Reset()
        for it in items:
            self.addItem(str(it))
            self.items.append(str(it))

    def keyPressEvent(self, ev):
        if ev.key() < 256:
            key = str(ev.text())
        else:
            key = chr(0)

        if (ev.key() == QtCore.Qt.Key_Delete):
            print("PRESSED DELETE (list event)!!!")
            # print("THE ITEM -> " + str(self.GetItemAtIndex().text()))
            # _pos = str(self.GetItemAtIndex().text())
            # parr = []
            # _posstr = _pos.replace('[', '').replace(']', '')
            # parr = _posstr.split(',')
            # fparr = []
            # for p in parr:
            #    fparr.append(float(p))
            # print("POS -> " + str(_pos))
            # act = GetPickedActor(fparr, widget_map['vtk_widget'].ren)
            # print("What is act?  "+str(act))
            # if (act ):
            #    widget_map['vtk_widget'].ren.RemoveActor(act)
            #    widget_map['vtk_widget'].Marks.RemoveLandmark(act)
            # self.Remove()


# create a landmark and add it to the renderer
def MakeLandmark(pos):
    source = vtk.vtkSphereSource()
    source.SetCenter(pos[0], pos[1], pos[2])
    source.SetRadius(0.1)
    source.Update()
    _mapper = vtk.vtkPolyDataMapper()
    _mapper.SetInputConnection(source.GetOutputPort())
    act = vtk.vtkActor()
    act.SetMapper(_mapper)
    widget_map['landmark_actors'].append(act)
    return act


# get the location where the mouse clicked
def GetPickedLocation(_ePos, _ren):
    clickPos = [i for i in _ePos]
    picker = vtk.vtkPropPicker();
    picker.Pick(clickPos[0], clickPos[1], 0, _ren)
    return [i for i in picker.GetPickPosition()]


# get the actor under the mouse
def GetPickedActor(_ePos, _ren):
    clickPos = [i for i in _ePos]
    picker = vtk.vtkPropPicker();
    picker.Pick(clickPos[0], clickPos[1], 0, _ren)
    return picker.GetActor()


# class that is a point object (tbd refactor to combine point and landmark)
class Point(object):
    def __init__(self, pt):
        pixeltype = itk.D
        dim = 3
        self.p = itk.Point[pixeltype, dim]()
        self.p.SetElement(0, pt[0]);
        self.p.SetElement(1, pt[1]);
        self.p.SetElement(2, pt[2]);

    def Get(self):
        return self


# class that is a pointset object (tbd refactor to combine pointset and landmarkset)
class PointSet(object):
    def __init__(self):
        self.length = 0;
        self.pixeltype = itk.D
        self.dim = 3
        self.traitstype = itk.DefaultStaticMeshTraits[itk.D, self.dim, self.dim]
        self.pointsettype = itk.PointSet[itk.D, self.dim, self.traitstype]
        self.pointset1 = self.pointsettype.New()
        self.points = self.pointset1.GetPoints()

    def AddPoint(self, p):
        self.length = self.length + 1
        pt = itk.Point[self.pixeltype, self.dim]()
        pt[0] = p[0];
        pt[1] = p[1];
        pt[2] = p[2];
        self.points.InsertElement(self.length, pt)

    def GetPoints(self):
        return self.points

    def PrintPoints(self):
        for i in range(0, self.length):
            pointType = itk.Point[itk.D, 3]
            pp = pointType()
            pp = self.pointset1.GetPoint(i)
            print ("Point is = " + str(pp.GetElement(0)) + ", " + str(pp.GetElement(1)) + ", " + str(pp.GetElement(2)))


# class that represents a landmark and some basic operations on the landmark
class Landmark(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


# class that holds a set of landmarks with some basic operations on the set
class LandmarkSet(object):
    def __init__(self):
        self.actors = []
        self.points = []

    def AddLandmark(self, _mark, _pos):
        self.actors.append(_mark)
        self.points.append(_pos)
        print("Added point to set.")
        print("we now have => " + str(len(self.points)))
        # widget_map['landmark_list'].Insert(str(_pos))

    def RemoveLandmark(self, _mark):
        if (_mark in self.actors) and isinstance(self.actors.index(_mark), int):
            idx = self.actors.index(_mark)
            self.actors.remove(_mark)
            self.points.pop(idx)
            print("Removed point from set.")
            print("we now have => " + str(len(self.points)) + " points")
            print("we now have => " + str(len(self.actors)) + " actors")
            widget_map['landmark_list'].SetItems((self.points))
            return idx

    def RemoveCurrentLandmark(self):
        # idx = self.actors.index(_mark)
        _mark = widget_map['landmark_list'].GetItemAtIndex()
        print("REMOVING CURRENT SELECTION -> " + str(_mark))
        return self.RemoveLandmark(_mark)

    def ExtractPoints(self):
        pts = []
        for p in self.points:
            print("POSITION -> " + str(p))
            pts.append(p)

    def Save(self, fn):
        f = open(fn, 'w')
        f.write(str(self.points))
        f.close()

    def Load(self, fn):
        self.actors = []
        self.points = []
        f = open(fn, 'r+')
        for line in f:
            self.actors.append(MakeLandmark(','.join(line)))
            self.points.append(line)

        print("Our actors and points -> " + str(self.actors) + ",         " + str(self.points))


# controller for different global button actions
class ButtonController(object):
    def __init__(self):
        print("Created button controller")

    def ResetScale(self):
        widget_map['x_scale_slider'].setValue(1)
        widget_map['y_scale_slider'].setValue(1)
        widget_map['z_scale_slider'].setValue(1)

    def ResetRotation(self):
        widget_map['theta_rot_slider'].setValue(0)
        widget_map['phi_rot_slider'].setValue(0)
        widget_map['rho_rot_slider'].setValue(0)

    def ResetTranslation(self):
        widget_map['x_trans_slider'].setValue(0)
        widget_map['y_trans_slider'].setValue(0)
        widget_map['z_trans_slider'].setValue(0)

    def ResetLUT(self):
        widget_map['min_lut_slider'].setValue(default_min_lut)
        widget_map['max_lut_slider'].setValue(default_max_lut)

        xferFunc = vtk.vtkPiecewiseFunction()
        xferFunc.AddPoint(default_min_lut, 0.0)
        xferFunc.AddPoint(default_max_lut, 255.0)
        widget_map['mri_volume_property'].SetColor(xferFunc)


# subclassed qwidget which is actually a composite qt and vtk widget
class QVTKRenderWindowInteractor(QtWidgets.QWidget):
    """ A QVTKRenderWindowInteractor for Python and Qt.  Uses a
    vtkGenericRenderWindowInteractor to handle the interactions.  Use
    GetRenderWindow() to get the vtkRenderWindow.  Create with the
    keyword stereo=1 in order to generate a stereo-capable window.

    The user interface is summarized in vtkInteractorStyle.h:

    - Keypress j / Keypress t: toggle between joystick (position
    sensitive) and trackball (motion sensitive) styles. In joystick
    style, motion occurs continuously as long as a mouse button is
    pressed. In trackball style, motion occurs when the mouse button
    is pressed and the mouse pointer moves.

    - Keypress c / Keypress o: toggle between camera and object
    (actor) modes. In camera mode, mouse events affect the camera
    position and focal point. In object mode, mouse events affect
    the actor that is under the mouse pointer.

    - Button 1: rotate the camera around its focal point (if camera
    mode) or rotate the actor around its origin (if actor mode). The
    rotation is in the direction defined from the center of the
    renderer's viewport towards the mouse position. In joystick mode,
    the magnitude of the rotation is determined by the distance the
    mouse is from the center of the render window.

    - Button 2: pan the camera (if camera mode) or translate the actor
    (if object mode). In joystick mode, the direction of pan or
    translation is from the center of the viewport towards the mouse
    position. In trackball mode, the direction of motion is the
    direction the mouse moves. (Note: with 2-button mice, pan is
    defined as <Shift>-Button 1.)

    - Button 3: zoom the camera (if camera mode) or scale the actor
    (if object mode). Zoom in/increase scale if the mouse position is
    in the top half of the viewport; zoom out/decrease scale if the
    mouse position is in the bottom half. In joystick mode, the amount
    of zoom is controlled by the distance of the mouse pointer from
    the horizontal centerline of the window.

    - Keypress 3: toggle the render window into and out of stereo
    mode.  By default, red-blue stereo pairs are created. Some systems
    support Crystal Eyes LCD stereo glasses; you have to invoke
    SetStereoTypeToCrystalEyes() on the rendering window.  Note: to
    use stereo you also need to pass a stereo=1 keyword argument to
    the constructor.

    - Keypress e: exit the application.

    - Keypress f: fly to the picked point

    - Keypress p: perform a pick operation. The render window interactor
    has an internal instance of vtkCellPicker that it uses to pick.

    - Keypress r: reset the camera view along the current view
    direction. Centers the actors and moves the camera so that all actors
    are visible.

    - Keypress s: modify the representation of all actors so that they
    are surfaces.

    - Keypress u: invoke the user-defined function. Typically, this
    keypress will bring up an interactor that you can type commands in.

    - Keypress w: modify the representation of all actors so that they
    are wireframe.
    """

    # Map between VTK and Qt cursors.
    _CURSOR_MAP = {
        0: QtCore.Qt.ArrowCursor,  # VTK_CURSOR_DEFAULT
        1: QtCore.Qt.ArrowCursor,  # VTK_CURSOR_ARROW
        2: QtCore.Qt.SizeBDiagCursor,  # VTK_CURSOR_SIZENE
        3: QtCore.Qt.SizeFDiagCursor,  # VTK_CURSOR_SIZENWSE
        4: QtCore.Qt.SizeBDiagCursor,  # VTK_CURSOR_SIZESW
        5: QtCore.Qt.SizeFDiagCursor,  # VTK_CURSOR_SIZESE
        6: QtCore.Qt.SizeVerCursor,  # VTK_CURSOR_SIZENS
        7: QtCore.Qt.SizeHorCursor,  # VTK_CURSOR_SIZEWE
        8: QtCore.Qt.SizeAllCursor,  # VTK_CURSOR_SIZEALL
        9: QtCore.Qt.PointingHandCursor,  # VTK_CURSOR_HAND
        10: QtCore.Qt.CrossCursor,  # VTK_CURSOR_CROSSHAIR
    }

    def __init__(self, parent=None, wflags=QtCore.Qt.WindowFlags(), **kw):
        # the current button
        self._ActiveButton = QtCore.Qt.NoButton

        # private attributes
        self.__oldFocus = None
        self.__saveX = 0
        self.__saveY = 0
        self.__saveModifiers = QtCore.Qt.NoModifier
        self.__saveButtons = QtCore.Qt.NoButton
        self.__wheelDelta = 0

        self.ren = None
        widget_map['landmark_points'] = LandmarkSet()

        self.Points = PointSet()
        self.Points.AddPoint(([0.0, 0.0, 0.0]))
        self.Points.AddPoint(([0.1, 0.0, 0.0]))
        self.Points.AddPoint(([0.0, 0.1, 0.0]))

        # do special handling of some keywords:
        # stereo, rw

        stereo = 0

        if kw.has_key('stereo'):
            if kw['stereo']:
                stereo = 1

        rw = None

        if kw.has_key('rw'):
            rw = kw['rw']

        # create qt-level widget
        super(QVTKRenderWindowInteractor, self).__init__(parent, wflags | QtCore.Qt.MSWindowsOwnDC)

        if rw:  # user-supplied render window
            self._RenderWindow = rw
        else:
            self._RenderWindow = vtk.vtkRenderWindow()

        self._RenderWindow.SetWindowInfo(str(int(self.winId())))

        if stereo:  # stereo mode
            self._RenderWindow.StereoCapableWindowOn()
            self._RenderWindow.SetStereoTypeToCrystalEyes()

        if kw.has_key('iren'):
            self._Iren = kw['iren']
        else:
            self._Iren = vtk.vtkGenericRenderWindowInteractor()
            self._Iren.SetRenderWindow(self._RenderWindow)

        # do all the necessary qt setup
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
        self.setMouseTracking(True)  # get all mouse events
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self._Timer = QtCore.QTimer(self)
        self._Timer.timeout.connect(self.TimerEvent)

        self._Iren.AddObserver('CreateTimerEvent', self.CreateTimer)
        self._Iren.AddObserver('DestroyTimerEvent', self.DestroyTimer)
        self._Iren.GetRenderWindow().AddObserver('CursorChangedEvent',
                                                 self.CursorChangedEvent)

    def __getattr__(self, attr):
        """Makes the object behave like a vtkGenericRenderWindowInteractor"""
        if attr == '__vtk__':
            return lambda t=self._Iren: t
        elif hasattr(self._Iren, attr):
            return getattr(self._Iren, attr)
        else:
            raise (AttributeError, self.__class__.__name__ + \
                   " has no attribute named " + attr)

    def SetRenderer(self, r):
        self.ren = r

    def SetParentActor(self, a):
        self.parentActor = a

    def CreateTimer(self, obj, evt):
        self._Timer.start(10)

    def DestroyTimer(self, obj, evt):
        self._Timer.stop()
        return 1

    def TimerEvent(self):
        self._Iren.TimerEvent()

    def AddActor(self, a):
        self.ren.addActor(a)

    def CursorChangedEvent(self, obj, evt):
        """Called when the CursorChangedEvent fires on the render window."""
        # This indirection is needed since when the event fires, the current
        # cursor is not yet set so we defer this by which time the current
        # cursor should have been set.
        QtCore.QTimer.singleShot(0, self.ShowCursor)

    def HideCursor(self):
        """Hides the cursor."""
        self.setCursor(QtCore.Qt.BlankCursor)

    def ShowCursor(self):
        """Shows the cursor."""
        vtk_cursor = self._Iren.GetRenderWindow().GetCurrentCursor()
        qt_cursor = self._CURSOR_MAP.get(vtk_cursor, QtCore.Qt.ArrowCursor)
        self.setCursor(qt_cursor)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def paintEngine(self):
        return None

    def paintEvent(self, ev):
        self._Iren.Render()

    def resizeEvent(self, ev):
        w = self.width()
        h = self.height()
        vtk.vtkRenderWindow.SetSize(self._RenderWindow, w, h)
        self._Iren.SetSize(w, h)
        self._Iren.ConfigureEvent()
        self.update()

    def _GetCtrlShift(self, ev):
        ctrl = shift = False

        if hasattr(ev, 'modifiers'):
            if ev.modifiers() & QtCore.Qt.ShiftModifier:
                shift = True
            if ev.modifiers() & QtCore.Qt.ControlModifier:
                ctrl = True
        else:
            if self.__saveModifiers & QtCore.Qt.ShiftModifier:
                shift = True
            if self.__saveModifiers & QtCore.Qt.ControlModifier:
                ctrl = True

        return ctrl, shift

    def enterEvent(self, ev):
        if not self.hasFocus():
            self.__oldFocus = self.focusWidget()
            self.setFocus()

        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, chr(0), 0, None)
        self._Iren.EnterEvent()

    def leaveEvent(self, ev):
        if self.__saveButtons == QtCore.Qt.NoButton and self.__oldFocus:
            self.__oldFocus.setFocus()
            self.__oldFocus = None

        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, chr(0), 0, None)
        self._Iren.LeaveEvent()

    def mousePressEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        repeat = 0
        if ev.type() == QtCore.QEvent.MouseButtonDblClick:
            repeat = 1
        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), repeat, None)
        self._ActiveButton = ev.button()

        if self._ActiveButton == QtCore.Qt.LeftButton:

            act = GetPickedActor(self.GetEventPosition(), self.ren)
            if (act and act == self.parentActor):

                l = GetPickedLocation(self.GetEventPosition(), self.ren);
                a = MakeLandmark(l)
                self.ren.AddActor(a)
                widget_map['landmark_points'].AddLandmark(a, l)
                widget_map['landmark_list'].Insert(str(l))
                # self.Points.PrintPoints()  - correct but somehow decoupled from the landmark list
                self.Render()

            else:
                print("THere is no actor at your click location")
                self._Iren.LeftButtonPressEvent()

        elif self._ActiveButton == QtCore.Qt.RightButton:
            #
            act = GetPickedActor(self.GetEventPosition(), self.ren)
            if (act and act != self.parentActor):
                widget_map['landmark_actors'].remove(act)
                self.ren.RemoveActor(act)
                idx = widget_map['landmark_points'].RemoveLandmark(act)
                print(str(widget_map['landmark_list'].GetItems()))
                print("Removed actor.")
                self.Render()
            else:
                print("Cannot remove parent actor")
                self._Iren.RightButtonPressEvent()

        elif self._ActiveButton == QtCore.Qt.MidButton:
            self._Iren.MiddleButtonPressEvent()
            print("TBD placeholder for mmc functionality")

    def mouseReleaseEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), 0, None)

        if self._ActiveButton == QtCore.Qt.LeftButton:
            self._Iren.LeftButtonReleaseEvent()
        elif self._ActiveButton == QtCore.Qt.RightButton:
            self._Iren.RightButtonReleaseEvent()
        elif self._ActiveButton == QtCore.Qt.MidButton:
            self._Iren.MiddleButtonReleaseEvent()

    def mouseMoveEvent(self, ev):
        self.__saveModifiers = ev.modifiers()
        self.__saveButtons = ev.buttons()
        self.__saveX = ev.x()
        self.__saveY = ev.y()

        ctrl, shift = self._GetCtrlShift(ev)
        self._Iren.SetEventInformationFlipY(ev.x(), ev.y(),
                                            ctrl, shift, chr(0), 0, None)
        self._Iren.MouseMoveEvent()

    def keyPressEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        if ev.key() < 256:
            key = str(ev.text())
        else:
            key = chr(0)

        if (ev.key() == QtCore.Qt.Key_Delete):
            print("PRESSED DELETE (vtk event)!!!")
            # _pos = self.Marks.RemoveCurrentLandmark()
            # print("POS -> " + str(_pos))
            # act = GetPickedActor(_pos, self.ren)
            # if (act and act != self.parentActor):
            #    self.ren.RemoveActor(act)

        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, key, 0, None)
        self._Iren.KeyPressEvent()
        self._Iren.CharEvent()

    def keyReleaseEvent(self, ev):
        ctrl, shift = self._GetCtrlShift(ev)
        if ev.key() < 256:
            key = chr(ev.key())
        else:
            key = chr(0)

        self._Iren.SetEventInformationFlipY(self.__saveX, self.__saveY,
                                            ctrl, shift, key, 0, None)
        self._Iren.KeyReleaseEvent()

    def wheelEvent(self, ev):
        if hasattr(ev, 'delta'):
            self.__wheelDelta += ev.delta()
        else:
            self.__wheelDelta += ev.angleDelta().y()

        if self.__wheelDelta >= 120:
            self._Iren.MouseWheelForwardEvent()
            self.__wheelDelta = 0
        elif self.__wheelDelta <= -120:
            self._Iren.MouseWheelBackwardEvent()

    def GetRenderWindow(self):
        return self._RenderWindow

    def Render(self):
        self.update()


class NiftiFile(object):
    def __init__(self):
        self.header = None
        self.data = None

    def ReadFile(self, fname):
        x = nib.load(fname)
        self.SetHeader(x.header)
        self.data = x

    def SetHeader(self, h):
        self.header = h

    def GetField(self, field):
        return self.header[field]

    def GetDimensions(self):
        return self.GetField('dim')

    def GetVoxelSize(self):
        return self.GetField('pixdim')

    def GetOrigin(self):
        return [self.GetField('qoffset_x'), self.GetField('qoffset_y'), self.GetField('qoffset_z')]

    def PrintHeader(self):
        print(self.header)

    def GetData(self):
        return self.data.get_data()

    def ToString(self):
        return self.GetData().tostring()

    def GetRange(self):
        return nib.volumeutils.finite_range(self.GetData())

    def GetMin(self):
        return self.GetRange()[0]

    def GetMax(self):
        return self.GetRange()[1]

    def SetType(self, t):
        self.data.set_data_dtype(t)
        print("Data type set to: " + str(t))


def MriVolumeRenderTest():
    # We begin by creating the data we want to render.
    # For this tutorial, we create a 3D-image containing three overlaping cubes.
    # This data can of course easily be replaced by data from a medical CT-scan or anything else three dimensional.
    # The only limit is that the data must be reduced to unsigned 8 bit or 16 bit integers.

    widget_map['mri_nifti_ptr'] = NiftiFile()
    if (home_pc):
        widget_map['mri_nifti_ptr'].ReadFile(os.getcwd() + '\\data\\structural_test.nii')

    elif(from_gui):
        widget_map['mri_nifti_ptr'].ReadFile(widget_map['mri_file'].GetText())

    else:
        widget_map['mri_nifti_ptr'].ReadFile('/stbb_home/jenkinsjc/dev/ColocalizedViewer/Latest/data/structural_test.nii')

    widget_map['mri_nifti_ptr'].SetType(np.uint8)

    min_val = widget_map['mri_nifti_ptr'].GetMin()
    max_val = widget_map['mri_nifti_ptr'].GetMax()
    spacing = widget_map['mri_nifti_ptr'].GetVoxelSize()
    origin  = widget_map['mri_nifti_ptr'].GetOrigin()

    img_data = widget_map['mri_nifti_ptr'].GetData()

    # img_data = nifti.GetData()
    img_data_shape = img_data.shape

    dataImporter = vtk.vtkImageImport()
    dataImporter.SetDataScalarTypeToUnsignedShort()
#    dataImporter.SetScalar
    data_string = widget_map['mri_nifti_ptr'].ToString()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))

    dataImporter.SetDataSpacing(spacing[1:4])
    dataImporter.SetDataOrigin(origin[0:3])

    # For some reason we need to invert the img_data_shape indexing (figure out what the strategy is in general)
    dataImporter.SetDataExtent(0, img_data_shape[2] - 1, 0, img_data_shape[1] - 1, 0, img_data_shape[0] - 1)
    dataImporter.SetWholeExtent(0, img_data_shape[2] - 1, 0, img_data_shape[1] - 1, 0, img_data_shape[0] - 1)
    dataImporter.Update()

    # The following class is used to store transparencyv-values for later retrival. In our case, we want the value 0 to be
    # completly opaque whereas the three different cubes are given different transperancy-values to show how it works.
    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(0, 0.0)  # 0
    alphaChannelFunc.AddPoint(min_val + 1, 0.05)  # .05
    alphaChannelFunc.AddPoint(max_val / 16, 0.1)  # .1
    alphaChannelFunc.AddPoint(max_val / 8, 0.3)  # .3
    alphaChannelFunc.AddPoint(max_val / 2, 0.5)  # .5

    print("Min -> " + str(min_val))
    print("Max -> " + str(max_val))

    widget_map['min_lut_value'] = min_val
    widget_map['max_lut_value'] = max_val

    xferFunc = vtk.vtkPiecewiseFunction()
    xferFunc.AddPoint(widget_map['min_lut_value'], 0.0)
    xferFunc.AddPoint(widget_map['max_lut_value'], 10000)
    # The preavius two classes stored properties. Because we want to apply these properties to the volume we want to render,
    # we have to store them in a class that stores volume prpoperties.

    widget_map['mri_volume_property'] = vtk.vtkVolumeProperty()
    # volumeProperty = vtk.vtkVolumeProperty()
    widget_map['mri_volume_property'].SetColor(xferFunc)
    widget_map['mri_volume_property'].SetScalarOpacity(alphaChannelFunc)
    #widget_map['mri_volume_property'].ShadeOn()        #not sure what this does

    # This class describes how the volume is rendered (through ray tracing).
    compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
    # We can finally create our volume. We also have to specify the data for it, as well as how the data will be rendered.
    volumeMapper = vtk.vtkVolumeRayCastMapper()
    volumeMapper.SetVolumeRayCastFunction(compositeFunction)
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

    # volumeMapper.SetMaximumImageSampleDistance(0.01)

    # The class vtkVolume is used to pair the preaviusly declared volume as well as the properties to be used when rendering that volume.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(widget_map['mri_volume_property'])

    widget_map['mri_actor'] = volume

    return widget_map['mri_actor']






# This class is the input validation (yes/no) check
class OkPopup(QtWidgets.QMessageBox):
    def __init__(self, to_hide, to_show):
        super(OkPopup, self).__init__()
        self.InitUi(to_hide, to_show)
        #self.exec_()
        self.show()

    def InitUi(self, hide, show):
        #self.setText()
        #self.setInformativeText('Are all of these values correct?')
        #self.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        #self.setDefaultButton(QtWidgets.QMessageBox.Yes)
        buttonReply = QtWidgets.QMessageBox.question(self, 'Check your values', self.FormatText(), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if buttonReply == QtWidgets.QMessageBox.Yes:
            print('Yes clicked.')
            self.hide()

            g_utils.SetupMriActor()
            g_utils.SetupHistologyActor()



            ShowWidgets(show)
            HideWidgets(hide)

        else:
            print('No clicked.')
            self.hide()
            #widget_map[to_show].hide()




        # Formats text in the relevant widgets and displays in a popup message

    def FormatText(self):
        labels = ["MRI Voxel dimension: ", "MRI Voxel size: ", "Histology Voxel dimension: ", "Histology Voxel size: ",
                  "Number of Histology Image Levels: "]
        mri_voxel_values = [widget_map['mri_n_voxels_x'].GetText(), '    ', widget_map['mri_n_voxels_y'].GetText(),
                            '   ', widget_map['mri_n_voxels_z'].GetText()]
        mri_voxel_sizes = [widget_map['mri_s_voxels_x'].GetText(), '   ', widget_map['mri_s_voxels_y'].GetText(), '   ',
                           widget_map['mri_s_voxels_z'].GetText()]
        histo_voxel_values = [widget_map['histo_n_voxels_x'].GetText(), '    ',
                              widget_map['histo_n_voxels_y'].GetText(), '   ', widget_map['histo_n_voxels_z'].GetText()]
        histo_voxel_sizes = [widget_map['histo_s_voxels_x'].GetText(), '   ', widget_map['histo_s_voxels_y'].GetText(),
                             '   ', widget_map['histo_s_voxels_z'].GetText()]
        n_levels = widget_map['num_levels'].GetText()
        fields = [mri_voxel_values, mri_voxel_sizes, histo_voxel_values, histo_voxel_sizes, n_levels]
        string = ""
        for i in range(0, len(labels)):
            fields_str = ""
            curr_field = fields[i]
            for j in range(0, len(curr_field)):
                fields_str = fields_str + str(curr_field[j])
            string = string + labels[i] + str(fields_str) + '\n'
        return ''.join(string)


class MainWindow(QtWidgets.QWidget):
  def __init__(self):
    super(MainWindow, self).__init__()
    #self.utils = UiUtils()
    window_layout = VBox([self.buildmri(), self.buildhisto(),self.buildoutput()])
    self.setLayout(window_layout)
    self.show()
  def mri_row1(self):
    return Frame('h',  [Label('MRI File'), TextBox("", filebox_width, 'mri_file'), Button('File', g_utils.mriopenfile), Button('Fill',  g_utils.FillMriFields)])
  def mri_row2(self):
    return Frame('h', [Label('X'), TextBox("",textbox_width,'mri_n_voxels_x'), Label('Y'), TextBox("",textbox_width,'mri_n_voxels_y'), Label('Z'), TextBox("",textbox_width, 'mri_n_voxels_z')])
  def mri_row3(self):
    return Frame('h', [Label('size X'), TextBox("",textbox_width, 'mri_s_voxels_x'), Label('size Y'), TextBox("",textbox_width,'mri_s_voxels_y'), Label('size Z'), TextBox("",textbox_width,'mri_s_voxels_z')])
  # build the mri part of the gui
  def buildmri(self):
    return Frame('v', [Label('1. MRI Info'), self.mri_row1(), self.mri_row2(), self.mri_row3()])
  def histo_row1(self):
    return Frame('h', [Label('Histology File'), TextBox("", filebox_width, 'histo_file'), Button('File', g_utils.histoopenfile)])
  def histo_row2(self):
    return Frame('h', [Label('X'), TextBox("", textbox_width, 'histo_n_voxels_x'), Label('Y'), TextBox("", textbox_width, 'histo_n_voxels_y'), Label('Z'), TextBox("", textbox_width, 'histo_n_voxels_z')])
  def histo_row3(self):
    return Frame('h', [Label('size X'), TextBox("", textbox_width, 'histo_s_voxels_x'), Label('size Y'), TextBox("", textbox_width, 'histo_s_voxels_y'), Label('size Z'), TextBox("", textbox_width, 'histo_s_voxels_z')])
  # build the histology part of the gui
  def buildhisto(self):
    return Frame('v', [Label('2. Histology Info'), self.histo_row1(), self.histo_row2(), self.histo_row3()])
  def out_row(self):
    return Frame('h', [Label('Number of Levels:'), DropDown(['1','2','3','4','5'], 'num_levels')])
  # build the output part of the gui
  def buildoutput(self):
    return Frame('v', [Label('3. Output'), self.out_row(), Button('OK', g_utils.CreatePopup)])



# Setup the qpplication elements
def QVTKRenderWidgetMain():
    """A simple example that uses the QVTKRenderWindowInteractor class."""

    # every QT app needs an app
    widget_map['main_application'] = QtWidgets.QApplication(['QVTKRenderWindowInteractor'])
    widget_map['root_window'] = QtWidgets.QWidget()

    widget_map['model_matrix'] = Matrix()

    widget_map['landmark_actors'] = []

    widget_map['button_controller'] = ButtonController()

    # create the widget
    widget_map['vtk_widget'] = (QVTKRenderWindowInteractor())
    widget_map['vtk_widget'].Initialize()
    widget_map['vtk_widget'].Start()
    # if you dont want the 'q' key to exit comment this.
    widget_map['vtk_widget'].AddObserver("ExitEvent", lambda o, e, a=widget_map['main_application']: a.quit())

    widget_map['v_ren'] = vtk.vtkRenderer()

    widget_map['vtk_widget'].GetRenderWindow().AddRenderer(widget_map['v_ren'])

    widget_map['vtk_widget'].SetRenderer(widget_map['v_ren'])

    #   this is the setup window where we input our mri and slice files.
    widget_map['setup_window'] = MainWindow()

    widget_map['vtk_options_frame'] = Frame('v', [
                Label('Landmark Points', 'lps'),
                List([], 'landmark_list'),

                Button('Reset scale', widget_map['button_controller'].ResetScale, 'reset_scale_button'),
                Label('sX:   0', 'sx_slider_label'), Slider('h', 0.00001, 10, 1, 'x_scale_slider', 'sx_slider_label'),
                Label('sY:   0', 'sy_slider_label'), Slider('h', 0.00001, 10, 1, 'y_scale_slider', 'sy_slider_label'),
                Label('sZ:   0', 'sz_slider_label'), Slider('h', 0.00001, 10, 1, 'z_scale_slider', 'sz_slider_label'),


                Button('Reset rotation', widget_map['button_controller'].ResetRotation, 'reset_rotation_button'),
                Label('Theta: 0', 'theta_slider_label'), Slider('h', -180, 180, 1, 'theta_rot_slider', 'theta_slider_label'),
                Label('Phi:   0', 'phi_slider_label'), Slider('h', -180, 180, 1, 'phi_rot_slider', 'phi_slider_label'),
                Label('Rho:   0', 'rho_slider_label'), Slider('h', -180, 180, 1, 'rho_rot_slider', 'rho_slider_label'),

                Button('Reset translation', widget_map['button_controller'].ResetTranslation, 'reset_translation_button'),
                Label('X: 0', 'x_slider_label'), Slider('h', -180, 180, 1, 'x_trans_slider', 'x_slider_label'),
                Label('Y:   0', 'y_slider_label'), Slider('h', -180, 180, 1, 'y_trans_slider', 'y_slider_label'),
                Label('Z:   0', 'z_slider_label'), Slider('h', -180, 180, 1, 'z_trans_slider', 'z_slider_label'),

                Button('Reset LUT', widget_map['button_controller'].ResetLUT, 'reset_lut_button'),
                Label('Min: 0', 'min_lut_label'), Slider('h', 0, 1000000, 9000, 'min_lut_slider', 'min_lut_label'),
                Label('Max: 500', 'max_lut_label'), Slider('h', 0, 1000000, 1000000, 'max_lut_slider', 'max_lut_label'),
            ])
    #widget_map['vtk_widget_frame'] = Frame('v',[]) #None #QtWidgets.QWidget([])
    #widget_map['vtk_widget_frame'] = VBox([])


    widget_map['root_window'].setLayout(HBox([
        widget_map['setup_window'],
        widget_map['vtk_options_frame'],
        widget_map['vtk_widget']
    ]))
    widget_map['root_window'].show()

    #   initially, hide the vtk stuff
    widget_map['vtk_options_frame'].hide()
    widget_map['vtk_widget'].hide()

    # start event processing
    widget_map['main_application'].exec_()


# The main entry point
if __name__ == "__main__":

    QVTKRenderWidgetMain()
