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
from numpy import *

# global mapping (only in this file) of widget names to their object
widget_map = {}
# GLOBAL props
textbox_width = 50;
filebox_width = 150;


# Register widget by nam e to our global mapping
def RegisterWidget(name, widget):
    widget_map[name] = widget


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
        mat=None
        if(m):
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

    def Update(self):
        self.m = (self.GetTz() * self.GetTy() * self.GetTx()) * (self.GetRz() * self.GetRy() * self.GetRx())

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
    def __init__(self, box_type, contents):
        super(Frame, self).__init__()
        box = None
        if (box_type == 'h'):
            box = HBox(contents)
        if (box_type == 'v'):
            box = VBox(contents)
        self.setLayout(box)


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
    def __init__(self, txt, size, w_name):
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
    def __init__(self, t, w_name):
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
    def __init__(self, t, f, w_name):
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
        if(_dir=='h'):
            super(Slider, self).__init__(QtCore.Qt.Horizontal)
        if(_dir=='v'):
            super(Slider, self).__init__(QtCore.Qt.Vertical)
        #slider = QSlider(Qt.Horizontal)
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
        if (self.disp_label.GetName() == 'x_slider_label'):
            self.disp_label.SetText("Theta: " + str(value))
            widget_map['model_matrix'].RotateX(math.radians(value))
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())

        if (self.disp_label.GetName() == 'y_slider_label'):
            self.disp_label.SetText("Phi: " + str(value))
            widget_map['model_matrix'].RotateY(math.radians(value))
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())

        if (self.disp_label.GetName() == 'z_slider_label'):
            self.disp_label.SetText("Rho: " + str(value))
            widget_map['model_matrix'].RotateZ(math.radians(value))
            widget_map['model_matrix'].Update()
            widget_map['model_matrix'].Print(widget_map['model_matrix'].Get())

        transformation = widget_map['model_matrix'].ToVtkTransform()
        widget_map['plane_actor'].SetUserTransform(transformation)

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
    def __init__(self, it, w_name):
        super(List, self).__init__()

        self.items=[]
        if(len(it)>0):
            self.items=it
            self.addItems(self.items)
        RegisterWidget(w_name, self)

    def Reset(self):
        self.items=[]
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

        if(ev.key() == QtCore.Qt.Key_Delete):
            print("PRESSED DELETE (list event)!!!")
            #print("THE ITEM -> " + str(self.GetItemAtIndex().text()))
            #_pos = str(self.GetItemAtIndex().text())
            #parr = []
            #_posstr = _pos.replace('[', '').replace(']', '')
            #parr = _posstr.split(',')
            #fparr = []
            #for p in parr:
            #    fparr.append(float(p))
            #print("POS -> " + str(_pos))
            #act = GetPickedActor(fparr, widget_map['vtk_widget'].ren)
            #print("What is act?  "+str(act))
            #if (act ):
            #    widget_map['vtk_widget'].ren.RemoveActor(act)
            #    widget_map['vtk_widget'].Marks.RemoveLandmark(act)
            #self.Remove()


# create a landmark and add it to the renderer
def MakeLandmark(pos):
    source = vtk.vtkSphereSource()
    source.SetCenter(pos[0],pos[1],pos[2])
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
    def __init__(self,pt):
        pixeltype = itk.D
        dim = 3
        self.p = itk.Point[pixeltype, dim]()
        self.p.SetElement(0, pt[0]); self.p.SetElement(1, pt[1]); self.p.SetElement(2, pt[2]);

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
        pt[0] = p[0];pt[1] = p[1];pt[2] = p[2];
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
        self.x=0
        self.y=0
        self.z=0


# class that holds a set of landmarks with some basic operations on the set
class LandmarkSet(object):

    def __init__(self):
        self.actors=[]
        self.points=[]

    def AddLandmark(self, _mark, _pos):
        self.actors.append(_mark)
        self.points.append(_pos)
        print("Added point to set.")
        print("we now have => "+str(len(self.points)))
        #widget_map['landmark_list'].Insert(str(_pos))

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
        #idx = self.actors.index(_mark)
        _mark = widget_map['landmark_list'].GetItemAtIndex()
        print("REMOVING CURRENT SELECTION -> " + str(_mark))
        return self.RemoveLandmark(_mark)

    def ExtractPoints(self):
        pts=[]
        for p in self.points:
            print("POSITION -> " + str(p))
            pts.append(p)

    def Save(self, fn):
        f = open(fn, 'w')
        f.write(str(self.points))
        f.close()

    def Load(self, fn):
        self.actors=[]
        self.points=[]
        f = open(fn, 'r+')
        for line in f:
            self.actors.append(MakeLandmark(','.join(line)))
            self.points.append(line)

        print("Our actors and points -> " + str(self.actors) + ",         " + str(self.points))


