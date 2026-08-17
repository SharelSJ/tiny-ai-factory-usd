# OpenUSD attributes are typed name/value properties 
# attached to prims, so downstream software can query 
# them directly rather than parsing names or guessing 
# from geometry
# tagging prims

# Once many applications need to agree on what 
# computeRack, zone, power capacity, cooling requirements, 
# operational state, etc. mean, arbitrary custom attributes
# stop scaling cleanly. You need contracts.

from pxr import Usd, Sdf

# CreateNew = start a new USD file
# Open = continue working on an existing USD file
stage = Usd.Stage.Open("payload_facility.usda")

rack_01 = stage.GetPrimAtPath(
    "/World/DataHall_A/Rack_01"
)

# rack.GetAttribute("assetType").Get() -> computeRack
# rack.GetAttribute("zone").Get() -> DataHall_A
rack_01.CreateAttribute(
    "assetType",
    Sdf.ValueTypeNames.Token
).Set("computeRack")

rack_01.CreateAttribute(
    "zone",
    Sdf.ValueTypeNames.Token
).Set("DataHall_A")

cooling = stage.DefinePrim(
    "/World/Cooling/CoolingUnit_01",
    "Xform"
)

cooling.CreateAttribute(
    "assetType",
    Sdf.ValueTypeNames.Token
).Set("coolingUnit")

stage.GetRootLayer().Save()

# Give me every compute rack in this facility
# project-specific convention
# assetType = "computeRack"
for prim in stage.Traverse():
    attr = prim.GetAttribute("assetType")

    if attr and attr.Get() == "computeRack":
        print(prim.GetPath())