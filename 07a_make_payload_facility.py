from pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.CreateNew("payload_facility.usda")

UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

#small always present DataHall_A
datahall_a = UsdGeom.Xform.Define(
    stage,
    "/World/DataHall_A"
)

rack = UsdGeom.Xform.Define(
    stage,
    "/World/DataHall_A/Rack_01"
)

# DataHall_B exists as location in facility
# but contents are behind a payload
datahall_b = UsdGeom.Xform.Define(
    stage,
    "/World/DataHall_B"
)

# mirrors GetReferences().AddReference("rack.usda")
datahall_b.GetPrim().GetPayloads().AddPayload(
    "datahall_b.usda"
)

datahall_b.AddTranslateOp().Set(
    Gf.Vec3d(0, 5, 0)
)

stage.GetRootLayer().Save()