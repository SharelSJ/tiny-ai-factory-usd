# Data Hall B gets rack 01, 02, 03 (rack_configurable.usda 3x)
# heavy

from pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.CreateNew("datahall_b.usda")

UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

datahall = UsdGeom.Xform.Define(stage, "/DataHall_B")
stage.SetDefaultPrim(datahall.GetPrim())

for i, x in enumerate([0, 2, 4], start=1):
    rack = UsdGeom.Xform.Define(
        stage,
        f"/DataHall_B/Rack_{i:02d}"
    )

    rack.GetPrim().GetReferences().AddReference(
        "rack_configurable.usda"
    )

    rack.AddTranslateOp().Set(
        Gf.Vec3d(x, 0, 0)
    )

stage.GetRootLayer().Save()