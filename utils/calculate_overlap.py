#   This program takes two images and comptues the overlap percentage

from __future__ import division

import os
import numpy as np
import nibabel as nib


def GetThreshold(data):
    dmin = data.min()
    dmax = data.max()
    return (dmax+dmin)/2

def CreateImage(data, sx, sy, sz):
    data = img.get_data()
    
def GetSize(data, factor):
    sz=[]
    sz.append((data.shape[0]-1)/factor)
    sz.append((data.shape[1]-1)/factor)
    sz.append((data.shape[2]-1)/factor)
    return sz    
    
def ThresholdImage(img, thresh):
    sz = GetSize(img.get_data(), 1)    
    x=sz[0];
    y=sz[1];
    z=sz[2];
    the_data=0    
    data = img.get_data()
    data_copy = img.get_data()    
    for i in range(0,int(x)):        
        for j in range(0,int(y)):
            for k in range(0,int(z)):
                the_data = data[i, j, k]
                if(the_data > thresh):
                    data_copy[i,j,k] = 1
                else:
                    data_copy[i,j,k] = 0                                        
    return data_copy                             

def GenerateBinaryImage(fname):    
    img1 = nib.load(fname)
    threshold_1 = GetThreshold(img1.get_data())
    print('threshold for -> '+fname+' = '+str(threshold_1))
    img_data = img1.dataobj
    img1_size = GetSize(img_data, 1)    
    test_voxel = img_data[img1_size[0], img1_size[1],img1_size[2]]
    img1_thresh = ThresholdImage(img1, threshold_1)
    return img1_thresh    
    
def SubtractImages(img1, img2):
    isz = GetSize(img1, 1)    
    n_voxels = (isz[0]+1)*(isz[1]+1)*(isz[2]+1)
    x=isz[0];
    y=isz[1];
    z=isz[2];    
    data1 = img1
    data2 = img2    
    data3 = img1    
    n_voxels_in_img2 = 0    
    for i in range(0,int(x)):        
        for j in range(0,int(y)):
            for k in range(0,int(z)):
                data3[i,j,k] = data1[i,j,k] - data2[i,j,k]
    return data3
    
def ComputeOverlap(img1, img2):
    pass
    
def SaveNifti(data, fname):
    #   example usage:
    #SaveNifti(SubtractImages(), '/qmi01_raid/bao/test.nii')
    nib.save(data,fname)
    print('saving image...')

def LoadNifti(fname):
    return nib.load(fname)    
    
    
