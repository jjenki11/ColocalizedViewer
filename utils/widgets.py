#This is our widgets class file
import sys
from PySide.QtCore import *
from PySide.QtGui import *
#utils is 'utils.py' in this folder
from utils import *

# GLOBAL props
textbox_width = 50
filebox_width  = 150

# Subclassed qframe widget
class Frame(QFrame):
  def __init__(self, box_type, contents):
    super(Frame, self).__init__()    
    box = None
    if(box_type == 'h'):
      box = HBox(contents)
    if(box_type == 'v'):
      box = VBox(contents)
    self.setLayout(box)

# Subclassed horizontal container widget
class HBox(QHBoxLayout):
  def __init__(self, contents):
    super(HBox, self).__init__()    
    self.append(contents)
  def append(self, items):
    for item in items:
      self.addWidget(item)

# Subclassed vertical container widget
class VBox(QVBoxLayout): 
  def __init__(self, contents):
    super(VBox, self).__init__()
    self.append(contents)
  def append(self, items):
    for item in items:
      self.addWidget(item)

# Subclassed text box widget
class TextBox(QLineEdit):
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
class Label(QLabel):
  def __init__(self, t):
    super(Label, self).__init__(t)
    self.SetText(t)
  def SetText(self, lbl):
    self.setText(str(lbl))
    
# Subclassed button widget
class Button(QPushButton):
  def __init__(self, t, f):
    super(Button, self).__init__()
    self.Text(t)
    self.clicked.connect(f)
    self.show()       
  def Text(self, t):
    self.setText(t)
    
# Subclassed combo box widget
class DropDown(QComboBox):
  def __init__(self, s, w_name):
    super(DropDown, self).__init__()
    RegisterWidget(w_name, self)
    self.setMaximumWidth(100)
    self.addItems(s)
  def GetText(self):
    return unicode(self.currentText())    
    
# The main window is the parent widget
class MainWindow(QWidget):
  def __init__(self):
    super(MainWindow, self).__init__()    
    self.utils = UiUtils()    
    window_layout = VBox([self.buildmri(), self.buildhisto(),self.buildoutput()])
    self.setLayout(window_layout)
    self.show()
  def mri_row1(self):
    return Frame('h',  [Label('MRI File'), TextBox("", filebox_width, 'mri_file'), Button('File', self.utils.mriopenfile), Button('Fill',  self.utils.FillMriFields)])
  def mri_row2(self):
    return Frame('h', [Label('X'), TextBox("",textbox_width,'mri_n_voxels_x'), Label('Y'), TextBox("",textbox_width,'mri_n_voxels_y'), Label('Z'), TextBox("",textbox_width, 'mri_n_voxels_z')])
  def mri_row3(self):
    return Frame('h', [Label('size X'), TextBox("",textbox_width, 'mri_s_voxels_x'), Label('size Y'), TextBox("",textbox_width,'mri_s_voxels_y'), Label('size Z'), TextBox("",textbox_width,'mri_s_voxels_z')])    
  # build the mri part of the gui
  def buildmri(self):
    return Frame('v', [Label('1. MRI Info'), self.mri_row1(), self.mri_row2(), self.mri_row3()])
  def histo_row1(self):
    return Frame('h', [Label('Histology File'), TextBox("", filebox_width, 'histo_file'), Button('File', self.utils.histoopenfile)])
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
    return Frame('v', [Label('3. Output'), self.out_row(), Button('OK', self.utils.CreatePopup)])    
    
# Basically what the main method calls
class HistoGui(object):
  def __init__(self):
    self.app = QApplication(sys.argv)
  def show(self):
    main_window = MainWindow()
    return self.app.exec_()
    
