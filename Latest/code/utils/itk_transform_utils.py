import itk
import numpy
import vtk


def writeITKtransform(fname):
    pass


def readITKtransform(transform_file):
    '''
    '''

    # read the transform
    transform = None
    with open(transform_file, 'r') as f:
        for line in f:

            # check for Parameters:
            if line.startswith('Parameters:'):
                values = line.split(': ')[1].split(' ')

                # filter empty spaces and line breaks
                values = [float(e) for e in values if (e != '' and e != '\n')]
                # create the upper left of the matrix
                transform_upper_left = numpy.reshape(values[0:9], (3, 3))
                # grab the translation as well
                translation = values[9:]

            # check for FixedParameters:
            if line.startswith('FixedParameters:'):
                values = line.split(': ')[1].split(' ')

                # filter empty spaces and line breaks
                values = [float(e) for e in values if (e != '' and e != '\n')]
                # setup the center
                center = values

    # compute the offset
    offset = numpy.ones(4)
    for i in range(0, 3):
        offset[i] = translation[i] + center[i];
        for j in range(0, 3):
            offset[i] -= transform_upper_left[i][j] * center[i]

    # add the [0, 0, 0] line
    transform = numpy.vstack((transform_upper_left, [0, 0, 0]))
    # and the [offset, 1] column
    transform = numpy.hstack((transform, numpy.reshape(offset, (4, 1))))

    return transform


def rotate_polydata(pd, rotation_center, theta_x=0,theta_y=0, theta_z=0):
    #I don't want to deal with translation
    translation=(0,0,0)
    rigid_euler = itk.Euler3DTransform(rotation_center, theta_x, theta_y, theta_z, translation)
    matrix = numpy.zeros([4,4])
    old_matrix=numpy.array(rigid_euler.GetMatrix()).reshape(3,3)
    matrix[:3,:3] = old_matrix
    matrix[-1,-1] = 1
    #ITK and VTK use different orders.
    matrix= matrix.T

    # to rotate about a center we first need to translate
    transform_t = vtk.vtkTransform()
    transform_t.Translate(-rotation_center)
    transformer_t = vtk.vtkTransformPolyDataFilter()
    transformer_t.SetTransform(transform_t)
    transformer_t.SetInputData(pd)
    transformer_t.Update()

    transform = vtk.vtkTransform()
    transform.SetMatrix(matrix.ravel())
    transform.Translate(translation)
    transform.PostMultiply()

    transformer = vtk.vtkTransformPolyDataFilter()
    transformer.SetTransform(transform)
    transformer.SetInputConnection(transformer_t.GetOutputPort())
    transformer.Update()

    # translate back
    transform_t2 = vtk.vtkTransform()
    transform_t2.Translate(rotation_center)
    transformer_t2 = vtk.vtkTransformPolyDataFilter()
    transformer_t2.SetTransform(transform_t2)
    transformer_t2.SetInputConnection(transformer.GetOutputPort())
    transformer_t2.Update()

    return transformer_t2.GetOutputDataObject(0)