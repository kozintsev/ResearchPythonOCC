from OCC.BRepBuilderAPI import *
from OCC.Display.SimpleGui import init_display
from OCC.gp import gp_Pnt

display, start_display, add_menu, add_function_to_menu = init_display()

mkWire = BRepBuilderAPI_MakeWire()

edge = BRepBuilderAPI_MakeEdge(gp_Pnt(-10., -10., 0.), gp_Pnt(10., -10., 0.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())


edge = BRepBuilderAPI_MakeEdge(gp_Pnt(10., -10., 0.), gp_Pnt(10., 10., 0.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())

edge = BRepBuilderAPI_MakeEdge(gp_Pnt(10., 10., 0.), gp_Pnt(-10., 10., 0.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())

edge = BRepBuilderAPI_MakeEdge(gp_Pnt(-10., 10., 0.), gp_Pnt(-10., -10., 0.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())

# make face
face_XY = BRepBuilderAPI_MakeFace(mkWire.Wire())

mkWire = BRepBuilderAPI_MakeWire()

edge = BRepBuilderAPI_MakeEdge(gp_Pnt(-10., 0., -10.), gp_Pnt(10., 0., -10.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())


edge = BRepBuilderAPI_MakeEdge(gp_Pnt(10., 0., -10.), gp_Pnt(10., 0., 10.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())

edge = BRepBuilderAPI_MakeEdge(gp_Pnt(10., 0., 10.), gp_Pnt(-10., 0., 10.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())

edge = BRepBuilderAPI_MakeEdge(gp_Pnt(-10., 0., 10.), gp_Pnt(-10., 0., -10.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())

# make face
face_XZ = BRepBuilderAPI_MakeFace(mkWire.Wire())

mkWire = BRepBuilderAPI_MakeWire()

edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0., -10., -10.), gp_Pnt(0., 10., -10.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())


edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0., 10., -10.), gp_Pnt(0., 10., 10.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())

edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0., 10., 10.), gp_Pnt(0., -10., 10.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())

edge = BRepBuilderAPI_MakeEdge(gp_Pnt(0., -10., 10.), gp_Pnt(0., -10., -10.))
wire = BRepBuilderAPI_MakeWire(edge.Edge())
mkWire.Add(wire.Wire())

# make face
face_ZY = BRepBuilderAPI_MakeFace(mkWire.Wire())
#  set color with either a full name in CAPITAL as a string, your choice among: WHITE, BLUE, RED, GREEN, YELLOW, CYAN,
#  ORANGE,BLACK
display.DisplayShape(face_XY.Face(), update=True, color='RED')
display.DisplayShape(face_XZ.Face(), update=True, color='BLUE')
display.DisplayShape(mkWire.Wire(), update=True, color='GREEN')

start_display()