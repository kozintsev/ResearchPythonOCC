import sys
from OCC.STEPControl import STEPControl_Reader
from OCC.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Display.SimpleGui import init_display
try:
    from PyQt5 import QtWidgets
except ImportError:
    try:
        from PyQt4 import QtGui
        QtWidgets = QtGui
    except ImportError:
        sys.exit(1)


display, start_display, add_menu, add_function_to_menu = init_display()


def open_file():
    fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '')
    step_reader = STEPControl_Reader()
    #status = step_reader.ReadFile('as1_pe_203.stp')
    status = step_reader.ReadFile(fname)

    if status == IFSelect_RetDone:  # check status
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)

        ok = step_reader.TransferRoot(1)
        _nbs = step_reader.NbShapes()
        aResShape = step_reader.Shape(1)
        display.DisplayShape(aResShape, update=True)
    else:
        print("Error: can't read file.")

def exit():
    sys.exit(0)

add_menu('STEP import')
add_function_to_menu('STEP import', open_file)
add_function_to_menu('STEP import', exit)
start_display()