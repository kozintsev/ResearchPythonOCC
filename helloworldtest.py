from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox, \
    BRepPrimAPI_MakeCylinder, \
    BRepPrimAPI_MakeSphere
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeWire
import math

display, start_display, add_menu, add_function_to_menu = init_display()
my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
my_cylinder = BRepPrimAPI_MakeCylinder(10., 20.).Shape()

display.DisplayShape(my_box, update=True)
display.DisplayShape(my_cylinder, update=True)

r_max = 35
r_min = 20
t_max = r_max - r_min
d = 100
gamma = (15 * math.pi) / 180
alpha = (10 * math.pi) / 180
# рисуем профиль детали
# Предварительно создаём массив линий
mkWire = BRepBuilderAPI_MakeWire()


def sphere(event=None):
    display.EraseAll()
    display.DisplayShape(BRepPrimAPI_MakeSphere(100).Shape(), update=True)


def cube(event=None):
    display.EraseAll()
    display.DisplayShape(BRepPrimAPI_MakeBox(1, 1, 1).Shape(), update=True)


add_menu('primitives')
add_function_to_menu('primitives', sphere)
add_function_to_menu('primitives', cube)

start_display()
