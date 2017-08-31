# Objects class

import os
import numpy
import vtk
import csv

# Path to the .mha file
filenameSegmentation = "/stbb_home/jenkinsjc/dev/ColocalizedViewer/model/brain_segmentation.mha"
# Path to colorfile.txt 
filenameColorfile = "/stbb_home/jenkinsjc/dev/ColocalizedViewer/model/colorfile.txt"
# Opacity of the different volumes (between 0.0 and 1.0)
volOpacityDef = 0.25


def ReadCSV(fname):    
    fid = open(fname, "r")
    reader = csv.reader(fid)
    dictRGB = {}
    for line in reader:
        dictRGB[int(line[0])] = [float(line[2])/255.0,
                                 float(line[3])/255.0,
                                 float(line[4])/255.0]
    fid.close()
    return dictRGB
    
#   does it have to be mha?
def ReadImage(fname):
    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(fname)
    castFilter = vtk.vtkImageCast()
    castFilter.SetInputConnection(reader.GetOutputPort())
    castFilter.SetOutputScalarTypeToUnsignedShort()
    castFilter.Update()
    imdataBrainSeg = castFilter.GetOutput()
    return imdataBrainSeg
    
class ColorTransferFunction(object):
     def __init__(self, pts):
        self.ctf = vtk.vtkColorTransferFunction()        
        for idx in pts.keys():
            self.ctf.AddRGBPoint(idx, pts[idx][0], pts[idx][1], pts[idx][2])        
     def Get(self):
        return self.ctf

class PiecewiseFunction(object):
    def __init__(self, pts, _type):
        self.func = vtk.vtkPiecewiseFunction()
        if(_type == 'scalar_opacity'):
            for idx in pts.keys():
                self.func.AddPoint(idx, volOpacityDef if idx<>0 else 0.0)       
        if(_type == 'gradient_opacity'):
            for p in pts:
                self.func.AddPoint(p['x'], p['y'])
    def Get(self):
        return self.func

#   Internal class of volume
class Property(object):        
    def __init__(self, c, o, g):
        self.prop = vtk.vtkVolumeProperty()
        self.prop.ShadeOff()
        self.prop.SetColor(c)
        self.prop.SetScalarOpacity(o)        
        self.prop.SetGradientOpacity(g)        
        self.prop.SetInterpolationTypeToLinear()     
    def Get(self):
        return self.prop

class Volume(object):
    def __init__(self):
        #super(Volume, self).__init__()                
        self.vol = vtk.vtkVolume()
        self.imdata = ReadImage(filenameSegmentation)
        self.rgbdata= ReadCSV(filenameColorfile)
        self.CreateMapper()
        self.CreateProperties()
        
    def CreateRayCaster(self):
        rc = vtk.vtkVolumeRayCastCompositeFunction()
        rc.SetCompositeMethodToClassifyFirst()
        return rc
                
    def CreateMapper(self):
        mv = vtk.vtkVolumeRayCastMapper()
        rc = self.CreateRayCaster()
        mv.SetVolumeRayCastFunction(rc)        
        mv.SetInputData(self.imdata)
        self.vol.SetMapper(mv)
        
    def CreateProperties(self):    
        #   Read the color transfer functions from somewhere
        '''
        c_pts = {
            0: [0, 0, 0],
            1: [245, 245, 245],
            2: [88, 106, 215],
            3: [88, 106, 215],       
        }  
        '''
        ctf = ColorTransferFunction(self.rgbdata)        
        #   Read the scalar opacity from somewhere
        so = PiecewiseFunction(self.rgbdata, 'scalar_opacity')
        #   Read the gradient opacity function from somewhere
        g_pts = [ 
                {'x': 1, 'y': 0.0},
                {'x': 5, 'y': 0.1},  
                {'x': 100, 'y': 1.0}, 
        ]        
        go = PiecewiseFunction(g_pts, 'gradient_opacity')        
        v_prop = Property(ctf.Get(), so.Get(), go.Get())
        self.vol.SetProperty(v_prop.Get())                    
    
    def Get(self):
        return self.vol

            
            
from IPython.display import Image
def vtk_show(renderer, a, width=400, height=300):
    """
    Takes vtkRenderer instance and returns an IPython Image with the rendering.
    """
    renderWindow = vtk.vtkRenderWindow()
    #renderWindow.SetOffScreenRendering(1)
    
    
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(width, height)
   
    
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)
    
    renderer.AddActor(a)
    renderWindow.Render()
    
    # screenshot code:
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renderWindow)
    w2if.Update()
     
    writer = vtk.vtkPNGWriter()
    writer.SetFileName("screenshot.png")
    writer.SetInputData(w2if.GetOutput())
    writer.Write()
     
    # enable user interface interactor
    iren.Initialize()
    iren.Start()
     
    #windowToImageFilter = vtk.vtkWindowToImageFilter()
    #windowToImageFilter.SetInput(renderWindow)
    #windowToImageFilter.Update()
     
    #writer = vtk.vtkPNGWriter()
    #writer.SetWriteToMemory(0)
    #writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    #writer.Write()

    #return Image(str(buffer(writer.GetResult())))
    #return renderWindow
            
class Renderer():
    def __init__(self):
            #super(Renderer, self).__init__()                  
            # Modify the camera with properties defined manually in ParaView            
        self.rend = vtk.vtkRenderer()
        camera = self.rend.MakeCamera()
        camera.SetPosition(30,30,30)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.SetViewAngle(30.0)
        self.rend.SetActiveCamera(camera)
    def AddActor(self, a):
        self.rend.AddActor(a)        
    def Get(self):
        return self.rend
    

aVolume = Volume()


renderer = Renderer()


r= renderer.Get()


rw = vtk_show(r, aVolume.Get(), 600, 600)


