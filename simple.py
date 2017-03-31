from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.gp import gp_Pnt, gp_Dir, gp_Ax2

display, start_display, add_menu, add_function_to_menu = init_display()
my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

my_cyl = BRepPrimAPI_MakeCylinder(10., 20.).Shape()
my_point = gp_Pnt(10., 10., 10.)

pnt = gp_Pnt(0., 0., 0.)
dr = gp_Dir(0., 1., 0.)
ax = gp_Ax2(pnt, dr)
my_cyl = BRepPrimAPI_MakeCylinder(ax, 10, 100)

display.DisplayShape(my_cyl, update=True)
start_display()
