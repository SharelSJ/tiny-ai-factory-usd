# operations.usda status = maintenance
# rack_assets.usda status = commissioned
# operations is stronger, status = maintenance,
# because 04d_make_facility.py set the subLayerPath order
# to have operations.usda before rack_assets.usda
# non-destructive composition

# rack.usda defines the reusable asset. 
# rack_assets.usda assembles rack assets into the 
# facility namespace. cooling.usda contributes 
# cooling information into that same namespace. 
# operations.usda contributes a stronger operational 
# opinion without editing the engineering layer. 
# facility.usda composes those layers into one Stage.

# conflcit here is subLayer strength

# A Stage ≠ one file.
# A Stage is the composed result
# of potentially many authored layers.

from pxr import Usd

stage = Usd.Stage.Open("facility.usda")

rack = stage.GetPrimAtPath(
    "/World/DataHall_A/Rack_01"
)

status = rack.GetAttribute("status")

print("Resolved status:", status.Get())

# inspect both opinions
# returns the property specs contributing opinions to 
# that property, ordered strongest to weakest. 
# OpenUSD explicitly describes this API as useful for 
# debugging and diagnostics.
print("\nAuthored opinions:")

for spec in status.GetPropertyStack():
    print(
        spec.layer.identifier,
        "→",
        spec.default
    )