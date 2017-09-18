
class Dimension(object):
    def __init__(self, _wid, _hei, _dep):
        self.width = _wid
        self.height = _hei
        self.depth = _dep

    def GetWidth(self):
        return self.width

    def GetHeight(self):
        return self.height

    def GetDepth(self):
        return self.depth

    def Get(self):
        return [self.GetWidth(), self.GetHeight(), self.GetDepth()]


