#cooling.usda does not need its own separate world.
# It contributes to the same /World namespace.

from pxr import Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("cooling.usda")

#"over" = contribute opinion at /World
#without claiming ownership of original definition
world = stage.OverridePrim("/World")

cooling = UsdGeom.Scope.Define(stage, "/World/Cooling")

cooling.GetPrim().CreateAttribute(
    "systemType",
    Sdf.ValueTypeNames.Token
).Set("liquidCooling")

stage.GetRootLayer().Save()