import nibabel
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io
import sys





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











