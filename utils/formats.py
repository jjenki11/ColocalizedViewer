# The xlator
#!/usr/bin/env python

import vtk
import nibabel as nib

img = nib.load('/qmi01_raid/jeff/drbuddi_data/AP/mot1_AP_north_proc_DRBUDDI_proc/structural_used.nii')
img_data = img.get_data()
img_data_shape = img_data.shape

dataImporter = vtk.vtkImageImport()
dataImporter.SetDataScalarTypeToFloat()
data_string = img_data.tostring()
dataImporter.SetNumberOfScalarComponents(1)
dataImporter.CopyImportVoidPointer(data_string, len(data_string))
# For some reason we need to invert the img_data_shape indexing
dataImporter.SetDataExtent(0, img_data_shape[2] - 1, 0, img_data_shape[1] - 1, 0, img_data_shape[0] - 1)
dataImporter.SetWholeExtent(0, img_data_shape[2] - 1, 0, img_data_shape[1] - 1, 0, img_data_shape[0] - 1)
dataImporter.Update()
temp_data = dataImporter.GetOutput()
new_data = vtk.vtkImageData()
new_data.DeepCopy(temp_data)

#outline
outline=vtk.vtkOutlineFilter()
outline.SetInputData(new_data)
outlineMapper=vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)

#Picker
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.005)

#PlaneWidget
planeWidgetX = vtk.vtkImagePlaneWidget()
planeWidgetX.DisplayTextOn()
planeWidgetX.SetInputData(new_data)
planeWidgetX.SetPlaneOrientationToXAxes()
planeWidgetX.SetSliceIndex(50)
planeWidgetX.SetPicker(picker)
planeWidgetX.SetKeyPressActivationValue("x")
prop1 = planeWidgetX.GetPlaneProperty()
prop1.SetColor(1, 0, 0)

planeWidgetY = vtk.vtkImagePlaneWidget()
planeWidgetY.DisplayTextOn()
planeWidgetY.SetInputData(new_data)
planeWidgetY.SetPlaneOrientationToYAxes()
planeWidgetY.SetSliceIndex(50)
planeWidgetY.SetPicker(picker)
planeWidgetY.SetKeyPressActivationValue("y")
prop2 = planeWidgetY.GetPlaneProperty()
prop2.SetColor(1, 1, 0)
planeWidgetY.SetLookupTable(planeWidgetX.GetLookupTable())

planeWidgetZ = vtk.vtkImagePlaneWidget()
planeWidgetZ.DisplayTextOn()
planeWidgetZ.SetInputData(new_data)
planeWidgetZ.SetPlaneOrientationToZAxes()
planeWidgetZ.SetSliceIndex(50)
planeWidgetZ.SetPicker(picker)
planeWidgetZ.SetKeyPressActivationValue("z")
prop2 = planeWidgetY.GetPlaneProperty()
prop2.SetColor(0, 0, 1)
planeWidgetZ.SetLookupTable(planeWidgetX.GetLookupTable())

#Renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0, 0, 1)

#RenderWindow
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)

#Add outlineactor
renderer.AddActor(outlineActor)
renwin.SetSize(800,800)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renwin)

#Load widget interactors and enable
planeWidgetX.SetInteractor(interactor)
planeWidgetX.On()
planeWidgetY.SetInteractor(interactor)
planeWidgetY.On()
planeWidgetZ.SetInteractor(interactor)
planeWidgetZ.On()

interactor.Initialize()
renwin.Render()
interactor.Start()

 
 
