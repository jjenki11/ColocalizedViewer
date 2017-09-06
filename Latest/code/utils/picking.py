import vtk
import sys
import os
import itk

#from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


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
        #self.ExtractPoints()

    def Load(self, fn):
        self.actors=[]
        self.points=[]
        f = open(fn, 'r+')
        for line in f:
            self.actors.append(MakeLandmark(','.join(line)))
            self.points.append(line)

        print("Our actors and points -> " + str(self.actors) + ",         " + str(self.points))


class MouseStyleInteractor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, _ren, pa):
        self.renderer = _ren
        self.parentActor = pa
        self.AddObserver("MiddleButtonPressEvent", self.middleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent", self.middleButtonReleaseEvent)
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.leftButtonReleaseEvent)
        self.AddObserver("RightButtonPressEvent", self.rightButtonPressEvent)
        self.AddObserver("RightButtonReleaseEvent", self.rightButtonReleaseEvent)
        self.Marks = LandmarkSet()


    def middleButtonPressEvent(self, obj, event):
        print("Middle Button pressed")
        self.OnMiddleButtonDown()
        self.Marks.Save('/stbb_home/jenkinsjc/Desktop/LandmarkTesting/test.txt')
        return

    def middleButtonReleaseEvent(self, obj, event):
        print("Middle Button released")
        self.OnMiddleButtonUp()
        return

    def leftButtonPressEvent(self, obj, event):
        print("Left Button pressed")
        self.OnLeftButtonDown();
        l = GetPickedLocation(self.GetInteractor().GetEventPosition(), self.renderer);
        a = MakeLandmark( l )
        self.renderer.AddActor(a)
        self.Marks.AddLandmark(a, l)
        return

    def leftButtonReleaseEvent(self, obj, event):
        print("Left Button released")
        self.OnLeftButtonUp()
        return

    def rightButtonPressEvent(self, obj, event):
        print("Right Button pressed")
        self.OnRightButtonDown()
        act = GetPickedActor(self.GetInteractor().GetEventPosition(), self.renderer)
        if not(act == self.parentActor):
            self.renderer.RemoveActor(act)
            self.Marks.RemoveLandmark(act)
            print("Removed actor.")
        else:
            print("Cannot remove parent actor")
        return

    def rightButtonReleaseEvent(self, obj, event):
        print("Right Button released")
        self.OnRightButtonUp()
        return







class MainWindow(object):
    def __init__(self, parent=None):

        # create a rendering window and renderer
        self.ren = vtk.vtkRenderer()

        self.renWin = vtk.vtkRenderWindow()
        self.renWin.AddRenderer(self.ren)

        # create plane as base obj
        self.planeSrc = vtk.vtkPlaneSource()
        self.planeSrc.Update()

        # load tiff file
        self.tiffFile = vtk.vtkTIFFReader()
        self.tiffFile.SetFileName('/stbb_home/jenkinsjc/Desktop/LandmarkTesting/1.tif');

        # make a texture out of the tiff file
        self.tex = vtk.vtkTexture()
        self.tex.SetInputConnection(self.tiffFile.GetOutputPort())

        # make a texture mapper for the plane
        self.map_to_plane = vtk.vtkTextureMapToPlane()
        self.map_to_plane.SetInputConnection(self.planeSrc.GetOutputPort())

        # mapper
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.map_to_plane.GetOutputPort())

        # actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.SetTexture(self.tex)

        # create a renderwindowinteractor and pass it our renderer object
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renWin)

        # create our custom style class
        self.style = MouseStyleInteractor(self.ren, self.actor)
        self.iren.SetInteractorStyle(self.style)

        # assign actor to the renderer
        self.ren.AddActor(self.actor)
        self.ren.ResetCamera()

        # enable user interface interactor
        self.renWin.Render()
        self.iren.Initialize()
        self.iren.Start()


if __name__ == "__main__":
    window = MainWindow()