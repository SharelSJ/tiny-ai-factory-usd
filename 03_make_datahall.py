from pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.CreateNew("datahall.usda")

UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

#facility root
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

#spatial grouping for one data hall
datahall = UsdGeom.Xform.Define(stage, "/World/DataHall_A")

#reuse rack.usda twice
rack_01 = UsdGeom.Xform.Define(stage, "/World/DataHall_A/Rack_01")
rack_01.GetPrim().GetReferences().AddReference("rack.usda")
rack_01.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0))

rack_02 = UsdGeom.Xform.Define(stage, "/World/DataHall_A/Rack_02")
rack_02.GetPrim().GetReferences().AddReference("rack.usda")
rack_02.AddTranslateOp().Set(Gf.Vec3d(2, 0, 0))

#discipline groupings
UsdGeom.Scope.Define(stage, "/World/Cooling")
UsdGeom.Scope.Define(stage, "/World/Power")

stage.GetRootLayer().Save()


