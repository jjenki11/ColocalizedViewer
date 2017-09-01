#this is our ui utils class
# This class holds all of the gui utilities
import nibabel as nib
from PySide.QtCore import *
from PySide.QtGui import *

# global mapping (only in this file) of widget names to their object
widget_map = {}

# Register widget by nam e to our global mapping
def RegisterWidget(name, widget):
    widget_map[name] = widget

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
    dim_array = widget_map['mri_header'].GetDimensions('dim')
    widget_map['mri_n_voxels_x'].SetText(dim_array[1])
    widget_map['mri_n_voxels_y'].SetText(dim_array[2])
    widget_map['mri_n_voxels_z'].SetText(dim_array[3])    
    size_array = widget_map['mri_header'].GetDimensions('pixdim')
    widget_map['mri_s_voxels_x'].SetText(size_array[1])
    widget_map['mri_s_voxels_y'].SetText(size_array[2])
    widget_map['mri_s_voxels_z'].SetText(size_array[3])
    
  #  Creates a popup
  def CreatePopup(self):
    popup = OkPopup()
  #opens a file dialog and populates the mrifile field    
  def mriopenfile(self):
    fname = QFileDialog.getOpenFileName()
    str_fname = ''.join(fname[0])
    print str_fname
    widget_map['mri_file'].SetText(str_fname)
  #opens a file dialog and populates the histofile field
  def histoopenfile(self):
    fname = QFileDialog.getOpenFileName()  
    str_fname = ''.join(fname[0])
    print str_fname
    widget_map['histo_file'].SetText(str_fname)    
    
# This class holds properties about the nifti
class NiftiFile(object):
  def __init__(self):
    self.header=None
  def ReadFile(self, fname):
    x = nib.load(fname)
    self.SetHeader(x.header)
    return x    
  def SetHeader(self, h):
    self.header = h
  def GetDimensions(self, field):
    return self.header[field]
  def PrintHeader(self):
    print(self.header)  
    
# This class is the input validation (yes/no) check
class OkPopup(QMessageBox):
  def __init__(self):
    super(OkPopup, self).__init__()    
    self.setText(self.FormatText())
    self.setInformativeText('Are all of these values correct?')
    self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    self.setDefaultButton(QMessageBox.Yes)
    self.exec_()    
    self.show()    
    
  # Formats text in the relevant widgets and displays in a popup message
  def FormatText(self):  
    labels                              = ["MRI Voxel dimension: ", "MRI Voxel size: ", "Histology Voxel dimension: ", "Histology Voxel size: ", "Number of Histology Image Levels: "]    
    mri_voxel_values        = [widget_map['mri_n_voxels_x'].GetText(), '    ', widget_map['mri_n_voxels_y'].GetText(), '   ',widget_map['mri_n_voxels_z'].GetText()]
    mri_voxel_sizes           = [widget_map['mri_s_voxels_x'].GetText(), '   ',widget_map['mri_s_voxels_y'].GetText(), '   ',widget_map['mri_s_voxels_z'].GetText()]    
    histo_voxel_values    = [widget_map['histo_n_voxels_x'].GetText(), '    ', widget_map['histo_n_voxels_y'].GetText(), '   ',widget_map['histo_n_voxels_z'].GetText()]
    histo_voxel_sizes       = [widget_map['histo_s_voxels_x'].GetText(), '   ',widget_map['histo_s_voxels_y'].GetText(), '   ',widget_map['histo_s_voxels_z'].GetText()]    
    n_levels                         = widget_map['num_levels'].GetText()
    fields = [mri_voxel_values, mri_voxel_sizes, histo_voxel_values, histo_voxel_sizes, n_levels]    
    string = ""        
    for i in range(0, len(labels)):    
      fields_str = ""
      curr_field = fields[i]
      for j in range(0, len(curr_field)):
        fields_str = fields_str + str(curr_field[j])        
      string = string + labels[i] + str(fields_str) + '\n'      
    return ''.join(string)
