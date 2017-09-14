from PyQt5 import QtCore, QtGui, QtWidgets

# Subclassed qframe widget
class Frame(QtWidgets.QFrame):
    def __init__(self, box_type, _contents):
        super(Frame, self).__init__()
        self.layout = None
        self.type = box_type
        self.contents = _contents
        if (self.type == 'h'):
            self.layout = HBox(self.contents)
        if (self.type == 'v'):
            self.layout = VBox(self.contents)
        self.setLayout(self.layout)

    def Append(self, cont):
        self.contents.append(cont)
        if(self.type == 'h'):
            self.layout = HBox(self.contents)
        if (self.type == 'v'):
            self.layout = VBox(self.contents)
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(self.layout)


# Subclassed horizontal container widget
class HBox(QtWidgets.QHBoxLayout):
    def __init__(self, contents):
        super(HBox, self).__init__()
        self.append(contents)

    def append(self, items):
        for item in items:
            self.addWidget(item)


# Subclassed vertical container widget
class VBox(QtWidgets.QVBoxLayout):
    def __init__(self, contents):
        super(VBox, self).__init__()
        self.append(contents)

    def append(self, items):
        for item in items:
            self.addWidget(item)


# Subclassed text box widget
class TextBox(QtWidgets.QLineEdit):
    def __init__(self, txt, size, w_name=None):
        super(TextBox, self).__init__()
        self.SetText(txt)
        self.setFixedWidth(size)
        #RegisterWidget(w_name, self)

    def SetText(self, txt):
        self.setText(str(txt))

    def GetText(self):
        return self.text()


# Subclassed label widget
class Label(QtWidgets.QLabel):
    def __init__(self, t, w_name=None):
        super(Label, self).__init__(t)
        self.SetText(t)
        self.name = w_name
        #RegisterWidget(w_name, self)

    def SetText(self, lbl):
        self.setText(str(lbl))

    def GetName(self):
        return self.name


# Subclassed button widget
class Button(QtWidgets.QPushButton):
    def __init__(self, t, f, w_name=None):
        super(Button, self).__init__()
        self.Text(t)
        self.clicked.connect(f)
        self.show()
        #RegisterWidget(w_name, self)

    def Text(self, t):
        self.setText(t)


# Subclassed slider widget with some global operations
class Slider(QtWidgets.QSlider):
    def __init__(self, _dir, _min, _max, _step, w_name, l_name):
        if (_dir == 'h'):
            super(Slider, self).__init__(QtCore.Qt.Horizontal)
        if (_dir == 'v'):
            super(Slider, self).__init__(QtCore.Qt.Vertical)
        # slider = QSlider(Qt.Horizontal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setTickPosition(self.TicksBothSides)
        self.setMinimum(_min)
        self.setMaximum(_max)
        self.setTickInterval(10)
        self.setSingleStep(_step)
        self.disp_label = widget_map[l_name]
        self.valueChanged[int].connect(self.changeValue)
        self.sliderMoved.connect(self.changeValue)
        #RegisterWidget(w_name, self)

    def GetValue(self):
        return self.value()

    def changeValue(self, value):
        print(str(self.disp_label.GetName()))



# Subclassed combo box widget
class DropDown(QtWidgets.QComboBox):
    def __init__(self, s, w_name):
        super(DropDown, self).__init__()
        #RegisterWidget(w_name, self)
        self.setMaximumWidth(100)
        self.addItems(s)

    def GetText(self):
        return unicode(self.currentText())


# Subclassed list widget
class List(QtWidgets.QListWidget):
    def __init__(self, it, w_name=None):
        super(List, self).__init__()

        self.items = []
        if (len(it) > 0):
            self.items = it
            self.addItems(self.items)
        #RegisterWidget(w_name, self)

    def Reset(self):
        self.items = []
        self.clear()

    def Insert(self, it):
        self.items.append(it)
        self.clear()
        self.addItems(self.items)

    def Remove(self):
        rnum = self.currentRow()
        item = self.takeItem(rnum)
        self.items.pop(rnum)
        del item
        return rnum

    def RemoveIndex(self, rnum):
        item = self.takeItem(rnum)
        self.items.pop(rnum)
        del item
        return rnum

    def GetItems(self):
        ret_items = []
        for index in xrange(self.count()):
            ret_items.append(self.item(index))
        return ret_items

    def GetItemAtIndex(self):
        return self.item(self.currentRow())

    def SetItems(self, items):
        self.Reset()
        for it in items:
            self.addItem(str(it))
            self.items.append(str(it))

    def keyPressEvent(self, ev):
        if ev.key() < 256:
            key = str(ev.text())
        else:
            key = chr(0)

        if (ev.key() == QtCore.Qt.Key_Delete):
            print("PRESSED DELETE (list event)!!!")
            # print("THE ITEM -> " + str(self.GetItemAtIndex().text()))
            # _pos = str(self.GetItemAtIndex().text())
            # parr = []
            # _posstr = _pos.replace('[', '').replace(']', '')
            # parr = _posstr.split(',')
            # fparr = []
            # for p in parr:
            #    fparr.append(float(p))
            # print("POS -> " + str(_pos))
            # act = GetPickedActor(fparr, widget_map['vtk_widget'].ren)
            # print("What is act?  "+str(act))
            # if (act ):
            #    widget_map['vtk_widget'].ren.RemoveActor(act)
            #    widget_map['vtk_widget'].Marks.RemoveLandmark(act)
            # self.Remove()