#layer that owns data hall and rack placements

from pxr import Usd, UsdGeom, Gf, Sdf

stage = Usd.Stage.CreateNew("rack_assets.usda")

#prims to establish facility namestace for contribution
world = UsdGeom.Xform.Define(stage, "/World")
datahall = UsdGeom.Xform.Define(stage, "/World/DataHall_A")

#Rack_01
rack_01 = UsdGeom.Xform.Define(
    stage,
    "/World/DataHall_A/Rack_01"
)

rack_01.GetPrim().GetReferences().AddReference("rack.usda")
rack_01.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0))

rack_01.GetPrim().CreateAttribute(
    "status",
    Sdf.ValueTypeNames.Token
).Set("commissioned")

#Rack_02
rack_02 = UsdGeom.Xform.Define(
    stage,
    "/World/DataHall_A/Rack_02"
)

rack_02.GetPrim().GetReferences().AddReference("rack.usda")
rack_02.AddTranslateOp().Set(Gf.Vec3d(2, 0, 0))

rack_01.GetPrim().CreateAttribute(
    "status",
    Sdf.ValueTypeNames.Token
).Set("commissioned")

stage.GetRootLayer().Save()

