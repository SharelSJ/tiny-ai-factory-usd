# Rack_01
#     ↓ same rack asset
# configuration = 72_GPU

# Rack_02
#     ↓ same rack asset
# configuration = 144_GPU

# gpuCount = 72 and gpuCount = 144 are absent
# Those values live in rack_configurable.usda.
# The facility only authors the selection.
# rack_configurable.usda owns: "What configurations are possible?"
# variant_facility.usda owns: "Which configuration does this particular rack use?"

from pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.CreateNew("variant_facility.usda")

UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

datahall = UsdGeom.Xform.Define(stage, "/World/DataHall_A")

# create rack_01 and reference reusable asset
rack_01 = UsdGeom.Xform.Define(
    stage,
    "/World/DataHall_A/Rack_01"
)

rack_01.GetPrim().GetReferences().AddReference(
    "rack_configurable.usda"
)

rack_01.AddTranslateOp().Set(
    Gf.Vec3d(0, 0, 0)
)

# set 72_GPU specifically for rack_01
# Get the variant set named "configuration" on Rack_01.
# select its "72_GPU" choice
config_01 = rack_01.GetPrim().GetVariantSet(
    "configuration"
)

config_01.SetVariantSelection("72_GPU")

# create rack_02 and reference reusable asset
rack_02 = UsdGeom.Xform.Define(
    stage,
    "/World/DataHall_A/Rack_02"
)
rack_02.GetPrim().GetReferences().AddReference(
    "rack_configurable.usda"
)

rack_02.AddTranslateOp().Set(
    Gf.Vec3d(2, 0, 0)
)

# choose other config for rack_02
config_02 = rack_02.GetPrim().GetVariantSet(
    "configuration"
)
config_02.SetVariantSelection("144_GPU")

stage.GetRootLayer().Save()