class Metric(object):
    def __init__(self):
        pass
        
    #   https://en.wikipedia.org/wiki/Overlap_coefficient
    def OverlapCoefficient(self, img1, img2):
        isz = GetSize(img1, 1)    
        n_voxels = (isz[0]+1)*(isz[1]+1)*(isz[2]+1)
        x=isz[0];
        y=isz[1];
        z=isz[2];    
        overlap_sum = 0    
        data1 = img1
        data2 = img2    
        n_voxels_in_img1 = 0
        n_voxels_in_img2 = 0    
        for i in range(0,int(x)):        
            for j in range(0,int(y)):
                for k in range(0,int(z)):            
                    if(data1[i,j,k] >0):
                        n_voxels_in_img1 = n_voxels_in_img1 +1    
                    if(data2[i,j,k] >0):
                        n_voxels_in_img2 = n_voxels_in_img2 +1                    
                    if ( (data1[i, j, k] == 1.0) and (data2[i,j,k] == 1.0) ):
                        overlap_sum = overlap_sum + 1    
        n_vox_min = n_voxels_in_img1 if (n_voxels_in_img1<n_voxels_in_img2) else n_voxels_in_img2
        print('minimum number of voxels between image1 and image2-> ' + str(n_vox_min))
        print('overlap sum -> ' +str(overlap_sum))
        overlap = (overlap_sum / n_vox_min)    
        return overlap*100
        
    #   https://en.wikipedia.org/wiki/Jaccard_index
    def JaccardCoefficient(self, img1, img2):
        isz = GetSize(img1, 1)    
        n_voxels = (isz[0]+1)*(isz[1]+1)*(isz[2]+1)
        x=isz[0];
        y=isz[1];
        z=isz[2];    
        overlap_sum = 0    
        data1 = img1
        data2 = img2    
        n_voxels_in_img1 = 0
        n_voxels_in_img2 = 0    
        for i in range(0,int(x)):        
            for j in range(0,int(y)):
                for k in range(0,int(z)):            
                    if(data1[i,j,k] >0):
                        n_voxels_in_img1 = n_voxels_in_img1 +1    
                    if(data2[i,j,k] >0):
                        n_voxels_in_img2 = n_voxels_in_img2 +1                    
                    if ( (data1[i, j, k] == 1.0) and (data2[i,j,k] == 1.0) ):
                        overlap_sum = overlap_sum + 1
        print('overlap sum -> ' +str(overlap_sum))
        overlap = (overlap_sum / (n_voxels_in_img1 + n_voxels_in_img2 - overlap_sum))    
        return overlap*100
        
    #   https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
    def DICECoefficient(self, img1, img2):
        isz = GetSize(img1, 1)    
        n_voxels = (isz[0]+1)*(isz[1]+1)*(isz[2]+1)
        x=isz[0];
        y=isz[1];
        z=isz[2];    
        overlap_sum = 0    
        data1 = img1
        data2 = img2    
        n_voxels_in_img1 = 0
        n_voxels_in_img2 = 0    
        for i in range(0,int(x)):        
            for j in range(0,int(y)):
                for k in range(0,int(z)):            
                    if(data1[i,j,k] >0):
                        n_voxels_in_img1 = n_voxels_in_img1 +1    
                    if(data2[i,j,k] >0):
                        n_voxels_in_img2 = n_voxels_in_img2 +1                    
                    if ( (data1[i, j, k] == 1.0) and (data2[i,j,k] == 1.0) ):
                        overlap_sum = overlap_sum + 1
        print('overlap sum -> ' +str(overlap_sum))
        overlap = (2*overlap_sum / (n_voxels_in_img1 + n_voxels_in_img2))    
        return overlap*100
    

if __name__ == '__main__':
    metric = Metric()   
    fname_1 = '/qmi01_raid/bao/CSH726/Analysis/default_TWI.nii'
    fname_2 = '/qmi01_raid/bao/CSH726/Analysis/CSD_2_TWI.nii'    
    #   for non-binary images, example 1
    img1_data = GenerateBinaryImage(fname_1)
    img2_data = GenerateBinaryImage(fname_2)    
    #   overlap coefficient
    overlap_percent1 = metric.OverlapCoefficient(img1_data, img2_data)
    print('Overlap Coefficient percent overlap ->    ' + str(overlap_percent1) + '%')
    #   jaccard index     
    overlap_percent2 = metric.JaccardCoefficient(img1_data, img2_data)
    print('Jaccard Index percent overlap ->    ' + str(overlap_percent2) + '%')
    #   dice coefficient
    overlap_percent3 = metric.DICECoefficient(img1_data, img2_data)
    print('Dice Coefficient percent overlap ->    ' + str(overlap_percent3) + '%') 
    SaveNifti(SubtractImages(), '/qmi01_raid/bao/test.nii')
    
    #   for binary images, example 2    
    #       need to provide proper filenames    
#    binary_fname_1 = '/some/file1.nii
#    binary_fname_2 = '/some/file2.nii
#    binary_img1_data = GenerateBinaryImage(binary_fname_1)    
#    binary_img2_data = GenerateBinaryImage(binary_fname_2)
    
    #   We dont need to generate binary images since they already are.    
#    overlap_percent2 = ComputeOverlap(binary_img1_data, binary_img2_data)
#    print('percent overlap ->    ' + str(overlap_percent2) + '%') 

