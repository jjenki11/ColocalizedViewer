from JWidgets import *
import vtk

print("YO")

widget_map = {}

def set_cam_pos(camera, pos):
    camera.SetPosition(pos[0], pos[1], pos[2]);
    camera.SetFocalPoint(0, 0, 0);


class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballActor):
    def __init__(self, _ren, pa):
        self.renderer = _ren
        self.parentActor = pa

        self.AddObserver("MiddleButtonPressEvent", self.middleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent", self.middleButtonReleaseEvent)
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.leftButtonReleaseEvent)
        self.AddObserver("RightButtonPressEvent", self.rightButtonPressEvent)
        self.AddObserver("RightButtonReleaseEvent", self.rightButtonReleaseEvent)

        self.cam_ref = self.renderer.GetActiveCamera()

        self.cam_perspective = [self.cam_ref.GetPosition()[0], self.cam_ref.GetPosition()[1], self.cam_ref.GetPosition()[2]]
        print("Cam pos -> " + str(self.cam_perspective))


    def middleButtonPressEvent(self, obj, event):
        print("Middle Button pressed")
        self.OnMiddleButtonDown()
        widget_map['cone_actor'].TranslateX(5)
        #set_cam_pos(self.cam_ref, [0, 1, 0])
        #self.Render()

        return

    def middleButtonReleaseEvent(self, obj, event):
        print("Middle Button released")
        self.OnMiddleButtonUp()
        #set_cam_pos(self.cam_ref, self.cam_perspective)
        #self.Render()
        return

    def leftButtonPressEvent(self, obj, event):
        print("Left Button pressed")
        self.OnLeftButtonDown();
        return

    def leftButtonReleaseEvent(self, obj, event):
        print("Left Button released")
        self.OnLeftButtonUp()
        return

    def rightButtonPressEvent(self, obj, event):
        print("Right Button pressed")
        self.OnRightButtonDown()
        return

    def rightButtonReleaseEvent(self, obj, event):
        print("Right Button released")
        self.OnRightButtonUp()
        return


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.utils = UiUtils()
        window_layout = VBox([self.buildmri(), self.buildhisto(), self.buildoutput()])
        self.setLayout(window_layout)
        self.show()






class vTextWidget(object):

    def __init__(self, txt):

        #super(vTextWidget, self).__init__()

        self.widget = vtk.vtkFollower()

        self.SetText(txt)

        '''
        textActor.SetInput(txt)
        textActor.GetTextProperty().SetColor((0, 1, 1))

        # Create the text representation. Used for positioning the text_actor
        text_representation = vtk.vtkTextRepresentation()
        text_representation.GetPositionCoordinate().SetValue(0.15, 0.15)
        text_representation.GetPosition2Coordinate().SetValue(0.7, 0.2)

        # Create the TextWidget
        # Note that the SelectableOff method MUST be invoked!
        # According to the documentation :
        #
        # SelectableOn/Off indicates whether the interior region of the widget can be
        # selected or not. If not, then events (such as left mouse down) allow the user
        # to "move" the widget, and no selection is possible. Otherwise the
        # SelectRegion() method is invoked.

        #super(vTextWidget, self).__init__()
        self.txt_widget = vtk.vtkTextSource()
        self.txt_widget.SetText(txt)
        self.txt_widget.SetForegroundColor(1.0, 0.0, 0.0)
        self.txt_widget.BackingOn()
        self.txt_widget.Update()

        '''

    def SetText(self, txt):

        self.setup(txt)

    def setup(self,txt):
        tw = vtk.vtkVectorText()

        tw.SetText(txt)

        mp = vtk.vtkPolyDataMapper()
        mp.SetInputConnection(tw.GetOutputPort())

        self.widget.SetMapper(mp)
        self.widget.GetProperty().SetColor(1, 0, 0)

        self.widget.SetScale(2, 2, 2)
        self.widget.AddPosition(0, -0.1, 0)

    def Get(self):
        return self.widget


class CreateUi(object):
    def __init__(self):
        self.build()




    def Build3dPane(self, idx, obj):
        ren = vtk.vtkRenderer()
        self.rw.AddRenderer(ren)
        ren.SetViewport(self.xmins[idx], self.ymins[idx], self.xmaxs[idx], self.ymaxs[idx])


        ren.AddActor(obj)
        ren.ResetCamera()
        self.style = CustomInteractorStyle(ren, obj)
        self.iren.SetInteractorStyle(self.style)


    def BuildTopView(self, idx, obj):
        ren = vtk.vtkRenderer()
        self.rw.AddRenderer(ren)
        ren.SetViewport(self.xmins[idx], self.ymins[idx], self.xmaxs[idx], self.ymaxs[idx])

        ren.AddActor(obj)

        #top_txt = vTextWidget('Top View')
        #top_txt.Get().SetCamera( ren.GetActiveCamera() )
        #tt = top_txt.Get()
        #ren.AddActor(tt)
        #tt.SetInteractor(self.iren)
        #self.iren.Render()

        #ren.AddActor(actor)
        ren.ResetCamera()
        self.style = CustomInteractorStyle(ren, obj)
        self.iren.SetInteractorStyle(self.style)

    def BuildFrontView(self, idx, obj):
        ren = vtk.vtkRenderer()
        self.rw.AddRenderer(ren)
        ren.SetViewport(self.xmins[idx], self.ymins[idx], self.xmaxs[idx], self.ymaxs[idx])

        ren.AddActor(obj)
        ren.ResetCamera()

        self.style = CustomInteractorStyle(ren, obj)
        self.iren.SetInteractorStyle(self.style)

    def BuildSideView(self, idx, obj):
        ren = vtk.vtkRenderer()
        self.rw.AddRenderer(ren)
        ren.SetViewport(self.xmins[idx], self.ymins[idx], self.xmaxs[idx], self.ymaxs[idx])

        ren.AddActor(obj)
        ren.ResetCamera()

        self.style = CustomInteractorStyle(ren, obj)
        self.iren.SetInteractorStyle(self.style)

    def build(self):
        print("buildling...")
        '''One render window, multiple viewports'''
        #iren_list = []
        self.rw = vtk.vtkRenderWindow()
        self.iren = vtk.vtkRenderWindowInteractor()
        #c_style = CustomInteractorStyle()

        #self.iren.SetInteractorStyle(c_style)
        self.iren.SetRenderWindow(self.rw)
        # Define viewport ranges
        self.xmins = [0, .5, 0, .5]
        self.xmaxs = [0.5, 1, 0.5, 1]
        self.ymins = [0, 0, .5, .5]
        self.ymaxs = [0.5, 0.5, 1, 1]

        widget_map['cone'] = vtk.vtkConeSource()
        widget_map['cone'].SetResolution(60)
        widget_map['cone'].SetCenter(0.0, 0.0, 0.0)
        widget_map['cone'].Update()

        # Create a mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(widget_map['cone'].GetOutputPort())
        widget_map['cone_actor'] = vtk.vtkActor()
        widget_map['cone_actor'].SetMapper(mapper)


        self.Build3dPane(0, widget_map['cone_actor'])

        self.BuildTopView(1, widget_map['cone_actor'])

        self.BuildFrontView(2, widget_map['cone_actor'])

        self.BuildSideView(3, widget_map['cone_actor'])


        self.rw.Render()

        self.rw.SetWindowName('RW: Multiple ViewPorts')

        self.iren.Start()





if __name__ == '__main__':

    ui  =  CreateUi()
    #ui.show()