# controller for different global button actions
class ButtonController(object):

    def __init__(self):
        print("Created button controller")

    def ResetRotation(self):
        widget_map['x_rot_slider'].setValue(0)
        widget_map['y_rot_slider'].setValue(0)
        widget_map['z_rot_slider'].setValue(0)


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
        0:  QtCore.Qt.ArrowCursor,          # VTK_CURSOR_DEFAULT
        1:  QtCore.Qt.ArrowCursor,          # VTK_CURSOR_ARROW
        2:  QtCore.Qt.SizeBDiagCursor,      # VTK_CURSOR_SIZENE
        3:  QtCore.Qt.SizeFDiagCursor,      # VTK_CURSOR_SIZENWSE
        4:  QtCore.Qt.SizeBDiagCursor,      # VTK_CURSOR_SIZESW
        5:  QtCore.Qt.SizeFDiagCursor,      # VTK_CURSOR_SIZESE
        6:  QtCore.Qt.SizeVerCursor,        # VTK_CURSOR_SIZENS
        7:  QtCore.Qt.SizeHorCursor,        # VTK_CURSOR_SIZEWE
        8:  QtCore.Qt.SizeAllCursor,        # VTK_CURSOR_SIZEALL
        9:  QtCore.Qt.PointingHandCursor,   # VTK_CURSOR_HAND
        10: QtCore.Qt.CrossCursor,          # VTK_CURSOR_CROSSHAIR
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
        super(QVTKRenderWindowInteractor, self).__init__(parent, wflags|QtCore.Qt.MSWindowsOwnDC)

        if rw: # user-supplied render window
            self._RenderWindow = rw
        else:
            self._RenderWindow = vtk.vtkRenderWindow()

        self._RenderWindow.SetWindowInfo(str(int(self.winId())))

        if stereo: # stereo mode
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
        self.setMouseTracking(True) # get all mouse events
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
            if(act and act == self.parentActor):

                l = GetPickedLocation(self.GetEventPosition(), self.ren);
                a = MakeLandmark(l)
                self.ren.AddActor(a)
                widget_map['landmark_points'].AddLandmark(a, l)
                widget_map['landmark_list'].Insert(str(l))
                #self.Points.PrintPoints()  - correct but somehow decoupled from the landmark list
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

        if(ev.key() == QtCore.Qt.Key_Delete):
            print("PRESSED DELETE (vtk event)!!!")
            #_pos = self.Marks.RemoveCurrentLandmark()
            #print("POS -> " + str(_pos))
            #act = GetPickedActor(_pos, self.ren)
            #if (act and act != self.parentActor):
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
        
        
        
        
def VolumeRenderTest():
        # We begin by creating the data we want to render.
    # For this tutorial, we create a 3D-image containing three overlaping cubes.
    # This data can of course easily be replaced by data from a medical CT-scan or anything else three dimensional.
    # The only limit is that the data must be reduced to unsigned 8 bit or 16 bit integers.
    data_matrix = zeros([75, 75, 75], dtype=uint8)
    data_matrix[0:35, 0:35, 0:35] = 50
    data_matrix[25:55, 25:55, 25:55] = 100
    data_matrix[45:74, 45:74, 45:74] = 150

    # For VTK to be able to use the data, it must be stored as a VTK-image. This can be done by the vtkImageImport-class which
    # imports raw data and stores it.
    dataImporter = vtk.vtkImageImport()
    # The preaviusly created array is converted to a string of chars and imported.
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    # The type of the newly imported data is set to unsigned char (uint8)
    dataImporter.SetDataScalarTypeToUnsignedChar()
    # Because the data that is imported only contains an intensity value (it isnt RGB-coded or someting similar), the importer
    # must be told this is the case.
    dataImporter.SetNumberOfScalarComponents(1)
    # The following two functions describe how the data is stored and the dimensions of the array it is stored in. For this
    # simple case, all axes are of length 75 and begins with the first element. For other data, this is probably not the case.
    # I have to admit however, that I honestly dont know the difference between SetDataExtent() and SetWholeExtent() although
    # VTK complains if not both are used.
    dataImporter.SetDataExtent(0, 74, 0, 74, 0, 74)
    dataImporter.SetWholeExtent(0, 74, 0, 74, 0, 74)

    # The following class is used to store transparencyv-values for later retrival. In our case, we want the value 0 to be
    # completly opaque whereas the three different cubes are given different transperancy-values to show how it works.
    alphaChannelFunc = vtk.vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(0, 0.0)
    alphaChannelFunc.AddPoint(1, 0.05)
    alphaChannelFunc.AddPoint(50, 0.1)
    alphaChannelFunc.AddPoint(100, 0.3)
    alphaChannelFunc.AddPoint(150, 0.5)

    # This class stores color data and can create color tables from a few color points. For this demo, we want the three cubes
    # to be of the colors red green and blue.
    colorFunc = vtk.vtkColorTransferFunction()
    colorFunc.AddRGBPoint(50, 1.0, 1.0, 0.0)
    colorFunc.AddRGBPoint(100, 0.0, 1.0, 0.0)
    colorFunc.AddRGBPoint(150, 0.0, 0.0, 1.0)

    # The preavius two classes stored properties. Because we want to apply these properties to the volume we want to render,
    # we have to store them in a class that stores volume prpoperties.
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorFunc)
    volumeProperty.SetScalarOpacity(alphaChannelFunc)

    # This class describes how the volume is rendered (through ray tracing).
    compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
    # We can finally create our volume. We also have to specify the data for it, as well as how the data will be rendered.
    volumeMapper = vtk.vtkVolumeRayCastMapper()
    volumeMapper.SetVolumeRayCastFunction(compositeFunction)
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

    # The class vtkVolume is used to pair the preaviusly declared volume as well as the properties to be used when rendering that volume.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    
    return volume


