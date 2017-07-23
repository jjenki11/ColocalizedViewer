import sys

#from PyQt4.QtCore import *
#from PyQt4.QtGui import *

from PySide.QtCore import *
from PySide.QtGui import *

import matplotlib

matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import nibabel
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import sys

#import logging
#import re
#import pyinotify


using_windows=True
runtime_location=""
if(using_windows):
    runtime_location=os.path.dirname(os.path.abspath(__file__))+'\\'
else:
    runtime_location=os.path.dirname(os.path.abspath(__file__))+'/'
    
import subprocess

  
    
    
class JImage(object):
    widget=None
    def __init__(self,widg):
        print("New jimage funkyness")
        self.widget = widg
        
    def prepare_2d_data(self, fn):
        data = mpimg.imread(runtime_location+fn)
        plt.figure()
        plt.imshow(data)
    
    
    def query_image(self, image, query):
        #This command could have multiple commands separated by a new line \n
        #some_command = "export PATH=$PATH://server.sample.mo/app/bin \n customupload abc.txt"
        
        qstring=""
        for i in range(len(query)):
            qstring = qstring + " " + query[i]
 
        print("WHAT IS IMAGE -> " + str(image))
        print("WHAT IS QUERY -> " + str(qstring))
 
        
        some_command = runtime_location+"ImageHelper2 " + image + " " + qstring       

        p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)

        (output, err) = p.communicate()  

        #This makes the wait possible
        p_status = p.wait()

        #This will give you the output of the command being executed
        print "Command output: " + output  
        
        result = '\\'.join(image.split('\\')[:-1]) + "\\crop_result.jpg"
    
        print(result)
        
        from pathlib import Path

        my_file = Path(result)
        if my_file.is_file():
            # file exists
            print("FILE EXISTSSSS")
            self.widget


def prepare_volume_data(fn):
    data = nibabel.load(os.path.join('', fn))
    sa = data.get_data()
    return sa.T
    


