#compose everything in facility.usda, the tiny file is the point.
# facility.usda doesn't need to contain all the facility data.
# It tells USD: Compose these contributions together.

from pxr import Usd, UsdGeom

stage = Usd.Stage.CreateNew("facility.usda")

UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

root_layer = stage.GetRootLayer()

root_layer.subLayerPaths = [
    "operations.usda",
    "cooling.usda",
    "rack_assets.usda",
]

stage.SetDefaultPrim(stage.GetPrimAtPath("/World"))

root_layer.Save()