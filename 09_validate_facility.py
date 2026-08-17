from pxr import Usd, UsdGeom

stage = Usd.Stage.Open("payload_facility.usda")

errors = []

# add checks one at a time
# check stage metadata such as metersPerUnit and upAxis, 
# because missing conventions can make exchanged assets 
# behave incorrectly.

# check metersPerUnit
meters_per_unit = UsdGeom.GetStageMetersPerUnit(stage)

if meters_per_unit != 1.0:
    errors.append(
        f"meters_per_unit should be 1.0. Got {meters_per_unit}"
    )

# check upAxis
up_axis = UsdGeom.GetStageUpAxis(stage)

if up_axis != UsdGeom.Tokens.z:
    errors.append(
        f"up_axis should be Z. Got {up_axis}"
    )

# find every rack
racks = []

for prim in stage.Traverse():
    if prim.GetName().startswith("Rack_"):
        racks.append(prim)

# /World/DataHall_A/Rack_01
# /World/DataHall_A/Rack_02
# /World/DataHall_B/Rack_01

# every rack must have assetType
# “Don't make me infer that this is a rack from its name or 
# shape. Tell me explicitly.”
for rack in racks:
    asset_type = rack.GetAttribute("assetType")

    if not asset_type or asset_type.Get() != "computeRack":
        errors.append(
            f"{rack.GetPath()} is missing assetType=computeRack"
        )

# every rack must belong to a zone
# “Every rack needs enough structured information for software 
# to know where it belongs.”
for rack in racks:
    zone = rack.GetAttribute("zone")

    if not zone or not zone.Get():
        errors.append(
            f"{rack.GetPath()} is missing zone attribute"
        )

# Check composition/reference errors
# returns errors encountered while composing the Stage, 
# which includes problems such as composition dependencies 
# that fail to resolve.
composition_errors = stage.GetCompositionErrors()

for error in composition_errors:
    errors.append(
        f"Composition error: {error}"
    )

# Check expected variants
# Every rack asset is supposed to expose this configuration 
# contract. Does it?
for rack in racks:
    variants = rack.GetVariantSets()

    if not variants.HasVariantSet("configuration"):
        errors.append(
            f"{rack.GetPath()} missing configuration variant set"
        )
        continue

    config = variants.GetVariantSet("configuration")
    names = config.GetVariantNames()

    expected = {"72_GPU", "144_GPU"}

    if not expected.issubset(set(names)):
        errors.append(
            f"{rack.GetPath()} configuration variants are {names}"
        )

    # print report
    if errors:
        print("VALIDATION FAILED\n")

        for error in errors:
            print("✗", error)
else:
    print("VALIDATION PASSED")

    print("✓ metersPerUnit = 1")
    print("✓ upAxis = Z")
    print("✓ every rack has assetType")
    print("✓ every rack has zone")
    print("✓ composition dependencies resolve")
    print("✓ expected configuration variants exist")