class KeyboardInputDemoWindow( QWidget ) :
    def __init__( self, parent = None ) :
        QWidget.__init__( self, parent )
        self.setGeometry( 100, 200, 800, 400 )
        self.setWindowTitle( "Combined MRI and Histology viewer" )
        
        #  The following methods will be called by the program
        #  execution system whenever keys of the keyboard are pressed.
        #  They receive a QKeyEvent object as a parameter.

        mri  = runtime_location+'T2W_structural_registered_Affine.nii'
        hist = runtime_location+'fluorescent_reduce_8_structural_reoriented.nii'

        mri_data = prepare_volume_data(mri)
        hist_data = prepare_volume_data(hist)

        # generate plot 1
        fig1 = Figure(figsize=(600, 600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax1 = fig1.add_subplot(111)

        ax1.volume = mri_data
        ax1.index = mri_data.shape[0] // 2
        ax1.imshow(mri_data[ax1.index])

        self.canvas1 = FigureCanvas(fig1)    
        
#        canvas1.mpl_connect('key_press_event', self.process_key1)
        self.canvas1.mpl_connect('button_press_event', self.process_click1)
        self.canvas1.mpl_connect('scroll_event', self.zoom_event)

        # generate plot 2
        fig2 = Figure(figsize=(600, 600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax2 = fig2.add_subplot(111)

        ax2.volume = hist_data
        ax2.index = hist_data.shape[0] // 2
        ax2.imshow(hist_data[ax2.index])

        self.canvas2 = FigureCanvas(fig2)    

#        canvas2.mpl_connect('key_press_event', self.process_key2)
        self.canvas2.mpl_connect('button_press_event', self.process_click2)
        self.canvas2.mpl_connect('scroll_event', self.zoom_event)

        linked_volumes_hb = QHBoxLayout()
        linked_volumes_hb.addWidget(self.canvas1)
        linked_volumes_hb.addWidget(self.canvas2)
        
        volume_control_hb = QHBoxLayout()
        
        self.slice_slider = QSlider(Qt.Horizontal)
        self.slice_slider.setMinimum(0)
        self.slice_slider.setMaximum(358)
        self.slice_slider.setValue(179)
        self.slice_slider.setTickPosition(QSlider.TicksBelow)
        self.slice_slider.setTickInterval(2)
        self.slice_slider.valueChanged.connect(self.slice_slide_event)
        
        self.slice_number = QTextEdit()
        self.slice_number.setText("179")
        self.slice_number.textChanged.connect(self.slice_text_change)
        
        volume_control_hb.addWidget(self.slice_slider)
        volume_control_hb.addWidget(self.slice_number)
        
        
        self.main_vb = QVBoxLayout()
        
        
        self.main_vb.addLayout(linked_volumes_hb)
        self.main_vb.addLayout(volume_control_hb)
        
   
        self.setLayout(self.main_vb)
        
        
    
        
    def slice_text_change(self):
        cursor = self.slice_number.textCursor()
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)

        self.slice_number.setTextCursor(cursor)
        self.slice_slider.setValue(int(self.slice_number.toPlainText()))
    
    def slice_slide_event(self):
        size = self.slice_slider.value()
        print("The slice -> " + str(size))
        ax1 = self.canvas1.figure.axes[0]        
        ax2 = self.canvas2.figure.axes[0]        
        self.set_slice(ax1, size)
        self.set_slice(ax2, size)
        self.canvas1.draw()
        self.canvas2.draw()
        
    def previous_slice(self,ax):
        """Go to the previous slice."""        
        self.update_slider(ax.index-1)
        self.set_slice(ax, (ax.index-1 % ax.volume.shape[0]))

    def next_slice(self,ax):
        """Go to the next slice."""
        self.update_slider(ax.index+1)
        self.set_slice(ax, (ax.index+1 % ax.volume.shape[0]))
        
    def set_slice(self, ax, idx):
        volume = ax.volume
        ax.index = (idx)
        ax.images[0].set_array(volume[ax.index])        
        self.slice_number.setText(str(idx))
        
    def update_slider(self, val):
        self.slice_slider.setValue(val)
        
        
    #   Will handle slice zooming for either image
    def zoom_event(self, evt):
        #print("Got a scroll event!    "+str(evt))
        ax1 = self.canvas1.figure.axes[0]        
        ax2 = self.canvas2.figure.axes[0]        
        if(evt.button == "up"):
            self.previous_slice(ax1)
            self.previous_slice(ax2)
        elif(evt.button == "down"):
            self.next_slice(ax1)
            self.next_slice(ax2)
        self.canvas1.draw()
        self.canvas2.draw()

    
    def mousePressEvent(self, QMouseEvent):
        #print mouse position
        print("WEWT")
        print(str(QMouseEvent))
        print(str(QMouseEvent.pos()))
    
    def process_click1(self, event):
        fig = event.canvas.figure
        ax = fig.axes[0]
        print(str(ax)+ "MRI    CLICKED at location ->  " + "(" + str(event.xdata) + ", " + str(event.ydata) + ")")               
        
        jmg = JImage(self)
        
        jmg.query_image(runtime_location+'smiley.png' , ['20', '20', '20', '20'])
        
        


   
        res_label = QLabel()
        pmap = QPixmap(runtime_location+'smiley.png')
        
        res_label.setPixmap(pmap)
        res_label.show()
        
        result_img = QHBoxLayout()
        result_img.addWidget(res_label)
        self.main_vb.addLayout(result_img)
        self.update()
        
        #cmd = runtime_location+"BAM_seychelles.jpg 1 2 3 4"        
        
        #   Below is some rudimentary (blocking) code to monitor the directory for output files
        """
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
        path = "/stbb_home/jenkinsjc/Desktop/MRI_HISTO_VIEWER/test.txt"
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_MODIFY
        handler = EventHandler(path)
        notifier = pyinotify.Notifier(wm, handler)

        wm.add_watch(handler.file_path, mask)        
        notifier.loop()        
        """
                
    def process_click2(self, event):
        fig = event.canvas.figure
        ax = fig.axes[0]
        print(str(ax)+ "Histology    CLICKED at location ->  " + "(" + str(event.xdata) + ", " + str(event.ydata) + ")")
        
    def LaunchExternal(self,cmd,arguments):
        command = cmd
        args = arguments
        process = QProcess()
        process.finished.connect(self.OnExternalFinished)
        process.startDetached(command, args)       

    def OnExternalFinished(self, e_code, e_status):
        print("DONE DONE DONE.")
        print("Exit code -> " + str(e_code))
        print("Exit status -> " + str(e_status))            
  
  
"""
pyinotify is not available for windows. this is not a sustainable solution for the time being but is possible
to use with proper thread handling (QProcess could be used for multiple-inheritance)
      
class EventHandler (pyinotify.ProcessEvent):
    def __init__(self, file_path, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.file_path = file_path
        self._last_position = 0
        logpats = r'I2G\(JV\)'
        self._logpat = re.compile(logpats)
    def process_IN_MODIFY(self, event):
        print "File changed: ", event.pathname
        if self._last_position > os.path.getsize(self.file_path):
            self._last_position = 0
        with open(self.file_path) as f:
            f.seek(self._last_position)
            loglines = f.readlines()
            self._last_position = f.tell()
            groups = (self._logpat.search(line.strip()) for line in loglines)
            for g in groups:
                if g:
                    print g.string
"""

if __name__ == '__main__':
    this_application = QApplication( sys.argv )
    application_window = KeyboardInputDemoWindow()
    application_window.show()
    this_application.exec_()
    

    
    print("Done?")
