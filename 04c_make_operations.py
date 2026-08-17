# Make the operations override
# no geometry
# At /World/DataHall_A/Rack_01:
# I have an opinion:
# status = maintenance
# not defining operattions from scratch
# contributing opinions to something expected to exist through
# composition.

from pxr import Usd, Sdf

stage = Usd.Stage.CreateNew("operations.usda")

rack_01 = stage.OverridePrim(
    "/World/DataHall_A/Rack_01"
)

rack_01.CreateAttribute(
    "status",
    Sdf.ValueTypeNames.Token
).Set("maintenance")

stage.GetRootLayer().Save()