# Setup the qpplication elements
def QVTKRenderWidgetMain():
    """A simple example that uses the QVTKRenderWindowInteractor class."""

    widget_map['model_matrix'] = Matrix()

    widget_map['landmark_actors'] = []

    widget_map['button_controller'] = ButtonController()

    # every QT app needs an app
    app = QtWidgets.QApplication(['QVTKRenderWindowInteractor'])

    # create the widget
    widget_map['vtk_widget'] = QVTKRenderWindowInteractor()
    widget_map['vtk_widget'].Initialize()
    widget_map['vtk_widget'].Start()
    # if you dont want the 'q' key to exit comment this.
    widget_map['vtk_widget'].AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

    ren = vtk.vtkRenderer()
    widget_map['vtk_widget'].GetRenderWindow().AddRenderer(ren)

    # create plane as base obj
    widget_map['plane_widget'] = vtk.vtkPlaneSource()
    widget_map['plane_widget'].Update()

    # load tiff file
    tiffFile = vtk.vtkTIFFReader()
    tiffFile.SetFileName('/stbb_home/jenkinsjc/Desktop/LandmarkTesting/76.tif');

    #   much nicer now that we are doing it with anaconda... doesnt require us to put a path relative to python 
    #tiffFile.SetFileName(os.getcwd()+'\\data\\76.tif')

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
    
    
    test_vol = VolumeRenderTest();
    ren.AddVolume(test_vol)

    
    
    
    

    ren.AddActor(widget_map['plane_actor'])

    widget_map['vtk_widget'].SetRenderer(ren)
    widget_map['vtk_widget'].SetParentActor(widget_map['plane_actor'])

    main_frame = Frame('v', [
            Label('Landmark Points', 'lps'),
            List([],'landmark_list'),
            Button('Reset rotation', widget_map['button_controller'].ResetRotation, 'reset_rotation_button'),
            Label('Theta: 0', 'x_slider_label'),Slider('h', -180, 180, 1, 'x_rot_slider','x_slider_label'),
            Label('Phi:   0', 'y_slider_label'),Slider('h', -180, 180, 1, 'y_rot_slider','y_slider_label'),
            Label('Rho:   0', 'z_slider_label'),Slider('h', -180, 180, 1, 'z_rot_slider','z_slider_label')
    ])

    w = QtWidgets.QWidget()

    w.setLayout(HBox([
            main_frame,
            widget_map['vtk_widget']
    ]))
    w.show()

    # start event processing
    app.exec_()


# The main entry point
if __name__ == "__main__":
    QVTKRenderWidgetMain()
