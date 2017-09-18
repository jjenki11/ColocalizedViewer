import math
import itk
from vtk import vtkMatrix4x4

# Subclassed itk matrix 4x4
class Matrix4(object):
    def __init__(self):
        self.m = itk.Matrix.D44()
        self.m.SetIdentity()

        self.tx = itk.Matrix.D44()
        self.tx.SetIdentity()

        self.ty = itk.Matrix.D44()
        self.ty.SetIdentity()

        self.tz = itk.Matrix.D44()
        self.tz.SetIdentity()

        self.rx = itk.Matrix.D44()
        self.rx.SetIdentity()

        self.ry = itk.Matrix.D44()
        self.ry.SetIdentity()

        self.rz = itk.Matrix.D44()
        self.rz.SetIdentity()

        self.sx = itk.Matrix.D44()
        self.sx.SetIdentity()

        self.sy = itk.Matrix.D44()
        self.sy.SetIdentity()

        self.sz = itk.Matrix.D44()
        self.sz.SetIdentity()

    def Get(self):
        return self.m.GetVnlMatrix()

    def GetTx(self):
        return self.tx

    def GetTy(self):
        return self.ty

    def GetTz(self):
        return self.tz

    def GetRx(self):
        return self.rx

    def GetRy(self):
        return self.ry

    def GetRz(self):
        return self.rz

    def GetSx(self):
        return self.sx

    def GetSy(self):
        return self.sy

    def GetSz(self):
        return self.sz

    def Print(self):
        m = self.Get()
        r1 = str(m.get(0, 0)) + ", " + str(m.get(0, 1)) + ", " + str(m.get(0, 2)) + ", " + str(m.get(0, 3))
        r2 = str(m.get(1, 0)) + ", " + str(m.get(1, 1)) + ", " + str(m.get(1, 2)) + ", " + str(m.get(1, 3))
        r3 = str(m.get(2, 0)) + ", " + str(m.get(2, 1)) + ", " + str(m.get(2, 2)) + ", " + str(m.get(2, 3))
        r4 = str(m.get(3, 0)) + ", " + str(m.get(3, 1)) + ", " + str(m.get(3, 2)) + ", " + str(m.get(3, 3))
        print(r1)
        print(r2)
        print(r3)
        print(r4)
        self.Update()

    def Print(self, m):
        mat = None
        if (m):
            mat = self.Get()
        else:
            mat = m.GetVnlMatrix()

        r1 = str(mat.get(0, 0)) + ", " + str(mat.get(0, 1)) + ", " + str(mat.get(0, 2)) + ", " + str(mat.get(0, 3))
        r2 = str(mat.get(1, 0)) + ", " + str(mat.get(1, 1)) + ", " + str(mat.get(1, 2)) + ", " + str(mat.get(1, 3))
        r3 = str(mat.get(2, 0)) + ", " + str(mat.get(2, 1)) + ", " + str(mat.get(2, 2)) + ", " + str(mat.get(2, 3))
        r4 = str(mat.get(3, 0)) + ", " + str(mat.get(3, 1)) + ", " + str(mat.get(3, 2)) + ", " + str(mat.get(3, 3))
        print("")
        print(r1)
        print(r2)
        print(r3)
        print(r4)
        print("")
        self.Update()

    def RotateX(self, rot):
        self.rx.GetVnlMatrix().set(1, 1, math.cos(rot))
        self.rx.GetVnlMatrix().set(1, 2, -math.sin(rot))
        self.rx.GetVnlMatrix().set(2, 1, math.sin(rot))
        self.rx.GetVnlMatrix().set(2, 2, math.cos(rot))
        self.Update()

    def RotateY(self, rot):
        self.ry.GetVnlMatrix().set(0, 0, math.cos(rot))
        self.ry.GetVnlMatrix().set(0, 2, math.sin(rot))
        self.ry.GetVnlMatrix().set(2, 0, -math.sin(rot))
        self.ry.GetVnlMatrix().set(2, 2, math.cos(rot))
        self.Update()

    def RotateZ(self, rot):

        #translate to origin

        self.rz.GetVnlMatrix().set(0, 0, math.cos(rot))
        self.rz.GetVnlMatrix().set(0, 1, -math.sin(rot))
        self.rz.GetVnlMatrix().set(1, 0, math.sin(rot))
        self.rz.GetVnlMatrix().set(1, 1, math.cos(rot))
        self.Update()

    def TranslateX(self, trans):
        self.tx.GetVnlMatrix().set(0, 3, trans)
        self.Update()

    def TranslateY(self, trans):
        self.ty.GetVnlMatrix().set(1, 3, trans)
        self.Update()

    def TranslateZ(self, trans):
        self.tz.GetVnlMatrix().set(2, 3, trans)
        self.Update()

    def Translate(self, trans_x, trans_y, trans_z):
        self.TranslateX(trans_x)
        self.TranslateY(trans_y)
        self.TranslateZ(trans_z)
        self.Update()

    def ScaleX(self, scl):
        self.tx.GetVnlMatrix().set(0, 0, scl)
        self.Update()

    def ScaleY(self, scl):
        self.ty.GetVnlMatrix().set(1, 1, scl)
        self.Update()

    def ScaleZ(self, scl):
        self.tz.GetVnlMatrix().set(2, 2, scl)
        self.Update()


    def Update(self):
        self.m = (self.GetTz() * self.GetTy() * self.GetTx()) \
               * (self.GetRz() * self.GetRy() * self.GetRx()) \
               * (self.GetSz() * self.GetSy() * self.GetSx())

    # be careful about transposing between itk and vtk matrix type
    def ToVtkTransform(self):
        mat = vtk.vtkMatrix4x4()
        m = self.Get()
        mat.SetElement(0, 0, m.get(0, 0))
        mat.SetElement(0, 1, m.get(0, 1))
        mat.SetElement(0, 2, m.get(0, 2))
        mat.SetElement(0, 3, m.get(0, 3))

        mat.SetElement(1, 0, m.get(1, 0))
        mat.SetElement(1, 1, m.get(1, 1))
        mat.SetElement(1, 2, m.get(1, 2))
        mat.SetElement(1, 3, m.get(1, 3))

        mat.SetElement(2, 0, m.get(2, 0))
        mat.SetElement(2, 1, m.get(2, 1))
        mat.SetElement(2, 2, m.get(2, 2))
        mat.SetElement(2, 3, m.get(2, 3))

        mat.SetElement(3, 0, m.get(3, 0))
        mat.SetElement(3, 1, m.get(3, 1))
        mat.SetElement(3, 2, m.get(3, 2))
        mat.SetElement(3, 3, m.get(3, 3))
        vmat = vtk.vtkTransform()
        vmat.Identity()
        vmat.SetMatrix(mat)
        vmat.Update()
        return vmat