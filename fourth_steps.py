import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import nibabel
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io
import sys




class KeyboardInputDemoWindow( QWidget ) :
   def __init__( self, parent = None ) :
      QWidget.__init__( self, parent )
      self.setGeometry( 100, 200, 800, 400 )
      self.setWindowTitle( "PRESS THE KEYS OF YOUR KEYBOARD" )
      self.code_of_last_pressed_key  =  63  #  The question mark ?
      self.large_font  = QFont( "SansSerif", 20, QFont.Bold )
      # The following statement may help to get keyboard input
      # to this window.
      self.setFocusPolicy( Qt.StrongFocus )
   #  The following methods will be called by the program
   #  execution system whenever keys of the keyboard are pressed.
   #  They receive a QKeyEvent object as a parameter.
   def keyPressEvent( self, event ) :
      self.code_of_last_pressed_key = event.key()
      self.update()

   def keyReleaseEvent( self, event ) :
      pass
      #print  "key release event"   #  This is Python 2.x statement.
      #print( "key release event" )  #  Python 3.x statement.

   def paintEvent( self, event ) :
      painter = QPainter()
      painter.begin( self )
      painter.setFont( self.large_font )
      #  The format specifier %c treats an integer value as a character,
      #  but the integer value must be less than 256.
      #  %s converts an object to a string.
      #  %X shows an integer in hexadecimal form.

      if  self.code_of_last_pressed_key  <  256  :
         text_to_show_as_string  =  "Last pressed key: %c %X %d"  %  \
                                    ( self.code_of_last_pressed_key,
                                      self.code_of_last_pressed_key,
                                      self.code_of_last_pressed_key )
      else :
         text_to_show_as_string  =  "Last pressed key: %s %X %d"  %  \
                                    ( self.code_of_last_pressed_key,
                                      self.code_of_last_pressed_key,
                                      self.code_of_last_pressed_key )                                            
      painter.drawText( 100, 200, text_to_show_as_string )
      if  self.code_of_last_pressed_key  ==  Qt.Key_F1  :
         painter.drawText( 100, 250, "You pressed the F1 key" )
         
      elif  self.code_of_last_pressed_key  ==  Qt.Key_Up  :
      
         painter.drawText( 100, 250, "You pressed the Arrow Up key" )
         
      elif  self.code_of_last_pressed_key  ==  Qt.Key_Down  :
      
         painter.drawText( 100, 250, "You pressed the Arrow Down key" )
         
      painter.end()
      
      
      
      
      






class MriHistologyTools(object):
    mri=None
    histology=None
    def __init__(self):
        print("MRI Tools class constructed.")

    def remove_keymap_conflicts(self, new_keys_set):
        for prop in plt.rcParams:
            if prop.startswith('keymap.'):
                keys = plt.rcParams[prop]
                remove_list = set(keys) & new_keys_set
                for key in remove_list:
                    keys.remove(key)

    def previous_slice(self):
        pass

    def next_slice(self):
        pass
            
    def multi_slice_viewer(self, volume1, volume2):
        self.remove_keymap_conflicts({'j', 'k'})
        fig, ax = plt.subplots()
        ax.volume = volume1
        ax.index = volume1.shape[0] // 2
        ax.imshow(volume1[ax.index])
        fig.canvas.mpl_connect('key_press_event', self.process_key)
        fig.canvas.mpl_connect('button_press_event', self.process_click)
        plt.show()

    def process_key(self, event):
        fig = event.canvas.figure
        ax = fig.axes[0]
        if event.key == 'j':
            self.previous_slice(ax)
        elif event.key == 'k':
            self.next_slice(ax)
        elif event.key == 'q':
            sys.exit(0)
        fig.canvas.draw()
        
    def process_click(self, event):
        fig = event.canvas.figure
        ax = fig.axes[0]
        print(str(ax)+ "    CLICKED at location ->  " + "(" + str(event.xdata) + ", " + str(event.ydata) + ")")

    def previous_slice(self, ax):
        """Go to the previous slice."""
        volume = ax.volume
        ax.index = (ax.index - 1) % volume.shape[0]  # wrap around using %
        ax.images[0].set_array(volume[ax.index])

    def next_slice(self, ax):
        """Go to the next slice."""
        volume = ax.volume
        ax.index = (ax.index + 1) % volume.shape[0]
        ax.images[0].set_array(volume[ax.index])
        
    def prepare_volume_data(self, fn):
        data = nibabel.load(os.path.join('/stbb_home/jenkinsjc/Desktop/MRI_HISTO_VIEWER/', fn))
        sa = data.get_data()
        return sa.T
        
    def prepare_2d_data(self, fn):
        data = mpimg.imread('/stbb_home/jenkinsjc/Desktop/MRI_HISTO_VIEWER/'+fn)
        plt.figure()
        plt.imshow(data)

# Read the image s
mri  = 'T2W_structural_registered_Affine.nii'
hist = 'fluorescent_reduce_8_structural_reoriented.nii'

jpg = 'BAM_seychelles.jpg'




mt = MriHistologyTools()

mt.prepare_2d_data(jpg)

# Get a plain NumPy array, without all the metadata
mri_data = mt.prepare_volume_data(mri)
hist_data = mt.prepare_volume_data(hist)
mt.multi_slice_viewer(mri_data, hist_data)


print("Done?")




this_application = QApplication( sys.argv )
application_window = KeyboardInputDemoWindow()
application_window.show()
this_application.exec_()






      
