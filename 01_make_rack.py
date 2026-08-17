# create reusable source asset: rack.usda
# python = what it was asked to author
# usda = what was actually persisted
# blender = what downstream visual app sees
# one USD layer containing a Stage whose default prim is /World. 
# Defined an Xform hierarchy /World/Rack, 
# authored a custom assetType property and a translation on the rack, 
# and defined a Cube child under /World/Rack/Geometry. 
# Established meter units and Z-up as stage conventions.

#Reference = reused at a location in another namespace

from pxr import Usd, UsdGeom, Gf, Sdf

stage = Usd.Stage.CreateNew("rack.usda")

UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

# root of asset
rack = UsdGeom.Xform.Define(stage, "/Rack")
stage.SetDefaultPrim(rack.GetPrim())

# machine-readable meaning
rack.GetPrim().CreateAttribute(
    "assetType",
    Sdf.ValueTypeNames.Token
).Set("computeRack")

# Geometry owned by this asset
UsdGeom.Scope.Define(stage, "/Rack/Geometry")

body = UsdGeom.Cube.Define(stage, "/Rack/Geometry/Body")
body.GetSizeAttr().Set(1.0)

stage.GetRootLayer().Save()