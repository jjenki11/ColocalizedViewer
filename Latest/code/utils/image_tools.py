import nibabel as nib


import glymur as gly




class BaseImage(object):

    def __init__(self):
        self.path = ""
        self.size = []
        self.name = ""
        self.type = ""

    def SetProperties(self, p, s, n, t):
        pass

    def GetProperties(self):
        pass

    def Convert(self, fmt):
        pass



class NiftiImage(BaseImage):

    def __init__(self):
        super(NiftiImage, self).__init__()
        self.header=None

    def SetProperties(self, p, s, n, t):
        self.path = p;
        self.size = s;
        self.name = n;
        self.type = t;

    def GetProperties(self):
        return {"path": self.path, "size": self.size, "name": self.name, "type": self.type};

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


class JP2000Image(BaseImage):
    def __init__(self):
        super(JP2000Image, self).__init__()
        self.header = None

    def SetProperties(self, p, s, n, t):
        self.path = p;
        self.size = s;
        self.name = n;
        self.type = t;

    def GetProperties(self):
        return {"path": self.path, "size": self.size, "name": self.name, "type": self.type};

    def Create(self, in_path, out_path):
        pass

class JP2000Image(BaseImage):
    def __init__(self):
        super(JP2000Image, self).__init__()
        self.header = None

    def SetProperties(self, p, s, n, t):
        self.path = p;
        self.size = s;
        self.name = n;
        self.type = t;

    def GetProperties(self):
        return {"path": self.path, "size": self.size, "name": self.name, "type": self.type};

    def Create(self, in_path, out_path):
        pass




inpath = '/raid2/data/jenkinsjc/CSHL/jp2000/Nissl_stain/PTM726-N13-2015.06.05-16.53.51_PTM726_1_0037.jp2'
outpath = '/raid2/data/jenkinsjc/output_jpeg.jpeg'

#jImage = TIFFImage()
#jImage.Create(inpath, outpath)


