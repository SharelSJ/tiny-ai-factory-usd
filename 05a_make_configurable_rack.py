from pxr import Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("rack_configurable.usda")

UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

rack = UsdGeom.Xform.Define(stage, "/Rack")
stage.SetDefaultPrim(rack.GetPrim())

rack.GetPrim().CreateAttribute(
    "assetType",
    Sdf.ValueTypeNames.Token
).Set("computeRack")

# Bring in the original rack, including its geometry
rack.GetPrim().GetReferences().AddReference("rack.usda")


# create variant set
# /Rack has a configurable dimension called configuration,
# and it has two legal choices.
config = rack.GetPrim().GetVariantSets().AddVariantSet("configuration")

# add 2 possible configurations
config.AddVariant("72_GPU")
config.AddVariant("144_GPU")

# Author what 72_GPU means
config.SetVariantSelection("72_GPU")

with config.GetVariantEditContext():
    rack.GetPrim().CreateAttribute(
        "gpuCount",
        Sdf.ValueTypeNames.Int
    ).Set(72)

# Author 144_GPU 
config.SetVariantSelection("144_GPU")

with config.GetVariantEditContext():
    rack.GetPrim().CreateAttribute(
        "gpuCount",
        Sdf.ValueTypeNames.Int
    ).Set(144)

# Now the same prim has two alternative descriptions
# Rack with 72 GPUs and Rack with 144 GPUs. 
# The variant set allows us to switch between these 
# two configurations; only one contributes at a time.

#set default variant selection to 72_GPU
config.SetVariantSelection("72_GPU")

stage.GetRootLayer().Save()