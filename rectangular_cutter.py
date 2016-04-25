from OCC.Display.SimpleGui import init_display
from OCC.BRepPrimAPI import *
from OCC.BRepBuilderAPI import *
from OCC.gp import *
from OCC.BRepAlgo import *
import math


def math_rez(D, r_min, angle, gamma, alpha):
    return 1


def make_curve(points):
    return 1


def make_cut_cylinder(share, points):
    return 1


r_max = 35
r_min = 20
t_max = r_max - r_min
D = 100
gamma = (15 * math.pi) / 180
alpha = (10 * math.pi) / 180

# Рисуем профиль детали Предварительно создаём массив линий
mkWire = BRepBuilderAPI_MakeWire()

xt1 = math_rez(D, r_min, 26.3, gamma, alpha)
xt2 = math_rez(D, r_min, 35, gamma, alpha)
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, 0), gp_Pnt(0, xt1, 0))
wire = BRepBuilderAPI_MakeWire(edge.Edge())

mkWire.Add(wire.Wire())
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0, xt1, 0), gp_Pnt(20, xt2, 0))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
xt3 = math_rez(D, r_min, 28.6, gamma, alpha)
xt4 = math_rez(D, r_min, 25, gamma, alpha)
xt5 = math_rez(D, r_min, 28.5, gamma, alpha)
xt6 = math_rez(D, r_min, 35, gamma, alpha)

edge = make_curve([(20, xt2, 0), (27, xt3, 0), (39.4, xt4, 0), (52.4, xt5, 0), (60, xt6, 0)])
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(60, xt6, 0), gp_Pnt(80, xt6, 0))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
xt7 = math_rez(D, r_min, 30, gamma, alpha)
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(80, xt6, 0), gp_Pnt(80, xt7, 0))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
xt8 = math_rez(D, r_min, 20, gamma, alpha)
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(80, xt7, 0), gp_Pnt(90, xt8, 0))

wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(90, xt8, 0), gp_Pnt(100, xt8, 0))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(100, xt8, 0), gp_Pnt(100, 0, 0))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(100, 0, 0), gp_Pnt(0, 0, 0))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
# делаем из контура фейс

face = BRepBuilderAPI_MakeFace(mkWire.Wire())
# поворациваем профель относительно однрй из своих сторон, ось
# вращения указана вектором, поворачиваем на 180 градусов

solid_of_revol = BRepPrimAPI_MakeRevol(face.Face(), gp_Ax1(gp_Pnt(0, 0, 0),
                                                           gp_Dir(1, 0, 0)), 2 * math.pi)
# Создаём вырез
# Рисуем профиль и вытягиваем его
R = D / 2
b_max = 23
y = - (b_max * math.tan(gamma))
z = -(R - b_max)
mkWire = BRepBuilderAPI_MakeWire()
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0, y, z), gp_Pnt(0, R, z))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0, R, z), gp_Pnt(0, R, -R))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0, R, -R), gp_Pnt(0, 0, -R))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0, 0, -R), gp_Pnt(0, y, z))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())
face = BRepBuilderAPI_MakeFace(mkWire.Wire())

extruded_solid = BRepPrimAPI_MakePrism(face.Face(), gp_Vec(100, 0, 0))

result_solid = BRepAlgo_Cut(solid_of_revol.Shape(), extruded_solid.Shape())
# делаем крепление
Z = 14 * math.cos(math.pi / 6)
Y = 14 * math.sin(math.pi / 6)
# производим вырез 7 отверстий в резце
shape = make_cut_cylinder(result_solid, [(0, 0, 0, 8, 30), (0, 14, 0, 4, 100), (0, -14, 0, 4, 100), (0, Y, -Z, 4, 100),
                                         (0, -Y, -Z, 4, 100), (0, Y, Z, 4, 100), (0, -Y, Z, 4, 100)])
