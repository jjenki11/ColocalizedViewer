import vtk
from grid import Grid

widget_map = {}

class CustomCameraInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
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
        return

    def middleButtonReleaseEvent(self, obj, event):
        print("Middle Button released")
        self.OnMiddleButtonUp()
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

class CustomActorInteractorStyle(vtk.vtkInteractorStyleTrackballActor):
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
        return

    def middleButtonReleaseEvent(self, obj, event):
        print("Middle Button released")
        self.OnMiddleButtonUp()
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

class Viewport(object):

    def __init__(self):
        self.rw = vtk.vtkRenderWindow()
        self.iren = vtk.vtkRenderWindowInteractor()
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

        self.Build3dPane(-1, widget_map['cone_actor'])

        #self.BuildTopView(1, widget_map['cone_actor'])

        #self.BuildFrontView(2, widget_map['cone_actor'])

        #self.BuildSideView(3, widget_map['cone_actor'])

        #self.Build3dPane(0, widget_map['cone_actor'])

        self.DrawGrid()
        self.rw.Render()
        self.rw.SetWindowName('Grid')
        self.iren.Start()


    def Build3dPane(self, idx, obj):
        #ren = vtk.vtkRenderer()
        self.ren = vtk.vtkRenderer()
        self.rw.AddRenderer(self.ren)
        if(int(idx)>=0):
            self.ren.SetViewport(self.xmins[idx], self.ymins[idx], self.xmaxs[idx], self.ymaxs[idx])

        self.ren.AddActor(obj)
        self.ren.ResetCamera()

        #   if we want render window mouse interactor to affect camera rotation and not actor
        self.style = CustomCameraInteractorStyle(self.ren, obj)

        #   if we want render window mouse interactor to affect actor rotation and not camera
        #self.style = CustomActorInteractorStyle(self.ren, obj)
        self.iren.SetInteractorStyle(self.style)

    def CreateGrid(self):
        pass

    def DrawActorList(self, a_list):
        for i in range(len(a_list)):
            if not(a_list[i] == None):
                self.ren.AddActor(a_list[i])
            else:
                print("Found a null actor at index " + str(i))

    def DrawGrid(self):
        g = Grid()

        gAxesActors = g.ConstructAxes()
        gBBox = g.ConstructBoundingBox()


        #test = g.ConstructViewVolume()



        self.DrawActorList(gBBox)
        #self.DrawActorList(test)


        self.DrawActorList(gAxesActors)



        self.ren.ResetCamera()
        print("size of # actors -> " + str(len(gAxesActors)))

    

        #

        self.rw.Render()

        print("Grid axes drawn.")


if __name__ == '__main__':
    Viewport()