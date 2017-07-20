import sys
import matplotlib

matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide import QtCore, QtGui

import nibabel
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#from skimage import io
import sys




#def crop(dic, i):
#    image = plt.imread(dic["filename"])
#    x0 = dic["annotations"][i]["x"]
#    y0 = dic["annotations"][i]["y"]
#    width = dic["annotations"][i]["width"]
#    height = dic["annotations"][i]["height"]
#    return image[y0:y0+height , x0:x0+width, :]





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
        return fig
        #plt.show()

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
             
    
        
    def prepare_2d_data(self, fn):
        data = mpimg.imread('/stbb_home/jenkinsjc/Desktop/MRI_HISTO_VIEWER/'+fn)
        #plt.figure()
        #plt.imshow(data)
        return data


def prepare_volume_data(fn):
    data = nibabel.load(os.path.join('/stbb_home/jenkinsjc/Desktop/MRI_HISTO_VIEWER/', fn))
    sa = data.get_data()
    return sa.T
    
def previous_slice():
    pass

def next_slice():
    pass
    
def previous_slice(ax):
        """Go to the previous slice."""
        volume = ax.volume
        ax.index = (ax.index - 1) % volume.shape[0]  # wrap around using %
        ax.images[0].set_array(volume[ax.index])

def next_slice(ax):
    """Go to the next slice."""
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[0]
    ax.images[0].set_array(volume[ax.index])

def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)

def process_key2(event):
    fig = event.canvas.figure
    print("DODODODODO")
    ax = fig.axes[0]
    if event.key == 'j':
        previous_slice(ax)
    elif event.key == 'k':
        next_slice(ax)
    elif event.key == 'q':
        sys.exit(0)
    fig.canvas.draw()
    
def process_click2(event):
        fig = event.canvas.figure
        ax = fig.axes[0]
        print(str(ax)+ "    CLICKED at location ->  " + "(" + str(event.xdata) + ", " + str(event.ydata) + ")")
        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    # generate plot 1
    fig1 = Figure(figsize=(600, 600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
    ax = fig1.add_subplot(111)
    ax.plot([0,1])
    # generate the canvas to display the plot
    canvas1 = FigureCanvas(fig1)
    
    mri  = 'T2W_structural_registered_Affine.nii'
    hist = 'fluorescent_reduce_8_structural_reoriented.nii'

    mri_data = prepare_volume_data(mri)
    hist_data = prepare_volume_data(hist)
    #afig = mt.multi_slice_viewer(mri_data, hist_data)
    
    
    
    
    # generate plot 2
    fig2 = Figure(figsize=(600, 600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
    ax2 = fig2.add_subplot(111)
    
    
    remove_keymap_conflicts({'j', 'k'})
    
    
    
    ax2.volume = mri_data
    ax2.index = mri_data.shape[0] // 2
    ax2.imshow(mri_data[ax2.index])
    
#   ax2.plot([0,10])
    
   #afig.show()
    canvas2 = FigureCanvas(fig2)    
    
    canvas2.mpl_connect('key_press_event', process_key2)
    canvas2.mpl_connect('button_press_event', process_click2)

    vb = QtGui.QHBoxLayout()
    
    vb.addWidget(canvas1)
    vb.addWidget(canvas2)

    fr = QtGui.QFrame()
#    fr.setTitle("HEHEHE")
    fr.setLayout(vb)

    win = QtGui.QMainWindow()
    # add the plot canvas to a window
    #win.setCentralWidget(canvas)
    win.setCentralWidget(fr)

    win.show()

    sys.exit(app.exec_())
    
    print("Done?")
