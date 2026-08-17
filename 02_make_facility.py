# create assembly: facility.usda => references rack.usda 3x

from pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.CreateNew("facility.usda")

UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

for i, x in enumerate( [0, 2, 4], start=1):
    rack = UsdGeom.Xform.Define(stage, f"/World/Rack_{i:02d}")

    rack.GetPrim().GetReferences().AddReference("rack.usda")

    rack.AddTranslateOp().Set(Gf.Vec3d(x, 0, 0))

# saves USD file, writes your in-memory USD layer to disk.
stage.GetRootLayer().Save()