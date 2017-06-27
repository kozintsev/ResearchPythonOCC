from __future__ import print_function
from __future__ import division

import sys
import logging
from OCC.Display.backend import load_backend, get_qt_modules
from PyQt5 import QtCore
from OCC import BRepPrimAPI, gp, Quantity, TDocStd, TopAbs, TopLoc
from OCC import TPrsStd, XCAFApp, XCAFDoc, XCAFPrs, TCollection

log = logging.getLogger(__name__)


class DocCtrl(object):
    """Controller for a document object. The document itself
    can be accessed as 'self.document'. """

    def __init__(self):

        # list which associates each shape label with a component
        # label - this list is used for deleting shapes:
        self._label_list = []
        self._doc_handle = TDocStd.Handle_TDocStd_Document()
        # print(dir(XCAFApp))
        self._xcaf_app = XCAFApp.XCAFApp_Application_GetApplication().GetObject()
        self._xcaf_app.NewDocument(TCollection.TCollection_ExtendedString(), self._doc_handle)
        # The document itself:
        self.document = self._doc_handle.GetObject()
        self._color_tool = XCAFDoc.XCAFDoc_DocumentTool().ColorTool(self.document.Main()).GetObject()
        self._shape_tool = XCAFDoc.XCAFDoc_DocumentTool().ShapeTool(self.document.Main()).GetObject()
        self.top_label = self._shape_tool.NewShape()
        self._loc = TopLoc.TopLoc_Location(gp.gp_Trsf())

    def add(self, shape):
        """Add a shape to the document"""

        shape_label = self._shape_tool.AddShape(shape, False)
        comp_label = self._shape_tool.AddComponent(
            self.top_label, shape_label, self._loc)
        self._color_tool.SetColor(shape_label,
                                  Quantity.Quantity_Color(0, 0, 1, 0),
                                  XCAFDoc.XCAFDoc_ColorGen)
        print("Added shape", shape_label.Tag())
        self._label_list.append([shape_label, comp_label])

    def remove(self, shape):
        """Remove a shape from the document"""
        # get the label of the shape which should be removed
        to_remove = self._shape_tool.FindShape(shape)

        # find the shape that corresponds to the label and remove the
        # associated component
        for shape_label, comp_label in self._label_list:
            if shape_label.IsEqual(to_remove):
                self._shape_tool.RemoveComponent(comp_label)
                self._shape_tool.RemoveShape(shape_label)
                print("Removed shape", shape_label.Tag())
                break

used_backend = load_backend(None)
log.info("GUI backend set to: {0}".format(used_backend))

from OCC.Display.qtDisplay import qtViewer3d


class qtViewer2(qtViewer3d):
    keyPressed = QtCore.pyqtSignal()

    def keyPressEvent(self, event):
        print("Key pressed:", event.key())
        print("========================================")
        print("removing selected")
        if event.key() == QtCore.Qt.Key_Delete:
            shapes = self._display.GetSelectedShapes()
            # print(shapes)
        for shape in shapes:
            # if shape:
            self.doc_ctrl.remove(shape)

        self.repaint()

    def __init__(self, parent):
        #
        qtViewer3d.__init__(self)

    def init2(self):
        """Perform the second initialization step."""

        self.doc_ctrl = DocCtrl()
        h = self._display.Context.GetHandle()
        self.AISViewer = TPrsStd.TPrsStd_AISViewer().New(self.doc_ctrl.top_label, h).GetObject()
        context = self.AISViewer.GetInteractiveContext().GetObject()
        context.OpenLocalContext()
        context.ActivateStandardMode(TopAbs.TopAbs_SOLID)

        self._ais_pres = TPrsStd.TPrsStd_AISPresentation().Set(self.doc_ctrl.top_label,
                                                               XCAFPrs.XCAFPrs_Driver_GetID()).GetObject()
        # self._ais_pres.Display(Update=  False)

    def repaint(self, Update=True):
        print("repaint")

        self._ais_pres.Update()
        self._ais_pres.Display()
        self._display.Context.UpdateCurrentViewer()
        self._display.Repaint()
        print("repaint succesful")


def init_display(backend_str=None, size=(1000, 600)):
    QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, *args):
            QtWidgets.QMainWindow.__init__(self, *args)

            self.resize(size[0], size[1])
            self.Viewer = qtViewer2(self)

            self.setCentralWidget(self.Viewer)
            self.centerOnScreen()

        def centerOnScreen(self):
            '''Centers the window on the screen.'''
            resolution = QtWidgets.QDesktopWidget().screenGeometry()
            self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                      (resolution.height() / 2) - (self.frameSize().height() / 2))

    # following couple of lines is a twek to enable ipython --gui='qt'
    app = QtWidgets.QApplication.instance()  # checks if QApplication already exists
    if not app:  # create QApplication if it doesnt exist
        app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.Viewer.InitDriver()
    display = win.Viewer._display

    # background gradient
    display.set_bg_gradient_color(206, 215, 222, 128, 128, 128)
    # display black trihedron
    display.display_trihedron()

    def start_display():
        win.raise_()  # make the application float to the top
        app.exec_()

    win.display = display
    win.show()
    win.Viewer.init2()
    # create and add shapes
    box = BRepPrimAPI.BRepPrimAPI_MakeBox(60, 30, 10).Shape()
    cyl = BRepPrimAPI.BRepPrimAPI_MakeCylinder(25, 40).Shape()

    tr = gp.gp_Trsf()
    tr.SetTranslation(gp.gp_Vec(0, 50, 0))
    loc = TopLoc.TopLoc_Location(tr)
    moved_box = box.Moved(loc)

    # these shapes can be deleted by selecting them and pressing 'Del':
    win.Viewer.doc_ctrl.add(box)
    win.Viewer.doc_ctrl.add(cyl)
    # this shape cannot be deleted in this implementation:
    win.Viewer.doc_ctrl.add(moved_box)

    win.Viewer.repaint(Update=False)

    display.FitAll()
    return display, start_display


display, start_display = init_display()

if __name__ == '__main__':
    start_display()