

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    try:
        from PySide import QtCore, QtGui
    except ImportError as err:
        raise ImportError("Cannot load either PyQt or PySide")
import vtk
import itk

# global mapping (only in this file) of widget names to their object
widget_map = {}

keyPressed = QtCore.pyqtSignal()

# Register widget by nam e to our global mapping
def RegisterWidget(name, widget):
    widget_map[name] = widget

# GLOBAL props
textbox_width = 50
filebox_width = 150

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
    def __init__(self, t):
        super(Label, self).__init__(t)
        self.SetText(t)

    def SetText(self, lbl):
        self.setText(str(lbl))

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
        del item
        return rnum

    def GetItems(self):
        ret_items = []
        for index in xrange(self.count()):
            ret_items.append(self.item(index))
        return ret_items

    def keyPressEvent(self, ev):
        if ev.key() < 256:
            key = str(ev.text())
        else:
            key = chr(0)

        if(ev.key() == QtCore.Qt.Key_Delete):
            print("PRESSED DELETE (list event)!!!")
            self.Remove()

def MakeLandmark(pos):
    source = vtk.vtkSphereSource()
    source.SetCenter(pos[0],pos[1],pos[2])
    source.SetRadius(0.1)
    source.Update()
    _mapper = vtk.vtkPolyDataMapper()
    _mapper.SetInputConnection(source.GetOutputPort())
    act = vtk.vtkActor()
    act.SetMapper(_mapper)
    return act

def GetPickedLocation(_ePos, _ren):
    clickPos = [i for i in _ePos]
    picker = vtk.vtkPropPicker();
    picker.Pick(clickPos[0], clickPos[1], 0, _ren)
    return [i for i in picker.GetPickPosition()]

def GetPickedActor(_ePos, _ren):
    clickPos = [i for i in _ePos]
    picker = vtk.vtkPropPicker();
    picker.Pick(clickPos[0], clickPos[1], 0, _ren)
    return picker.GetActor()


class Point(object):
    def __init__(self,pt):
        pixeltype = itk.D
        dim = 3
        self.p = itk.Point[pixeltype, dim]()
        self.p.SetElement(0, pt[0]); self.p.SetElement(1, pt[1]); self.p.SetElement(2, pt[2]);

    def Get(self):
        return self


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
            print "Point is = " + str(pp.GetElement(0)) + ", " + str(pp.GetElement(1)) + ", " + str(pp.GetElement(2))


class Landmark(object):

    def __init__(self):
        self.x=0
        self.y=0
        self.z=0

class LandmarkSet(object):

    def __init__(self):
        self.actors=[]
        self.points=[]

    def AddLandmark(self, _mark, _pos):
        self.actors.append(_mark)
        self.points.append(_pos)
        print("Added point to set.")
        print("we now have => "+str(len(self.points)))

    def RemoveLandmark(self, _mark):
        idx = self.actors.index(_mark)
        self.actors.remove(_mark)
        self.points.pop(idx)
        print("Removed point from set.")
        print("we now have => " + str(len(self.points)) + " points")
        print("we now have => " + str(len(self.actors)) + " actors")

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
        self.Marks = LandmarkSet()

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
        QtWidgets.QWidget.__init__(self, parent, wflags|QtCore.Qt.MSWindowsOwnDC)

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
            raise AttributeError, self.__class__.__name__ + \
                  " has no attribute named " + attr

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
            self._Iren.LeftButtonPressEvent()
            act = GetPickedActor(self.GetEventPosition(), self.ren)
            if(act and act == self.parentActor):

                l = GetPickedLocation(self.GetEventPosition(), self.ren);
                a = MakeLandmark(l)
                self.ren.AddActor(a)
                self.Marks.AddLandmark(a, l)
                widget_map['landmark_list'].Insert(str(l))
                self.Points.PrintPoints()

            else:
                print("THere is no actor at your click location")

        elif self._ActiveButton == QtCore.Qt.RightButton:
            self._Iren.RightButtonPressEvent()
            act = GetPickedActor(self.GetEventPosition(), self.ren)
            if not (act == self.parentActor):
                self.ren.RemoveActor(act)
                self.Marks.RemoveLandmark(act)
                print(str(widget_map['landmark_list'].GetItems()))
                print("Removed actor.")
            else:
                print("Cannot remove parent actor")

        elif self._ActiveButton == QtCore.Qt.MidButton:
            self._Iren.MiddleButtonPressEvent()

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




def QVTKRenderWidgetConeExample():
    """A simple example that uses the QVTKRenderWindowInteractor class."""

    # every QT app needs an app
    app = QtWidgets.QApplication(['QVTKRenderWindowInteractor'])



    # create the widget
    widget = QVTKRenderWindowInteractor()
    widget.Initialize()
    widget.Start()
    # if you dont want the 'q' key to exit comment this.
    widget.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

    ren = vtk.vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)

    # create plane as base obj
    planeSrc = vtk.vtkPlaneSource()
    planeSrc.Update()

    # load tiff file
    tiffFile = vtk.vtkTIFFReader()
    tiffFile.SetFileName('/stbb_home/jenkinsjc/Desktop/LandmarkTesting/76.tif');

    # make a texture out of the tiff file
    tex = vtk.vtkTexture()
    tex.SetInputConnection(tiffFile.GetOutputPort())

    # make a texture mapper for the plane
    map_to_plane = vtk.vtkTextureMapToPlane()
    map_to_plane.SetInputConnection(planeSrc.GetOutputPort())

    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(map_to_plane.GetOutputPort())

    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(tex)

    ren.AddActor(actor)

    widget.SetRenderer(ren)
    widget.SetParentActor(actor)

    main_frame = Frame('v', [Label('Landmark Points'), List([],'landmark_list')])

    #self.setLayout(v_layout)
    w = QtWidgets.QWidget()



    w.setLayout(HBox([main_frame,widget]))
    w.show()

   # main_frame.show()

    # start event processing
    app.exec_()

if __name__ == "__main__":
    QVTKRenderWidgetConeExample()