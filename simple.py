from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.gp import gp_Pnt

display, start_display, add_menu, add_function_to_menu = init_display()
# my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

my_cyl = BRepPrimAPI_MakeCylinder(10., 20.).Shape()
my_point = gp_Pnt(10., 10., 10.)

display.DisplayShape(my_cyl, update=True)
start_display()
